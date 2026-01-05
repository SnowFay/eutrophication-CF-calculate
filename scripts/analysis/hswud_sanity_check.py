"""Sanity check for aggregated HSWUD water use totals.

This script loads the cleaned 2010–2020 mean HSWUD grid table and reports
basic totals (national-level order of magnitude) for each sector and the
combined total, in both m3/year and km3/year.

Usage:
    python -m scripts.analysis.hswud_sanity_check
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_ROOT = Path("data")
PROCESSED_WATER_USE = DATA_ROOT / "processed" / "water_use" / "hswud_0p1_2010_2020_mean_clean.parquet"


def load_hswud() -> pd.DataFrame:
    if not PROCESSED_WATER_USE.exists():
        raise FileNotFoundError(PROCESSED_WATER_USE)
    df = pd.read_parquet(PROCESSED_WATER_USE)
    # safety: clip to non-negative
    for col in [
        "q_dom_m3",
        "q_ele_m3",
        "q_irr_m3",
        "q_manu_m3",
        "q_total_m3",
    ]:
        if col in df.columns:
            df[col] = df[col].clip(lower=0.0)
    return df


def main() -> None:
    df = load_hswud()

    print("Loaded HSWUD grid table:")
    print("  rows:", len(df))
    print("  columns:", list(df.columns))

    sectors = ["dom", "ele", "irr", "manu", "total"]
    print("\nTotal annual water use (2010–2020 mean, national sum):")
    for s in sectors:
        col = f"q_{s}_m3" if s != "total" else "q_total_m3"
        if col not in df.columns:
            continue
        total_m3 = float(df[col].sum())
        total_km3 = total_m3 / 1e9
        print(f"  {s:5s}: {total_m3: .3e} m3/yr  ({total_km3: .3f} km3/yr)")


if __name__ == "__main__":
    main()
