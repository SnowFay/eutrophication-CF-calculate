"""Build BasinATLAS basin cores for selected levels over China+buffer.

This script reads BasinATLAS_v10_levXX layers from the original GDB,
intersects them with the same China+buffer mask you used elsewhere,
and writes simplified core parquet files like:

- data/processed/hydrology/basinatlas_lev03_china_core.parquet
- data/processed/hydrology/basinatlas_lev08_china_core.parquet
- (lev10 already exists, but the function is generic.)

The goal is to have geometry + key hydrological fields (HYBAS_ID,
NEXT_DOWN, PFAF_ID, SUB_AREA, UP_AREA, run_mm_syr) for easy plotting
and aggregation.
"""

from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
RAW_GDB = (
    ROOT
    / "data"
    / "HydroSHEDS data"
    / "BasinATLAS_Data_v10.gdb"
    / "BasinATLAS_v10.gdb"
)
PROCESSED_DIR = ROOT / "data" / "processed" / "hydrology"

# 使用 GADM 中国国界（0 级）作为中国范围基础掩膜；如果你有单独
# 的 China+buffer shapefile，可以把这个路径改成那个文件。
CHINA_MASK = (
    ROOT
    / "data"
    / "boundary data"
    / "gadm41_CHN_shp"
    / "gadm41_CHN_0.shp"
)


def load_china_mask() -> gpd.GeoDataFrame | None:
    if CHINA_MASK is None:
        return None
    mask = gpd.read_file(CHINA_MASK)
    if mask.crs is None:
        mask = mask.set_crs(4326)
    else:
        mask = mask.to_crs(4326)
    return mask


def build_core_for_level(level: int) -> None:
    layer = f"BasinATLAS_v10_lev{level:02d}"
    print(f"Loading {layer} from {RAW_GDB} ...")
    gdf = gpd.read_file(RAW_GDB, layer=layer)

    # Ensure CRS
    if gdf.crs is None:
        gdf = gdf.set_crs(4326)
    else:
        gdf = gdf.to_crs(4326)

    # Clip to China+buffer
    mask = load_china_mask()
    if mask is not None:
        print("Clipping to China+buffer mask ...")
        # 这里用 spatial join 而不是 overlay，避免复杂多部件多边形
        # 带来的 organizePolygons 警告和性能问题。假设 China mask
        # 是一个（或少数几个）包含中国+buffer 的简单多边形。
        gdf = gpd.sjoin(gdf, mask.to_crs(gdf.crs), how="inner", predicate="intersects")
        # sjoin 会多出一些列（例如 index_right），这里只保留原始流域字段
        gdf = gdf[gdf.geometry.notna()]

    # Keep a subset of useful fields if present
    keep_cols = [
        "HYBAS_ID",
        "NEXT_DOWN",
        "NEXT_SINK",
        "MAIN_BAS",
        "PFAF_ID",
        "ENDO",
        "COAST",
        "ORDER_",
        "SORT",
        "SUB_AREA",
        "UP_AREA",
        "run_mm_syr",
    ]
    cols = [c for c in keep_cols if c in gdf.columns]
    cols.append("geometry")
    core = gdf[cols].copy()

    out_path = PROCESSED_DIR / f"basinatlas_lev{level:02d}_china_core.parquet"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Writing {out_path} with {len(core)} features ...")
    core.to_parquet(out_path)


def main() -> None:
    # Build for levels 3–8; 10 already exists but function is generic.
    for level in range(3, 9):
        build_core_for_level(level)


if __name__ == "__main__":
    main()
