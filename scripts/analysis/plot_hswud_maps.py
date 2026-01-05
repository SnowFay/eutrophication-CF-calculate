"""Quick-look maps for HSWUD 2010-2020 mean water use over China.

This script reads the cleaned HSWUD NetCDF file and the China boundary
shapefile, then plots spatial distributions for each sectoral water use
(dom, ele, irr, manu) and the total water use.

Usage (from project root, after activating env):

    python -m scripts.analysis.plot_hswud_maps

Outputs:
- Figures saved under `results/figures/hswud/` as PNG files.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import geopandas as gpd

# Paths
DATA_ROOT = Path("data")
PROCESSED_WATER_USE_YEAR = DATA_ROOT / "processed" / "water_use" / "hswud_0p1_2010_2020_mean_clean.nc"
PROCESSED_WATER_USE_DAY = DATA_ROOT / "processed" / "water_use" / "hswud_0p1_2010_2020_mean_clean_m3_per_day.nc"
CHINA_BOUNDARY = DATA_ROOT / "boundary data" / "gadm41_CHN_shp" / "gadm41_CHN_0.shp"

FIG_DIR = Path("results") / "figures" / "hswud"


def load_data(use_daily: bool = False):
    """Load HSWUD Dataset (yearly or daily) and China boundary.

    Parameters
    ----------
    use_daily : bool, default False
        If True, load the m3/day version; otherwise load the m3/year version.
    """

    nc_path = PROCESSED_WATER_USE_DAY if use_daily else PROCESSED_WATER_USE_YEAR

    if not nc_path.exists():
        raise FileNotFoundError(nc_path)
    if not CHINA_BOUNDARY.exists():
        raise FileNotFoundError(CHINA_BOUNDARY)

    ds = xr.open_dataset(nc_path)
    gdf_china = gpd.read_file(CHINA_BOUNDARY)

    # we expect a single time slice (multi-year mean)
    if "time" in ds.dims:
        ds = ds.isel(time=0)

    return ds, gdf_china


def _plot_single_map(ax, da: xr.DataArray, gdf_china: gpd.GeoDataFrame, title: str, vmin=None, vmax=None):
    """Plot a single pcolormesh map with China boundary overlay.

    We use log10 scale for color by default (add +1 to avoid log(0)).
    """

    # Handle log scale
    data = da.values
    data = np.where(data < 0, 0, data)  # safety: ensure non-negative
    log_data = np.log10(data + 1.0)

    lon = da["lon"].values
    lat = da["lat"].values

    mesh = ax.pcolormesh(lon, lat, log_data, shading="auto", cmap="viridis", vmin=vmin, vmax=vmax)

    # Overlay China boundary
    gdf_china.boundary.plot(ax=ax, edgecolor="black", linewidth=0.5)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(title)

    return mesh


def _build_var_map(use_daily: bool = False) -> dict[str, str]:
    """Return mapping from logical sector name to variable name in the dataset."""

    suffix = "_m3_per_day" if use_daily else "_m3"
    sectors = ["dom", "ele", "irr", "manu"]
    var_map = {s: f"q_{s}{suffix}" for s in sectors}
    var_map["total"] = f"q_total{suffix}"
    return var_map


def plot_hswud_maps(use_daily: bool = False):
    ds, gdf_china = load_data(use_daily=use_daily)

    FIG_DIR.mkdir(parents=True, exist_ok=True)

    sectors = ["dom", "ele", "irr", "manu"]
    var_map = _build_var_map(use_daily=use_daily)

    # Determine common color scale on log10 for comparability
    all_data = []
    for key, var in var_map.items():
        if var in ds:
            arr = ds[var].values
            arr = np.where(arr < 0, 0, arr)
            all_data.append(np.log10(arr + 1.0).ravel())
    all_data = np.concatenate(all_data)
    finite = all_data[np.isfinite(all_data)]
    vmin = np.nanpercentile(finite, 5)
    vmax = np.nanpercentile(finite, 99)

    # Plot sectoral maps
    for sector in sectors + ["total"]:
        var = var_map[sector]
        if var not in ds:
            continue
        da = ds[var]

        fig, ax = plt.subplots(figsize=(8, 6))
        units_label = "m3/day" if use_daily else "m3/year"
        mesh = _plot_single_map(
            ax,
            da,
            gdf_china,
            title=f"HSWUD {sector} water use (2010-2020 mean) [log10({units_label})]",
            vmin=vmin,
            vmax=vmax,
        )
        cbar = fig.colorbar(mesh, ax=ax, shrink=0.8)
        cbar.set_label(f"log10(q + 1) [log10({units_label})]")

        fig.tight_layout()
        suffix = "m3_per_day" if use_daily else "m3_per_year"
        out_path = FIG_DIR / f"hswud_{sector}_2010_2020_mean_{suffix}.png"
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        print(f"Saved {out_path}")


def main() -> None:
    # First: yearly maps (m3/year), original behaviour
    plot_hswud_maps(use_daily=False)
    # Then: daily maps (m3/day) derived from the yearly dataset
    plot_hswud_maps(use_daily=True)


if __name__ == "__main__":
    main()
