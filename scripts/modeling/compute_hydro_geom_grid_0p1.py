"""Stage C: Hydrology-year & geometry quantities on 0.1° China grid.

This script focuses on action_plan Stage C outputs:
  - Q (best-available throughflow discharge), runoff
  - river length and basic channel geometry (W/D via Wollheim)
  - Vriver, Vlake, Vres, Ai (cell area)

Key point: RiverATLAS/BasinATLAS mapping tables in this workspace do not provide
per-reach discharge; thus we derive a fallback discharge by routing runoff along
an existing single-downstream grid topology.

Outputs:
  data/processed/grid_0p1/grid_hydro_geom_china_0p1.nc
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd

SECONDS_PER_DAY = 86400.0
SECONDS_PER_YEAR = 365.0 * SECONDS_PER_DAY
M3_PER_KM3 = 1e9

# HydroLAKES TechDoc v1.0: Vol_total / Vol_res are in million cubic meters (mcm)
# 1 mcm = 0.001 km^3
MCM_TO_KM3 = 1e-3

# Wollheim et al. (2006) constants (Online Resource 1)
# Q in km^3/yr, W/D in km
AW = 0.0013
BW = 0.50
AD = 0.0004
BD = 0.40

DEFAULT_GRID_NC = Path("data/processed/grid_0p1/grid_cells_china_0p1.nc")
DEFAULT_GRID_PARQUET = Path("data/processed/grid_0p1/grid_cells_china_0p1.parquet")
DEFAULT_TOPOLOGY_NC = Path("data/processed/grid_0p1/grid_topology_china_0p1.nc")

DEFAULT_HYDRORIVERS_MAP = Path("data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet")
DEFAULT_HYDROLAKES_MAP = Path("data/processed/grid_0p1/grid_hydrolakes_china_0p1_mapping.parquet")
DEFAULT_BASINATLAS_MAP = Path("data/processed/grid_0p1/grid_basinatlas_lev10_china_0p1_mapping.parquet")
DEFAULT_RIVERATLAS_MAP = Path("data/processed/grid_0p1/grid_riveratlas_china_0p1_mapping.parquet")

DEFAULT_OUT = Path("data/processed/grid_0p1/grid_hydro_geom_china_0p1.nc")


def _compute_cell_area_km2(grid_parquet: Path) -> pd.Series:
    g = gpd.read_parquet(grid_parquet)
    if "grid_id" not in g.columns or "geometry" not in g.columns:
        raise KeyError("grid parquet must contain grid_id and geometry")
    area_km2 = g.to_crs(6933).geometry.area / 1e6
    return pd.Series(area_km2.to_numpy(dtype=np.float64), index=g["grid_id"].to_numpy(dtype=np.int64))


def _compute_runoff_m_per_year_by_gid(df_basin: pd.DataFrame, df_riveratlas: pd.DataFrame) -> pd.Series:
    """Best-available runoff depth for each grid cell.

    Prefer BasinATLAS `run_mm_syr` (assumed mm/yr). Fall back to RiverATLAS `run_mm_cyr` (mm/yr climatology).
    Aggregation is overlap-area-weighted mean because runoff is an areal depth.
    """

    def area_wmean(df: pd.DataFrame, value_col: str) -> pd.Series:
        if value_col not in df.columns:
            raise KeyError(value_col)
        if "grid_id" not in df.columns or "overlap_area_km2" not in df.columns:
            raise KeyError("mapping missing grid_id/overlap_area_km2")
        v = pd.to_numeric(df[value_col], errors="coerce").to_numpy(dtype=np.float64)
        w = pd.to_numeric(df["overlap_area_km2"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)
        num = np.where(np.isfinite(v), v * w, 0.0)
        den = np.where(np.isfinite(v), w, 0.0)
        tmp = pd.DataFrame({"grid_id": df["grid_id"].to_numpy(dtype=np.int64), "num": num, "den": den})
        g = tmp.groupby("grid_id", as_index=True)
        return g["num"].sum(min_count=1) / g["den"].sum(min_count=1).replace(0.0, np.nan)

    runoff_mm = None
    if "run_mm_syr" in df_basin.columns:
        runoff_mm = area_wmean(df_basin, "run_mm_syr")

    if runoff_mm is None or runoff_mm.isna().all():
        if "run_mm_cyr" in df_riveratlas.columns:
            runoff_mm = area_wmean(df_riveratlas, "run_mm_cyr")

    if runoff_mm is None:
        raise RuntimeError("No runoff field found (expected run_mm_syr or run_mm_cyr)")

    runoff_m = (runoff_mm / 1000.0).astype(np.float64)
    runoff_m = runoff_m.clip(lower=0.0)
    return runoff_m


def _compute_hydrorivers_main_discharge_by_gid(df_riv: pd.DataFrame) -> pd.Series:
    required = ["grid_id", "DIS_AV_CMS", "overlap_length_km"]
    for c in required:
        if c not in df_riv.columns:
            raise KeyError(f"HydroRIVERS mapping missing required column '{c}'")
    w = pd.to_numeric(df_riv["overlap_length_km"], errors="coerce").fillna(0.0).clip(lower=0.0)
    idx_main = w.groupby(df_riv["grid_id"]).idxmax()
    main = df_riv.loc[idx_main, ["grid_id", "DIS_AV_CMS"]].copy()
    main["DIS_AV_CMS"] = pd.to_numeric(main["DIS_AV_CMS"], errors="coerce")
    main = main.dropna(subset=["grid_id"])
    return pd.Series(main["DIS_AV_CMS"].to_numpy(dtype=np.float64), index=main["grid_id"].to_numpy(dtype=np.int64))


def _compute_river_length_km_by_gid(df_riv: pd.DataFrame) -> pd.Series:
    if "grid_id" not in df_riv.columns or "overlap_length_km" not in df_riv.columns:
        raise KeyError("HydroRIVERS mapping missing grid_id/overlap_length_km")
    l_km = pd.to_numeric(df_riv["overlap_length_km"], errors="coerce").fillna(0.0).clip(lower=0.0)
    return l_km.groupby(df_riv["grid_id"]).sum(min_count=1)


def _compute_river_volume_km3_by_gid_segments(df_riv: pd.DataFrame) -> pd.Series:
    required = ["grid_id", "DIS_AV_CMS", "overlap_length_km"]
    for c in required:
        if c not in df_riv.columns:
            raise KeyError(f"HydroRIVERS mapping missing required column '{c}'")

    q_cms = pd.to_numeric(df_riv["DIS_AV_CMS"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)
    q_km3_yr = (q_cms * SECONDS_PER_YEAR) / M3_PER_KM3

    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        width_km = AW * np.power(q_km3_yr, BW)
        depth_km = AD * np.power(q_km3_yr, BD)

    width_km = np.where(np.isfinite(width_km), width_km, 0.0)
    depth_km = np.where(np.isfinite(depth_km), depth_km, 0.0)

    l_km = pd.to_numeric(df_riv["overlap_length_km"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)
    v_seg_km3 = width_km * depth_km * l_km
    v_seg_km3 = np.where(np.isfinite(v_seg_km3), v_seg_km3, 0.0)

    tmp = pd.DataFrame({"grid_id": df_riv["grid_id"].to_numpy(dtype=np.int64), "v": v_seg_km3})
    return tmp.groupby("grid_id")["v"].sum(min_count=1)


def _compute_waterbody_components_by_gid(df_lake: pd.DataFrame) -> pd.DataFrame:
    required = ["grid_id", "overlap_area_km2", "Lake_area", "Vol_total", "Vol_res"]
    for c in required:
        if c not in df_lake.columns:
            raise KeyError(f"HydroLAKES mapping missing required column '{c}'")

    area_in_cell = (
        pd.to_numeric(df_lake["overlap_area_km2"], errors="coerce")
        .fillna(0.0)
        .clip(lower=0.0)
        .to_numpy(dtype=np.float64)
    )
    lake_area_total = pd.to_numeric(df_lake["Lake_area"], errors="coerce").replace(0.0, np.nan).to_numpy(dtype=np.float64)

    vol_total_km3 = (
        pd.to_numeric(df_lake["Vol_total"], errors="coerce")
        .fillna(0.0)
        .clip(lower=0.0)
        .to_numpy(dtype=np.float64)
        * MCM_TO_KM3
    )
    vol_res_km3 = (
        pd.to_numeric(df_lake["Vol_res"], errors="coerce")
        .fillna(0.0)
        .clip(lower=0.0)
        .to_numpy(dtype=np.float64)
        * MCM_TO_KM3
    )
    vol_lake_km3 = np.clip(vol_total_km3 - vol_res_km3, 0.0, None)

    with np.errstate(divide="ignore", invalid="ignore"):
        frac = area_in_cell / lake_area_total
    frac = np.where(np.isfinite(frac), frac, 0.0)
    frac = np.clip(frac, 0.0, 1.0)

    v_wb_in_cell = vol_total_km3 * frac
    v_res_in_cell = vol_res_km3 * frac
    v_lake_in_cell = vol_lake_km3 * frac

    tmp = pd.DataFrame(
        {
            "grid_id": df_lake["grid_id"].to_numpy(dtype=np.int64),
            "a_wb_km2": area_in_cell,
            "v_wb_km3": v_wb_in_cell,
            "v_res_km3": v_res_in_cell,
            "v_lake_km3": v_lake_in_cell,
        }
    )
    g = tmp.groupby("grid_id", as_index=True)
    out = pd.DataFrame(index=g.size().index)
    out["waterbody_area_km2_in_cell"] = g["a_wb_km2"].sum(min_count=1)
    out["v_waterbody_km3_in_cell"] = g["v_wb_km3"].sum(min_count=1)
    out["v_reservoir_km3_in_cell"] = g["v_res_km3"].sum(min_count=1)
    out["v_lake_km3_in_cell"] = g["v_lake_km3"].sum(min_count=1)
    return out


def _route_accumulation_km3_per_year(
    grid_ids_flat: np.ndarray, next_grid_ids_flat: np.ndarray, local_km3_yr: np.ndarray
) -> tuple[np.ndarray, int]:
    """Accumulate local runoff volumes downstream along a single-downstream topology.

    Returns (accum_km3_yr, remaining_cycle_nodes).
    """

    n = grid_ids_flat.size
    gid_to_idx = {int(gid): int(i) for i, gid in enumerate(grid_ids_flat.tolist()) if np.isfinite(gid)}

    down_idx = np.full(n, -1, dtype=np.int64)
    for i in range(n):
        ng = next_grid_ids_flat[i]
        if not np.isfinite(ng):
            continue
        ngi = int(ng)
        # Treat negative ids and self-loops as "no downstream"
        if ngi < 0 or ngi == int(grid_ids_flat[i]):
            continue
        j = gid_to_idx.get(ngi, -1)
        down_idx[i] = j

    indeg = np.zeros(n, dtype=np.int64)
    for j in down_idx:
        if j >= 0:
            indeg[j] += 1

    accum = local_km3_yr.astype(np.float64, copy=True)
    q = deque(int(i) for i in np.where(indeg == 0)[0].tolist())

    def _consume_queue() -> None:
        while q:
            i = q.popleft()
            j = down_idx[i]
            if j >= 0:
                accum[j] += accum[i]
                indeg[j] -= 1
                if indeg[j] == 0:
                    q.append(j)

    _consume_queue()

    # If cycles remain (should be rare), break them by removing outgoing edges
    # of the remaining nodes so that accumulation becomes well-defined.
    remaining_nodes = np.where(indeg > 0)[0]
    if remaining_nodes.size > 0:
        for i in remaining_nodes.tolist():
            j = int(down_idx[i])
            if j >= 0:
                indeg[j] -= 1
            down_idx[i] = -1
        # After edge removals, new zero-indeg nodes may appear.
        new_zeros = np.where(indeg == 0)[0]
        q.extend(int(i) for i in new_zeros.tolist())
        _consume_queue()

    remaining = int(np.sum(indeg > 0))
    return accum, remaining


def _put_from_gid_series(
    out: xr.Dataset,
    name: str,
    s: pd.Series,
    gid_to_flat: pd.Series,
    grid_shape: tuple[int, int],
    fill: float,
    dtype: np.dtype,
) -> None:
    arr = np.full(int(np.prod(grid_shape)), fill, dtype=np.float64)
    common = s.index.intersection(gid_to_flat.index)
    if len(common) > 0:
        idx = gid_to_flat.loc[common].to_numpy(dtype=np.int64)
        vals = s.loc[common].to_numpy(dtype=np.float64)
        arr[idx] = vals
    out[name] = ("lat", "lon"), arr.reshape(grid_shape).astype(dtype)


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage C: compute grid hydrology-year and geometry quantities")
    ap.add_argument("--grid-nc", type=str, default=str(DEFAULT_GRID_NC))
    ap.add_argument("--grid-parquet", type=str, default=str(DEFAULT_GRID_PARQUET))
    ap.add_argument("--topology-nc", type=str, default=str(DEFAULT_TOPOLOGY_NC))
    ap.add_argument("--hydrorivers-map", type=str, default=str(DEFAULT_HYDRORIVERS_MAP))
    ap.add_argument("--hydrolakes-map", type=str, default=str(DEFAULT_HYDROLAKES_MAP))
    ap.add_argument("--basinatlas-map", type=str, default=str(DEFAULT_BASINATLAS_MAP))
    ap.add_argument("--riveratlas-map", type=str, default=str(DEFAULT_RIVERATLAS_MAP))
    ap.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    args = ap.parse_args()

    ds_grid = xr.open_dataset(Path(args.grid_nc))
    ds_topo = xr.open_dataset(Path(args.topology_nc))

    grid_ids = ds_grid["grid_id"].values.astype(np.int64)
    grid_shape = grid_ids.shape
    grid_ids_flat = grid_ids.reshape(-1)

    gid_to_flat = pd.Series(np.arange(grid_ids_flat.size, dtype=np.int64), index=grid_ids_flat)

    next_gid = ds_topo["hydrorivers_next_grid_id"].values.reshape(-1).astype(np.float64)

    df_riv = pd.read_parquet(Path(args.hydrorivers_map))
    df_lake = pd.read_parquet(Path(args.hydrolakes_map))
    df_basin = pd.read_parquet(Path(args.basinatlas_map))
    df_riveratlas = pd.read_parquet(Path(args.riveratlas_map))

    cell_area_km2 = _compute_cell_area_km2(Path(args.grid_parquet))

    runoff_m_yr = _compute_runoff_m_per_year_by_gid(df_basin, df_riveratlas)
    q_hyriv_main_cms = _compute_hydrorivers_main_discharge_by_gid(df_riv)
    river_len_km = _compute_river_length_km_by_gid(df_riv)
    v_river_seg_km3 = _compute_river_volume_km3_by_gid_segments(df_riv)
    wb = _compute_waterbody_components_by_gid(df_lake)

    # Assemble per-grid frame
    all_gids = pd.Index(gid_to_flat.index.to_numpy(dtype=np.int64), name="grid_id")
    df = pd.DataFrame(index=all_gids)
    df["cell_area_km2"] = cell_area_km2
    df["runoff_m_yr"] = runoff_m_yr
    df["q_hyriv_main_cms"] = q_hyriv_main_cms
    df["river_length_km_in_cell"] = river_len_km
    df["v_river_km3"] = v_river_seg_km3
    df = df.join(wb, how="left")

    for c in [
        "cell_area_km2",
        "runoff_m_yr",
        "q_hyriv_main_cms",
        "river_length_km_in_cell",
        "v_river_km3",
        "waterbody_area_km2_in_cell",
        "v_waterbody_km3_in_cell",
        "v_reservoir_km3_in_cell",
        "v_lake_km3_in_cell",
    ]:
        if c not in df.columns:
            df[c] = np.nan

    df["river_length_km_in_cell"] = df["river_length_km_in_cell"].fillna(0.0)
    df["v_river_km3"] = df["v_river_km3"].fillna(0.0)
    for c in ["waterbody_area_km2_in_cell", "v_waterbody_km3_in_cell", "v_reservoir_km3_in_cell", "v_lake_km3_in_cell"]:
        df[c] = df[c].fillna(0.0)

    # Local runoff volume per year (km3/yr)
    # km3/yr = runoff(m/yr) * area(km2) * 1e-3
    local_km3_yr = (
        pd.to_numeric(df["runoff_m_yr"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)
        * pd.to_numeric(df["cell_area_km2"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)
        * 1e-3
    )

    # Route runoff only on cells that contain river segments (topology is defined there).
    has_river = df["river_length_km_in_cell"].fillna(0.0).to_numpy(dtype=np.float64) > 0.0
    local_km3_yr_routed = np.where(has_river, local_km3_yr, 0.0)

    accum_km3_yr, remaining = _route_accumulation_km3_per_year(grid_ids_flat, next_gid, local_km3_yr_routed)

    q_local_cms = (local_km3_yr * M3_PER_KM3) / SECONDS_PER_YEAR
    q_accum_cms = (accum_km3_yr * M3_PER_KM3) / SECONDS_PER_YEAR

    q_hyriv = pd.to_numeric(df["q_hyriv_main_cms"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float64)
    q_best = np.where(q_hyriv > 0.0, q_hyriv, q_accum_cms)

    q_source = np.where(q_hyriv > 0.0, 1, np.where(q_accum_cms > 0.0, 2, 0)).astype(np.int16)

    # Wollheim width/depth from q_best (diagnostics)
    q_best_km3_yr = (q_best * SECONDS_PER_YEAR) / M3_PER_KM3
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        w_km = AW * np.power(q_best_km3_yr, BW)
        d_km = AD * np.power(q_best_km3_yr, BD)
    river_width_m = np.where(np.isfinite(w_km), w_km * 1000.0, 0.0)
    river_depth_m = np.where(np.isfinite(d_km), d_km * 1000.0, 0.0)

    # River volume fallback using q_best and total river length
    l_km = df["river_length_km_in_cell"].to_numpy(dtype=np.float64)
    v_river_fallback = np.where(
        (q_best > 0.0) & (l_km > 0.0),
        (w_km * d_km * l_km).astype(np.float64),
        0.0,
    )
    v_river_seg = df["v_river_km3"].to_numpy(dtype=np.float64)
    v_river = np.where(v_river_seg > 0.0, v_river_seg, v_river_fallback)
    v_river_source = np.where(v_river_seg > 0.0, 1, np.where(v_river_fallback > 0.0, 2, 0)).astype(np.int16)

    # Total volume
    v_tot_km3 = v_river + df["v_waterbody_km3_in_cell"].to_numpy(dtype=np.float64)

    out = xr.Dataset(coords={"lat": ds_grid["lat"], "lon": ds_grid["lon"]})
    out["grid_id"] = ds_grid["grid_id"]
    out["in_china"] = ds_grid["in_china"]

    def put_arr(name: str, flat: np.ndarray, dtype) -> None:
        out[name] = ("lat", "lon"), flat.reshape(grid_shape).astype(dtype)

    # Stage C core
    _put_from_gid_series(out, "cell_area_km2", df["cell_area_km2"].dropna(), gid_to_flat, grid_shape, np.nan, np.float32)
    _put_from_gid_series(out, "runoff_m_per_year", df["runoff_m_yr"].dropna(), gid_to_flat, grid_shape, np.nan, np.float32)

    put_arr("q_local_runoff_cms", q_local_cms, np.float32)
    put_arr("q_accum_runoff_cms", q_accum_cms, np.float32)
    put_arr("q_hydrorivers_main_cms", q_hyriv, np.float32)
    put_arr("q_best_cms", q_best, np.float32)
    put_arr("q_source", q_source, np.int16)  # 0 none, 1 hydrorivers, 2 runoff-accum

    _put_from_gid_series(
        out,
        "river_length_km_in_cell",
        df["river_length_km_in_cell"].dropna(),
        gid_to_flat,
        grid_shape,
        0.0,
        np.float32,
    )

    put_arr("river_width_m_from_qbest", river_width_m, np.float32)
    put_arr("river_depth_m_from_qbest", river_depth_m, np.float32)

    # Volumes/areas
    put_arr("v_river_km3", v_river, np.float32)
    put_arr("v_river_source", v_river_source, np.int16)  # 0 none, 1 segment-based, 2 qbest+L

    _put_from_gid_series(out, "waterbody_area_km2_in_cell", df["waterbody_area_km2_in_cell"].dropna(), gid_to_flat, grid_shape, 0.0, np.float32)
    _put_from_gid_series(out, "v_waterbody_km3_in_cell", df["v_waterbody_km3_in_cell"].dropna(), gid_to_flat, grid_shape, 0.0, np.float32)
    _put_from_gid_series(out, "v_lake_km3_in_cell", df["v_lake_km3_in_cell"].dropna(), gid_to_flat, grid_shape, 0.0, np.float32)
    _put_from_gid_series(out, "v_reservoir_km3_in_cell", df["v_reservoir_km3_in_cell"].dropna(), gid_to_flat, grid_shape, 0.0, np.float32)

    put_arr("v_tot_km3", v_tot_km3, np.float32)

    out.attrs.update(
        {
            "stage": "C",
            "method": "Runoff-depth to local volume; single-downstream accumulation for discharge fallback; Wollheim power laws for channel geometry.",
            "topology": "hydrorivers_next_grid_id",
            "remaining_cycle_nodes": int(remaining),
            "inputs_grid_nc": str(Path(args.grid_nc)),
            "inputs_grid_parquet": str(Path(args.grid_parquet)),
            "inputs_topology_nc": str(Path(args.topology_nc)),
            "inputs_hydrorivers_map": str(Path(args.hydrorivers_map)),
            "inputs_hydrolakes_map": str(Path(args.hydrolakes_map)),
            "inputs_basinatlas_map": str(Path(args.basinatlas_map)),
            "inputs_riveratlas_map": str(Path(args.riveratlas_map)),
            "hydrolakes_volume_unit_in_mapping": "mcm",
            "hydrolakes_volume_mcm_to_km3": float(MCM_TO_KM3),
        }
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_netcdf(out_path)
    ds_grid.close()
    ds_topo.close()
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
