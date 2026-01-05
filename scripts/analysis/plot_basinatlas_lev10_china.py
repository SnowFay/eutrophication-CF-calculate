"""Quick visualization of BasinATLAS level-10 basins over China.

This script reads the preprocessed `basinatlas_lev10_china_core.parquet`
(geometry + core attributes) and produces a simple choropleth map
for a chosen variable (default: UP_AREA) over the China+buffer extent.

Output: PNG under `results/figures/hydrology/`.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import geopandas as gpd

# Paths
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed" / "hydrology"
RESULTS_DIR = ROOT / "results" / "figures" / "hydrology"


def load_basinatlas_china(level: int) -> gpd.GeoDataFrame:
    """Load BasinATLAS basins for China+buffer at a given level.

    Parameters
    ----------
    level : int
        BasinATLAS level (e.g., 3, 8, 10).
    """
    path = DATA_DIR / f"basinatlas_lev{level:02d}_china_core.parquet"
    gdf = gpd.read_parquet(path)
    # Ensure CRS is set (most likely EPSG:4326)
    if gdf.crs is None:
        gdf = gdf.set_crs(4326)
    return gdf


def plot_basin_variable(
    gdf: gpd.GeoDataFrame,
    column: str = "run_mm_syr",
    level: int = 10,
) -> None:
    """Plot a simple choropleth of a basin-level variable over China.

    Parameters
    ----------
    gdf : GeoDataFrame
        BasinATLAS level-10 basins (China subset).
    column : str, default "UP_AREA"
        Column to visualize; e.g., "UP_AREA" (km²) or "run_mm_syr" (mm/yr).
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if column not in gdf.columns:
        raise ValueError(f"Column '{column}' not found in BasinATLAS lev10 core.")

    fig, ax = plt.subplots(figsize=(8, 8))

    # 自定义颜色：0 为白色，值越大越接近深蓝色。
    # 为了让颜色分布更均匀，按分位数裁掉极端高值（例如 top 1%）。
    vmin = float(gdf[column].min())
    vmax = float(gdf[column].quantile(0.99))
    norm = Normalize(vmin=vmin, vmax=vmax, clip=True)

    # 构造从白色到深蓝的线性渐变 colormap
    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list("white_to_blue", ["#ffffff", "#08306b"])

    gdf.plot(
        column=column,
        cmap=cmap,
        norm=norm,
        linewidth=0.1,
        edgecolor="k",
        ax=ax,
    )

    ax.set_title(
        f"BasinATLAS level-{level:02d} basins in China\n"
        f"colored by {column} (long-term mean runoff depth, mm/yr)"
    )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Nice equal aspect
    ax.set_aspect("equal", adjustable="datalim")

    # Remove axis frame clutter
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label(column)

    out_path = RESULTS_DIR / f"basinatlas_lev{level:02d}_china_{column}.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_basin_variable_quantiles(
    gdf: gpd.GeoDataFrame,
    column: str = "run_mm_syr",
    level: int = 10,
) -> None:
    """Plot a quantile-based classified map for the given variable.

    This is useful when the distribution is highly skewed: each color
    class corresponds to a value range between selected quantiles, so
   颜色分布更均匀，便于肉眼辨认高低。"""

    import mapclassify

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if column not in gdf.columns:
        raise ValueError(f"Column '{column}' not found in BasinATLAS lev10 core.")

    fig, ax = plt.subplots(figsize=(8, 8))

    # 使用分位数分级，例如 5 个等级（20,40,60,80 百分位）
    scheme = mapclassify.Quantiles(gdf[column], k=5)

    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list(
        "white_to_blue_5",
        ["#ffffff", "#deebf7", "#9ecae1", "#3182bd", "#08306b"],
    )

    gdf.plot(
        column=column,
        cmap=cmap,
        scheme="Quantiles",
        k=5,
        linewidth=0.1,
        edgecolor="k",
        ax=ax,
        legend=True,
        legend_kwds={
            "loc": "lower left",
            "title": f"{column} quantiles",
            "fontsize": 8,
        },
    )

    ax.set_title(
        f"BasinATLAS level-{level:02d} basins in China\n"
        f"quantile classes of {column} (mm/yr)"
    )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal", adjustable="datalim")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out_path = (
        RESULTS_DIR
        / f"basinatlas_lev{level:02d}_china_{column}_quantiles.png"
    )
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    # Plot for levels 3–8 and 10 so you can visually compare across
    # multiple basin hierarchies over China.
    for level in (3, 4, 5, 6, 7, 8, 10):
        gdf = load_basinatlas_china(level)

        # Default: plot run_mm_syr = long-term mean runoff depth (mm/yr)
        # 这更直观地反映每个流域的“湿润/干旱”和水量供给条件。
        plot_basin_variable(gdf, column="run_mm_syr", level=level)

        # 额外输出：按分位数分级着色的一张图，便于 PPT 展示等级差异
        plot_basin_variable_quantiles(gdf, column="run_mm_syr", level=level)


if __name__ == "__main__":
    main()
