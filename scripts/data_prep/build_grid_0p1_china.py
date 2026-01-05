"""Build a 0.1° grid clipped to China (GADM level-0).

Outputs
-------
data/processed/grid_0p1/grid_cells_china_0p1.parquet
    GeoParquet with columns:
    - grid_id: unique integer id (lat10*10000 + lon10)
    - lon_min, lat_min, lon_max, lat_max
    - lon_c, lat_c
    - geometry: grid cell polygon in EPSG:4326
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import geopandas as gpd
import numpy as np
from shapely.geometry import box


DATA_ROOT = Path("data")
BOUNDARY_CHN = DATA_ROOT / "boundary data" / "gadm41_CHN_shp" / "gadm41_CHN_0.shp"
OUTPUT_DIR = DATA_ROOT / "processed" / "grid_0p1"
OUTPUT_GRID = OUTPUT_DIR / "grid_cells_china_0p1.parquet"


def _snap_floor(x: float, step: float) -> float:
    return math.floor(x / step) * step


def _snap_ceil(x: float, step: float) -> float:
    return math.ceil(x / step) * step


def build_grid_0p1_china(buffer_deg: float = 0.0, cell_deg: float = 0.1) -> gpd.GeoDataFrame:
    if not BOUNDARY_CHN.exists():
        raise FileNotFoundError(f"China boundary not found: {BOUNDARY_CHN}")

    china = gpd.read_file(BOUNDARY_CHN)
    if china.crs is None:
        china = china.set_crs(4326)
    else:
        china = china.to_crs(4326)

    if buffer_deg != 0.0:
        china["geometry"] = china.geometry.buffer(buffer_deg)

    minx, miny, maxx, maxy = china.total_bounds
    minx = _snap_floor(minx, cell_deg)
    miny = _snap_floor(miny, cell_deg)
    maxx = _snap_ceil(maxx, cell_deg)
    maxy = _snap_ceil(maxy, cell_deg)

    # Use integer arithmetic to avoid floating drift: 0.1° -> multiply by 10.
    step10 = int(round(cell_deg * 10))
    if step10 <= 0:
        raise ValueError("cell_deg must be > 0")

    lon10_min = int(round(minx * 10))
    lon10_max = int(round(maxx * 10))
    lat10_min = int(round(miny * 10))
    lat10_max = int(round(maxy * 10))

    lon10_vals = np.arange(lon10_min, lon10_max, step10, dtype=np.int32)
    lat10_vals = np.arange(lat10_min, lat10_max, step10, dtype=np.int32)

    geoms = []
    lon_min_list = []
    lat_min_list = []
    lon_max_list = []
    lat_max_list = []
    lon_c_list = []
    lat_c_list = []
    grid_id_list = []

    for lat10 in lat10_vals:
        for lon10 in lon10_vals:
            lon_min = lon10 / 10.0
            lat_min = lat10 / 10.0
            lon_max = (lon10 + step10) / 10.0
            lat_max = (lat10 + step10) / 10.0
            geoms.append(box(lon_min, lat_min, lon_max, lat_max))
            lon_min_list.append(lon_min)
            lat_min_list.append(lat_min)
            lon_max_list.append(lon_max)
            lat_max_list.append(lat_max)
            lon_c_list.append((lon_min + lon_max) / 2.0)
            lat_c_list.append((lat_min + lat_max) / 2.0)
            grid_id_list.append(int(lat10) * 10000 + int(lon10))

    grid = gpd.GeoDataFrame(
        {
            "grid_id": grid_id_list,
            "lon_min": lon_min_list,
            "lat_min": lat_min_list,
            "lon_max": lon_max_list,
            "lat_max": lat_max_list,
            "lon_c": lon_c_list,
            "lat_c": lat_c_list,
        },
        geometry=geoms,
        crs=4326,
    )

    # Clip to China by intersection test (fast). Geometry stays as full cell polygons.
    china_union = china.geometry.unary_union
    grid = grid[grid.geometry.intersects(china_union)].copy()
    grid = grid.reset_index(drop=True)
    return grid


def main() -> None:
    parser = argparse.ArgumentParser(description="Build 0.1° grid clipped to China.")
    parser.add_argument("--buffer-deg", type=float, default=0.0, help="Buffer China boundary in degrees (EPSG:4326).")
    parser.add_argument("--cell-deg", type=float, default=0.1, help="Grid cell size in degrees. Default 0.1")
    parser.add_argument("--output", type=str, default=str(OUTPUT_GRID), help="Output GeoParquet path")
    args = parser.parse_args()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    grid = build_grid_0p1_china(buffer_deg=args.buffer_deg, cell_deg=args.cell_deg)
    print(f"Grid cells (China): {len(grid):,}")
    print(f"Writing: {out_path}")
    grid.to_parquet(out_path, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
