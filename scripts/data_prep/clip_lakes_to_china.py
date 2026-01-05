"""Clip lake datasets (HydroLAKES / LakeATLAS core tables) to China + buffer.

This script mirrors the behaviour of `clip_hydro_to_china.py`, but
operates on the lake core products:

- hydrolakes_global_core.parquet -> hydrolakes_china_core.parquet
- lakeatlas_global_core.parquet  -> lakeatlas_china_core.parquet

It uses the GADM level-0 China boundary and an optional buffer (in
degrees) to select features that intersect the buffered China extent.
"""

from __future__ import annotations

import pathlib
from typing import Literal

import geopandas as gpd


DATA_ROOT = pathlib.Path("data")
BOUNDARY_CHN = (
    DATA_ROOT
    / "boundary data"
    / "gadm41_CHN_shp"
    / "gadm41_CHN_0.shp"
)

HYDROLAKES_CORE = DATA_ROOT / "processed" / "hydrology" / "hydrolakes_global_core.parquet"
LAKEATLAS_CORE = DATA_ROOT / "processed" / "hydrology" / "lakeatlas_global_core.parquet"

OUTPUT_DIR = DATA_ROOT / "processed" / "hydrology"
OUTPUT_HL = OUTPUT_DIR / "hydrolakes_china_core.parquet"
OUTPUT_LA = OUTPUT_DIR / "lakeatlas_china_core.parquet"


LakeClipTarget = Literal["hydrolakes", "lakeatlas", "all"]


def _load_china_boundary(buffer_deg: float) -> gpd.GeoDataFrame:
    """Load China GADM level-0 boundary and apply an optional buffer (in degrees).

    Parameters
    ----------
    buffer_deg : float
        Buffer radius in degrees applied in the data CRS (WGS84 lon/lat).
        For example, 1.0 ~ roughly 100 km. Use 0 for no buffer.
    """

    if not BOUNDARY_CHN.exists():
        raise FileNotFoundError(f"China boundary shapefile not found: {BOUNDARY_CHN}")

    gdf = gpd.read_file(BOUNDARY_CHN)

    # Ensure we are in geographic coordinates; original is EPSG:4326 per inventory.
    if gdf.crs is None:
        gdf = gdf.set_crs(4326)
    else:
        gdf = gdf.to_crs(4326)

    if buffer_deg != 0.0:
        gdf["geometry"] = gdf.geometry.buffer(buffer_deg)

    return gdf[["geometry"]]


def _clip_to_china(
    core_path: pathlib.Path,
    china_geom: gpd.GeoDataFrame,
    output_path: pathlib.Path,
    label: str,
) -> None:
    """Clip a lake core GeoDataFrame to features intersecting buffered China.

    Selection is based on spatial intersection (not containment): any
    feature whose geometry intersects the buffered China polygon is kept.
    """

    if not core_path.exists():
        raise FileNotFoundError(f"Core file not found for {label}: {core_path}")

    print(f"Reading {label} core from: {core_path}")
    gdf = gpd.read_parquet(core_path)

    if gdf.crs is None:
        # All hydro products are expected to be in EPSG:4326.
        gdf = gdf.set_crs(4326)
    else:
        gdf = gdf.to_crs(4326)

    print(f"Clipping {label} to China + buffer ...")
    gdf_clipped = gdf[gdf.geometry.intersects(china_geom.unary_union)].copy()

    print(f"{label}: {len(gdf):,} features total, {len(gdf_clipped):,} after clip")

    print(f"Writing clipped core to: {output_path}")
    gdf_clipped.to_parquet(output_path, index=False)
    print("Done.")


def clip_lakes_to_china(buffer_deg: float = 1.0, target: LakeClipTarget = "all") -> None:
    """Clip HydroLAKES / LakeATLAS core tables to China + buffer.

    Parameters
    ----------
    buffer_deg : float, default 1.0
        Buffer radius in degrees applied to the China boundary in EPSG:4326.
        A value around 1° (~100 km) generally keeps upstream/neighboring
        basins that slightly cross the Chinese border.
    target : {"hydrolakes", "lakeatlas", "all"}
        Which dataset(s) to process.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    china = _load_china_boundary(buffer_deg=buffer_deg)

    if target in ("hydrolakes", "all"):
        _clip_to_china(HYDROLAKES_CORE, china, OUTPUT_HL, label="HydroLAKES")

    if target in ("lakeatlas", "all"):
        _clip_to_china(LAKEATLAS_CORE, china, OUTPUT_LA, label="LakeATLAS")


if __name__ == "__main__":
    # Default: clip both lake datasets with a 1-degree buffer.
    clip_lakes_to_china(buffer_deg=1.0, target="all")
