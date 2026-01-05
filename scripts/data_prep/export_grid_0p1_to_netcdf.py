"""Export 0.1° China grid to NetCDF.

Why
---
GeoParquet is great for vector-style operations, but NetCDF is convenient for
gridded workflows (xarray, raster-like operations, model IO).

This exporter converts the clipped China 0.1° grid (GeoParquet) into a regular
lat/lon 2D grid with a mask.

Output
------
data/processed/grid_0p1/grid_cells_china_0p1.nc
    Variables:
    - grid_id(lat, lon): int32, -1 for outside-China
    - in_china(lat, lon): bool
    Coordinates:
    - lat: cell centers
    - lon: cell centers

Notes
-----
The grid is clipped to China, so the NetCDF domain is the bounding rectangle
covering China at 0.1° resolution with a mask.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import numpy as np
import xarray as xr


DEFAULT_GRID = Path("data/processed/grid_0p1/grid_cells_china_0p1.parquet")
DEFAULT_OUT = Path("data/processed/grid_0p1/grid_cells_china_0p1.nc")


def export_grid_to_netcdf(grid_path: Path, out_path: Path) -> None:
    if not grid_path.exists():
        raise FileNotFoundError(f"Grid parquet not found: {grid_path}")

    grid = gpd.read_parquet(grid_path)
    if "grid_id" not in grid.columns or "lon_c" not in grid.columns or "lat_c" not in grid.columns:
        raise KeyError("Expected columns not found in grid parquet: grid_id, lon_c, lat_c")

    # Avoid float-key issues by using integer indices at 0.1° precision.
    lat10 = np.rint(grid["lat_c"].to_numpy(dtype=float) * 10).astype(np.int32)
    lon10 = np.rint(grid["lon_c"].to_numpy(dtype=float) * 10).astype(np.int32)

    lat10_vals = np.array(sorted(np.unique(lat10)), dtype=np.int32)
    lon10_vals = np.array(sorted(np.unique(lon10)), dtype=np.int32)

    lat_index = {int(v): i for i, v in enumerate(lat10_vals)}
    lon_index = {int(v): j for j, v in enumerate(lon10_vals)}

    grid_id = np.full((len(lat10_vals), len(lon10_vals)), -1, dtype=np.int32)

    gids = grid["grid_id"].to_numpy(dtype=np.int32)
    for gid, la10, lo10 in zip(gids, lat10, lon10):
        grid_id[lat_index[int(la10)], lon_index[int(lo10)]] = int(gid)

    in_china = grid_id != -1

    ds = xr.Dataset(
        data_vars={
            "grid_id": (("lat", "lon"), grid_id),
            "in_china": (("lat", "lon"), in_china),
        },
        coords={
            "lat": ("lat", (lat10_vals / 10.0).astype(np.float32), {"long_name": "grid cell center latitude", "units": "degrees_north"}),
            "lon": ("lon", (lon10_vals / 10.0).astype(np.float32), {"long_name": "grid cell center longitude", "units": "degrees_east"}),
        },
        attrs={
            "title": "China 0.1 degree grid (masked)",
            "source": str(grid_path),
            "notes": "grid_id is -1 outside China mask",
        },
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    ds.to_netcdf(out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export China 0.1° grid parquet to NetCDF")
    parser.add_argument("--grid", type=str, default=str(DEFAULT_GRID))
    parser.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    args = parser.parse_args()

    export_grid_to_netcdf(Path(args.grid), Path(args.out))
    print(f"Wrote: {args.out}")


if __name__ == "__main__":
    main()
