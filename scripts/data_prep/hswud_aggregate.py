"""Aggregate HSWUD NetCDF water use data to annual 0.1° grid totals.

This script reads the four HSWUD sectoral NetCDF files (domestic, electricity,
irrigation, manufacturing), harmonises units to m^3/year, aggregates over time
(either a single year or a multi-year mean), and writes a flattened
lat/lon grid table to Parquet for downstream modelling.

Inputs (expected paths, can be overridden by CLI args):
- data/water use data/27610524/HSWUD_dom.nc
- data/water use data/27610524/HSWUD_ele.nc
- data/water use data/27610524/HSWUD_irr_.nc
- data/water use data/27610524/HSWUD_manu.nc

Output:
- data/processed/water_use/hswud_0p1_annual.parquet

Time handling strategy:
- mode="single_year": extract a specific year and sum monthly values to annual.
- mode="multi_year_mean": average over a year range (e.g. 2010–2020) to get a
  representative annual volume.

Note: For now we keep lat/lon as explicit columns and do not assign a grid_id.
      A consistent grid_id scheme can be joined later.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import xarray as xr


DATA_ROOT = Path("data")
RAW_WATER_USE_DIR = DATA_ROOT / "water use data" / "27610524"
PROCESSED_DIR = DATA_ROOT / "processed" / "water_use"


@dataclass
class HSWUDConfig:
    """Configuration for HSWUD aggregation.

    Attributes
    ----------
    start_year : int
        Start year for aggregation (inclusive).
    end_year : int
        End year for aggregation (inclusive). Ignored in single_year mode.
    mode : str
        Either "single_year" or "multi_year_mean".
    overwrite : bool
        Whether to overwrite existing output file.
    """

    start_year: int
    end_year: int
    mode: str = "multi_year_mean"
    overwrite: bool = False


SECTOR_FILES: Dict[str, str] = {
    "dom": "HSWUD_dom.nc",
    "ele": "HSWUD_ele.nc",
    "irr": "HSWUD_irr_.nc",
    "manu": "HSWUD_manu.nc",
}


def _select_time_range(ds: xr.Dataset, cfg: HSWUDConfig) -> xr.Dataset:
    """Subset dataset to the requested time range and aggregate over time.

    Assumes `time` coordinate is datetime-like or convertible to year.
    """

    if "time" not in ds.dims and "time" not in ds.coords:
        raise ValueError("HSWUD dataset has no 'time' dimension/coord")

    # Ensure we have a datetime-like time coordinate
    if not pd.api.types.is_datetime64_any_dtype(ds["time"].dtype):
        ds["time"] = xr.conventions.times.decode_cf_datetime(
            ds["time"], ds["time"].attrs.get("units", None)
        )

    years = ds["time"].dt.year
    if cfg.mode == "single_year":
        mask = years == cfg.start_year
    else:  # multi_year_mean
        mask = (years >= cfg.start_year) & (years <= cfg.end_year)

    ds_sel = ds.sel(time=mask)

    if ds_sel.sizes.get("time", 0) == 0:
        raise ValueError(
            f"No time steps found in requested range {cfg.start_year}-{cfg.end_year}"
        )

    # Aggregate to annual volume: if data are monthly volumes, sum over time;
    # if they are monthly rates, user should adapt logic here later.
    return ds_sel.sum(dim="time", keep_attrs=True)


def _harmonise_units_to_m3_per_year(
    ds: xr.Dataset, var_name: str, sector: str
) -> xr.DataArray:
        """Return a DataArray in m^3/year, with explicit 10^8 m³ handling and
        conservative outlier masking.

        Assumptions (agreed with user and consistent with metadata):
        - All four HSWUD sector files store **annual/period volumes in units of
            10^8 m³ per grid cell per time step**. 这在 dom/irr/manu 的 units 中
            明确写出，对 ele 则由数值范围和文档推断。

        Best-effort data cleaning (avoid arbitrary surgery):
        - Respect `_FillValue` / `missing_value` attributes by masking它们为 NaN；
        - 另外，一些文件把“无数据”编码成极端的最小浮点数（例如 -1.7e308,
            -3.4e38, -3.4e39），但没有写成 `_FillValue`。我们使用一个非常宽松的
            物理下限阈值，将“小于 -1e20 的值视为无效”（mask 为 NaN）。
            这样不会触及任何合理的用水量，但可以去掉这些显然非物理值，避免
            溢出和 -inf。

        单位转换规则：
        - 先完成缺失值和极端负值掩蔽；
        - 然后统一按 10^8 m³ → m³：全部乘以 1e8；
        - 最终 attrs["units"] 统一设为 "m3/year"。
        """

        if var_name not in ds.data_vars:
            # Fall back: try the first data variable
            if len(ds.data_vars) != 1:
                raise ValueError(
                    f"Variable '{var_name}' not found and dataset has multiple variables: {list(ds.data_vars)}"
                )
            var_name = list(ds.data_vars)[0]

        da = ds[var_name].astype("float64")

        # 1) Mask fill values / missing values before scaling to avoid inf/-inf
        fill_value = da.attrs.get("_FillValue")
        missing_value = da.attrs.get("missing_value")
        if fill_value is not None:
            da = da.where(da != fill_value)
        if missing_value is not None:
            da = da.where(da != missing_value)

        # 2) Mask 极端负值：典型的无数据编码为 -1.7e308, -3.4e38 等
        EXTREME_NEG_THRESHOLD = -1e20
        da = da.where(da >= EXTREME_NEG_THRESHOLD)

        # 3) 统一单位转换：10^8 m³ → m³
        da_converted = da * 1e8
        da_converted.attrs["units"] = "m3/year"
        return da_converted


def aggregate_hswud(cfg: HSWUDConfig) -> pd.DataFrame:
    """Aggregate all HSWUD sectors to an annual lat/lon table.

    Returns a DataFrame with columns: lat, lon, q_dom_m3, q_ele_m3,
    q_irr_m3, q_manu_m3, q_total_m3.
    """

    sector_arrays: Dict[str, xr.DataArray] = {}

    for sector, fname in SECTOR_FILES.items():
        path = RAW_WATER_USE_DIR / fname
        if not path.exists():
            raise FileNotFoundError(path)

        ds = xr.open_dataset(path)

        # Use the first data variable name as default
        var_name = list(ds.data_vars)[0] if ds.data_vars else None
        if var_name is None:
            raise ValueError(f"No data variables found in {path}")

        ds_agg = _select_time_range(ds, cfg)
        da_m3_year = _harmonise_units_to_m3_per_year(ds_agg, var_name, sector)

        # Replace NaNs with 0 (assume no data == no use)
        da_m3_year = da_m3_year.fillna(0.0)

        sector_arrays[sector] = da_m3_year

    # Align all sectors on common lat/lon grid
    # Start from one sector as reference
    ref = next(iter(sector_arrays.values()))

    # Build a new Dataset combining all sectors
    ds_combined = xr.Dataset(
        {
            f"q_{sector}_m3": da.broadcast_like(ref)
            for sector, da in sector_arrays.items()
        }
    )

    # Compute total
    ds_combined["q_total_m3"] = sum(
        ds_combined[f"q_{sector}_m3"] for sector in sector_arrays.keys()
    )

    # Flatten to DataFrame
    df = ds_combined.to_dataframe().reset_index()

    # Keep only lat/lon and value columns, drop all-zero rows to save space
    value_cols = [
        f"q_{sector}_m3" for sector in sector_arrays.keys()
    ] + ["q_total_m3"]
    keep_cols = [col for col in ["lat", "lon"] if col in df.columns] + value_cols

    df = df[keep_cols]

    # Drop rows where all sectoral volumes and total are zero
    df = df[df[value_cols].sum(axis=1) != 0]

    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate HSWUD NetCDF to annual Parquet table.")
    parser.add_argument("--start-year", type=int, default=2010, help="Start year (inclusive) for aggregation.")
    parser.add_argument("--end-year", type=int, default=2020, help="End year (inclusive) for aggregation (multi_year_mean mode).")
    parser.add_argument(
        "--mode",
        choices=["single_year", "multi_year_mean"],
        default="multi_year_mean",
        help="Aggregation mode: one year or multi-year mean.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROCESSED_DIR / "hswud_0p1_annual.parquet",
        help="Output Parquet file path.",
    )
    parser.add_argument(
        "--output-nc",
        type=Path,
        default=None,
        help="Optional output NetCDF file path (lat, lon, time, sectoral water use). If not provided, no NetCDF is written.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output file if it exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    cfg = HSWUDConfig(
        start_year=args.start_year,
        end_year=args.end_year,
        mode=args.mode,
        overwrite=args.overwrite,
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_path: Path = args.output
    if output_path.exists() and not cfg.overwrite:
        raise FileExistsError(f"Output file already exists: {output_path}. Use --overwrite to replace it.")

    df = aggregate_hswud(cfg)

    # Write to Parquet (flattened lat/lon table)
    df.to_parquet(output_path, index=False)
    print(f"Wrote {len(df)} rows to {output_path}")

    # Optionally also write a NetCDF file with lat, lon, time and sectoral water use
    if args.output_nc is not None:
        output_nc: Path = args.output_nc
        if output_nc.exists() and not cfg.overwrite:
            raise FileExistsError(f"Output NetCDF file already exists: {output_nc}. Use --overwrite to replace it.")

        # Reconstruct lat/lon grid and a singleton time dimension for the aggregated period
        # Assumes df contains unique combinations of lat, lon representing a regular grid
        ds_nc = (
            df.set_index(["lat", "lon"])
            .to_xarray()
        )

        # 添加时间维度：用聚合区间代表年份（例如 2010-2020 多年平均）
        import pandas as _pd

        if cfg.mode == "single_year":
            time_label = _pd.Timestamp(int(cfg.start_year), 1, 1)
        else:
            # 多年平均：用中间年份或区间标签
            mid_year = (cfg.start_year + cfg.end_year) // 2
            time_label = _pd.Timestamp(int(mid_year), 1, 1)

        ds_nc = ds_nc.expand_dims({"time": [time_label]})

        # 写出 NetCDF 文件
        ds_nc.to_netcdf(output_nc)
        print(f"Wrote NetCDF to {output_nc}")


if __name__ == "__main__":
    main()
