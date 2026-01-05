"""Visualize HydroRIVERS and HydroLAKES over China+buffer.

This script reads the original HydroRIVERS (line) and HydroLAKES
(polygon) shapefiles, clips them to the same China boundary used
elsewhere, and produces simple maps where all rivers / lakes are
shown in blue.

Output PNGs are written to `results/figures/hydrology/`.
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "HydroSHEDS data"
BOUNDARY_DIR = ROOT / "data" / "boundary data"
RESULTS_DIR = ROOT / "results" / "figures" / "hydrology"

# Input datasets
HYDRORIVERS_SHP = (
    DATA_DIR
    / "HydroRIVERS_v10_as_shp"
    / "HydroRIVERS_v10_as_shp"
    / "HydroRIVERS_v10_as.shp"
)
HYDROLAKES_POLY_SHP = (
    DATA_DIR
    / "HydroLAKES_polys_v10_shp"
    / "HydroLAKES_polys_v10_shp"
    / "HydroLAKES_polys_v10.shp"
)

CHINA_MASK_SHP = (
    BOUNDARY_DIR
    / "gadm41_CHN_shp"
    / "gadm41_CHN_0.shp"
)


def load_china_mask() -> gpd.GeoDataFrame:
    mask = gpd.read_file(CHINA_MASK_SHP)
    if mask.crs is None:
        mask = mask.set_crs(4326)
    else:
        mask = mask.to_crs(4326)
    return mask


def clip_to_china(gdf: gpd.GeoDataFrame, mask: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Clip a GeoDataFrame to the China mask using an intersects spatial join."""
    if gdf.crs is None:
        gdf = gdf.set_crs(4326)
    else:
        gdf = gdf.to_crs(4326)

    gdf_clipped = gpd.sjoin(
        gdf,
        mask.to_crs(gdf.crs),
        how="inner",
        predicate="intersects",
    )
    gdf_clipped = gdf_clipped[gdf_clipped.geometry.notna()].copy()
    # Drop join helper columns like index_right if present
    for col in ["index_right"]:
        if col in gdf_clipped.columns:
            gdf_clipped = gdf_clipped.drop(columns=[col])
    return gdf_clipped


def plot_hydrorivers_china() -> None:
    mask = load_china_mask()
    print(f"Loading HydroRIVERS from {HYDRORIVERS_SHP} ...")
    rivers = gpd.read_file(HYDRORIVERS_SHP)
    rivers_china = clip_to_china(rivers, mask)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    mask.boundary.plot(ax=ax, color="black", linewidth=0.5)
    rivers_china.plot(ax=ax, color="blue", linewidth=0.4)

    ax.set_title("HydroRIVERS v1.0 over China")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal", adjustable="datalim")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out_path = RESULTS_DIR / "hydrorivers_china_blue.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_hydrolakes_china() -> None:
    mask = load_china_mask()
    print(f"Loading HydroLAKES polygons from {HYDROLAKES_POLY_SHP} ...")
    lakes = gpd.read_file(HYDROLAKES_POLY_SHP)
    lakes_china = clip_to_china(lakes, mask)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    mask.boundary.plot(ax=ax, color="black", linewidth=0.5)
    lakes_china.plot(ax=ax, facecolor="blue", edgecolor="blue", linewidth=0.1)

    ax.set_title("HydroLAKES v1.0 polygons over China")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal", adjustable="datalim")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out_path = RESULTS_DIR / "hydrolakes_china_blue.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    plot_hydrorivers_china()
    plot_hydrolakes_china()


if __name__ == "__main__":
    main()
