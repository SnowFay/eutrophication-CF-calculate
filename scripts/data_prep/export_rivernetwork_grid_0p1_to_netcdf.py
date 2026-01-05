"""Export river-network attributes to a 0.1° grid NetCDF.

Goal
----
Aggregate river *line* mapping tables (HydroRIVERS / RiverATLAS -> grid) into
per-grid-cell layers and write them as a NetCDF aligned to the existing 0.1° China
grid NetCDF.

Why this script exists
----------------------
- Mapping tables preserve *all* feature fields without lossy aggregation.
- For modeling, we often need a *single value per grid cell*.
- Correct aggregation depends on variable semantics:
  - extensive quantities (e.g., river length in the cell) -> sum
  - intensive quantities (e.g., slope, elevation-like attributes) -> length-weighted mean

This script uses `overlap_length_km` as weights by default, which is the length of
intersection *within each grid cell*.

Inputs (defaults)
-----------------
- Grid base NetCDF:
  data/processed/grid_0p1/grid_cells_china_0p1.nc
- Mapping tables (line -> grid):
  data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet
  data/processed/grid_0p1/grid_riveratlas_china_0p1_mapping.parquet

Outputs (default)
-----------------
data/processed/grid_0p1/grid_rivernetwork_china_0p1.nc

Optional split outputs
----------------------
For workflows that prefer separating routing topology from attributes, you can
write two files:

- `--out-attrs`: per-cell aggregated attributes (length, counts, weighted means)
- `--out-direction`: per-cell routing pointers (main segment id and next-grid)

Both outputs are aligned to the same base grid (lat/lon, grid_id, in_china).

What is exported by default
---------------------------
To avoid making incorrect assumptions about variable meaning, the default export
is intentionally conservative:
- `<source>_river_length_km`  (sum of overlap_length_km)
- `<source>_segment_count`    (count of rows, and count of unique HYRIV_ID if present)

To export additional variables with correct weighting, provide a JSON spec via
`--spec`.

Directionality (grid-to-grid)
-----------------------------
If `--add-directionality` is enabled (recommended for river-network routing), this
script additionally exports a *single downstream pointer per grid cell* based on
the original segment topology:

- For each grid cell, choose a **main segment** (the intersecting segment with the
    maximum `overlap_length_km`).
- Take its `NEXT_DOWN` (downstream segment id).
- Convert downstream segment id -> downstream grid id by assigning each segment to
    its **main grid cell** (again by maximum `overlap_length_km`).

This yields:
- `<source>_main_hyriv_id(lat,lon)`
- `<source>_main_next_down(lat,lon)`
- `<source>_next_grid_id(lat,lon)`
- `<source>_next_lat_index(lat,lon)` and `<source>_next_lon_index(lat,lon)`

Notes:
- A single pointer is a simplification when a grid cell contains multiple channels.
    The exported aggregates (total length, counts, weighted means) still describe
    all segments in the cell.
- If `NEXT_DOWN` is missing/<=0/outside domain, `next_*` will be -1.

Spec format (JSON)
------------------
{
  "sources": {
    "hydrorivers": {
      "mapping_path": "data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet",
      "id_col": "HYRIV_ID",
      "weight_col": "overlap_length_km",
      "sum": ["overlap_length_km"],
      "weighted_mean": ["ORD_FLOW", "DIS_AV_CMS"],
      "mean": [],
      "first": [],
      "rename": {
        "overlap_length_km": "river_length_km"
      }
    }
  }
}

Aggregation rules
-----------------
- sum(var):   per-cell sum of var (optionally w/ overlap-fraction mode in future)
- weighted_mean(var): sum(var * weight) / sum(weight) using non-null pairs only
- mean(var):  arithmetic mean over non-null values
- first(var): first non-null value in the group (use carefully)

Notes
-----
- This script does not attempt to interpret HydroATLAS semantics automatically.
  You should decide per variable whether it should be summed, length-weighted, etc.
- Cells with no intersecting segments:
  - sums -> 0
  - counts -> 0
  - means / weighted means -> NaN

"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd
import xarray as xr


DEFAULT_GRID_NC = Path("data/processed/grid_0p1/grid_cells_china_0p1.nc")
DEFAULT_HYDRORIVERS_MAP = Path("data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet")
DEFAULT_RIVERATLAS_MAP = Path("data/processed/grid_0p1/grid_riveratlas_china_0p1_mapping.parquet")
DEFAULT_OUT = Path("data/processed/grid_0p1/grid_rivernetwork_china_0p1.nc")
DEFAULT_OUT_ATTRS = Path("data/processed/grid_0p1/grid_rivernetwork_attributes_china_0p1.nc")
DEFAULT_OUT_DIRECTION = Path("data/processed/grid_0p1/grid_rivernetwork_direction_china_0p1.nc")


AggKind = Literal["sum", "weighted_mean", "mean", "first"]


@dataclass(frozen=True)
class SourceSpec:
    name: str
    mapping_path: Path
    id_col: str | None
    weight_col: str
    sum_vars: list[str]
    weighted_mean_vars: list[str]
    mean_vars: list[str]
    first_vars: list[str]
    rename: dict[str, str]


def _load_spec_or_default(
    *,
    sources: list[str],
    spec_path: Path | None,
    hydrorivers_map: Path,
    riveratlas_map: Path,
) -> list[SourceSpec]:
    if spec_path is None:
        specs: list[SourceSpec] = []
        wanted = {s.strip().lower() for s in sources if s.strip()}
        if "hydrorivers" in wanted:
            specs.append(
                SourceSpec(
                    name="hydrorivers",
                    mapping_path=hydrorivers_map,
                    id_col="HYRIV_ID",
                    weight_col="overlap_length_km",
                    sum_vars=["overlap_length_km"],
                    weighted_mean_vars=[],
                    mean_vars=[],
                    first_vars=[],
                    rename={"overlap_length_km": "river_length_km"},
                )
            )
        if "riveratlas" in wanted:
            specs.append(
                SourceSpec(
                    name="riveratlas",
                    mapping_path=riveratlas_map,
                    id_col="HYRIV_ID",
                    weight_col="overlap_length_km",
                    sum_vars=["overlap_length_km"],
                    weighted_mean_vars=[],
                    mean_vars=[],
                    first_vars=[],
                    rename={"overlap_length_km": "river_length_km"},
                )
            )
        return specs

    if not spec_path.exists():
        raise FileNotFoundError(f"Spec not found: {spec_path}")

    raw = json.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or "sources" not in raw:
        raise ValueError("Spec must be a JSON object with top-level key 'sources'.")

    out: list[SourceSpec] = []
    for name, cfg in raw["sources"].items():
        if not isinstance(cfg, dict):
            raise ValueError(f"Spec for source '{name}' must be an object")

        mapping_path = Path(cfg.get("mapping_path", ""))
        if not mapping_path:
            raise ValueError(f"Spec for source '{name}' missing mapping_path")

        out.append(
            SourceSpec(
                name=str(name),
                mapping_path=mapping_path,
                id_col=cfg.get("id_col"),
                weight_col=str(cfg.get("weight_col", "overlap_length_km")),
                sum_vars=list(cfg.get("sum", [])),
                weighted_mean_vars=list(cfg.get("weighted_mean", [])),
                mean_vars=list(cfg.get("mean", [])),
                first_vars=list(cfg.get("first", [])),
                rename=dict(cfg.get("rename", {})),
            )
        )

    wanted = {s.strip().lower() for s in sources if s.strip()}
    return [s for s in out if s.name.lower() in wanted]


def _validate_grid_base(ds: xr.Dataset) -> None:
    for v in ["grid_id", "in_china"]:
        if v not in ds:
            raise KeyError(f"Grid base NetCDF missing variable: {v}")
    if ds["grid_id"].ndim != 2:
        raise ValueError("Expected grid_id to be 2D (lat, lon)")
    if "lat" not in ds.coords or "lon" not in ds.coords:
        raise KeyError("Grid base NetCDF must have lat/lon coordinates")


def _build_gid_to_flat_index(grid_id_2d: np.ndarray) -> pd.Series:
    """Return Series: index=grid_id(int), value=flat_index(int). Excludes -1."""
    flat = grid_id_2d.reshape(-1)
    valid_mask = flat != -1
    gids = flat[valid_mask].astype(np.int64)
    flat_idx = np.nonzero(valid_mask)[0].astype(np.int64)
    return pd.Series(flat_idx, index=gids)


def _safe_numeric(s: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(s):
        return s
    return pd.to_numeric(s, errors="coerce")


def _group_sum(df: pd.DataFrame, var: str) -> pd.Series:
    if var not in df.columns:
        return pd.Series(dtype=float)
    s = _safe_numeric(df[var])
    return s.groupby(df["grid_id"]).sum(min_count=1)


def _group_mean(df: pd.DataFrame, var: str) -> pd.Series:
    if var not in df.columns:
        return pd.Series(dtype=float)
    s = _safe_numeric(df[var])
    return s.groupby(df["grid_id"]).mean()


def _group_first(df: pd.DataFrame, var: str) -> pd.Series:
    if var not in df.columns:
        return pd.Series(dtype=float)
    # first non-null per group
    s = df[var]
    return s.groupby(df["grid_id"]).apply(lambda x: x.dropna().iloc[0] if x.notna().any() else np.nan)


def _group_weighted_mean(df: pd.DataFrame, var: str, weight_col: str) -> pd.Series:
    if var not in df.columns or weight_col not in df.columns:
        return pd.Series(dtype=float)

    x = _safe_numeric(df[var])
    w = _safe_numeric(df[weight_col])

    valid = x.notna() & w.notna() & (w > 0)
    if valid.sum() == 0:
        return pd.Series(dtype=float)

    x = x[valid]
    w = w[valid]
    gids = df.loc[valid, "grid_id"]

    num = (x * w).groupby(gids).sum(min_count=1)
    den = w.groupby(gids).sum(min_count=1)
    return num / den


def _scatter_to_grid(
    *,
    grid_shape: tuple[int, int],
    gid_to_flat: pd.Series,
    values_by_gid: pd.Series,
    dtype: Any,
    fill: Any,
) -> np.ndarray:
    """Scatter per-gid series into a 2D array aligned to grid_id array."""
    out_flat = np.full((grid_shape[0] * grid_shape[1],), fill, dtype=dtype)
    if len(values_by_gid) == 0:
        return out_flat.reshape(grid_shape)

    # Ensure int grid_id index
    s = values_by_gid.copy()
    s.index = s.index.astype(np.int64)

    # Keep only gids present in the grid
    common = s.index.intersection(gid_to_flat.index)
    if len(common) == 0:
        return out_flat.reshape(grid_shape)

    idx = gid_to_flat.loc[common].to_numpy(dtype=np.int64)
    vals = s.loc[common].to_numpy()

    # Convert values if needed
    if np.issubdtype(np.dtype(dtype), np.integer):
        # counts: NaN -> 0
        vals = np.nan_to_num(vals, nan=0.0).astype(dtype)
    else:
        vals = vals.astype(dtype, copy=False)

    out_flat[idx] = vals
    return out_flat.reshape(grid_shape)


def _compute_weight(df: pd.DataFrame, weight_col: str, multiply_col: str | None) -> pd.Series:
    """Compute a non-negative weight series for choosing 'main' elements.

    By default uses `weight_col` (typically overlap_length_km).
    If multiply_col is provided, uses: weight_col * multiply_col.
    Non-numeric values are coerced to NaN then treated as 0.
    """
    if weight_col not in df.columns:
        raise KeyError(f"Weight column '{weight_col}' not found")
    w = pd.to_numeric(df[weight_col], errors="coerce").fillna(0.0)
    if multiply_col is None:
        return w.clip(lower=0.0)
    if multiply_col not in df.columns:
        raise KeyError(f"Multiply column '{multiply_col}' not found")
    m = pd.to_numeric(df[multiply_col], errors="coerce").fillna(0.0)
    return (w * m).clip(lower=0.0)


def _pick_main_row_per_grid(df: pd.DataFrame, weight: pd.Series) -> pd.DataFrame:
    """Pick the 'main' intersecting segment row per grid cell.

    Rule: argmax weight within each grid_id.
    Ties: keep the first occurrence.
    """
    if len(df) == 0:
        return df.iloc[0:0].copy()
    if "grid_id" not in df.columns:
        raise KeyError("Expected column grid_id")

    w = pd.to_numeric(weight, errors="coerce").fillna(0.0)
    # idxmax per group returns first occurrence of max.
    idx = w.groupby(df["grid_id"]).idxmax()
    return df.loc[idx].copy()


def _pick_main_grid_per_segment(df: pd.DataFrame, seg_id_col: str, weight: pd.Series) -> pd.Series:
    """Return mapping: segment_id -> main_grid_id.

    Rule: assign each segment to the grid cell where it has the maximum weight.
    """
    if seg_id_col not in df.columns:
        raise KeyError(f"Expected segment id column '{seg_id_col}'")
    if "grid_id" not in df.columns:
        raise KeyError("Expected column grid_id")

    w = pd.to_numeric(weight, errors="coerce").fillna(0.0)
    idx = w.groupby(df[seg_id_col]).idxmax()
    main = df.loc[idx, [seg_id_col, "grid_id"]].copy()
    # Ensure integer ids if possible
    main[seg_id_col] = pd.to_numeric(main[seg_id_col], errors="coerce")
    main["grid_id"] = pd.to_numeric(main["grid_id"], errors="coerce")
    main = main.dropna(subset=[seg_id_col, "grid_id"])
    return pd.Series(main["grid_id"].to_numpy(dtype=np.int64), index=main[seg_id_col].to_numpy(dtype=np.int64))


def aggregate_source_to_grid(
    *,
    grid_ds: xr.Dataset,
    source: SourceSpec,
    add_directionality: bool = False,
    main_weight_col: str | None = None,
    main_weight_multiply_col: str | None = None,
) -> xr.Dataset:
    if not source.mapping_path.exists():
        raise FileNotFoundError(f"Missing mapping table: {source.mapping_path}")

    df = pd.read_parquet(source.mapping_path)
    if "grid_id" not in df.columns:
        raise KeyError(f"Mapping missing grid_id: {source.mapping_path}")
    if source.weight_col not in df.columns:
        raise KeyError(f"Mapping missing weight_col '{source.weight_col}': {source.mapping_path}")

    # Base per-cell counts
    row_count = df.groupby("grid_id").size().astype(np.int32)
    unique_id_count: pd.Series | None = None
    if source.id_col and source.id_col in df.columns:
        unique_id_count = df.groupby("grid_id")[source.id_col].nunique(dropna=True).astype(np.int32)

    gid_to_flat = _build_gid_to_flat_index(grid_ds["grid_id"].to_numpy())
    grid_shape = grid_ds["grid_id"].shape

    out = xr.Dataset(coords={"lat": grid_ds["lat"], "lon": grid_ds["lon"]})

    # Always export these stable layers
    # 1) total river length in the cell
    length_sum = _group_sum(df, "overlap_length_km")
    length_name = source.rename.get("overlap_length_km", "river_length_km")
    out[f"{source.name}_{length_name}"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=length_sum,
            dtype=np.float32,
            fill=np.nan,
        ),
        {"long_name": f"{source.name} total river length within grid cell", "units": "km"},
    )

    # 2) counts
    out[f"{source.name}_segment_row_count"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=row_count,
            dtype=np.int32,
            fill=0,
        ),
        {"long_name": f"{source.name} intersecting segments (rows) per grid cell"},
    )
    if unique_id_count is not None:
        out[f"{source.name}_segment_count"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=unique_id_count,
                dtype=np.int32,
                fill=0,
            ),
            {"long_name": f"{source.name} unique segment IDs per grid cell"},
        )

    # Directionality (grid -> downstream grid) based on segment topology columns.
    if add_directionality:
        # We require segment id and NEXT_DOWN in the mapping table.
        seg_id_col = source.id_col or "HYRIV_ID"
        if seg_id_col not in df.columns:
            raise KeyError(
                f"Cannot add directionality: segment id column '{seg_id_col}' not found in {source.mapping_path}"
            )
        if "NEXT_DOWN" not in df.columns:
            raise KeyError(f"Cannot add directionality: NEXT_DOWN not found in {source.mapping_path}")

        # Choose main segment / main grid using an optional weighted rule.
        # Default: overlap_length_km (or source.weight_col if overridden by spec)
        mw_col = main_weight_col or source.weight_col
        w_main = _compute_weight(df, mw_col, main_weight_multiply_col)

        main_rows = _pick_main_row_per_grid(df, w_main)

        main_seg = pd.to_numeric(main_rows[seg_id_col], errors="coerce")
        main_down = pd.to_numeric(main_rows["NEXT_DOWN"], errors="coerce")
        # Normalize missing/out-of-network downstream ids to -1
        main_down = main_down.where(main_down.notna() & (main_down > 0), other=-1)

        seg_to_main_grid = _pick_main_grid_per_segment(df, seg_id_col, w_main)

        # Segment id -> NEXT_DOWN (reach topology). Should be constant per HYRIV_ID.
        seg_next = df[[seg_id_col, "NEXT_DOWN"]].copy()
        seg_next[seg_id_col] = pd.to_numeric(seg_next[seg_id_col], errors="coerce")
        seg_next["NEXT_DOWN"] = pd.to_numeric(seg_next["NEXT_DOWN"], errors="coerce")
        seg_next = seg_next.dropna(subset=[seg_id_col]).copy()
        seg_next = seg_next[seg_next[seg_id_col] > 0]
        seg_next["NEXT_DOWN"] = seg_next["NEXT_DOWN"].where(seg_next["NEXT_DOWN"].notna() & (seg_next["NEXT_DOWN"] > 0), other=-1)
        seg_next = seg_next.drop_duplicates(subset=[seg_id_col], keep="first")
        hyriv_to_next = pd.Series(
            seg_next["NEXT_DOWN"].to_numpy(dtype=np.int64),
            index=seg_next[seg_id_col].to_numpy(dtype=np.int64),
            dtype=np.int64,
        )

        # grid_id -> next_grid_id
        # If NEXT_DOWN remains in the same grid cell (grid-level self-loop), walk further downstream
        # until leaving the current cell or reaching termination.
        next_grid_vals: list[int] = []
        for gid, down_id in zip(main_rows["grid_id"].to_numpy(dtype=np.int64), main_down.to_numpy(dtype=np.int64)):
            if down_id <= 0:
                next_grid_vals.append(-1)
                continue
            seen: set[int] = set()
            cur = int(down_id)
            out_gid = -1
            while cur > 0:
                if cur in seen:
                    out_gid = -1
                    break
                seen.add(cur)
                ng = seg_to_main_grid.get(cur, None)
                if ng is None:
                    out_gid = -1
                    break
                ng_int = int(ng)
                if ng_int != int(gid):
                    out_gid = ng_int
                    break
                cur = int(hyriv_to_next.get(cur, -1))
            next_grid_vals.append(out_gid)

        next_grid = pd.Series(next_grid_vals, index=main_rows["grid_id"].to_numpy(dtype=np.int64), dtype=np.int64)

        # Scatter main ids and next pointers to 2D.
        out[f"{source.name}_main_hyriv_id"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=pd.Series(main_seg.to_numpy(dtype=np.float64), index=main_rows["grid_id"].to_numpy(dtype=np.int64)),
                dtype=np.int32,
                fill=-1,
            ),
            {
                "long_name": f"{source.name} main segment id per grid cell (argmax main_weight)",
                "main_weight_col": str(mw_col),
                "main_weight_multiply_col": str(main_weight_multiply_col) if main_weight_multiply_col else "",
            },
        )
        out[f"{source.name}_main_next_down"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=pd.Series(main_down.to_numpy(dtype=np.float64), index=main_rows["grid_id"].to_numpy(dtype=np.int64)),
                dtype=np.int32,
                fill=-1,
            ),
            {"long_name": f"{source.name} NEXT_DOWN of main segment per grid cell"},
        )
        out[f"{source.name}_next_grid_id"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=next_grid,
                dtype=np.int32,
                fill=-1,
            ),
            {"long_name": f"{source.name} downstream grid_id pointer based on main segment NEXT_DOWN"},
        )

        # Also export downstream indices for fast stepping on the 2D array.
        nlat, nlon = grid_shape
        next_flat = pd.Series(-1, index=next_grid.index, dtype=np.int64)
        common = next_grid[next_grid > 0].index.intersection(gid_to_flat.index)
        if len(common) > 0:
            ngids = next_grid.loc[common].astype(np.int64)
            # Keep only ngids present in gid_to_flat
            ngids = ngids[ngids.isin(gid_to_flat.index)]
            if len(ngids) > 0:
                next_flat.loc[ngids.index] = gid_to_flat.loc[ngids.to_numpy(dtype=np.int64)].to_numpy(dtype=np.int64)

        next_lat_idx = (next_flat // nlon).where(next_flat >= 0, other=-1)
        next_lon_idx = (next_flat % nlon).where(next_flat >= 0, other=-1)

        out[f"{source.name}_next_lat_index"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=next_lat_idx,
                dtype=np.int16,
                fill=-1,
            ),
            {"long_name": f"{source.name} downstream pointer: lat index in grid array"},
        )
        out[f"{source.name}_next_lon_index"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=next_lon_idx,
                dtype=np.int16,
                fill=-1,
            ),
            {"long_name": f"{source.name} downstream pointer: lon index in grid array"},
        )

    # Additional variables from spec
    # sums
    for var in source.sum_vars:
        if var == "overlap_length_km":
            continue  # already handled
        series = _group_sum(df, var)
        if len(series) == 0:
            continue
        out_name = source.rename.get(var, var)
        out[f"{source.name}_{out_name}"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=series,
                dtype=np.float32,
                fill=np.nan,
            ),
            {"aggregation": "sum"},
        )

    # weighted means
    for var in source.weighted_mean_vars:
        series = _group_weighted_mean(df, var, source.weight_col)
        if len(series) == 0:
            continue
        out_name = source.rename.get(var, var)
        out[f"{source.name}_{out_name}"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=series,
                dtype=np.float32,
                fill=np.nan,
            ),
            {"aggregation": f"length_weighted_mean(weight={source.weight_col})"},
        )

    # plain means
    for var in source.mean_vars:
        series = _group_mean(df, var)
        if len(series) == 0:
            continue
        out_name = source.rename.get(var, var)
        out[f"{source.name}_{out_name}"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=series,
                dtype=np.float32,
                fill=np.nan,
            ),
            {"aggregation": "mean"},
        )

    # first
    for var in source.first_vars:
        series = _group_first(df, var)
        if len(series) == 0:
            continue
        out_name = source.rename.get(var, var)
        out[f"{source.name}_{out_name}"] = (
            ("lat", "lon"),
            _scatter_to_grid(
                grid_shape=grid_shape,
                gid_to_flat=gid_to_flat,
                values_by_gid=series,
                dtype=np.float32,
                fill=np.nan,
            ),
            {"aggregation": "first_non_null"},
        )

    # Apply mask outside China (keep counts at 0; keep continuous as NaN)
    in_china = grid_ds["in_china"].to_numpy().astype(bool)
    for name, da in list(out.data_vars.items()):
        if np.issubdtype(da.dtype, np.integer):
            out[name] = da.where(in_china, other=0)
        else:
            out[name] = da.where(in_china)

    return out


def export_rivernetwork_to_netcdf(
    *,
    grid_nc: Path,
    sources: list[str],
    spec_path: Path | None,
    hydrorivers_map: Path,
    riveratlas_map: Path,
    out_path: Path | None,
    out_attrs_path: Path | None,
    out_direction_path: Path | None,
    add_directionality: bool,
    main_weight_col: str | None,
    main_weight_multiply_col: str | None,
) -> None:
    if not grid_nc.exists():
        raise FileNotFoundError(f"Grid base NetCDF not found: {grid_nc}")

    grid_ds = xr.open_dataset(grid_nc)
    _validate_grid_base(grid_ds)

    source_specs = _load_spec_or_default(
        sources=sources,
        spec_path=spec_path,
        hydrorivers_map=hydrorivers_map,
        riveratlas_map=riveratlas_map,
    )
    if len(source_specs) == 0:
        raise ValueError("No sources selected. Use --sources hydrorivers,riveratlas")

    combined = xr.Dataset(
        coords={"lat": grid_ds["lat"], "lon": grid_ds["lon"]},
        attrs={
            "title": "China 0.1° river-network grid summary",
            "grid_base": str(grid_nc),
            "notes": "Derived from grid-to-line mapping tables using per-cell overlap_length_km weighting.",
        },
    )

    # Keep base alignment variables
    combined["grid_id"] = grid_ds["grid_id"].astype(np.int32)
    combined["in_china"] = grid_ds["in_china"].astype(bool)

    for spec in source_specs:
        part = aggregate_source_to_grid(
            grid_ds=grid_ds,
            source=spec,
            add_directionality=add_directionality,
            main_weight_col=main_weight_col,
            main_weight_multiply_col=main_weight_multiply_col,
        )
        combined = xr.merge([combined, part], compat="override")

    def _encoding_for(ds: xr.Dataset) -> dict[str, dict[str, Any]]:
        encoding: dict[str, dict[str, Any]] = {}
        for name, da in ds.data_vars.items():
            if name in {"grid_id", "in_china"}:
                continue
            if np.issubdtype(da.dtype, np.floating):
                encoding[name] = {"zlib": True, "complevel": 4, "dtype": "float32"}
            elif np.issubdtype(da.dtype, np.integer):
                encoding[name] = {"zlib": True, "complevel": 4}
        return encoding

    # Write combined output (backward-compatible) if requested.
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        combined.to_netcdf(out_path, encoding=_encoding_for(combined))

    # Optionally split into attributes and directionality.
    if out_attrs_path is not None or out_direction_path is not None:
        direction_suffixes = (
            "_main_hyriv_id",
            "_main_next_down",
            "_next_grid_id",
            "_next_lat_index",
            "_next_lon_index",
        )
        dir_vars = [v for v in combined.data_vars if v.endswith(direction_suffixes)]
        base_vars = ["grid_id", "in_china"]

        if out_attrs_path is not None:
            attrs_vars = [v for v in combined.data_vars if v not in dir_vars]
            attrs_ds = combined[attrs_vars]
            out_attrs_path.parent.mkdir(parents=True, exist_ok=True)
            attrs_ds.to_netcdf(out_attrs_path, encoding=_encoding_for(attrs_ds))

        if out_direction_path is not None:
            if not add_directionality:
                raise ValueError("--out-direction requires --add-directionality")
            if len(dir_vars) == 0:
                # Still write base vars so the file is readable, but warn by metadata.
                dir_ds = combined[base_vars].copy()
                dir_ds.attrs["warning"] = "No directionality variables found; check mapping columns or enable --add-directionality"
            else:
                dir_ds = combined[base_vars + dir_vars]
            out_direction_path.parent.mkdir(parents=True, exist_ok=True)
            dir_ds.to_netcdf(out_direction_path, encoding=_encoding_for(dir_ds))


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate river-network mapping tables to 0.1° grid NetCDF")
    parser.add_argument("--grid-nc", type=str, default=str(DEFAULT_GRID_NC))
    parser.add_argument(
        "--sources",
        type=str,
        default="hydrorivers,riveratlas",
        help="Comma-separated: hydrorivers,riveratlas",
    )
    parser.add_argument(
        "--spec",
        type=str,
        default=None,
        help="Optional JSON spec defining aggregation variables and rules.",
    )
    parser.add_argument("--hydrorivers-map", type=str, default=str(DEFAULT_HYDRORIVERS_MAP))
    parser.add_argument("--riveratlas-map", type=str, default=str(DEFAULT_RIVERATLAS_MAP))
    parser.add_argument(
        "--out",
        type=str,
        default=str(DEFAULT_OUT),
        help="Optional combined output NetCDF. Use empty string to disable.",
    )
    parser.add_argument(
        "--out-attrs",
        type=str,
        default=None,
        help=f"Optional attributes-only NetCDF (suggested default: {DEFAULT_OUT_ATTRS}).",
    )
    parser.add_argument(
        "--out-direction",
        type=str,
        default=None,
        help=f"Optional directionality-only NetCDF (suggested default: {DEFAULT_OUT_DIRECTION}). Requires --add-directionality.",
    )
    parser.add_argument(
        "--add-directionality",
        action="store_true",
        help="Also export a single downstream pointer per grid cell based on HYRIV_ID -> NEXT_DOWN topology.",
    )
    parser.add_argument(
        "--main-weight-col",
        type=str,
        default=None,
        help="Weight column used to choose the main segment/grid for directionality. Default: same as weight_col (typically overlap_length_km).",
    )
    parser.add_argument(
        "--main-weight-multiply-col",
        type=str,
        default=None,
        help="Optional multiplier column for main-weight (e.g., DIS_AV_CMS). Effective weight = main_weight_col * multiplier.",
    )
    args = parser.parse_args()

    export_rivernetwork_to_netcdf(
        grid_nc=Path(args.grid_nc),
        sources=[s.strip() for s in args.sources.split(",") if s.strip()],
        spec_path=Path(args.spec) if args.spec else None,
        hydrorivers_map=Path(args.hydrorivers_map),
        riveratlas_map=Path(args.riveratlas_map),
        out_path=Path(args.out) if str(args.out).strip() else None,
        out_attrs_path=Path(args.out_attrs) if args.out_attrs else None,
        out_direction_path=Path(args.out_direction) if args.out_direction else None,
        add_directionality=bool(args.add_directionality),
        main_weight_col=args.main_weight_col,
        main_weight_multiply_col=args.main_weight_multiply_col,
    )
    if str(args.out).strip():
        print(f"Wrote: {args.out}")
    if args.out_attrs:
        print(f"Wrote: {args.out_attrs}")
    if args.out_direction:
        print(f"Wrote: {args.out_direction}")


if __name__ == "__main__":
    main()
