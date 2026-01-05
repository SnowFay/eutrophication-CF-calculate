"""National overview plots for Stage D/E outputs on the China 0.1° grid.

Inputs
------
- Stage D: data/processed/grid_0p1/grid_k_params_china_0p1.nc
- Stage E: data/processed/grid_0p1/grid_ff_cf_china_0p1.nc

Outputs (by default)
--------------------
- results/figures/ff_cf_overview/*.png
- results/tables/ff_day_top100_cells.csv

This script is designed for quick, reproducible, nation-wide visualization.
It intentionally avoids cartopy (no basemap dependency) and uses plain lon/lat axes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap, LogNorm


DEFAULT_K_NC = Path("data/processed/grid_0p1/grid_k_params_china_0p1.nc")
DEFAULT_E_NC = Path("data/processed/grid_0p1/grid_ff_cf_china_0p1.nc")
DEFAULT_OUT_DIR = Path("results/figures/ff_cf_overview")
DEFAULT_TOP100_CSV = Path("results/tables/ff_day_top100_cells.csv")


def _as_2d(ds: xr.Dataset, name: str) -> np.ndarray:
    if name not in ds:
        raise KeyError(f"Missing variable: {name}")
    a = ds[name].to_numpy()
    if a.ndim != 2:
        raise ValueError(f"Expected 2D (lat,lon) for {name}, got shape {a.shape}")
    return a


def _mask_china(ds: xr.Dataset, a: np.ndarray) -> np.ndarray:
    in_china = _as_2d(ds, "in_china").astype(bool)
    out = a.astype(np.float64, copy=True)
    out[~in_china] = np.nan
    return out


def _plot_map(
    *,
    lon: np.ndarray,
    lat: np.ndarray,
    z: np.ndarray,
    title: str,
    out_png: Path,
    cmap: str,
    norm: matplotlib.colors.Normalize | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    cbar_label: str = "",
) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    # pcolormesh expects 2D; use xarray-like convention (lat, lon)
    mesh = ax.pcolormesh(lon, lat, z, shading="auto", cmap=cmap, norm=norm, vmin=vmin, vmax=vmax)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    cbar = fig.colorbar(mesh, ax=ax, shrink=0.92)
    if cbar_label:
        cbar.set_label(cbar_label)

    fig.savefig(out_png, dpi=200)
    plt.close(fig)


def _plot_hist_logx(*, values: np.ndarray, title: str, out_png: Path, xlabel: str) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    v = values[np.isfinite(values)]
    v = v[v > 0]
    if v.size == 0:
        return

    lo = np.nanpercentile(v, 0.1)
    hi = np.nanpercentile(v, 99.9)
    lo = max(lo, np.nanmin(v))
    hi = max(hi, lo * 10)

    bins = np.logspace(np.log10(lo), np.log10(hi), 60)

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    ax.hist(v, bins=bins, color="#4C78A8", alpha=0.9)
    ax.set_xscale("log")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Cell count")
    fig.savefig(out_png, dpi=200)
    plt.close(fig)


def _plot_map_binned(
    *,
    lon: np.ndarray,
    lat: np.ndarray,
    z: np.ndarray,
    title: str,
    out_png: Path,
    bins: list[float],
    labels: list[str],
    cmap_name: str = "plasma",
) -> None:
    """Plot a 2D field with discrete bins and labeled legend."""
    out_png.parent.mkdir(parents=True, exist_ok=True)

    if len(bins) < 2:
        raise ValueError("bins must have at least 2 edges")
    if len(labels) != len(bins) - 1:
        raise ValueError("labels must have length len(bins)-1")

    zf = z.astype(np.float64, copy=False)
    finite = np.isfinite(zf)
    if not np.any(finite):
        return

    # Replace the last edge (often a placeholder) with the data max to avoid inf in BoundaryNorm
    data_max = float(np.nanmax(zf[finite]))
    edges = np.array(bins, dtype=np.float64)
    if not np.isfinite(edges[-1]) or edges[-1] <= edges[-2]:
        edges[-1] = max(data_max * 1.000001, edges[-2] * 10.0)

    base = plt.get_cmap(cmap_name)
    n = len(edges) - 1
    colors = base(np.linspace(0.10, 0.95, n))
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(edges, ncolors=n, clip=False)

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    mesh = ax.pcolormesh(lon, lat, zf, shading="auto", cmap=cmap, norm=norm)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Colorbar centered on bins
    cbar = fig.colorbar(mesh, ax=ax, shrink=0.92)
    centers = (edges[:-1] + edges[1:]) / 2.0
    cbar.set_ticks(centers)
    cbar.set_ticklabels(labels)
    cbar.ax.tick_params(labelsize=8)

    fig.savefig(out_png, dpi=200)
    plt.close(fig)


def _top_n_table(
    *,
    ds_k: xr.Dataset,
    ds_e: xr.Dataset,
    n: int,
) -> pd.DataFrame:
    in_china = _as_2d(ds_e, "in_china").astype(bool)

    ff = _as_2d(ds_e, "ff_day").astype(np.float64)
    valid = in_china & np.isfinite(ff)
    if not np.any(valid):
        return pd.DataFrame()

    # Pick top-N indices
    flat_ff = ff[valid]
    # argsort for top N (descending)
    n = min(n, flat_ff.size)

    # map back to indices
    idx_all = np.argwhere(valid)
    order = np.argsort(flat_ff)[::-1][:n]
    ij = idx_all[order]

    lat_vals = ds_e["lat"].to_numpy().astype(np.float64)
    lon_vals = ds_e["lon"].to_numpy().astype(np.float64)

    rows = []
    for i, j in ij:
        rows.append(
            {
                "lat": float(lat_vals[i]),
                "lon": float(lon_vals[j]),
                "grid_id": int(ds_e["grid_id"].to_numpy()[i, j]),
                "ff_day": float(ff[i, j]),
                "tau_day": float(_as_2d(ds_k, "tau_day")[i, j]) if "tau_day" in ds_k else np.nan,
                "f_transfer": float(_as_2d(ds_e, "f_transfer")[i, j]) if "f_transfer" in ds_e else np.nan,
                "export_frac_to_outlet": float(_as_2d(ds_e, "export_frac_to_outlet")[i, j]) if "export_frac_to_outlet" in ds_e else np.nan,
                "steps_to_outlet": int(_as_2d(ds_e, "steps_to_outlet")[i, j]) if "steps_to_outlet" in ds_e else 0,
                "cycle_break_flag": int(_as_2d(ds_e, "cycle_break_flag")[i, j]) if "cycle_break_flag" in ds_e else 0,
                "k_adv_day": float(_as_2d(ds_k, "k_adv_day")[i, j]) if "k_adv_day" in ds_k else np.nan,
                "k_ret_day": float(_as_2d(ds_k, "k_ret_day")[i, j]) if "k_ret_day" in ds_k else np.nan,
                "k_use_day": float(_as_2d(ds_k, "k_use_day")[i, j]) if "k_use_day" in ds_k else np.nan,
            }
        )

    df = pd.DataFrame(rows)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="National overview plots for FF/CF results (0.1° China grid)")
    parser.add_argument("--k-nc", type=str, default=str(DEFAULT_K_NC))
    parser.add_argument("--e-nc", type=str, default=str(DEFAULT_E_NC))
    parser.add_argument("--out-dir", type=str, default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--top-n", type=int, default=100)
    parser.add_argument("--top-csv", type=str, default=str(DEFAULT_TOP100_CSV))
    args = parser.parse_args()

    out_dir = Path(args.out_dir)

    ds_k = xr.open_dataset(Path(args.k_nc))
    ds_e = xr.open_dataset(Path(args.e_nc))

    lon = ds_e["lon"].to_numpy().astype(np.float64)
    lat = ds_e["lat"].to_numpy().astype(np.float64)

    # Maps
    tau = _mask_china(ds_k, _as_2d(ds_k, "tau_day"))
    ff = _mask_china(ds_e, _as_2d(ds_e, "ff_day"))
    ftr = _mask_china(ds_e, _as_2d(ds_e, "f_transfer"))
    expf = _mask_china(ds_e, _as_2d(ds_e, "export_frac_to_outlet"))

    # Use robust percentiles for color limits
    def pclip(a: np.ndarray, lo: float, hi: float) -> tuple[float, float]:
        v = a[np.isfinite(a)]
        if v.size == 0:
            return (0.0, 1.0)
        return (float(np.nanpercentile(v, lo)), float(np.nanpercentile(v, hi)))

    # tau_day map (log)
    tau_lo, tau_hi = pclip(tau, 1, 99)
    tau_lo = max(tau_lo, 1e-6)
    tau_hi = max(tau_hi, tau_lo * 10)
    _plot_map(
        lon=lon,
        lat=lat,
        z=tau,
        title="Stage D: tau_day (residence time)",
        out_png=out_dir / "01_tau_day_map.png",
        cmap="viridis",
        norm=LogNorm(vmin=tau_lo, vmax=tau_hi),
        cbar_label="day (log)",
    )

    # f_transfer map
    _plot_map(
        lon=lon,
        lat=lat,
        z=ftr,
        title="Stage E: f_transfer = k_adv/(k_adv+k_ret+k_use)",
        out_png=out_dir / "02_f_transfer_map.png",
        cmap="magma",
        vmin=0.0,
        vmax=1.0,
        cbar_label="fraction",
    )

    # ff_day map (log)
    ff_lo, ff_hi = pclip(ff, 1, 99)
    ff_lo = max(ff_lo, 1e-6)
    ff_hi = max(ff_hi, ff_lo * 10)
    _plot_map(
        lon=lon,
        lat=lat,
        z=ff,
        title="Stage E: FF (ff_day)",
        out_png=out_dir / "03_ff_day_map.png",
        cmap="plasma",
        norm=LogNorm(vmin=ff_lo, vmax=ff_hi),
        cbar_label="day (log)",
    )

    # ff_day map (discrete bins for presentation)
    # User-facing bins in days: 0–3, 3–10, 10–30, 30–100, 100–300, 300–1000, >1000
    ff_bins = [0.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, float("nan")]
    ff_labels = [
        "0–3",
        "3–10",
        "10–30",
        "30–100",
        "100–300",
        "300–1000",
        ">1000",
    ]
    _plot_map_binned(
        lon=lon,
        lat=lat,
        z=ff,
        title="Stage E: FF (ff_day) binned (day)",
        out_png=out_dir / "03b_ff_day_map_binned.png",
        bins=ff_bins,
        labels=ff_labels,
        cmap_name="plasma",
    )

    # export fraction map
    _plot_map(
        lon=lon,
        lat=lat,
        z=expf,
        title="Stage E: export fraction to outlet",
        out_png=out_dir / "04_export_frac_to_outlet_map.png",
        cmap="cividis",
        vmin=0.0,
        vmax=1.0,
        cbar_label="fraction",
    )

    # coverage map for ff
    in_china = _as_2d(ds_e, "in_china").astype(bool)
    ff_finite = np.isfinite(ff)
    cov = np.where(in_china, ff_finite.astype(np.float32), np.nan)
    _plot_map(
        lon=lon,
        lat=lat,
        z=cov,
        title="Stage E: FF availability (1=fine, 0=NaN)",
        out_png=out_dir / "05_ff_availability_map.png",
        cmap="gray",
        vmin=0.0,
        vmax=1.0,
        cbar_label="availability",
    )

    # Histogram of ff_day (log-x)
    _plot_hist_logx(
        values=ff,
        title="Stage E: FF (ff_day) distribution (log-x)",
        out_png=out_dir / "06_ff_day_hist_logx.png",
        xlabel="ff_day (day, log)",
    )

    # Top-N diagnostic table
    df_top = _top_n_table(ds_k=ds_k, ds_e=ds_e, n=int(args.top_n))
    out_csv = Path(args.top_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df_top.to_csv(out_csv, index=False)

    print(f"Wrote figures to: {out_dir}")
    print(f"Wrote top-{len(df_top)} table: {out_csv}")

    ds_k.close()
    ds_e.close()


if __name__ == "__main__":
    main()
