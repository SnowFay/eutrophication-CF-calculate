"""Compute Helmes-style grid-level k parameters on the China 0.1° grid.

This script derives per-grid hydrologic volumes and removal rates following
Helmes et al. (2012) and Online Resource 1 formulas (as captured in
materials/articles/*11367_2012_382_MOESM1_ESM*.md):

Core equations (grid cell i/j)
------------------------------
Advection:
    k_adv,i = Q_i / V_tot,i
where Q is discharge (km^3/day) and V_tot is total freshwater volume (km^3).

Retention (simplified form from Online Resource 1 Eq.4):
    k_ret,j = (V_riv,j * k_ret,riv,j + v_f * (A_lake,j + A_res,j)) / V_tot,j

Water use (Helmes Eq.9):
    k_use,j = f_WTA,j * (1 - f_DITW,j) * k_adv,j * (1 - f_soil,j)

Persistence:
    tau_j = 1 / (k_adv,j + k_ret,j + k_use,j)

Data sources in this repo
-------------------------
- HydroRIVERS mapping (per grid_id, per reach overlap): DIS_AV_CMS, overlap_length_km
- HydroLAKES mapping (per grid_id, per lake overlap): Vol_total, Lake_area, overlap_area_km2
- BasinATLAS lev10 mapping (per grid_id overlap): run_mm_syr
- HSWUD processed water use (0.1°): q_*_m3_per_day

Important implementation choices
--------------------------------
- Grid discharge Q_i is taken as the discharge of the *main* reach in the cell
  (argmax overlap_length_km), aligned with the single downstream pointer logic.
- River volume is computed by summing per-intersection segment volume:
      V_seg = W(Q_seg) * D(Q_seg) * L_overlap
  where W and D follow Wollheim et al. (2006) power laws (Online Resource 1 Eq.1-2).
- Lake/reservoir volume is spatially distributed across grid cells by area fraction:
      V_lake_in_cell = Vol_total * (overlap_area_km2 / Lake_area)
- f_soil uses only f_DIP + f_DOP (particulate P transfer omitted for now).

Outputs
-------
- data/processed/grid_0p1/grid_k_params_china_0p1.nc

"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd


DEFAULT_GRID_NC = Path("data/processed/grid_0p1/grid_cells_china_0p1.nc")
DEFAULT_GRID_PARQUET = Path("data/processed/grid_0p1/grid_cells_china_0p1.parquet")
DEFAULT_HYDRO_GEOM_NC = Path("data/processed/grid_0p1/grid_hydro_geom_china_0p1.nc")

DEFAULT_HYDRORIVERS_MAP = Path("data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet")
DEFAULT_HYDROLAKES_MAP = Path("data/processed/grid_0p1/grid_hydrolakes_china_0p1_mapping.parquet")
DEFAULT_BASINATLAS_MAP = Path("data/processed/grid_0p1/grid_basinatlas_lev10_china_0p1_mapping.parquet")

DEFAULT_HSWUD = Path("data/processed/water_use/hswud_0p1_2010_2020_mean_clean_m3_per_day.parquet")

DEFAULT_OUT = Path("data/processed/grid_0p1/grid_k_params_china_0p1.nc")


SECONDS_PER_DAY = 86400.0
SECONDS_PER_YEAR = 31557600.0  # 365.25 days
M3_PER_KM3 = 1e9

# HydroLAKES TechDoc v1.0: Vol_total / Vol_res are in million cubic meters (mcm)
# 1 mcm = 0.001 km^3
MCM_TO_KM3 = 1e-3

# Wollheim et al. (2006) constants (Online Resource 1 Table 1.1)
AW = 5.01e-2
BW = 0.52
AD = 1.04e-3
BD = 0.37

# Uptake velocity (Alexander et al. 2004) per Online Resource 1
VF_KM_PER_DAY = 3.8e-5

# Numerical stability: mask rates when total volume is implausibly tiny.
# 1e-9 km^3 = 1 m^3.
V_TOT_MIN_KM3_FOR_RATES = 1.0e-9

# River retention rate kriv (yr^-1) piecewise by discharge Q (km^3/yr)
KRIV_Q1 = 0.0882
KRIV_Q2 = 0.4473
KRIV_LOW = 71.2
KRIV_MID = 25.0
KRIV_HIGH = 4.4


def _validate_grid_base(ds: xr.Dataset) -> None:
    for v in ["grid_id", "in_china"]:
        if v not in ds:
            raise KeyError(f"Grid base NetCDF missing variable: {v}")
    if ds["grid_id"].ndim != 2:
        raise ValueError("Expected grid_id to be 2D (lat, lon)")


def _build_gid_to_flat_index(grid_id_2d: np.ndarray) -> pd.Series:
    flat = grid_id_2d.reshape(-1)
    valid_mask = flat != -1
    gids = flat[valid_mask].astype(np.int64)
    flat_idx = np.nonzero(valid_mask)[0].astype(np.int64)
    return pd.Series(flat_idx, index=gids)


def _scatter_to_grid(
    *,
    grid_shape: tuple[int, int],
    gid_to_flat: pd.Series,
    values_by_gid: pd.Series,
    dtype: object,
    fill: object,
) -> np.ndarray:
    out_flat = np.full((grid_shape[0] * grid_shape[1],), fill, dtype=dtype)
    if len(values_by_gid) == 0:
        return out_flat.reshape(grid_shape)

    s = values_by_gid.copy()
    s.index = s.index.astype(np.int64)
    common = s.index.intersection(gid_to_flat.index)
    if len(common) == 0:
        return out_flat.reshape(grid_shape)

    idx = gid_to_flat.loc[common].to_numpy(dtype=np.int64)
    vals = s.loc[common].to_numpy()

    if np.issubdtype(np.dtype(dtype), np.floating):
        vals = vals.astype(np.float64, copy=False)
        out_flat[idx] = vals.astype(dtype, copy=False)
    else:
        vals = np.nan_to_num(vals, nan=float(fill) if isinstance(fill, (int, float)) else 0.0).astype(dtype, copy=False)
        out_flat[idx] = vals

    return out_flat.reshape(grid_shape)


def _q_cms_to_km3_per_day(q_cms: np.ndarray) -> np.ndarray:
    return (q_cms.astype(np.float64) * SECONDS_PER_DAY) / M3_PER_KM3


def _q_cms_to_km3_per_year(q_cms: np.ndarray) -> np.ndarray:
    return (q_cms.astype(np.float64) * SECONDS_PER_YEAR) / M3_PER_KM3


def _compute_main_reach_discharge_by_gid(df_riv: pd.DataFrame) -> pd.Series:
    required = ["grid_id", "DIS_AV_CMS", "overlap_length_km"]
    for c in required:
        if c not in df_riv.columns:
            raise KeyError(f"HydroRIVERS mapping missing required column '{c}'")

    w = pd.to_numeric(df_riv["overlap_length_km"], errors="coerce").fillna(0.0).clip(lower=0.0)
    idx_main = w.groupby(df_riv["grid_id"]).idxmax()
    main = df_riv.loc[idx_main, ["grid_id", "DIS_AV_CMS"]].copy()
    main["DIS_AV_CMS"] = pd.to_numeric(main["DIS_AV_CMS"], errors="coerce")
    main = main.dropna(subset=["grid_id"])
    return pd.Series(main["DIS_AV_CMS"].to_numpy(dtype=np.float64), index=main["grid_id"].to_numpy(dtype=np.int64))


def _compute_river_length_km_by_gid(df_riv: pd.DataFrame) -> pd.Series:
    if "grid_id" not in df_riv.columns or "overlap_length_km" not in df_riv.columns:
        raise KeyError("HydroRIVERS mapping missing required columns: grid_id, overlap_length_km")
    l_km = pd.to_numeric(df_riv["overlap_length_km"], errors="coerce").fillna(0.0).clip(lower=0.0)
    return l_km.groupby(df_riv["grid_id"]).sum(min_count=1)


def _compute_river_volume_km3_by_gid(df_riv: pd.DataFrame) -> pd.Series:
    required = ["grid_id", "DIS_AV_CMS", "overlap_length_km"]
    for c in required:
        if c not in df_riv.columns:
            raise KeyError(f"HydroRIVERS mapping missing required column '{c}'")

    q_cms = pd.to_numeric(df_riv["DIS_AV_CMS"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)
    q_km3_yr = _q_cms_to_km3_per_year(q_cms)

    # Wollheim power laws: Q in km^3/yr, W/D in km
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        width_km = AW * np.power(q_km3_yr, BW)
        depth_km = AD * np.power(q_km3_yr, BD)

    width_km = np.where(np.isfinite(width_km), width_km, 0.0)
    depth_km = np.where(np.isfinite(depth_km), depth_km, 0.0)

    l_km = pd.to_numeric(df_riv["overlap_length_km"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)

    v_seg_km3 = width_km * depth_km * l_km
    v_seg_km3 = np.where(np.isfinite(v_seg_km3), v_seg_km3, 0.0)

    df_tmp = pd.DataFrame({"grid_id": df_riv["grid_id"].to_numpy(dtype=np.int64), "v_km3": v_seg_km3})
    return df_tmp.groupby("grid_id")["v_km3"].sum(min_count=1)


def _compute_lake_area_and_volume_by_gid(df_lake: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    required = ["grid_id", "overlap_area_km2", "Lake_area", "Vol_total"]
    for c in required:
        if c not in df_lake.columns:
            raise KeyError(f"HydroLAKES mapping missing required column '{c}'")

    area_in_cell = pd.to_numeric(df_lake["overlap_area_km2"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)
    lake_area_total = pd.to_numeric(df_lake["Lake_area"], errors="coerce").replace(0.0, np.nan).to_numpy(dtype=np.float64)
    vol_total_km3 = (
        pd.to_numeric(df_lake["Vol_total"], errors="coerce")
        .fillna(0.0)
        .clip(lower=0.0)
        .to_numpy(dtype=np.float64)
        * MCM_TO_KM3
    )

    with np.errstate(divide="ignore", invalid="ignore"):
        frac = area_in_cell / lake_area_total
    frac = np.where(np.isfinite(frac), frac, 0.0)
    frac = np.clip(frac, 0.0, 1.0)

    v_in_cell = vol_total_km3 * frac

    df_tmp = pd.DataFrame(
        {
            "grid_id": df_lake["grid_id"].to_numpy(dtype=np.int64),
            "a_km2": area_in_cell,
            "v_km3": v_in_cell,
        }
    )

    a_by_gid = df_tmp.groupby("grid_id")["a_km2"].sum(min_count=1)
    v_by_gid = df_tmp.groupby("grid_id")["v_km3"].sum(min_count=1)
    return a_by_gid, v_by_gid


def _compute_waterbody_components_by_gid(df_lake: pd.DataFrame) -> pd.DataFrame:
    """Compute per-grid waterbody components from HydroLAKES mapping.

    Uses per-feature total attributes distributed into grid cells by area fraction.

    Returns a DataFrame indexed by grid_id with columns:
      - a_wb_km2_in_cell: sum overlap_area_km2
      - v_wb_km3_in_cell: sum Vol_total * frac
      - v_res_km3_in_cell: sum Vol_res * frac
      - v_lake_km3_in_cell: sum max(Vol_total-Vol_res,0) * frac
      - dis_avg_cms_wmean: area-weighted mean of Dis_avg (m3/s)
    - res_time_day_wmean: area-weighted mean of Res_time (days)
    """

    required = ["grid_id", "overlap_area_km2", "Lake_area", "Vol_total", "Vol_res", "Dis_avg", "Res_time"]
    for c in required:
        if c not in df_lake.columns:
            raise KeyError(f"HydroLAKES mapping missing required column '{c}'")

    area_in_cell = (
        pd.to_numeric(df_lake["overlap_area_km2"], errors="coerce")
        .fillna(0.0)
        .clip(lower=0.0)
        .to_numpy(dtype=np.float64)
    )
    lake_area_total = pd.to_numeric(df_lake["Lake_area"], errors="coerce").replace(0.0, np.nan).to_numpy(dtype=np.float64)

    vol_total_km3 = (
        pd.to_numeric(df_lake["Vol_total"], errors="coerce")
        .fillna(0.0)
        .clip(lower=0.0)
        .to_numpy(dtype=np.float64)
        * MCM_TO_KM3
    )
    vol_res_km3 = (
        pd.to_numeric(df_lake["Vol_res"], errors="coerce")
        .fillna(0.0)
        .clip(lower=0.0)
        .to_numpy(dtype=np.float64)
        * MCM_TO_KM3
    )
    vol_lake_km3 = np.clip(vol_total_km3 - vol_res_km3, 0.0, None)

    dis_avg_cms = pd.to_numeric(df_lake["Dis_avg"], errors="coerce").to_numpy(dtype=np.float64)
    res_time_day = pd.to_numeric(df_lake["Res_time"], errors="coerce").to_numpy(dtype=np.float64)

    with np.errstate(divide="ignore", invalid="ignore"):
        frac = area_in_cell / lake_area_total
    frac = np.where(np.isfinite(frac), frac, 0.0)
    frac = np.clip(frac, 0.0, 1.0)

    v_wb_in_cell = vol_total_km3 * frac
    v_res_in_cell = vol_res_km3 * frac
    v_lake_in_cell = vol_lake_km3 * frac

    # Weighted means for Dis_avg and Res_time using overlap area as weights
    w = area_in_cell
    dis_num = np.where(np.isfinite(dis_avg_cms) & (dis_avg_cms > 0), dis_avg_cms * w, 0.0)
    dis_den = np.where(np.isfinite(dis_avg_cms) & (dis_avg_cms > 0), w, 0.0)
    rt_num = np.where(np.isfinite(res_time_day) & (res_time_day > 0), res_time_day * w, 0.0)
    rt_den = np.where(np.isfinite(res_time_day) & (res_time_day > 0), w, 0.0)

    df_tmp = pd.DataFrame(
        {
            "grid_id": df_lake["grid_id"].to_numpy(dtype=np.int64),
            "a_wb_km2": w,
            "v_wb_km3": v_wb_in_cell,
            "v_res_km3": v_res_in_cell,
            "v_lake_km3": v_lake_in_cell,
            "dis_num": dis_num,
            "dis_den": dis_den,
            "rt_num": rt_num,
            "rt_den": rt_den,
        }
    )

    g = df_tmp.groupby("grid_id", as_index=True)
    out = pd.DataFrame(index=g.size().index)
    out["a_wb_km2_in_cell"] = g["a_wb_km2"].sum(min_count=1)
    out["v_wb_km3_in_cell"] = g["v_wb_km3"].sum(min_count=1)
    out["v_res_km3_in_cell"] = g["v_res_km3"].sum(min_count=1)
    out["v_lake_km3_in_cell"] = g["v_lake_km3"].sum(min_count=1)
    out["dis_avg_cms_wmean"] = g["dis_num"].sum(min_count=1) / g["dis_den"].sum(min_count=1).replace(0.0, np.nan)
    out["res_time_day_wmean"] = g["rt_num"].sum(min_count=1) / g["rt_den"].sum(min_count=1).replace(0.0, np.nan)
    return out


def _compute_cell_area_km2(grid_parquet: Path) -> pd.Series:
    if not grid_parquet.exists():
        raise FileNotFoundError(grid_parquet)
    g = gpd.read_parquet(grid_parquet)
    if "grid_id" not in g.columns or "geometry" not in g.columns:
        raise KeyError("grid parquet must contain grid_id and geometry")
    area_km2 = g.to_crs(6933).geometry.area / 1e6
    return pd.Series(area_km2.to_numpy(dtype=np.float64), index=g["grid_id"].to_numpy(dtype=np.int64))


def _compute_runoff_m_per_year_by_gid(df_basin: pd.DataFrame) -> pd.Series:
    required = ["grid_id", "run_mm_syr", "overlap_area_km2"]
    for c in required:
        if c not in df_basin.columns:
            raise KeyError(f"BasinATLAS mapping missing required column '{c}'")

    run_mm = pd.to_numeric(df_basin["run_mm_syr"], errors="coerce").to_numpy(dtype=np.float64)
    area = pd.to_numeric(df_basin["overlap_area_km2"], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(dtype=np.float64)

    # Area-weighted mean runoff in mm/yr
    df_tmp = pd.DataFrame({"grid_id": df_basin["grid_id"].to_numpy(dtype=np.int64), "run_mm": run_mm, "w": area})
    num = (df_tmp["run_mm"] * df_tmp["w"]).groupby(df_tmp["grid_id"]).sum(min_count=1)
    den = df_tmp["w"].groupby(df_tmp["grid_id"]).sum(min_count=1).replace(0.0, np.nan)
    run_mm_mean = num / den

    run_m = run_mm_mean / 1000.0
    return run_m


def _compute_water_use_by_gid(
    *,
    grid_ds: xr.Dataset,
    hswud_path: Path,
) -> pd.DataFrame:
    if not hswud_path.exists():
        raise FileNotFoundError(hswud_path)

    df = pd.read_parquet(hswud_path)
    for c in [
        "lat",
        "lon",
        "q_dom_m3_per_day",
        "q_ele_m3_per_day",
        "q_irr_m3_per_day",
        "q_manu_m3_per_day",
        "q_total_m3_per_day",
    ]:
        if c not in df.columns:
            raise KeyError(f"HSWUD missing required column '{c}'")

    # Map lat/lon to grid_id via integer 0.1° indices.
    lat10_vals = np.rint(grid_ds["lat"].to_numpy().astype(np.float64) * 10).astype(np.int32)
    lon10_vals = np.rint(grid_ds["lon"].to_numpy().astype(np.float64) * 10).astype(np.int32)

    lat10_to_i = {int(v): i for i, v in enumerate(lat10_vals)}
    lon10_to_j = {int(v): j for j, v in enumerate(lon10_vals)}

    gid_2d = grid_ds["grid_id"].to_numpy().astype(np.int32)

    lat10 = np.rint(df["lat"].to_numpy(dtype=np.float64) * 10).astype(np.int32)
    lon10 = np.rint(df["lon"].to_numpy(dtype=np.float64) * 10).astype(np.int32)

    gids = np.full((len(df),), -1, dtype=np.int32)
    for idx, (la10, lo10) in enumerate(zip(lat10, lon10)):
        i = lat10_to_i.get(int(la10))
        j = lon10_to_j.get(int(lo10))
        if i is None or j is None:
            continue
        gids[idx] = gid_2d[i, j]

    out = df[[
        "q_dom_m3_per_day",
        "q_ele_m3_per_day",
        "q_irr_m3_per_day",
        "q_manu_m3_per_day",
        "q_total_m3_per_day",
    ]].copy()
    out["grid_id"] = gids.astype(np.int64)
    out = out[out["grid_id"] != -1]

    # Aggregate in case of duplicates (should typically be 1 row per cell)
    out = out.groupby("grid_id", as_index=True).sum(numeric_only=True)
    return out


def _f_dip(runoff_m_yr: np.ndarray) -> np.ndarray:
    # Online Resource 1 Eq.8
    R = runoff_m_yr.astype(np.float64)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        out = 0.29 / (1.0 + np.power(R / 0.85, -2.0))
    return out


def _f_dop(runoff_m_yr: np.ndarray) -> np.ndarray:
    # Online Resource 1 Eq.9
    R = runoff_m_yr.astype(np.float64)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        out = 0.01 * np.power(R, 0.95)
    return out


def _kriv_day_from_q_km3_yr(q_km3_yr: np.ndarray) -> np.ndarray:
    q = q_km3_yr.astype(np.float64)
    kriv_yr = np.where(
        q < KRIV_Q1,
        KRIV_LOW,
        np.where(q < KRIV_Q2, KRIV_MID, KRIV_HIGH),
    )
    return kriv_yr / 365.25


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Helmes-style k parameters on China 0.1° grid")
    parser.add_argument("--grid-nc", type=str, default=str(DEFAULT_GRID_NC))
    parser.add_argument("--grid-parquet", type=str, default=str(DEFAULT_GRID_PARQUET))
    parser.add_argument(
        "--hydro-geom-nc",
        type=str,
        default=str(DEFAULT_HYDRO_GEOM_NC),
        help="Stage-C hydro/geometry NetCDF (authoritative Q/runoff/areas/volumes)",
    )
    parser.add_argument("--hydrorivers-map", type=str, default=str(DEFAULT_HYDRORIVERS_MAP))
    parser.add_argument("--hydrolakes-map", type=str, default=str(DEFAULT_HYDROLAKES_MAP))
    parser.add_argument("--basinatlas-map", type=str, default=str(DEFAULT_BASINATLAS_MAP))
    parser.add_argument("--hswud", type=str, default=str(DEFAULT_HSWUD))
    parser.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    args = parser.parse_args()

    grid_path = Path(args.grid_nc)
    ds_grid = xr.open_dataset(grid_path)
    _validate_grid_base(ds_grid)

    hg_path = Path(args.hydro_geom_nc)
    ds_hg = xr.open_dataset(hg_path)

    grid_shape = ds_grid["grid_id"].shape
    gid_to_flat = _build_gid_to_flat_index(ds_grid["grid_id"].to_numpy())
    in_china = ds_grid["in_china"].to_numpy().astype(bool)

    if ds_hg["grid_id"].shape != grid_shape:
        raise ValueError(f"Stage-C hydro/geom grid shape mismatch: {ds_hg['grid_id'].shape} vs {grid_shape}")

    # Load mapping tables
    df_riv = pd.read_parquet(Path(args.hydrorivers_map))
    df_lake = pd.read_parquet(Path(args.hydrolakes_map))
    df_basin = pd.read_parquet(Path(args.basinatlas_map))

    # Per-grid derived quantities
    q_main_cms_by_gid = _compute_main_reach_discharge_by_gid(df_riv)
    l_riv_km_by_gid = _compute_river_length_km_by_gid(df_riv)
    v_riv_km3_by_gid = _compute_river_volume_km3_by_gid(df_riv)

    # Waterbody components (lake+reservoir)
    wb = _compute_waterbody_components_by_gid(df_lake)
    runoff_m_yr_by_gid = _compute_runoff_m_per_year_by_gid(df_basin)

    df_use = _compute_water_use_by_gid(grid_ds=ds_grid, hswud_path=Path(args.hswud))

    # Align all per-gid series into one frame (outer join)
    df_all = pd.DataFrame(index=pd.Index(gid_to_flat.index.to_numpy(dtype=np.int64), name="grid_id"))
    df_all["q_main_cms"] = q_main_cms_by_gid
    df_all["river_length_km_in_cell"] = l_riv_km_by_gid
    df_all["v_riv_km3"] = v_riv_km3_by_gid
    df_all = df_all.join(wb, how="left")
    df_all["runoff_m_yr"] = runoff_m_yr_by_gid

    for c in df_use.columns:
        df_all[c] = df_use[c]

    # Fill missing volumes/areas with zeros (no overlap)
    for c in [
        "river_length_km_in_cell",
        "v_riv_km3",
        "a_wb_km2_in_cell",
        "v_wb_km3_in_cell",
        "v_res_km3_in_cell",
        "v_lake_km3_in_cell",
    ]:
        df_all[c] = df_all[c].fillna(0.0)

    # Optional: cell area (useful for diagnostics / later extensions)
    try:
        cell_area = _compute_cell_area_km2(Path(args.grid_parquet))
        df_all["cell_area_km2"] = cell_area
    except Exception:
        df_all["cell_area_km2"] = np.nan

    # === Stage-C authoritative inputs (aligned to df_all.index via gid_to_flat) ===
    gid_index = df_all.index.to_numpy(dtype=np.int64)
    flat_index = gid_to_flat.loc[gid_index].to_numpy(dtype=np.int64)

    def _hg_1d(var: str) -> np.ndarray:
        if var not in ds_hg:
            raise KeyError(f"Stage-C hydro/geom missing variable: {var}")
        return ds_hg[var].to_numpy().reshape(-1)[flat_index].astype(np.float64, copy=False)

    q_best_cms = _hg_1d("q_best_cms")
    runoff_m_yr = _hg_1d("runoff_m_per_year")
    cell_area_km2 = _hg_1d("cell_area_km2")
    v_riv_km3 = _hg_1d("v_river_km3")
    a_wb_km2 = _hg_1d("waterbody_area_km2_in_cell")
    v_wb_km3 = _hg_1d("v_waterbody_km3_in_cell")
    v_lake_km3 = _hg_1d("v_lake_km3_in_cell")
    v_res_km3 = _hg_1d("v_reservoir_km3_in_cell")
    v_tot_km3 = _hg_1d("v_tot_km3")

    # Q (authoritative from Stage C)
    q_cell_cms = q_best_cms
    # Diagnostics (mapping-based)
    q_river_main_cms = df_all["q_main_cms"].fillna(0.0).to_numpy(dtype=np.float64)
    q_lake_disavg_cms = df_all["dis_avg_cms_wmean"].fillna(0.0).to_numpy(dtype=np.float64)

    q_km3_day = _q_cms_to_km3_per_day(q_cell_cms)
    q_km3_yr = _q_cms_to_km3_per_year(q_cell_cms)

    v_tot_km3_for_rates = np.where(v_tot_km3 >= V_TOT_MIN_KM3_FOR_RATES, v_tot_km3, np.nan)
    n_vtot_masked = int(np.isfinite(v_tot_km3).sum() - np.isfinite(v_tot_km3_for_rates).sum())

    # Wollheim width/depth for main channel (diagnostics)
    q_main_km3_yr = _q_cms_to_km3_per_year(q_river_main_cms)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        w_main_km = AW * np.power(q_main_km3_yr, BW)
        d_main_km = AD * np.power(q_main_km3_yr, BD)
    w_main_m = np.where(np.isfinite(w_main_km), w_main_km * 1000.0, 0.0)
    d_main_m = np.where(np.isfinite(d_main_km), d_main_km * 1000.0, 0.0)

    with np.errstate(divide="ignore", invalid="ignore"):
        k_adv_day = np.where(np.isfinite(v_tot_km3_for_rates), q_km3_day / v_tot_km3_for_rates, np.nan)

    # k_ret
    kriv_day = _kriv_day_from_q_km3_yr(q_km3_yr)

    with np.errstate(divide="ignore", invalid="ignore"):
        k_ret_day = np.where(
            np.isfinite(v_tot_km3_for_rates),
            (v_riv_km3 * kriv_day + VF_KM_PER_DAY * a_wb_km2) / v_tot_km3_for_rates,
            np.nan,
        )

    # f_soil (DIP + DOP)
    # f_soil (DIP + DOP): use Stage-C runoff
    f_dip = _f_dip(runoff_m_yr)
    f_dop = _f_dop(runoff_m_yr)
    f_soil = f_dip + f_dop
    f_soil = np.clip(f_soil, 0.0, 1.0)

    # f_WTA and f_DITW
    q_total_m3_day = df_all.get("q_total_m3_per_day", pd.Series(index=df_all.index, data=np.nan)).fillna(0.0).to_numpy(dtype=np.float64)
    q_dom_m3_day = df_all.get("q_dom_m3_per_day", pd.Series(index=df_all.index, data=np.nan)).fillna(0.0).to_numpy(dtype=np.float64)
    q_ele_m3_day = df_all.get("q_ele_m3_per_day", pd.Series(index=df_all.index, data=np.nan)).fillna(0.0).to_numpy(dtype=np.float64)
    q_manu_m3_day = df_all.get("q_manu_m3_per_day", pd.Series(index=df_all.index, data=np.nan)).fillna(0.0).to_numpy(dtype=np.float64)

    q_main_m3_day = q_cell_cms * SECONDS_PER_DAY

    with np.errstate(divide="ignore", invalid="ignore"):
        f_wta = np.where(q_main_m3_day > 0.0, q_total_m3_day / q_main_m3_day, np.nan)
    # When demand exists but discharge is ~0, treat as supply-limited and cap
    f_wta = np.where((~np.isfinite(f_wta)) & (q_total_m3_day > 0.0), 500.0, f_wta)
    f_wta = np.where((~np.isfinite(f_wta)) & (q_total_m3_day <= 0.0), 0.0, f_wta)
    f_wta = np.clip(f_wta, 0.0, 500.0)

    ditw_num = q_dom_m3_day + q_manu_m3_day + q_ele_m3_day
    with np.errstate(divide="ignore", invalid="ignore"):
        f_ditw = np.where(q_total_m3_day > 0.0, ditw_num / q_total_m3_day, 0.0)
    f_ditw = np.clip(f_ditw, 0.0, 1.0)

    # k_use
    with np.errstate(divide="ignore", invalid="ignore"):
        k_use_day = f_wta * (1.0 - f_ditw) * k_adv_day * (1.0 - f_soil)

    # tau
    denom = k_adv_day + k_ret_day + k_use_day
    with np.errstate(divide="ignore", invalid="ignore"):
        tau_day = np.where(denom > 0.0, 1.0 / denom, np.nan)

    # Build output dataset
    out = xr.Dataset(coords={"lat": ds_grid["lat"], "lon": ds_grid["lon"]})
    out["grid_id"] = ds_grid["grid_id"]
    out["in_china"] = ds_grid["in_china"]

    def put(name: str, values: np.ndarray, dtype=np.float32) -> None:
        s = pd.Series(values, index=gid_index)
        arr = _scatter_to_grid(grid_shape=grid_shape, gid_to_flat=gid_to_flat, values_by_gid=s, dtype=dtype, fill=np.nan)
        out[name] = (("lat", "lon"), arr)
        out[name] = out[name].where(in_china)

    # Keep legacy names but base them on Stage-C Q
    put("q_cell_cms", q_cell_cms, np.float32)
    put("q_best_cms", q_cell_cms, np.float32)
    put("q_river_main_cms", q_river_main_cms, np.float32)
    put("q_lake_disavg_cms", q_lake_disavg_cms, np.float32)
    put("q_cell_km3_per_day", q_km3_day, np.float32)
    put("q_cell_km3_per_year", q_km3_yr, np.float32)

    put("river_length_km_in_cell", df_all["river_length_km_in_cell"].to_numpy(dtype=np.float64), np.float32)
    put("river_width_m_main", w_main_m, np.float32)
    put("river_depth_m_main", d_main_m, np.float32)

    put("cell_area_km2", cell_area_km2, np.float32)

    put("v_river_km3", v_riv_km3, np.float32)
    put("waterbody_area_km2_in_cell", a_wb_km2, np.float32)
    put("v_waterbody_km3_in_cell", v_wb_km3, np.float32)
    put("v_lake_km3_in_cell", v_lake_km3, np.float32)
    put("v_reservoir_km3_in_cell", v_res_km3, np.float32)
    put("v_tot_km3", v_tot_km3, np.float32)

    # Diagnostics from HydroLAKES (not used in main equations directly)
    put("hydrolakes_res_time_day_wmean", df_all["res_time_day_wmean"].to_numpy(dtype=np.float64), np.float32)

    put("k_adv_day", k_adv_day, np.float32)
    put("k_ret_day", k_ret_day, np.float32)
    put("k_use_day", k_use_day, np.float32)
    put("tau_day", tau_day, np.float32)

    put("runoff_m_per_year", runoff_m_yr, np.float32)
    put("f_dip", f_dip, np.float32)
    put("f_dop", f_dop, np.float32)
    put("f_soil", f_soil, np.float32)

    put("f_wta", f_wta, np.float32)
    put("f_ditw", f_ditw, np.float32)

    out.attrs.update(
        {
            "method": "Helmes et al. (2012) freshwater P fate (grid k parameters)",
            "notes": "D stage: k_adv/k_ret/k_use/tau computed using Stage-C hydro/geometry as authoritative inputs; f_soil excludes particulate P.",
            "constants_aw": AW,
            "constants_bw": BW,
            "constants_ad": AD,
            "constants_bd": BD,
            "vf_km_per_day": VF_KM_PER_DAY,
            "kriv_q1_km3_per_year": KRIV_Q1,
            "kriv_q2_km3_per_year": KRIV_Q2,
            "kriv_low_yr_inv": KRIV_LOW,
            "kriv_mid_yr_inv": KRIV_MID,
            "kriv_high_yr_inv": KRIV_HIGH,
            "inputs_grid_nc": str(grid_path),
            "inputs_grid_parquet": str(Path(args.grid_parquet)),
            "inputs_hydro_geom_nc": str(hg_path),
            "inputs_hydrorivers_map": str(Path(args.hydrorivers_map)),
            "inputs_hydrolakes_map": str(Path(args.hydrolakes_map)),
            "inputs_basinatlas_map": str(Path(args.basinatlas_map)),
            "inputs_hswud": str(Path(args.hswud)),
            "v_tot_min_km3_for_rates": float(V_TOT_MIN_KM3_FOR_RATES),
            "n_cells_masked_due_to_tiny_v_tot": n_vtot_masked,
        }
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_netcdf(out_path)
    print(f"Wrote: {out_path}")

    ds_hg.close()


if __name__ == "__main__":
    main()
