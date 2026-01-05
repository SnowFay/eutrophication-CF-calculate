import pathlib

import geopandas as gpd


DATA_ROOT = pathlib.Path("data")
RAW_RIVER_ATLAS_GDB = DATA_ROOT / "HydroSHEDS data" / "RiverATLAS_Data_v10.gdb" / "RiverATLAS_v10.gdb"
OUTPUT_DIR = DATA_ROOT / "processed" / "hydrology"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "riveratlas_v10_core.parquet"

LAYER_NAME = "RiverATLAS_v10"

CORE_COLUMNS = [
    # identifiers / topology (mirroring HydroRIVERS)
    "HYRIV_ID",
    "NEXT_DOWN",
    "MAIN_RIV",
    "ENDORHEIC",
    "ORD_STRA",
    "ORD_CLAS",
    "ORD_FLOW",
    "HYBAS_L12",
    # hydrology core
    "run_mm_cyr",
    # a few climate/terrain fields that are often useful diagnostics
    "pre_mm_cyr",
    "aet_mm_cyr",
    "ele_mt_cav",
    "sgr_dk_rav",
]


def build_riveratlas_v10_core() -> None:
    """Build a lightweight RiverATLAS core table for the global river network.

    Notes
    -----
    - Reads the main RiverATLAS_v10 layer from the FileGDB.
    - Keeps only IDs/topology plus a small set of hydrology/terrain attributes
      that are likely to be needed for discharge/runoff and k_adv/k_ret prototypes.
    - Geometry is preserved for potential spatial operations or plotting.
    - No spatial clipping is applied here yet; downstream scripts can
      restrict to China or a bounding box if needed.
    """

    print(f"Reading RiverATLAS from: {RAW_RIVER_ATLAS_GDB} (layer={LAYER_NAME})")
    gdf = gpd.read_file(RAW_RIVER_ATLAS_GDB, layer=LAYER_NAME)

    missing = [c for c in CORE_COLUMNS if c not in gdf.columns]
    if missing:
        raise KeyError(f"Missing expected columns in RiverATLAS: {missing}")

    gdf_core = gdf[CORE_COLUMNS + ["geometry"]].copy()

    print("RiverATLAS core schema:")
    print(gdf_core.dtypes)
    print(f"Number of features: {len(gdf_core):,}")

    print(f"Writing core parquet to: {OUTPUT_PATH}")
    gdf_core.to_parquet(OUTPUT_PATH, index=False)
    print("Done.")


if __name__ == "__main__":
    build_riveratlas_v10_core()
