import pathlib

import geopandas as gpd


DATA_ROOT = pathlib.Path("data")
RAW_BASIN_ATLAS_GDB = DATA_ROOT / "HydroSHEDS data" / "BasinATLAS_Data_v10.gdb" / "BasinATLAS_v10.gdb"
OUTPUT_DIR = DATA_ROOT / "processed" / "hydrology"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "basinatlas_lev10_core.parquet"

LAYER_NAME = "BasinATLAS_v10_lev10"

CORE_COLUMNS = [
    # identifiers / topology
    "HYBAS_ID",
    "NEXT_DOWN",
    "NEXT_SINK",
    "MAIN_BAS",
    "PFAF_ID",
    "ENDO",
    "COAST",
    "ORDER_",
    "SORT",
    # area metrics
    "SUB_AREA",
    "UP_AREA",
    # hydrology core
    "run_mm_syr",
]


def build_basinatlas_lev10_core() -> None:
    """Build a lightweight BasinATLAS level-10 core table.

    Notes
    -----
    - Reads the lev10 layer from BasinATLAS_v10.gdb.
    - Keeps IDs/topology (HYBAS_ID, NEXT_DOWN, PFAF_ID, etc.),
      area metrics (SUB_AREA, UP_AREA), and the key runoff depth field run_mm_syr.
    - Geometry is preserved, CRS is WGS84.
    - No spatial clipping is applied yet; downstream scripts may
      restrict to China / neighboring basins as needed.
    """

    print(f"Reading BasinATLAS lev10 from: {RAW_BASIN_ATLAS_GDB} (layer={LAYER_NAME})")
    gdf = gpd.read_file(RAW_BASIN_ATLAS_GDB, layer=LAYER_NAME)

    missing = [c for c in CORE_COLUMNS if c not in gdf.columns]
    if missing:
        raise KeyError(f"Missing expected columns in BasinATLAS lev10: {missing}")

    gdf_core = gdf[CORE_COLUMNS + ["geometry"]].copy()

    print("BasinATLAS lev10 core schema:")
    print(gdf_core.dtypes)
    print(f"Number of features: {len(gdf_core):,}")

    print(f"Writing core parquet to: {OUTPUT_PATH}")
    gdf_core.to_parquet(OUTPUT_PATH, index=False)
    print("Done.")


if __name__ == "__main__":
    build_basinatlas_lev10_core()
