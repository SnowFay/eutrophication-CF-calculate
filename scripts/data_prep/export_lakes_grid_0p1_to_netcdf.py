"""Export lake/reservoir attributes to a 0.1° grid NetCDF.

This script aggregates polygon->grid mapping tables (HydroLAKES / LakeATLAS) into
per-grid-cell layers aligned to the existing grid base NetCDF.

Design principles
-----------------
- Mapping tables keep all lake fields (lossless). NetCDF output must be *one value
  per grid cell*.
- Correct aggregation depends on semantics:
  - Extensive quantities within a cell (e.g., lake area within cell) -> sum
  - Lake attributes (e.g., residence time, average depth) -> area-weighted mean

Default output is conservative and always meaningful:
- `<source>_lake_area_km2_in_cell` = sum(overlap_area_km2)
- `<source>_lake_count` = nunique(Hylak_id)
- `<source>_lake_area_frac_of_cell` = area_in_cell / cell_area_km2

Optional extra variables can be exported via a JSON spec (`--spec`).

Inputs (defaults)
-----------------
- Grid base NetCDF:
  data/processed/grid_0p1/grid_cells_china_0p1.nc
- Grid cells GeoParquet (for accurate cell areas in km2):
  data/processed/grid_0p1/grid_cells_china_0p1.parquet
- Mapping tables:
  data/processed/grid_0p1/grid_hydrolakes_china_0p1_mapping.parquet
  data/processed/grid_0p1/grid_lakeatlas_china_0p1_mapping.parquet

Outputs (defaults)
-----------------
- data/processed/grid_0p1/grid_lakes_attributes_china_0p1.nc

"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr


DEFAULT_GRID_NC = Path("data/processed/grid_0p1/grid_cells_china_0p1.nc")
DEFAULT_GRID_PARQUET = Path("data/processed/grid_0p1/grid_cells_china_0p1.parquet")

DEFAULT_HYDROLAKES_MAP = Path("data/processed/grid_0p1/grid_hydrolakes_china_0p1_mapping.parquet")
DEFAULT_LAKEATLAS_MAP = Path("data/processed/grid_0p1/grid_lakeatlas_china_0p1_mapping.parquet")

DEFAULT_OUT_ATTRS = Path("data/processed/grid_0p1/grid_lakes_attributes_china_0p1.nc")

AggKind = Literal["sum", "weighted_mean", "mean", "first"]


@dataclass(frozen=True)
class SourceSpec:
    name: str
    mapping_path: Path
    id_col: str
    weight_col: str
    sum_vars: list[str]
    weighted_mean_vars: list[str]
    mean_vars: list[str]
    first_vars: list[str]
    rename: dict[str, str]


def _validate_grid_base(ds: xr.Dataset) -> None:
    for v in ["grid_id", "in_china"]:
        if v not in ds:
            raise KeyError(f"Grid base NetCDF missing variable: {v}")
    if ds["grid_id"].ndim != 2:
        raise ValueError("Expected grid_id to be 2D (lat, lon)")
    if "lat" not in ds.coords or "lon" not in ds.coords:
        raise KeyError("Grid base NetCDF must have lat/lon coordinates")


def _build_gid_to_flat_index(grid_id_2d: np.ndarray) -> pd.Series:
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

    if np.issubdtype(np.dtype(dtype), np.integer):
        vals = np.nan_to_num(vals, nan=0.0).astype(dtype)
    else:
        vals = vals.astype(dtype, copy=False)

    out_flat[idx] = vals
    return out_flat.reshape(grid_shape)


def _compute_cell_area_km2(grid_parquet: Path) -> pd.Series:
    if not grid_parquet.exists():
        raise FileNotFoundError(f"Grid parquet not found: {grid_parquet}")
    g = gpd.read_parquet(grid_parquet)
    if "grid_id" not in g.columns or "geometry" not in g.columns:
        raise KeyError("Grid parquet must contain grid_id and geometry")
    # Equal-area projection
    area_km2 = g.to_crs(6933).geometry.area / 1e6
    return pd.Series(area_km2.to_numpy(dtype=float), index=g["grid_id"].to_numpy(dtype=np.int64))


def _load_spec_or_default(
    *,
    sources: list[str],
    spec_path: Path | None,
    hydrolakes_map: Path,
    lakeatlas_map: Path,
) -> list[SourceSpec]:
    wanted = {s.strip().lower() for s in sources if s.strip()}

    if spec_path is None:
        specs: list[SourceSpec] = []
        if "hydrolakes" in wanted:
            specs.append(
                SourceSpec(
                    name="hydrolakes",
                    mapping_path=hydrolakes_map,
                    id_col="Hylak_id",
                    weight_col="overlap_area_km2",
                    sum_vars=["overlap_area_km2"],
                    weighted_mean_vars=[],
                    mean_vars=[],
                    first_vars=[],
                    rename={"overlap_area_km2": "lake_area_km2_in_cell"},
                )
            )
        if "lakeatlas" in wanted:
            specs.append(
                SourceSpec(
                    name="lakeatlas",
                    mapping_path=lakeatlas_map,
                    id_col="Hylak_id",
                    weight_col="overlap_area_km2",
                    sum_vars=["overlap_area_km2"],
                    weighted_mean_vars=[],
                    mean_vars=[],
                    first_vars=[],
                    rename={"overlap_area_km2": "lake_area_km2_in_cell"},
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
                id_col=str(cfg.get("id_col", "Hylak_id")),
                weight_col=str(cfg.get("weight_col", "overlap_area_km2")),
                sum_vars=list(cfg.get("sum", [])),
                weighted_mean_vars=list(cfg.get("weighted_mean", [])),
                mean_vars=list(cfg.get("mean", [])),
                first_vars=list(cfg.get("first", [])),
                rename=dict(cfg.get("rename", {})),
            )
        )

    return [s for s in out if s.name.lower() in wanted]


def aggregate_lake_source_to_grid(
    *,
    grid_ds: xr.Dataset,
    gid_to_flat: pd.Series,
    grid_shape: tuple[int, int],
    cell_area_km2_by_gid: pd.Series,
    source: SourceSpec,
) -> xr.Dataset:
    if not source.mapping_path.exists():
        raise FileNotFoundError(f"Missing mapping table: {source.mapping_path}")

    df = pd.read_parquet(source.mapping_path)
    if "grid_id" not in df.columns:
        raise KeyError(f"Mapping missing grid_id: {source.mapping_path}")
    if source.id_col not in df.columns:
        raise KeyError(f"Mapping missing id_col '{source.id_col}': {source.mapping_path}")
    if source.weight_col not in df.columns:
        raise KeyError(f"Mapping missing weight_col '{source.weight_col}': {source.mapping_path}")

    out = xr.Dataset(coords={"lat": grid_ds["lat"], "lon": grid_ds["lon"]})

    # Default stable layers
    area_sum = _group_sum(df, "overlap_area_km2")
    area_name = source.rename.get("overlap_area_km2", "lake_area_km2_in_cell")
    out[f"{source.name}_{area_name}"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=area_sum,
            dtype=np.float32,
            fill=np.nan,
        ),
        {"long_name": f"{source.name} lake area within grid cell", "units": "km2"},
    )

    lake_count = df.groupby("grid_id")[source.id_col].nunique(dropna=True).astype(np.int32)
    out[f"{source.name}_lake_count"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=lake_count,
            dtype=np.int32,
            fill=0,
        ),
        {"long_name": f"{source.name} unique lakes per grid cell"},
    )

    # lake area fraction of cell
    # compute per-gid fraction then scatter
    common = area_sum.index.intersection(cell_area_km2_by_gid.index)
    frac = pd.Series(dtype=float)
    if len(common) > 0:
        denom = cell_area_km2_by_gid.loc[common].replace(0, np.nan)
        frac = (area_sum.loc[common] / denom).clip(lower=0.0)

    out[f"{source.name}_lake_area_frac_of_cell"] = (
        ("lat", "lon"),
        _scatter_to_grid(
            grid_shape=grid_shape,
            gid_to_flat=gid_to_flat,
            values_by_gid=frac,
            dtype=np.float32,
            fill=np.nan,
        ),
        {"long_name": f"{source.name} lake area fraction of grid cell", "units": "1"},
    )

    # Extra variables from spec
    for var in source.sum_vars:
        if var == "overlap_area_km2":
            continue
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
            {"aggregation": f"area_weighted_mean(weight={source.weight_col})"},
        )

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

    # Apply mask outside China
    in_china = grid_ds["in_china"].to_numpy().astype(bool)
    for name, da in list(out.data_vars.items()):
        if np.issubdtype(da.dtype, np.integer):
            out[name] = da.where(in_china, other=0)
        else:
            out[name] = da.where(in_china)

    return out


def export_lakes_to_netcdf(
    *,
    grid_nc: Path,
    grid_parquet: Path,
    sources: list[str],
    spec_path: Path | None,
    hydrolakes_map: Path,
    lakeatlas_map: Path,
    out_attrs_path: Path,
) -> None:
    if not grid_nc.exists():
        raise FileNotFoundError(f"Grid base NetCDF not found: {grid_nc}")

    grid_ds = xr.open_dataset(grid_nc)
    _validate_grid_base(grid_ds)

    gid_to_flat = _build_gid_to_flat_index(grid_ds["grid_id"].to_numpy())
    grid_shape = grid_ds["grid_id"].shape

    cell_area_km2_by_gid = _compute_cell_area_km2(grid_parquet)

    specs = _load_spec_or_default(
        sources=sources,
        spec_path=spec_path,
        hydrolakes_map=hydrolakes_map,
        lakeatlas_map=lakeatlas_map,
    )
    if len(specs) == 0:
        raise ValueError("No sources selected. Use --sources hydrolakes,lakeatlas")

    out = xr.Dataset(
        coords={"lat": grid_ds["lat"], "lon": grid_ds["lon"]},
        attrs={
            "title": "China 0.1° lakes grid attributes",
            "grid_base": str(grid_nc),
            "notes": "Derived from grid-to-polygon mapping tables using per-cell overlap_area_km2 weighting.",
        },
    )
    out["grid_id"] = grid_ds["grid_id"].astype(np.int32)
    out["in_china"] = grid_ds["in_china"].astype(bool)

    for spec in specs:
        part = aggregate_lake_source_to_grid(
            grid_ds=grid_ds,
            gid_to_flat=gid_to_flat,
            grid_shape=grid_shape,
            cell_area_km2_by_gid=cell_area_km2_by_gid,
            source=spec,
        )
        out = xr.merge([out, part], compat="override")

    out_attrs_path.parent.mkdir(parents=True, exist_ok=True)

    encoding: dict[str, dict[str, Any]] = {}
    for name, da in out.data_vars.items():
        if name in {"grid_id", "in_china"}:
            continue
        if np.issubdtype(da.dtype, np.floating):
            encoding[name] = {"zlib": True, "complevel": 4, "dtype": "float32"}
        elif np.issubdtype(da.dtype, np.integer):
            encoding[name] = {"zlib": True, "complevel": 4}

    out.to_netcdf(out_attrs_path, encoding=encoding)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate lakes mapping tables to 0.1° grid NetCDF")
    parser.add_argument("--grid-nc", type=str, default=str(DEFAULT_GRID_NC))
    parser.add_argument("--grid-parquet", type=str, default=str(DEFAULT_GRID_PARQUET))
    parser.add_argument(
        "--sources",
        type=str,
        default="hydrolakes,lakeatlas",
        help="Comma-separated: hydrolakes,lakeatlas",
    )
    parser.add_argument(
        "--spec",
        type=str,
        default=None,
        help="Optional JSON spec defining aggregation variables and rules.",
    )
    parser.add_argument("--hydrolakes-map", type=str, default=str(DEFAULT_HYDROLAKES_MAP))
    parser.add_argument("--lakeatlas-map", type=str, default=str(DEFAULT_LAKEATLAS_MAP))
    parser.add_argument("--out-attrs", type=str, default=str(DEFAULT_OUT_ATTRS))
    args = parser.parse_args()

    export_lakes_to_netcdf(
        grid_nc=Path(args.grid_nc),
        grid_parquet=Path(args.grid_parquet),
        sources=[s.strip() for s in args.sources.split(",") if s.strip()],
        spec_path=Path(args.spec) if args.spec else None,
        hydrolakes_map=Path(args.hydrolakes_map),
        lakeatlas_map=Path(args.lakeatlas_map),
        out_attrs_path=Path(args.out_attrs),
    )
    print(f"Wrote: {args.out_attrs}")


if __name__ == "__main__":
    main()
