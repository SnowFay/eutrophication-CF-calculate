"""Skeleton script to compute grid-level f_WTA from HSWUD and available water.

This is an initial structure only. It:
- loads the cleaned 2010–2020 mean HSWUD grid table;
- expects (in the future) a grid-level table of available water resources;
- merges them by lat/lon (or grid_id, once defined);
- computes a placeholder f_WTA as q_total_m3 / q_available_m3.

At this stage, q_available_m3 is not yet defined; the script includes a
stub and clear TODOs so that the hydrology input can be wired in later.

Usage (once q_available_m3 is available):

    python -m scripts.modeling.compute_f_wta
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

DATA_ROOT = Path("data")
PROCESSED_WATER_USE = DATA_ROOT / "processed" / "water_use" / "hswud_0p1_2010_2020_mean_clean.parquet"

# Placeholder for future available water resource table
# For example: per-grid annual renewable water availability in m3/year
AVAILABLE_WATER_TABLE = DATA_ROOT / "processed" / "hydrology" / "grid_0p1_available_water_m3_per_year.parquet"
OUTPUT_F_WTA = DATA_ROOT / "processed" / "water_use" / "f_wta_0p1_2010_2020.parquet"


def load_hswud() -> pd.DataFrame:
    """Load cleaned HSWUD grid table and ensure non-negative water use."""

    if not PROCESSED_WATER_USE.exists():
        raise FileNotFoundError(PROCESSED_WATER_USE)

    df = pd.read_parquet(PROCESSED_WATER_USE)
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


def load_available_water(strict: bool = False) -> Optional[pd.DataFrame]:
    """Load grid-level available water table if present.

    The expected schema (to be implemented later) is roughly:
    - lat, lon (or grid_id)
    - q_available_m3: annual available freshwater volume in m3/year

    For now, this function can return None if the file is not yet prepared.
    """

    if not AVAILABLE_WATER_TABLE.exists():
        if strict:
            raise FileNotFoundError(AVAILABLE_WATER_TABLE)
        print(
            f"[INFO] Available water table not found at {AVAILABLE_WATER_TABLE}.\n"
            "       Please prepare this file (per-grid q_available_m3) before computing f_WTA."
        )
        return None

    df = pd.read_parquet(AVAILABLE_WATER_TABLE)
    if "q_available_m3" not in df.columns:
        raise ValueError("Expected column 'q_available_m3' in available water table.")
    return df


def compute_f_wta(df_hswud: pd.DataFrame, df_avail: pd.DataFrame) -> pd.DataFrame:
    """Compute f_WTA on the grid, given HSWUD and available water.

    f_WTA_total = q_total_m3 / q_available_m3

    In the future, sector-specific f_WTA (dom/ele/irr/manu) can also be
    computed in the same way.
    """

    # Merge on lat/lon for now; later we may switch to grid_id
    merge_keys = [k for k in ["lat", "lon"] if k in df_hswud.columns and k in df_avail.columns]
    if not merge_keys:
        raise ValueError("No common keys to merge HSWUD and available water tables (expected lat/lon or grid_id).")

    df = df_hswud.merge(df_avail, on=merge_keys, how="inner")

    # Basic sanity: avoid division by zero
    df["q_available_m3"] = df["q_available_m3"].clip(lower=1e-6)

    df["f_wta_total"] = df["q_total_m3"] / df["q_available_m3"]

    # Optional: clip extreme f_WTA for stability (e.g., > 1e3)
    # df["f_wta_total"] = df["f_wta_total"].clip(upper=1e3)

    return df


def main() -> None:
    df_hswud = load_hswud()
    df_avail = load_available_water(strict=False)

    if df_avail is None:
        print("[WARN] Available water table not found; f_WTA cannot be computed yet.")
        print("       Once you have per-grid q_available_m3, place it at:")
        print(f"           {AVAILABLE_WATER_TABLE}")
        print("       with at least columns: ['lat', 'lon', 'q_available_m3'].")
        return

    df_f_wta = compute_f_wta(df_hswud, df_avail)

    OUTPUT_F_WTA.parent.mkdir(parents=True, exist_ok=True)
    df_f_wta.to_parquet(OUTPUT_F_WTA, index=False)
    print(f"Wrote f_WTA table to {OUTPUT_F_WTA} with {len(df_f_wta)} rows.")


if __name__ == "__main__":
    main()
