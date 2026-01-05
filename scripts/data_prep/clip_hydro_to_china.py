"""Clip HydroRIVERS / RiverATLAS / BasinATLAS core tables to China + buffer.

This script uses the GADM level-0 China boundary and an optional buffer
(in degrees) to select features from the global/Asia-wide core tables
that intersect the buffered China extent.

Outputs live under data/processed/hydrology/ with a *_china_core suffix.
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
  
HYDRORIVERS_CORE = DATA_ROOT / "processed" / "hydrology" / "hydrorivers_asia_core.parquet"
RIVERATLAS_CORE = DATA_ROOT / "processed" / "hydrology" / "riveratlas_v10_core.parquet"
BASINATLAS_CORE = DATA_ROOT / "processed" / "hydrology" / "basinatlas_lev10_core.parquet"

OUTPUT_DIR = DATA_ROOT / "processed" / "hydrology"
OUTPUT_HR = OUTPUT_DIR / "hydrorivers_china_core.parquet"
OUTPUT_RA = OUTPUT_DIR / "riveratlas_china_core.parquet"
OUTPUT_BA = OUTPUT_DIR / "basinatlas_lev10_china_core.parquet"


ClipTarget = Literal["hydrorivers", "riveratlas", "basinatlas", "all"]


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
    """Clip a core GeoDataFrame to features intersecting buffered China.

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

    # Spatial join-style intersection filter; use sindex for speed if available.
    print(f"Clipping {label} to China + buffer ...")
    gdf_clipped = gdf[gdf.geometry.intersects(china_geom.unary_union)].copy()

    print(f"{label}: {len(gdf):,} features total, {len(gdf_clipped):,} after clip")

    print(f"Writing clipped core to: {output_path}")
    gdf_clipped.to_parquet(output_path, index=False)
    print("Done.")


def clip_hydro_to_china(buffer_deg: float = 1.0, target: ClipTarget = "all") -> None:
    """Clip HydroSHEDS/HydroATLAS core tables to China + buffer.

    Parameters
    ----------
    buffer_deg : float, default 1.0
        Buffer radius in degrees applied to the China boundary in EPSG:4326.
        A value around 1° (~100 km) generally keeps upstream/neighboring
        basins that slightly cross the Chinese border.
    target : {"hydrorivers", "riveratlas", "basinatlas", "all"}
        Which dataset(s) to process.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    china = _load_china_boundary(buffer_deg=buffer_deg)

    if target in ("hydrorivers", "all"):
        _clip_to_china(HYDRORIVERS_CORE, china, OUTPUT_HR, label="HydroRIVERS")

    if target in ("riveratlas", "all"):
        _clip_to_china(RIVERATLAS_CORE, china, OUTPUT_RA, label="RiverATLAS")

    if target in ("basinatlas", "all"):
        _clip_to_china(BASINATLAS_CORE, china, OUTPUT_BA, label="BasinATLAS lev10")


if __name__ == "__main__":
    # Default: clip all three datasets with a 1-degree buffer.
    clip_hydro_to_china(buffer_deg=1.0, target="all")
