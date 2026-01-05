"""Convert HSWUD multi-year mean from m3/year to m3/day.

Reads the cleaned multi-year mean HSWUD table and NetCDF and writes
new versions with variables expressed in m3/day. This is useful for
combining with daily-based residence times or rate constants.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import xarray as xr


DATA_ROOT = Path("data")
PROCESSED_DIR = DATA_ROOT / "processed" / "water_use"

INPUT_PARQUET = PROCESSED_DIR / "hswud_0p1_2010_2020_mean_clean.parquet"
INPUT_NC = PROCESSED_DIR / "hswud_0p1_2010_2020_mean_clean.nc"

OUTPUT_PARQUET = PROCESSED_DIR / "hswud_0p1_2010_2020_mean_clean_m3_per_day.parquet"
OUTPUT_NC = PROCESSED_DIR / "hswud_0p1_2010_2020_mean_clean_m3_per_day.nc"

# Columns in the Parquet file that are currently in m3/year
YEARLY_COLS = [
    "q_dom_m3",
    "q_ele_m3",
    "q_irr_m3",
    "q_manu_m3",
    "q_total_m3",
]

DAYS_PER_YEAR = 365.0


def convert_parquet_to_m3_per_day() -> None:
    if not INPUT_PARQUET.exists():
        raise FileNotFoundError(f"HSWUD Parquet not found: {INPUT_PARQUET}")

    print(f"Reading yearly HSWUD parquet from: {INPUT_PARQUET}")
    df = pd.read_parquet(INPUT_PARQUET)

    missing = [c for c in YEARLY_COLS if c not in df.columns]
    if missing:
        raise KeyError(f"Missing expected yearly columns in HSWUD parquet: {missing}")

    for col in YEARLY_COLS:
        new_col = col.replace("_m3", "_m3_per_day")
        df[new_col] = df[col] / DAYS_PER_YEAR

    print("New daily columns added:", [c for c in df.columns if c.endswith("_m3_per_day")])

    print(f"Writing daily HSWUD parquet to: {OUTPUT_PARQUET}")
    df.to_parquet(OUTPUT_PARQUET, index=False)
    print("Done.")


def convert_nc_to_m3_per_day() -> None:
    if not INPUT_NC.exists():
        raise FileNotFoundError(f"HSWUD NetCDF not found: {INPUT_NC}")

    print(f"Reading yearly HSWUD NetCDF from: {INPUT_NC}")
    ds = xr.open_dataset(INPUT_NC)

    # For safety, only convert variables that match the expected yearly names
    for var in YEARLY_COLS:
        if var in ds.data_vars:
            new_name = var.replace("_m3", "_m3_per_day")
            ds[new_name] = ds[var] / DAYS_PER_YEAR
            ds[new_name].attrs["units"] = "m3/day"

    print("New daily variables added:", [v for v in ds.data_vars if v.endswith("_m3_per_day")])

    print(f"Writing daily HSWUD NetCDF to: {OUTPUT_NC}")
    ds.to_netcdf(OUTPUT_NC)
    print("Done.")


def main() -> None:
    convert_parquet_to_m3_per_day()
    convert_nc_to_m3_per_day()


if __name__ == "__main__":
    main()
