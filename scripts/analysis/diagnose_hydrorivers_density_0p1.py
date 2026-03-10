"""Diagnose HydroRIVERS density inside 0.1° China grid.

Goal
----
Quantify how many HydroRIVERS reaches intersect each grid cell, and how
concentrated the river length is in the "main" reach used by the pipeline.
This helps evaluate whether high reach density could plausibly induce large
errors in the single-downstream grid topology.

Inputs (defaults)
-----------------
- data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet
- data/processed/grid_0p1/grid_cells_china_0p1.nc
- data/processed/grid_0p1/grid_topology_china_0p1.nc

Outputs
-------
- results/tables/hydrorivers_density_grid_0p1_summary.csv
- results/tables/hydrorivers_density_grid_0p1_top_cells.csv

"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


DEFAULT_HYDRORIVERS_MAP = Path("data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet")
DEFAULT_GRID_NC = Path("data/processed/grid_0p1/grid_cells_china_0p1.nc")
DEFAULT_TOPO_NC = Path("data/processed/grid_0p1/grid_topology_china_0p1.nc")

DEFAULT_OUT_SUMMARY = Path("results/tables/hydrorivers_density_grid_0p1_summary.csv")
DEFAULT_OUT_TOP = Path("results/tables/hydrorivers_density_grid_0p1_top_cells.csv")


def _describe(series: pd.Series) -> dict[str, float]:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return {"count": 0.0}
    q = s.quantile([0.0, 0.5, 0.9, 0.95, 0.99, 1.0]).to_dict()
    return {
        "count": float(s.size),
        "min": float(q.get(0.0, np.nan)),
        "p50": float(q.get(0.5, np.nan)),
        "p90": float(q.get(0.9, np.nan)),
        "p95": float(q.get(0.95, np.nan)),
        "p99": float(q.get(0.99, np.nan)),
        "max": float(q.get(1.0, np.nan)),
        "mean": float(s.mean()),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hydrorivers-map", default=str(DEFAULT_HYDRORIVERS_MAP))
    ap.add_argument("--grid-nc", default=str(DEFAULT_GRID_NC))
    ap.add_argument("--topo-nc", default=str(DEFAULT_TOPO_NC))
    ap.add_argument("--out-summary", default=str(DEFAULT_OUT_SUMMARY))
    ap.add_argument("--out-top", default=str(DEFAULT_OUT_TOP))
    ap.add_argument("--top-n", type=int, default=200)
    args = ap.parse_args()

    df = pd.read_parquet(Path(args.hydrorivers_map))
    required = ["grid_id", "HYRIV_ID", "overlap_length_km", "NEXT_DOWN", "DIST_DN_KM"]
    for c in required:
        if c not in df.columns:
            raise KeyError(f"HydroRIVERS mapping missing column: {c}")

    df = df.copy()
    df["grid_id"] = pd.to_numeric(df["grid_id"], errors="coerce").astype("Int64")
    df["overlap_length_km"] = pd.to_numeric(df["overlap_length_km"], errors="coerce")
    df["HYRIV_ID"] = pd.to_numeric(df["HYRIV_ID"], errors="coerce")
    df["NEXT_DOWN"] = pd.to_numeric(df["NEXT_DOWN"], errors="coerce")
    df["DIST_DN_KM"] = pd.to_numeric(df["DIST_DN_KM"], errors="coerce")
    df = df.dropna(subset=["grid_id"]).copy()
    df["overlap_length_km"] = df["overlap_length_km"].fillna(0.0).clip(lower=0.0)

    # Estimate outlet multiplicity per grid cell.
    # Caution: A reach (NEXT_DOWN) can intersect multiple grid cells, including the current one.
    # We only count it as an "exit" if NEXT_DOWN does NOT intersect the current grid cell.
    # When it is an exit, we estimate the downstream grid cell as the most downstream
    # (min DIST_DN_KM) intersection of NEXT_DOWN *excluding* the current grid cell.
    df_tmp = df.dropna(subset=["HYRIV_ID"]).copy()
    df_tmp["HYRIV_ID"] = df_tmp["HYRIV_ID"].astype(np.int64)
    df_tmp["NEXT_DOWN"] = df_tmp["NEXT_DOWN"].astype("Int64")

    # Build reach -> set of intersected grid_ids (for "is NEXT_DOWN inside same cell" test)
    reach_gids = df_tmp.groupby("HYRIV_ID", as_index=True)["grid_id"].unique().to_dict()

    # Build per reach a table of (grid_id, min DIST_DN_KM) to pick downstream-most occurrence
    reach_grid_min_dist = (
        df_tmp.dropna(subset=["DIST_DN_KM"])
        .groupby(["HYRIV_ID", "grid_id"], as_index=False)["DIST_DN_KM"]
        .min()
    )
    # For fast lookup: (HYRIV_ID, grid_id) -> min_dist
    # We'll still use pandas filtering per-row to keep code simple and robust.

    def estimate_next_gid(row: pd.Series) -> float:
        nd = row.get("NEXT_DOWN")
        if pd.isna(nd) or int(nd) <= 0:
            return np.nan
        cur_gid = int(row["grid_id"])
        gids = reach_gids.get(int(nd))
        if gids is None:
            return np.nan
        # If NEXT_DOWN intersects current grid, it's an internal transition (not an exit).
        if cur_gid in set(map(int, gids)):
            return np.nan
        # Otherwise choose the downstream-most grid occurrence of NEXT_DOWN.
        cand = reach_grid_min_dist[reach_grid_min_dist["HYRIV_ID"] == int(nd)]
        if cand.empty:
            return np.nan
        # Prefer any candidate grid_id (all are != cur_gid by construction)
        best = cand.sort_values("DIST_DN_KM", ascending=True).iloc[0]
        return float(best["grid_id"])

    df_tmp["next_gid_est"] = df_tmp.apply(estimate_next_gid, axis=1)
    df_tmp["exit_to_other_cell"] = df_tmp["next_gid_est"].notna()

    exits = df_tmp[df_tmp["exit_to_other_cell"]].copy()
    exits_g = exits.groupby("grid_id", as_index=True)
    exits_per = pd.DataFrame(
        {
            "n_exit_reaches": exits_g["HYRIV_ID"].nunique(dropna=True),
            "n_exit_downstream_cells": exits_g["next_gid_est"].nunique(dropna=True),
        }
    )

    # Per-grid counts and lengths
    g = df.groupby("grid_id", as_index=True)
    per = pd.DataFrame(
        {
            "n_reaches": g["HYRIV_ID"].nunique(dropna=True),
            "total_length_km": g["overlap_length_km"].sum(min_count=1),
            "max_seg_length_km": g["overlap_length_km"].max(),
        }
    ).reset_index()

    # Main reach defined in pipeline: argmax overlap_length_km
    idx_main = g["overlap_length_km"].idxmax()
    main = df.loc[idx_main, ["grid_id", "HYRIV_ID", "overlap_length_km"]].rename(
        columns={"HYRIV_ID": "main_hyriv_id", "overlap_length_km": "main_length_km"}
    )

    per = per.merge(main, on="grid_id", how="left")
    per["main_length_frac"] = per["main_length_km"] / per["total_length_km"].replace(0.0, np.nan)

    per = per.merge(exits_per.reset_index(), on="grid_id", how="left")
    per["n_exit_reaches"] = per["n_exit_reaches"].fillna(0).astype(np.int64)
    per["n_exit_downstream_cells"] = per["n_exit_downstream_cells"].fillna(0).astype(np.int64)

    # Join grid mask and topology diagnostics
    ds_grid = xr.open_dataset(Path(args.grid_nc))
    ds_topo = xr.open_dataset(Path(args.topo_nc))
    grid_id = ds_grid["grid_id"].values.reshape(-1)
    in_china = ds_grid["in_china"].values.reshape(-1).astype(bool)

    next_gid = ds_topo["hydrorivers_next_grid_id"].values.reshape(-1)
    next_gid = np.where(np.isfinite(next_gid), next_gid, np.nan)

    df_gid = pd.DataFrame({"grid_id": grid_id.astype(np.int64), "in_china": in_china, "next_grid_id": next_gid})
    df_gid = df_gid[df_gid["grid_id"] != -1].copy()

    per = per.merge(df_gid, on="grid_id", how="left")
    per["has_next"] = per["next_grid_id"].notna() & (per["next_grid_id"] > 0)

    # Summaries (China-only, and all)
    per_china = per[per["in_china"] == True].copy()  # noqa: E712

    summary_rows: list[dict[str, object]] = []

    def add_block(label: str, frame: pd.DataFrame) -> None:
        summary_rows.append({"scope": label, "metric": "n_cells", "value": int(frame.shape[0])})
        for k, v in _describe(frame["n_reaches"]).items():
            summary_rows.append({"scope": label, "metric": f"n_reaches_{k}", "value": v})
        for k, v in _describe(frame["total_length_km"]).items():
            summary_rows.append({"scope": label, "metric": f"total_length_km_{k}", "value": v})
        for k, v in _describe(frame["main_length_frac"]).items():
            summary_rows.append({"scope": label, "metric": f"main_length_frac_{k}", "value": v})
        summary_rows.append({
            "scope": label,
            "metric": "share_cells_main_frac_lt_0p5",
            "value": float((frame["main_length_frac"] < 0.5).mean()),
        })
        summary_rows.append({
            "scope": label,
            "metric": "share_cells_n_reaches_ge_10",
            "value": float((frame["n_reaches"] >= 10).mean()),
        })
        summary_rows.append({
            "scope": label,
            "metric": "share_cells_has_next",
            "value": float(frame["has_next"].mean()),
        })
        summary_rows.append({
            "scope": label,
            "metric": "share_cells_multi_exit_downstream_cells_ge_2",
            "value": float((frame["n_exit_downstream_cells"] >= 2).mean()),
        })
        summary_rows.append({
            "scope": label,
            "metric": "share_cells_any_exit_reach",
            "value": float((frame["n_exit_reaches"] >= 1).mean()),
        })

    add_block("all", per)
    add_block("china", per_china)

    out_summary = Path(args.out_summary)
    out_summary.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(out_summary, index=False)

    # Top cells by number of reaches and by total length
    top_a = per_china.sort_values(["n_reaches", "total_length_km"], ascending=False).head(args.top_n)
    top_b = per_china.sort_values(["total_length_km", "n_reaches"], ascending=False).head(args.top_n)
    top_c = per_china.sort_values(["n_exit_downstream_cells", "n_exit_reaches"], ascending=False).head(args.top_n)
    top = (
        pd.concat(
            [
                top_a.assign(rank_by="n_reaches"),
                top_b.assign(rank_by="total_length_km"),
                top_c.assign(rank_by="n_exit_downstream_cells"),
            ],
            ignore_index=True,
        )
        .drop_duplicates(subset=["grid_id", "rank_by"], keep="first")
        .reset_index(drop=True)
    )

    out_top = Path(args.out_top)
    out_top.parent.mkdir(parents=True, exist_ok=True)
    top.to_csv(out_top, index=False)

    print(f"Wrote: {out_summary}")
    print(f"Wrote: {out_top}")


if __name__ == "__main__":
    main()
