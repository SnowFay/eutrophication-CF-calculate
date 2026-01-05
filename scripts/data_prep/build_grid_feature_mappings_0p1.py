"""Build grid-to-feature mapping tables for 0.1° grid.

Design
------
The user requirement is to "store all fields currently present in core tables in grid data".
To avoid lossy aggregation (a grid cell can intersect multiple features), we output a
*mapping table* per dataset:

    grid_id + overlap metrics + ALL non-geometry fields from the core table

This keeps every core field, while still linking it to the grid.

Outputs (default)
-----------------
data/processed/grid_0p1/
    grid_hydrolakes_china_0p1_mapping.parquet
    grid_lakeatlas_china_0p1_mapping.parquet

Notes
-----
 - This script currently focuses on lake polygons (HydroLAKES/LakeATLAS) since they are
   comparatively small and are the user's immediate priority.
 - River/flowline mapping can be added with the same pattern but may require chunking
   due to data volume.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import box

try:
    import pyarrow as pa
    import pyarrow.parquet as pq

    _HAVE_PYARROW = True
except Exception:
    _HAVE_PYARROW = False


DATA_ROOT = Path("data")
HYDRO_DIR = DATA_ROOT / "processed" / "hydrology"
GRID_DIR = DATA_ROOT / "processed" / "grid_0p1"

DEFAULT_GRID = GRID_DIR / "grid_cells_china_0p1.parquet"

HYDROLAKES_CHINA = HYDRO_DIR / "hydrolakes_china_core.parquet"
LAKEATLAS_CHINA = HYDRO_DIR / "lakeatlas_china_core.parquet"

HYDRORIVERS_CHINA = HYDRO_DIR / "hydrorivers_china_core.parquet"
RIVERATLAS_CHINA = HYDRO_DIR / "riveratlas_china_core.parquet"
BASINATLAS_LEV10_CHINA = HYDRO_DIR / "basinatlas_lev10_china_core.parquet"

OUT_HYDROLAKES = GRID_DIR / "grid_hydrolakes_china_0p1_mapping.parquet"
OUT_LAKEATLAS = GRID_DIR / "grid_lakeatlas_china_0p1_mapping.parquet"

OUT_HYDRORIVERS = GRID_DIR / "grid_hydrorivers_china_0p1_mapping.parquet"
OUT_RIVERATLAS = GRID_DIR / "grid_riveratlas_china_0p1_mapping.parquet"
OUT_BASINATLAS_LEV10 = GRID_DIR / "grid_basinatlas_lev10_china_0p1_mapping.parquet"


def _ensure_crs4326(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.crs is None:
        return gdf.set_crs(4326)
    return gdf.to_crs(4326)


def _compute_polygon_area_km2(gdf: gpd.GeoDataFrame) -> pd.Series:
    return gdf.to_crs(6933).geometry.area / 1e6


def _compute_line_length_km(gdf: gpd.GeoDataFrame) -> pd.Series:
    return gdf.to_crs(6933).geometry.length / 1000.0


class _ParquetAppender:
    def __init__(self, out_path: Path):
        self.out_path = out_path
        self._writer = None

        # Avoid accidental appends to old outputs (e.g., bbox test runs).
        if self.out_path.exists():
            self.out_path.unlink()

        # If we fall back to chunked directory output, clear any prior chunks.
        chunk_dir = self.out_path.parent / (self.out_path.stem + "_chunks")
        if chunk_dir.exists():
            for part in chunk_dir.glob("part_*.parquet"):
                part.unlink()

    def append(self, df: pd.DataFrame) -> None:
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        if len(df) == 0:
            return

        if _HAVE_PYARROW:
            table = pa.Table.from_pandas(df, preserve_index=False)
            if self._writer is None:
                self._writer = pq.ParquetWriter(self.out_path, table.schema)
            self._writer.write_table(table)
            return

        # Fallback: write one file per chunk.
        chunk_dir = self.out_path.parent / (self.out_path.stem + "_chunks")
        chunk_dir.mkdir(parents=True, exist_ok=True)
        part_path = chunk_dir / f"part_{len(list(chunk_dir.glob('part_*.parquet'))):06d}.parquet"
        df.to_parquet(part_path, index=False)

    def close(self) -> None:
        if self._writer is not None:
            self._writer.close()
            self._writer = None


def build_polygon_mapping(
    *,
    grid: gpd.GeoDataFrame,
    features: gpd.GeoDataFrame,
    feature_id_col: str,
    out_path: Path,
) -> None:
    """Create mapping table: each (grid cell, feature) intersection row keeps all feature fields."""

    if feature_id_col not in features.columns:
        raise KeyError(f"feature_id_col '{feature_id_col}' not found in features")

    grid = _ensure_crs4326(grid)
    features = _ensure_crs4326(features)

    # Precompute feature areas in km2 for overlap fraction.
    feature_area_km2 = _compute_polygon_area_km2(features)
    features = features.copy()
    features["_feature_area_km2"] = feature_area_km2

    grid_geom_by_id = dict(zip(grid["grid_id"].tolist(), grid.geometry.tolist()))

    # Spatial join (features -> grid) to get candidate pairs.
    pairs = gpd.sjoin(
        features,
        grid[["grid_id", "geometry"]],
        how="inner",
        predicate="intersects",
    )
    if len(pairs) == 0:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(columns=["grid_id", feature_id_col, "overlap_area_km2", "overlap_frac"]).to_parquet(
            out_path, index=False
        )
        return

    # Compute intersection areas.
    # pairs.geometry is feature geometry; intersect with the matching grid cell geometry.
    inter_geoms = []
    grid_ids = pairs["grid_id"].tolist()
    for geom, gid in zip(pairs.geometry.tolist(), grid_ids):
        inter_geoms.append(geom.intersection(grid_geom_by_id[gid]))

    inter_area_km2 = gpd.GeoSeries(inter_geoms, crs=4326).to_crs(6933).area / 1e6
    pairs = pairs.copy()
    # Ensure index alignment (sjoin preserves original feature index).
    pairs["overlap_area_km2"] = pd.Series(inter_area_km2.to_numpy(), index=pairs.index)
    pairs["overlap_frac"] = pairs["overlap_area_km2"] / pairs["_feature_area_km2"].replace(0, pd.NA)

    # Keep: grid_id + overlap metrics + ALL feature fields (except geometry).
    drop_cols = {"geometry", "index_right"}
    keep_cols = [c for c in pairs.columns if c not in drop_cols]
    out_df = pairs[keep_cols].copy()

    # Remove the helper column unless user wants it (keep derived metrics only).
    if "_feature_area_km2" in out_df.columns:
        out_df = out_df.drop(columns=["_feature_area_km2"])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_parquet(out_path, index=False)


def build_line_mapping_chunked(
    *,
    grid: gpd.GeoDataFrame,
    features: gpd.GeoDataFrame,
    feature_id_col: str,
    out_path: Path,
    chunk_size: int = 50000,
) -> None:
    """Create mapping table for line features with chunking.

    Output columns:
    - grid_id
    - overlap_length_km
    - overlap_frac (relative to total feature length)
    - ALL non-geometry fields from features
    """

    if feature_id_col not in features.columns:
        raise KeyError(f"feature_id_col '{feature_id_col}' not found in features")

    grid = _ensure_crs4326(grid)
    features = _ensure_crs4326(features)

    # Precompute feature total length in km.
    feat_len_km = _compute_line_length_km(features)
    features = features.copy()
    features["_feature_len_km"] = feat_len_km

    # Grid geometry lookup for fast intersections.
    grid_geom_by_id = dict(zip(grid["grid_id"].tolist(), grid.geometry.tolist()))

    appender = _ParquetAppender(out_path)
    try:
        n = len(features)
        for start in range(0, n, chunk_size):
            end = min(start + chunk_size, n)
            chunk = features.iloc[start:end]
            pairs = gpd.sjoin(
                chunk,
                grid[["grid_id", "geometry"]],
                how="inner",
                predicate="intersects",
            )

            if len(pairs) == 0:
                continue

            # Prevent pandas index alignment issues when assigning computed arrays.
            pairs = pairs.copy()
            pairs = pairs.reset_index(drop=True)

            grid_ids = pairs["grid_id"].tolist()
            inter_geoms = []
            for geom, gid in zip(pairs.geometry.tolist(), grid_ids):
                inter_geoms.append(geom.intersection(grid_geom_by_id[gid]))

            inter_len_km = gpd.GeoSeries(inter_geoms, crs=4326).to_crs(6933).length / 1000.0
            pairs["overlap_length_km"] = pd.Series(inter_len_km.to_numpy(), index=pairs.index)
            pairs["overlap_frac"] = pairs["overlap_length_km"] / pairs["_feature_len_km"].replace(0, pd.NA)

            drop_cols = {"geometry", "index_right"}
            keep_cols = [c for c in pairs.columns if c not in drop_cols]
            out_df = pairs[keep_cols].copy()
            if "_feature_len_km" in out_df.columns:
                out_df = out_df.drop(columns=["_feature_len_km"])

            appender.append(out_df)
    finally:
        appender.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build 0.1° grid-to-feature mapping tables.")
    parser.add_argument("--grid", type=str, default=str(DEFAULT_GRID), help="Grid GeoParquet path")
    parser.add_argument(
        "--bbox",
        type=str,
        default=None,
        help="Optional bbox 'minx,miny,maxx,maxy' in EPSG:4326 for quick testing",
    )
    parser.add_argument(
        "--datasets",
        type=str,
        default="hydrolakes,lakeatlas",
        help="Comma-separated: hydrolakes,lakeatlas,hydrorivers,riveratlas,basinatlas10",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=50000,
        help="Chunk size for line mapping (hydrorivers/riveratlas).",
    )
    args = parser.parse_args()

    bbox = None
    if args.bbox:
        parts = [float(x) for x in args.bbox.split(",")]
        if len(parts) != 4:
            raise ValueError("--bbox must be 'minx,miny,maxx,maxy'")
        bbox = (parts[0], parts[1], parts[2], parts[3])

    grid = gpd.read_parquet(Path(args.grid))
    grid = _ensure_crs4326(grid)
    if bbox is not None:
        minx, miny, maxx, maxy = bbox
        bbox_poly = box(minx, miny, maxx, maxy)
        grid = grid[grid.geometry.intersects(bbox_poly)].copy()

    datasets = {d.strip().lower() for d in args.datasets.split(",") if d.strip()}

    if "hydrolakes" in datasets:
        if not HYDROLAKES_CHINA.exists():
            raise FileNotFoundError(f"Missing: {HYDROLAKES_CHINA}")
        lakes = gpd.read_parquet(HYDROLAKES_CHINA)
        lakes = _ensure_crs4326(lakes)
        if bbox is not None:
            minx, miny, maxx, maxy = bbox
            bbox_poly = box(minx, miny, maxx, maxy)
            lakes = lakes[lakes.geometry.intersects(bbox_poly)].copy()
        print(f"HydroLAKES features: {len(lakes):,}; grid cells: {len(grid):,}")
        build_polygon_mapping(grid=grid, features=lakes, feature_id_col="Hylak_id", out_path=OUT_HYDROLAKES)
        print(f"Wrote: {OUT_HYDROLAKES}")

    if "lakeatlas" in datasets:
        if not LAKEATLAS_CHINA.exists():
            raise FileNotFoundError(f"Missing: {LAKEATLAS_CHINA}")
        la = gpd.read_parquet(LAKEATLAS_CHINA)
        la = _ensure_crs4326(la)
        if bbox is not None:
            minx, miny, maxx, maxy = bbox
            bbox_poly = box(minx, miny, maxx, maxy)
            la = la[la.geometry.intersects(bbox_poly)].copy()
        print(f"LakeATLAS features: {len(la):,}; grid cells: {len(grid):,}")
        build_polygon_mapping(grid=grid, features=la, feature_id_col="Hylak_id", out_path=OUT_LAKEATLAS)
        print(f"Wrote: {OUT_LAKEATLAS}")

    if "basinatlas10" in datasets:
        if not BASINATLAS_LEV10_CHINA.exists():
            raise FileNotFoundError(f"Missing: {BASINATLAS_LEV10_CHINA}")
        ba = gpd.read_parquet(BASINATLAS_LEV10_CHINA)
        ba = _ensure_crs4326(ba)
        if bbox is not None:
            minx, miny, maxx, maxy = bbox
            bbox_poly = box(minx, miny, maxx, maxy)
            ba = ba[ba.geometry.intersects(bbox_poly)].copy()
        print(f"BasinATLAS lev10 features: {len(ba):,}; grid cells: {len(grid):,}")
        build_polygon_mapping(grid=grid, features=ba, feature_id_col="HYBAS_ID", out_path=OUT_BASINATLAS_LEV10)
        print(f"Wrote: {OUT_BASINATLAS_LEV10}")

    if "hydrorivers" in datasets:
        if not HYDRORIVERS_CHINA.exists():
            raise FileNotFoundError(f"Missing: {HYDRORIVERS_CHINA}")
        hr = gpd.read_parquet(HYDRORIVERS_CHINA)
        hr = _ensure_crs4326(hr)
        if bbox is not None:
            minx, miny, maxx, maxy = bbox
            bbox_poly = box(minx, miny, maxx, maxy)
            hr = hr[hr.geometry.intersects(bbox_poly)].copy()
        print(f"HydroRIVERS features: {len(hr):,}; grid cells: {len(grid):,}")
        build_line_mapping_chunked(
            grid=grid,
            features=hr,
            feature_id_col="HYRIV_ID",
            out_path=OUT_HYDRORIVERS,
            chunk_size=args.chunk_size,
        )
        print(f"Wrote: {OUT_HYDRORIVERS}")

    if "riveratlas" in datasets:
        if not RIVERATLAS_CHINA.exists():
            raise FileNotFoundError(f"Missing: {RIVERATLAS_CHINA}")
        ra = gpd.read_parquet(RIVERATLAS_CHINA)
        ra = _ensure_crs4326(ra)
        if bbox is not None:
            minx, miny, maxx, maxy = bbox
            bbox_poly = box(minx, miny, maxx, maxy)
            ra = ra[ra.geometry.intersects(bbox_poly)].copy()
        print(f"RiverATLAS features: {len(ra):,}; grid cells: {len(grid):,}")
        build_line_mapping_chunked(
            grid=grid,
            features=ra,
            feature_id_col="HYRIV_ID",
            out_path=OUT_RIVERATLAS,
            chunk_size=args.chunk_size,
        )
        print(f"Wrote: {OUT_RIVERATLAS}")


if __name__ == "__main__":
    main()
