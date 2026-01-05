"""Compute grid-level fate factor (FF) and (optional) CF by downstream recursion.

Implements Stage E in materials/action_plan.md:
  FF_i = sum_j f_{i,j} * tau_j

Given a single-downstream-pointer river network, f_{i,j} becomes the product of
cell-to-cell advective transfer fractions along the unique downstream path.
Under a well-mixed, first-order removal model for each cell:
  transfer fraction (cell -> next) = k_adv / (k_adv + k_ret + k_use)
  tau = 1 / (k_adv + k_ret + k_use)

This script computes, for each grid cell i:
  - ff_day: sum_{j downstream including i} tau_j * prod_{p along path i->j-1} f_p
  - export_frac_to_outlet: prod_{p along path i->outlet} f_p
  - steps_to_outlet: number of cells on the downstream path (including i)

CF requires an effect factor (EF). Since EF is not yet parameterized in this repo,
we provide an optional scalar --effect-factor and output:
  cf = ff_day * effect_factor

Outputs a NetCDF with (lat, lon) variables.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


DEFAULT_GRID_NC = Path("data/processed/grid_0p1/grid_cells_china_0p1.nc")
DEFAULT_TOPO_NC = Path("data/processed/grid_0p1/grid_topology_china_0p1.nc")
DEFAULT_K_NC = Path("data/processed/grid_0p1/grid_k_params_china_0p1.nc")
DEFAULT_OUT = Path("data/processed/grid_0p1/grid_ff_cf_china_0p1.nc")


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


def _scatter_flat_to_grid(
    *,
    grid_shape: tuple[int, int],
    flat_values: np.ndarray,
    fill: float | int | bool | np.number,
    dtype: object,
) -> np.ndarray:
    out = np.full((grid_shape[0] * grid_shape[1],), fill, dtype=dtype)
    if flat_values.shape[0] != out.shape[0]:
        raise ValueError("flat_values must have length lat*lon")
    out[:] = flat_values.astype(dtype, copy=False)
    return out.reshape(grid_shape)


def _compute_transfer_fraction(
    k_adv_day: np.ndarray,
    k_ret_day: np.ndarray,
    k_use_day: np.ndarray,
) -> np.ndarray:
    denom = k_adv_day + k_ret_day + k_use_day
    with np.errstate(divide="ignore", invalid="ignore"):
        f = np.where(np.isfinite(denom) & (denom > 0.0), k_adv_day / denom, np.nan)
    # keep within [0,1] when numeric
    f = np.where(np.isfinite(f), np.clip(f, 0.0, 1.0), np.nan)
    return f


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage E: compute FF/CF by downstream recursion on 0.1° grid")
    parser.add_argument("--grid-nc", type=str, default=str(DEFAULT_GRID_NC))
    parser.add_argument("--topology-nc", type=str, default=str(DEFAULT_TOPO_NC))
    parser.add_argument("--k-params-nc", type=str, default=str(DEFAULT_K_NC))
    parser.add_argument(
        "--pointer",
        type=str,
        default="hydrorivers",
        choices=["hydrorivers", "riveratlas"],
        help="Which downstream pointer to use from the topology NetCDF",
    )
    parser.add_argument(
        "--effect-factor",
        type=float,
        default=1.0,
        help="Scalar effect factor (EF) applied as CF = FF * EF. Default 1.0 (i.e., CF==FF).",
    )
    parser.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    args = parser.parse_args()

    grid_path = Path(args.grid_nc)
    topo_path = Path(args.topology_nc)
    k_path = Path(args.k_params_nc)

    ds_grid = xr.open_dataset(grid_path)
    _validate_grid_base(ds_grid)

    ds_topo = xr.open_dataset(topo_path)
    ds_k = xr.open_dataset(k_path)

    grid_shape = ds_grid["grid_id"].shape
    for ds, label in [(ds_topo, "topology"), (ds_k, "k_params")]:
        if ds["grid_id"].shape != grid_shape:
            raise ValueError(f"{label} grid shape mismatch: {ds['grid_id'].shape} vs {grid_shape}")

    in_china = ds_grid["in_china"].to_numpy().astype(bool)
    flat_in_china = in_china.reshape(-1)

    gid_to_flat = _build_gid_to_flat_index(ds_grid["grid_id"].to_numpy())

    next_gid_var = f"{args.pointer}_next_grid_id"
    if next_gid_var not in ds_topo:
        raise KeyError(f"Topology missing downstream pointer: {next_gid_var}")

    flat_grid_id = ds_grid["grid_id"].to_numpy().reshape(-1).astype(np.int64)
    flat_next_gid = ds_topo[next_gid_var].to_numpy().reshape(-1).astype(np.int64)

    # Build flat downstream index pointer for all cells
    n_flat = flat_grid_id.size
    next_flat = np.full((n_flat,), -1, dtype=np.int64)

    gid_to_flat_dict = {int(g): int(i) for g, i in zip(gid_to_flat.index.to_numpy(), gid_to_flat.to_numpy())}
    for i in range(n_flat):
        gid = int(flat_grid_id[i])
        if gid == -1:
            continue
        ngid = int(flat_next_gid[i])
        nxt = gid_to_flat_dict.get(ngid, -1)
        next_flat[i] = nxt

    # Load k/tau and compute transfer fraction
    for v in ["k_adv_day", "k_ret_day", "k_use_day", "tau_day"]:
        if v not in ds_k:
            raise KeyError(f"k_params NetCDF missing variable: {v}")

    k_adv = ds_k["k_adv_day"].to_numpy().reshape(-1).astype(np.float64)
    k_ret = ds_k["k_ret_day"].to_numpy().reshape(-1).astype(np.float64)
    k_use = ds_k["k_use_day"].to_numpy().reshape(-1).astype(np.float64)
    tau = ds_k["tau_day"].to_numpy().reshape(-1).astype(np.float64)

    f_trans = _compute_transfer_fraction(k_adv, k_ret, k_use)

    # Restrict computation domain: valid & in_china
    valid = (flat_grid_id != -1) & flat_in_china

    ff = np.full((n_flat,), np.nan, dtype=np.float64)
    export_frac = np.full((n_flat,), np.nan, dtype=np.float64)
    steps = np.zeros((n_flat,), dtype=np.int32)
    cycle_break = np.zeros((n_flat,), dtype=bool)

    state = np.zeros((n_flat,), dtype=np.uint8)  # 0=unvisited,1=visiting,2=done

    def solve(start: int) -> None:
        stack: list[int] = [start]
        while stack:
            i = stack[-1]
            if not valid[i]:
                state[i] = 2
                stack.pop()
                continue

            if state[i] == 2:
                stack.pop()
                continue

            if state[i] == 0:
                state[i] = 1

            j = int(next_flat[i])
            if j != -1 and valid[j] and state[j] == 0:
                stack.append(j)
                continue

            if j != -1 and valid[j] and state[j] == 1:
                # Found a cycle; break it at i (local cut)
                cycle_break[i] = True
                next_flat[i] = -1
                j = -1

            # downstream values
            if j != -1 and valid[j] and state[j] == 2:
                ff_next = ff[j]
                export_next = export_frac[j]
                steps_next = steps[j]
            else:
                ff_next = 0.0
                export_next = 1.0
                steps_next = 0

            tau_i = tau[i]
            f_i = f_trans[i]

            if np.isfinite(tau_i) and np.isfinite(f_i):
                ff[i] = tau_i + f_i * ff_next
                export_frac[i] = f_i * export_next
                steps[i] = 1 + int(steps_next)
            else:
                ff[i] = np.nan
                export_frac[i] = np.nan
                steps[i] = 0

            state[i] = 2
            stack.pop()

    # Solve for all valid nodes
    valid_indices = np.nonzero(valid)[0]
    for idx in valid_indices:
        if state[idx] == 0:
            solve(int(idx))

    n_cycles = int(cycle_break[valid].sum())

    cf = ff * float(args.effect_factor)

    out = xr.Dataset(coords={"lat": ds_grid["lat"], "lon": ds_grid["lon"]})
    out["grid_id"] = ds_grid["grid_id"]
    out["in_china"] = ds_grid["in_china"]

    out["downstream_grid_id"] = (
        ("lat", "lon"),
        _scatter_flat_to_grid(grid_shape=grid_shape, flat_values=flat_next_gid, fill=-1, dtype=np.int32),
    )

    out["f_transfer"] = (
        ("lat", "lon"),
        _scatter_flat_to_grid(grid_shape=grid_shape, flat_values=f_trans, fill=np.nan, dtype=np.float32),
    )
    out["ff_day"] = (
        ("lat", "lon"),
        _scatter_flat_to_grid(grid_shape=grid_shape, flat_values=ff, fill=np.nan, dtype=np.float32),
    )
    out["export_frac_to_outlet"] = (
        ("lat", "lon"),
        _scatter_flat_to_grid(grid_shape=grid_shape, flat_values=export_frac, fill=np.nan, dtype=np.float32),
    )
    out["steps_to_outlet"] = (
        ("lat", "lon"),
        _scatter_flat_to_grid(grid_shape=grid_shape, flat_values=steps, fill=0, dtype=np.int32),
    )
    out["cycle_break_flag"] = (
        ("lat", "lon"),
        _scatter_flat_to_grid(grid_shape=grid_shape, flat_values=cycle_break.astype(np.int8), fill=0, dtype=np.int8),
    )

    out["cf"] = (
        ("lat", "lon"),
        _scatter_flat_to_grid(grid_shape=grid_shape, flat_values=cf, fill=np.nan, dtype=np.float32),
    )

    # Mask outside China
    for v in [
        "downstream_grid_id",
        "f_transfer",
        "ff_day",
        "export_frac_to_outlet",
        "steps_to_outlet",
        "cycle_break_flag",
        "cf",
    ]:
        out[v] = out[v].where(out["in_china"])

    out.attrs.update(
        {
            "method": "Stage E: downstream recursion on single-pointer river network",
            "definition_ff": "FF_i = sum_j f_{i,j} * tau_j with f_{i,j}=product of per-cell transfer fractions along unique downstream path",
            "transfer_fraction": "f = k_adv / (k_adv + k_ret + k_use)",
            "cf_definition": "cf = ff_day * effect_factor (scalar)",
            "effect_factor": float(args.effect_factor),
            "pointer_variable": next_gid_var,
            "n_cycle_breaks": n_cycles,
            "inputs_grid_nc": str(grid_path),
            "inputs_topology_nc": str(topo_path),
            "inputs_k_params_nc": str(k_path),
        }
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_netcdf(out_path)
    print(f"Wrote: {out_path}")

    ds_grid.close()
    ds_topo.close()
    ds_k.close()


if __name__ == "__main__":
    main()
