import pathlib

import geopandas as gpd


DATA_ROOT = pathlib.Path("data")
RAW_LAKEATLAS_GDB = (
    DATA_ROOT
    / "HydroSHEDS data"
    / "LakeATLAS_Data_v10.gdb"
    / "LakeATLAS_v10.gdb"
)
LAYER_NAME = "LakeATLAS_v10_pol"

OUTPUT_DIR = DATA_ROOT / "processed" / "hydrology"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_GLOBAL = OUTPUT_DIR / "lakeatlas_global_core.parquet"


CORE_COLUMNS = [
    # identifiers / metadata
    "Hylak_id",
    "Lake_name",
    "Country",
    "Continent",
    "Poly_src",
    "Lake_type",
    "Grand_id",
    # linkage to basins and rivers
    "HYBAS_L12",
    "HYRIV_RCH",
    "HYRIV_CAT",
    # basic geometry / elevation
    "Elevation",
    "Pour_long",
    "Pour_lat",
    # a few hydrology / climate attributes (can be extended later)
    "run_mm_vyr",
    "Res_time",
]


def build_lakeatlas_core() -> None:
    """Build a lightweight LakeATLAS core table (global polygons).

    Notes
    -----
    - Provides the bridge from lakes (Hylak_id) to HydroBASINS (HYBAS_L12)
      and HydroRIVERS (HYRIV_RCH / HYRIV_CAT).
    - Keeps basic lake metadata and a minimal set of hydrology attributes.
    """

    if not RAW_LAKEATLAS_GDB.exists():
        raise FileNotFoundError(f"LakeATLAS GDB not found: {RAW_LAKEATLAS_GDB}")

    print(f"Reading LakeATLAS polygons from: {RAW_LAKEATLAS_GDB} (layer={LAYER_NAME})")
    gdf = gpd.read_file(RAW_LAKEATLAS_GDB, layer=LAYER_NAME)

    missing = [c for c in CORE_COLUMNS if c not in gdf.columns]
    if missing:
        raise KeyError(f"Missing expected columns in LakeATLAS: {missing}")

    gdf_core = gdf[CORE_COLUMNS + ["geometry"]].copy()

    print("LakeATLAS core schema:")
    print(gdf_core.dtypes)
    print(f"Number of lake polygons: {len(gdf_core):,}")

    print(f"Writing global LakeATLAS core to: {OUTPUT_GLOBAL}")
    gdf_core.to_parquet(OUTPUT_GLOBAL, index=False)
    print("Done.")


if __name__ == "__main__":
    build_lakeatlas_core()
