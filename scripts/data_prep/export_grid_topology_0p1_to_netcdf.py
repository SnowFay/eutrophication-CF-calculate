"""Export a unified 0.1° grid topology NetCDF (river routing + lakes context).

What this file represents
-------------------------
A single, consistent *spatial topology* on the 0.1° China grid that you can use for
Helmes/Henderson-style along-network calculations:

- River routing backbone: one downstream pointer per grid cell (single next cell)
- Lake context on nodes: lake area fraction / presence (does not change edges)

Why not encode full multi-direction routing here?
-------------------------------------------------
To stay as consistent as possible with Helmes (2012) and Henderson (2021) routing
assumptions, we default to a single downstream pointer per grid cell (main channel).
Multi-direction (Zhuang-style) can be added later via an edge list / sparse matrix.

Inputs (defaults)
-----------------
- Grid base NetCDF:
  data/processed/grid_0p1/grid_cells_china_0p1.nc
- River mapping tables:
  data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet
  data/processed/grid_0p1/grid_riveratlas_china_0p1_mapping.parquet
- Lake mapping tables:
  data/processed/grid_0p1/grid_hydrolakes_china_0p1_mapping.parquet
  data/processed/grid_0p1/grid_lakeatlas_china_0p1_mapping.parquet
- Grid parquet (for accurate cell areas):
  data/processed/grid_0p1/grid_cells_china_0p1.parquet

Outputs (default)
-----------------
- data/processed/grid_0p1/grid_topology_china_0p1.nc

Exported variables (per source)
-------------------------------
River (directionality):
- `<river>_main_hyriv_id`
- `<river>_main_next_down`
- `<river>_next_grid_id`
- `<river>_next_lat_index`
- `<river>_next_lon_index`

Lakes (context):
- `<lakes>_lake_area_km2_in_cell`
- `<lakes>_lake_area_frac_of_cell`
- `<lakes>_has_lake`

"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

import geopandas as gpd


DEFAULT_GRID_NC = Path("data/processed/grid_0p1/grid_cells_china_0p1.nc")
DEFAULT_GRID_PARQUET = Path("data/processed/grid_0p1/grid_cells_china_0p1.parquet")

DEFAULT_HYDRORIVERS_MAP = Path("data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet")
DEFAULT_RIVERATLAS_MAP = Path("data/processed/grid_0p1/grid_riveratlas_china_0p1_mapping.parquet")

DEFAULT_HYDROLAKES_MAP = Path("data/processed/grid_0p1/grid_hydrolakes_china_0p1_mapping.parquet")
DEFAULT_LAKEATLAS_MAP = Path("data/processed/grid_0p1/grid_lakeatlas_china_0p1_mapping.parquet")

DEFAULT_OUT = Path("data/processed/grid_0p1/grid_topology_china_0p1.nc")


def _validate_grid_base(ds: xr.Dataset) -> None:
    for v in ["grid_id", "in_china"]:
        if v not in ds:
            raise KeyError(f"Grid base NetCDF missing variable: {v}")
    if ds["grid_id"].ndim != 2:
        raise ValueError("Expected grid_id to be 2D (lat, lon)")


def _build_gid_to_flat_index(grid_id_2d: np.ndarray) -> pd.Series:
    flat = grid_id_2d.reshape(-1)
    valid_mask = flat != -1
    gids = flat[valid_mask].astype(np.int64)
    flat_idx = np.nonzero(valid_mask)[0].astype(np.int64)
    return pd.Series(flat_idx, index=gids)


def _scatter_to_grid(
    *,
    grid_shape: tuple[int, int],
    gid_to_flat: pd.Series,
    values_by_gid: pd.Series,
    dtype: object,
    fill: object,
) -> np.ndarray:
    out_flat = np.full((grid_shape[0] * grid_shape[1],), fill, dtype=dtype)
    if len(values_by_gid) == 0:
        return out_flat.reshape(grid_shape)

    s = values_by_gid.copy()
    s.index = s.index.astype(np.int64)
    common = s.index.intersection(gid_to_flat.index)
    if len(common) == 0:
        return out_flat.reshape(grid_shape)

    idx = gid_to_flat.loc[common].to_numpy(dtype=np.int64)
    vals = s.loc[common].to_numpy()
    vals = np.nan_to_num(vals, nan=float(fill) if isinstance(fill, (int, float)) else 0.0).astype(dtype, copy=False)
    out_flat[idx] = vals
    return out_flat.reshape(grid_shape)


def _compute_cell_area_km2(grid_parquet: Path) -> pd.Series:
    if not grid_parquet.exists():
        raise FileNotFoundError(f"Grid parquet not found: {grid_parquet}")
    g = gpd.read_parquet(grid_parquet)
    if "grid_id" not in g.columns or "geometry" not in g.columns:
        raise KeyError("Grid parquet must contain grid_id and geometry")
    area_km2 = g.to_crs(6933).geometry.area / 1e6
    return pd.Series(area_km2.to_numpy(dtype=float), index=g["grid_id"].to_numpy(dtype=np.int64))


def _river_directionality_layers(
    *,
    grid_ds: xr.Dataset,
    mapping_path: Path,
    prefix: str,
    main_weight_col: str | None,
    main_weight_multiply_col: str | None,
) -> xr.Dataset:
    """Build per-cell single downstream pointer based on HYRIV_ID -> NEXT_DOWN.

    Main-segment selection weight:
    - default: overlap_length_km
    - if multiply col provided: overlap_length_km * multiply
    """
    if not mapping_path.exists():
        raise FileNotFoundError(f"Missing mapping table: {mapping_path}")

    df = pd.read_parquet(mapping_path)
    for c in ["grid_id", "HYRIV_ID", "NEXT_DOWN", "overlap_length_km"]:
        if c not in df.columns:
            raise KeyError(f"Mapping missing required column '{c}': {mapping_path}")

    wcol = main_weight_col or "overlap_length_km"
    if wcol not in df.columns:
        raise KeyError(f"main_weight_col '{wcol}' not found in {mapping_path}")

    w = pd.to_numeric(df[wcol], errors="coerce").fillna(0.0)
    if main_weight_multiply_col:
        if main_weight_multiply_col not in df.columns:
            raise KeyError(f"main_weight_multiply_col '{main_weight_multiply_col}' not found in {mapping_path}")
        m = pd.to_numeric(df[main_weight_multiply_col], errors="coerce").fillna(0.0)
        w = (w * m).fillna(0.0)
    w = w.clip(lower=0.0)

    # 1) For each grid cell: pick main intersecting segment row (argmax weight)
    idx_main_row = w.groupby(df["grid_id"]).idxmax()
    main = df.loc[idx_main_row, ["grid_id", "HYRIV_ID", "NEXT_DOWN"]].copy()

    main["HYRIV_ID"] = pd.to_numeric(main["HYRIV_ID"], errors="coerce")
    main["NEXT_DOWN"] = pd.to_numeric(main["NEXT_DOWN"], errors="coerce")
    main["NEXT_DOWN"] = main["NEXT_DOWN"].where(main["NEXT_DOWN"].notna() & (main["NEXT_DOWN"] > 0), other=-1)

    # 2) For each segment: assign it to a main grid (argmax weight)
    idx_main_grid = w.groupby(df["HYRIV_ID"]).idxmax()
    seg_main = df.loc[idx_main_grid, ["HYRIV_ID", "grid_id"]].copy()
    seg_main["HYRIV_ID"] = pd.to_numeric(seg_main["HYRIV_ID"], errors="coerce")
    seg_main["grid_id"] = pd.to_numeric(seg_main["grid_id"], errors="coerce")
    seg_main = seg_main.dropna(subset=["HYRIV_ID", "grid_id"])
    seg_to_grid = pd.Series(seg_main["grid_id"].to_numpy(dtype=np.int64), index=seg_main["HYRIV_ID"].to_numpy(dtype=np.int64))

    # Segment id -> NEXT_DOWN (reach topology). Should be constant per HYRIV_ID.
    seg_next = df[["HYRIV_ID", "NEXT_DOWN"]].copy()
    seg_next["HYRIV_ID"] = pd.to_numeric(seg_next["HYRIV_ID"], errors="coerce")
    seg_next["NEXT_DOWN"] = pd.to_numeric(seg_next["NEXT_DOWN"], errors="coerce")
    seg_next = seg_next.dropna(subset=["HYRIV_ID"]).copy()
    seg_next = seg_next[seg_next["HYRIV_ID"] > 0]
    seg_next["NEXT_DOWN"] = seg_next["NEXT_DOWN"].where(seg_next["NEXT_DOWN"].notna() & (seg_next["NEXT_DOWN"] > 0), other=-1)
    seg_next = seg_next.drop_duplicates(subset=["HYRIV_ID"], keep="first")
    hyriv_to_next = pd.Series(
        seg_next["NEXT_DOWN"].to_numpy(dtype=np.int64),
        index=seg_next["HYRIV_ID"].to_numpy(dtype=np.int64),
        dtype=np.int64,
    )

    # 3) grid_id -> next_grid_id using NEXT_DOWN
    # If NEXT_DOWN remains in the same grid cell (a grid-level self-loop), walk further downstream
    # until leaving the current cell or reaching termination.
    next_grid_vals: list[int] = []
    for gid, down in zip(main["grid_id"].to_numpy(dtype=np.int64), main["NEXT_DOWN"].to_numpy(dtype=np.int64)):
        if down <= 0:
            next_grid_vals.append(-1)
            continue
        seen: set[int] = set()
        cur = int(down)
        out_gid = -1
        while cur > 0:
            if cur in seen:
                out_gid = -1
                break
            seen.add(cur)
            ng = seg_to_grid.get(cur, None)
            if ng is None:
                out_gid = -1
                break
            ng_int = int(ng)
            if ng_int != int(gid):
                out_gid = ng_int
                break
            # still in same grid cell; advance along reach topology
            cur = int(hyriv_to_next.get(cur, -1))
        next_grid_vals.append(out_gid)

    next_grid = pd.Series(next_grid_vals, index=main["grid_id"].to_numpy(dtype=np.int64), dtype=np.int64)

    gid_to_flat = _build_gid_to_flat_index(grid_ds["grid_id"].to_numpy())
    grid_shape = grid_ds["grid_id"].shape
    nlat, nlon = grid_shape

    out = xr.Dataset(coords={"lat": grid_ds["lat"], "lon": grid_ds["lon"]})
    out[f"{prefix}_main_hyriv_id"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=pd.Series(main["HYRIV_ID"].to_numpy(dtype=np.float64), index=main["grid_id"].to_numpy(dtype=np.int64)),
            dtype=np.int32,
            fill=-1,
        ),
    )
    out[f"{prefix}_main_next_down"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=pd.Series(main["NEXT_DOWN"].to_numpy(dtype=np.float64), index=main["grid_id"].to_numpy(dtype=np.int64)),
            dtype=np.int32,
            fill=-1,
        ),
    )
    out[f"{prefix}_next_grid_id"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=next_grid,
            dtype=np.int32,
            fill=-1,
        ),
    )

    # next indices
    next_flat = pd.Series(-1, index=next_grid.index, dtype=np.int64)
    valid = next_grid[next_grid > 0]
    if len(valid) > 0:
        ngids = valid[valid.isin(gid_to_flat.index)].astype(np.int64)
        if len(ngids) > 0:
            next_flat.loc[ngids.index] = gid_to_flat.loc[ngids.to_numpy(dtype=np.int64)].to_numpy(dtype=np.int64)

    next_lat_idx = (next_flat // nlon).where(next_flat >= 0, other=-1)
    next_lon_idx = (next_flat % nlon).where(next_flat >= 0, other=-1)
    out[f"{prefix}_next_lat_index"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=next_lat_idx,
            dtype=np.int16,
            fill=-1,
        ),
    )
    out[f"{prefix}_next_lon_index"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=next_lon_idx,
            dtype=np.int16,
            fill=-1,
        ),
    )

    in_china = grid_ds["in_china"].to_numpy().astype(bool)
    for v in out.data_vars:
        out[v] = out[v].where(in_china, other=-1)

    out.attrs.update(
        {
            "main_weight_col": str(wcol),
            "main_weight_multiply_col": str(main_weight_multiply_col) if main_weight_multiply_col else "",
            "mapping_path": str(mapping_path),
        }
    )
    return out


def _lake_context_layers(
    *,
    grid_ds: xr.Dataset,
    grid_parquet: Path,
    mapping_path: Path,
    prefix: str,
) -> xr.Dataset:
    if not mapping_path.exists():
        raise FileNotFoundError(f"Missing mapping table: {mapping_path}")
    df = pd.read_parquet(mapping_path)
    for c in ["grid_id", "overlap_area_km2"]:
        if c not in df.columns:
            raise KeyError(f"Mapping missing required column '{c}': {mapping_path}")

    area_sum = pd.to_numeric(df["overlap_area_km2"], errors="coerce").groupby(df["grid_id"]).sum(min_count=1)
    cell_area = _compute_cell_area_km2(grid_parquet)
    common = area_sum.index.intersection(cell_area.index)
    frac = pd.Series(dtype=float)
    if len(common) > 0:
        denom = cell_area.loc[common].replace(0, np.nan)
        frac = (area_sum.loc[common] / denom).clip(lower=0.0)

    gid_to_flat = _build_gid_to_flat_index(grid_ds["grid_id"].to_numpy())
    grid_shape = grid_ds["grid_id"].shape

    out = xr.Dataset(coords={"lat": grid_ds["lat"], "lon": grid_ds["lon"]})
    out[f"{prefix}_lake_area_km2_in_cell"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=area_sum,
            dtype=np.float32,
            fill=np.nan,
        ),
    )
    out[f"{prefix}_lake_area_frac_of_cell"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=frac,
            dtype=np.float32,
            fill=np.nan,
        ),
    )
    out[f"{prefix}_has_lake"] = (out[f"{prefix}_lake_area_km2_in_cell"] > 0).astype(bool)

    in_china = grid_ds["in_china"].to_numpy().astype(bool)
    out[f"{prefix}_lake_area_km2_in_cell"] = out[f"{prefix}_lake_area_km2_in_cell"].where(in_china)
    out[f"{prefix}_lake_area_frac_of_cell"] = out[f"{prefix}_lake_area_frac_of_cell"].where(in_china)
    out[f"{prefix}_has_lake"] = out[f"{prefix}_has_lake"].where(in_china, other=False)
    out.attrs.update({"mapping_path": str(mapping_path)})
    return out


def export_grid_topology(
    *,
    grid_nc: Path,
    grid_parquet: Path,
    hydrorivers_map: Path,
    riveratlas_map: Path,
    hydrolakes_map: Path,
    lakeatlas_map: Path,
    out_path: Path,
    main_weight_col: str | None,
    main_weight_multiply_col: str | None,
) -> None:
    if not grid_nc.exists():
        raise FileNotFoundError(f"Grid base NetCDF not found: {grid_nc}")

    grid_ds = xr.open_dataset(grid_nc)
    _validate_grid_base(grid_ds)

    out = xr.Dataset(coords={"lat": grid_ds["lat"], "lon": grid_ds["lon"]})
    out.attrs.update(
        {
            "title": "China 0.1° grid topology (river routing + lakes context)",
            "grid_base": str(grid_nc),
            "notes": "Single downstream pointer per cell for Helmes/Henderson-style routing; lakes are node context.",
        }
    )

    out["grid_id"] = grid_ds["grid_id"].astype(np.int32)
    out["in_china"] = grid_ds["in_china"].astype(bool)

    # --- Rivers: directionality layers ---
    if hydrorivers_map.exists():
        out = xr.merge(
            [
                out,
                _river_directionality_layers(
                    grid_ds=grid_ds,
                    mapping_path=hydrorivers_map,
                    prefix="hydrorivers",
                    main_weight_col=main_weight_col,
                    main_weight_multiply_col=main_weight_multiply_col,
                ),
            ],
            compat="override",
        )
    if riveratlas_map.exists():
        out = xr.merge(
            [
                out,
                _river_directionality_layers(
                    grid_ds=grid_ds,
                    mapping_path=riveratlas_map,
                    prefix="riveratlas",
                    main_weight_col=main_weight_col,
                    main_weight_multiply_col=main_weight_multiply_col,
                ),
            ],
            compat="override",
        )

    # --- Lakes: context layers ---
    if hydrolakes_map.exists():
        out = xr.merge(
            [
                out,
                _lake_context_layers(
                    grid_ds=grid_ds,
                    grid_parquet=grid_parquet,
                    mapping_path=hydrolakes_map,
                    prefix="hydrolakes",
                ),
            ],
            compat="override",
        )
    if lakeatlas_map.exists():
        out = xr.merge(
            [
                out,
                _lake_context_layers(
                    grid_ds=grid_ds,
                    grid_parquet=grid_parquet,
                    mapping_path=lakeatlas_map,
                    prefix="lakeatlas",
                ),
            ],
            compat="override",
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)

    encoding: dict[str, dict[str, object]] = {}
    for name, da in out.data_vars.items():
        if name in {"grid_id", "in_china"}:
            continue
        if np.issubdtype(da.dtype, np.floating):
            encoding[name] = {"zlib": True, "complevel": 4, "dtype": "float32"}
        elif np.issubdtype(da.dtype, np.integer):
            encoding[name] = {"zlib": True, "complevel": 4}
        elif da.dtype == bool:
            encoding[name] = {"zlib": True, "complevel": 4}

    out.to_netcdf(out_path, encoding=encoding)


def main() -> None:
    p = argparse.ArgumentParser(description="Export unified 0.1° grid topology NetCDF")
    p.add_argument("--grid-nc", type=str, default=str(DEFAULT_GRID_NC))
    p.add_argument("--grid-parquet", type=str, default=str(DEFAULT_GRID_PARQUET))

    p.add_argument("--hydrorivers-map", type=str, default=str(DEFAULT_HYDRORIVERS_MAP))
    p.add_argument("--riveratlas-map", type=str, default=str(DEFAULT_RIVERATLAS_MAP))

    p.add_argument("--hydrolakes-map", type=str, default=str(DEFAULT_HYDROLAKES_MAP))
    p.add_argument("--lakeatlas-map", type=str, default=str(DEFAULT_LAKEATLAS_MAP))

    p.add_argument("--out", type=str, default=str(DEFAULT_OUT))

    p.add_argument(
        "--main-weight-col",
        type=str,
        default=None,
        help="Weight column used to choose the main segment/grid for river directionality. Default: overlap_length_km.",
    )
    p.add_argument(
        "--main-weight-multiply-col",
        type=str,
        default=None,
        help="Optional multiplier column for main-weight (e.g., DIS_AV_CMS). Effective weight = main_weight_col * multiplier.",
    )

    args = p.parse_args()

    export_grid_topology(
        grid_nc=Path(args.grid_nc),
        grid_parquet=Path(args.grid_parquet),
        hydrorivers_map=Path(args.hydrorivers_map),
        riveratlas_map=Path(args.riveratlas_map),
        hydrolakes_map=Path(args.hydrolakes_map),
        lakeatlas_map=Path(args.lakeatlas_map),
        out_path=Path(args.out),
        main_weight_col=args.main_weight_col,
        main_weight_multiply_col=args.main_weight_multiply_col,
    )
    print(f"Wrote: {args.out}")


if __name__ == "__main__":
    main()
