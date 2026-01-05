import pathlib

import geopandas as gpd


DATA_ROOT = pathlib.Path("data")
RAW_HYDRO_RIVERS = DATA_ROOT / "HydroSHEDS data" / "HydroRIVERS_v10_as_shp" / "HydroRIVERS_v10_as_shp" / "HydroRIVERS_v10_as.shp"
OUTPUT_DIR = DATA_ROOT / "processed" / "hydrology"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "hydrorivers_asia_core.parquet"


CORE_COLUMNS = [
    # identifiers / topology
    "HYRIV_ID",
    "NEXT_DOWN",
    "MAIN_RIV",
    "ENDORHEIC",
    "HYBAS_L12",
    # geometry-related and sizes
    "LENGTH_KM",
    "DIST_DN_KM",
    "DIST_UP_KM",
    "CATCH_SKM",
    "UPLAND_SKM",
    # discharge and stream order
    "DIS_AV_CMS",
    "ORD_STRA",
    "ORD_CLAS",
    "ORD_FLOW",
]


def build_hydrorivers_asia_core() -> None:
    """Build a lightweight HydroRIVERS core table for the Asia subset.

    Notes
    -----
    - Geometry and CRS are preserved as in the original shapefile (WGS84 lat/lon).
    - We keep only the fields required for topology (HYRIV_ID, NEXT_DOWN, MAIN_RIV,
      ENDORHEIC, HYBAS_L12), basic size metrics (LENGTH_KM, CATCH_SKM, UPLAND_SKM),
      and a first-order discharge/stream-order description (DIS_AV_CMS, ORD_*).
    - No spatial clipping is applied here yet; this is the full Asia subset.
    """

    print(f"Reading HydroRIVERS from: {RAW_HYDRO_RIVERS}")
    gdf = gpd.read_file(RAW_HYDRO_RIVERS)

    missing = [c for c in CORE_COLUMNS if c not in gdf.columns]
    if missing:
        raise KeyError(f"Missing expected columns in HydroRIVERS: {missing}")

    gdf_core = gdf[CORE_COLUMNS + ["geometry"]].copy()

    print("HydroRIVERS core schema:")
    print(gdf_core.dtypes)
    print(f"Number of features: {len(gdf_core):,}")

    print(f"Writing core parquet to: {OUTPUT_PATH}")
    gdf_core.to_parquet(OUTPUT_PATH, index=False)
    print("Done.")


if __name__ == "__main__":
    build_hydrorivers_asia_core()
