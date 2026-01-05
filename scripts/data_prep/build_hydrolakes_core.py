import pathlib

import geopandas as gpd


DATA_ROOT = pathlib.Path("data")
RAW_HYDROLAKES_POLY = (
    DATA_ROOT
    / "HydroSHEDS data"
    / "HydroLAKES_polys_v10_shp"
    / "HydroLAKES_polys_v10_shp"
    / "HydroLAKES_polys_v10.shp"
)
OUTPUT_DIR = DATA_ROOT / "processed" / "hydrology"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_GLOBAL = OUTPUT_DIR / "hydrolakes_global_core.parquet"


CORE_COLUMNS = [
    # identifiers / basic metadata
    "Hylak_id",
    "Lake_name",
    "Country",
    "Continent",
    "Poly_src",
    "Lake_type",
    "Grand_id",
    # geometry / volume / depth
    "Lake_area",  # km2
    "Shore_len",
    "Shore_dev",
    "Vol_total",  # km3
    "Vol_res",    # km3
    "Vol_src",
    "Depth_avg",  # m
    # hydrology-like attributes
    "Dis_avg",    # m3/s
    "Res_time",   # years
    # context
    "Elevation",
    "Wshd_area",  # km2
]


def build_hydrolakes_core() -> None:
    """Build a lightweight HydroLAKES core table (global polygons).

    Notes
    -----
    - Preserves geometry (lake polygons) in WGS84.
    - Keeps identifiers, volume/area/depth, discharge and residence time.
    - This table can later be spatially clipped to China + buffer using
      the same pattern as other *_china_core products.
    """

    if not RAW_HYDROLAKES_POLY.exists():
        raise FileNotFoundError(f"HydroLAKES polygons not found: {RAW_HYDROLAKES_POLY}")

    print(f"Reading HydroLAKES polygons from: {RAW_HYDROLAKES_POLY}")
    gdf = gpd.read_file(RAW_HYDROLAKES_POLY)

    missing = [c for c in CORE_COLUMNS if c not in gdf.columns]
    if missing:
        raise KeyError(f"Missing expected columns in HydroLAKES: {missing}")

    gdf_core = gdf[CORE_COLUMNS + ["geometry"]].copy()

    print("HydroLAKES core schema:")
    print(gdf_core.dtypes)
    print(f"Number of lake polygons: {len(gdf_core):,}")

    print(f"Writing global HydroLAKES core to: {OUTPUT_GLOBAL}")
    gdf_core.to_parquet(OUTPUT_GLOBAL, index=False)
    print("Done.")


if __name__ == "__main__":
    build_hydrolakes_core()
