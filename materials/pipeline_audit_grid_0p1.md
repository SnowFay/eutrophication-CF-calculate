# 0.1° 网格 CF 计算链路审计（B→C→D→E）

本文档回答四个问题：
1) 我们目前算出来的结果“是不是对的”（逐步、逐参数、逐数据源说明）。
2) 在“数据与参数口径正确”的前提下，结果的科学合理性/主要不确定性来源。
3) 在结果逻辑正确的情况下，哪些环节能提升精度。
4) 如何从结果角度进行验证（说服别人）。

## 一、总览：当前计算在算什么

目标：在中国 0.1° 规则网格上输出淡水系统中“单下游路径”的 Fate Factor（FF，day），并为后续 CF（CF = FF × EF）提供底座。

核心数学对象：
- **网格拓扑**：每个网格单元 i 有一个下游指针 `next(i)`（或无下游/出界）。上游可以有多个。
- **一阶过程速率**（day⁻¹）：`k_adv`, `k_ret`, `k_use`。
- **停留时间**（day）：`tau = 1/(k_adv+k_ret+k_use)`。
- **传输分数**：`f = k_adv/(k_adv+k_ret+k_use)`。
- **FF 递推**：`FF_i = tau_i + f_i * FF_next(i)`（单下游指针的特例）。

## 二、Stage B（映射与拓扑底座）

### B1. “无损映射”表（parquet）
我们采用“网格主表 + 每数据集 mapping parquet”的模式：
- 网格主表：data/processed/grid_0p1/grid_cells_china_0p1.nc（以及 parquet 版本用于几何/面积）
- 河流映射：data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet
- 湖库映射：data/processed/grid_0p1/grid_hydrolakes_china_0p1_mapping.parquet
- 流域属性映射：data/processed/grid_0p1/grid_basinatlas_lev10_china_0p1_mapping.parquet
- 其他（如 RiverATLAS）：data/processed/grid_0p1/grid_riveratlas_china_0p1_mapping.parquet

映射表原则：一行 = (grid_id × feature_id 的相交记录)，保留原始字段 + overlap 指标（长度/面积/比例）。

### B2. 网格拓扑（NetCDF）
- 文件：data/processed/grid_0p1/grid_topology_china_0p1.nc
- 关键变量：`hydrorivers_next_grid_id`（以及可能存在的 `riveratlas_next_grid_id`）
- 目标拓扑形态：**single-downstream**（每格最多一个下游），允许多上游。

重要说明：该拓扑并不是严格意义的 DEM-D8（D8 约束“下游只能是 8 邻格之一”）。我们采用的是“河网驱动的单下游指针”，下游网格不必是 8 邻格。

已做过的关键修复：
- self-loop：当主河段下游仍落在同一网格时，沿河段 `NEXT_DOWN` 继续追踪直到离开本网格，避免网格级自环。

## 三、Stage C：水文年与几何量（grid_hydro_geom）

- 脚本：scripts/modeling/compute_hydro_geom_grid_0p1.py
- 输出：data/processed/grid_0p1/grid_hydro_geom_china_0p1.nc
- 目的：统一口径生成后续 D/E 所需的权威水文/几何输入。

### C1. 输入数据与对齐
- 网格：grid_cells_china_0p1.nc（`grid_id`, `in_china`, lat/lon 2D）
- 网格几何：grid_cells_china_0p1.parquet（用于投影到 EPSG:6933 计算 `cell_area_km2`）
- 拓扑：grid_topology_china_0p1.nc（用于 runoff 累积得到 `q_accum_runoff_cms`）
- HydroRIVERS mapping：用于 `q_hydrorivers_main_cms` 和 `river_length_km_in_cell` 以及河流体积
- BasinATLAS + RiverATLAS mapping：用于 `runoff_m_per_year`（优先 BasinATLAS `run_mm_syr`，fallback RiverATLAS `run_mm_cyr`）
- HydroLAKES mapping：用于 `waterbody_area_km2_in_cell` 与水体体积拆分

“对齐”是通过 `grid_id` 完成的：所有 mapping 表都包含 `grid_id`，再散射到 (lat, lon)。

### C2. 关键计算与参数
1) **径流深（m/yr）**
- 对 BasinATLAS 的 `run_mm_syr`（mm/yr）按 overlap_area_km2 做面积加权平均 → `runoff_m_per_year`。

2) **局地径流量与累积流量**
- `q_local_runoff_cms = runoff_m_per_year * cell_area_m2 / seconds_per_year`
- 沿 `hydrorivers_next_grid_id` 做单下游累积 → `q_accum_runoff_cms`
- 如存在 cycles，会做 cycle-breaking 使累积定义稳定，并在 attrs 记录 `remaining_cycle_nodes`。

3) **河道流量（来自 HydroRIVERS）**
- 每格选择 overlap_length_km 最大的河段作为主河段 → `q_hydrorivers_main_cms`。

4) **最优流量口径**
- `q_best_cms`：优先 HydroRIVERS 主河段流量；否则使用 runoff 累积流量。
- `q_source`：0/1/2 标记来源。

5) **河道几何与河流体积**
- 采用 Wollheim (2006) 幂律从 Q 推宽度/深度（脚本内常数 AW,BW,AD,BD）。
- 河流体积两种来源：
  - “segment-based”：按每个 overlap 片段的 Q 推 W/D，再乘 overlap_length 得段体积并汇总。
  - fallback：用 `q_best` 推 W/D，再乘格内总河长。

6) **湖库面积与体积拆分（重要单位口径）**
- HydroLAKES TechDoc：`Vol_total`, `Vol_res` 单位为 mcm（百万立方米），1 mcm = 0.001 km³。
- 脚本实现：MCM_TO_KM3 = 1e-3，将 mcm 转 km³后再按面积分数分配到网格。
- 体积分量：
  - `v_waterbody_km3_in_cell`（总水体体积）
  - `v_reservoir_km3_in_cell`
  - `v_lake_km3_in_cell = max(Vol_total-Vol_res,0)`

7) **总淡水体积**
- `v_tot_km3 = v_river_km3 + v_waterbody_km3_in_cell`

### C3. Stage C 输出变量（示例）
- 面积/驱动：`cell_area_km2`, `runoff_m_per_year`
- 流量：`q_local_runoff_cms`, `q_accum_runoff_cms`, `q_hydrorivers_main_cms`, `q_best_cms`, `q_source`
- 河道：`river_length_km_in_cell`, `river_width_m_from_qbest`, `river_depth_m_from_qbest`, `v_river_km3`
- 湖库：`waterbody_area_km2_in_cell`, `v_waterbody_km3_in_cell`, `v_lake_km3_in_cell`, `v_reservoir_km3_in_cell`
- 汇总：`v_tot_km3`

## 四、Stage D：k 参数与 tau（grid_k_params）

- 脚本：scripts/modeling/compute_k_params_grid_0p1.py
- 输出：data/processed/grid_0p1/grid_k_params_china_0p1.nc
- 关键原则：**以 Stage C 的 grid_hydro_geom 为权威输入**，保证 C→D 口径一致。

### D1. 关键参数（脚本常量）
本节目标：把 D 阶段所有公式中出现的“最终参数 + 中间参数”全部列举出来，并说明它们：
1) 单位；2) 来源文件与变量名；3) 在脚本中的计算方法或选择规则；4) 进入哪个公式。

#### D1.1 输入/输出文件
- 输入（网格底座）：data/processed/grid_0p1/grid_cells_china_0p1.nc
- 输入（Stage C 权威）：data/processed/grid_0p1/grid_hydro_geom_china_0p1.nc
- 输入（映射表，仅用于 diagnostics/对齐）：
  - data/processed/grid_0p1/grid_hydrorivers_china_0p1_mapping.parquet
  - data/processed/grid_0p1/grid_hydrolakes_china_0p1_mapping.parquet
  - data/processed/grid_0p1/grid_basinatlas_lev10_china_0p1_mapping.parquet
- 输入（用水）：data/processed/water_use/hswud_0p1_2010_2020_mean_clean_m3_per_day.parquet
- 输出：data/processed/grid_0p1/grid_k_params_china_0p1.nc

#### D1.2 常量（脚本写死）
- 时间与单位：
  - `SECONDS_PER_DAY = 86400.0`
  - `SECONDS_PER_YEAR = 31557600.0`（365.25 天）
  - `M3_PER_KM3 = 1e9`
- 水体吸收速度（Helmes Online Resource / Alexander 2004）：
  - `VF_KM_PER_DAY = 3.8e-5`（km/day）
  - 进入：`k_ret_day` 的水体项 `VF_KM_PER_DAY * a_wb_km2`
- 数值稳定阈值：
  - `V_TOT_MIN_KM3_FOR_RATES = 1e-9`（km³；= 1 m³）
  - 用途：当 `v_tot_km3 < threshold` 时把 `v_tot_km3_for_rates` 置为 NaN，使 k 与 tau 为 NaN，避免 `Q/V` 爆炸。
- 河道滞留参数（Helmes Online Resource 的 kriv 分段；单位 yr⁻¹，按 Q（km³/yr）分段）：
  - `KRIV_Q1 = 0.0882`（km³/yr）
  - `KRIV_Q2 = 0.4473`（km³/yr）
  - `KRIV_LOW = 71.2`（yr⁻¹）当 `Q < KRIV_Q1`
  - `KRIV_MID = 25.0`（yr⁻¹）当 `KRIV_Q1 ≤ Q < KRIV_Q2`
  - `KRIV_HIGH = 4.4`（yr⁻¹）当 `Q ≥ KRIV_Q2`
  - 换算到 day⁻¹：`kriv_day = kriv_yr / 365.25`
- Wollheim (2006) 河道几何幂律常数（仅用于 diagnostics 的主河段宽/深，不进入 k 公式）：
  - `AW = 5.01e-2`, `BW = 0.52`, `AD = 1.04e-3`, `BD = 0.37`
  - 计算：`W_km = AW * Q_km3_yr^BW`, `D_km = AD * Q_km3_yr^BD`

#### D1.3 中间量与最终量（按公式分组）

**(A) k_adv（day⁻¹）**

公式：

$$k_{adv} = \frac{Q}{V_{tot}}$$

其中：
- `Q`（km³/day）：脚本变量 `q_km3_day`
  - 来源：Stage C `q_best_cms`
  - 选择规则：D 阶段不再自行选择 Q，完全信任 Stage C（`q_cell_cms = q_best_cms`）。
  - 单位换算：
    - `q_cell_cms`（m³/s）→ `q_km3_day = q_cell_cms * SECONDS_PER_DAY / 1e9`
    - 同时计算 `q_km3_yr = q_cell_cms * SECONDS_PER_YEAR / 1e9` 供 kriv 使用。
- `V_tot`（km³）：脚本变量 `v_tot_km3`
  - 来源：Stage C `v_tot_km3`
  - 数值稳定处理：
    - `v_tot_km3_for_rates = v_tot_km3` 若 `v_tot_km3 ≥ V_TOT_MIN_KM3_FOR_RATES`，否则 NaN。

**(B) k_ret（day⁻¹）**

脚本实现的简化形式：

$$k_{ret} = \frac{V_{riv}\,k_{riv} + v_f\,A_{wb}}{V_{tot}}$$

其中：
- `V_riv`（km³）：脚本变量 `v_riv_km3`
  - 来源：Stage C `v_river_km3`
  - 注意：虽然脚本也能从 HydroRIVERS overlap 计算 `v_riv_km3_by_gid`，但最终用于 k 公式的是 Stage C 权威值。
- `k_riv`（day⁻¹）：脚本变量 `kriv_day`
  - 由 `q_km3_yr` 分段得到：`_kriv_day_from_q_km3_yr(q_km3_yr)`。
- `v_f`（km/day）：脚本常量 `VF_KM_PER_DAY`
- `A_wb`（km²）：脚本变量 `a_wb_km2`
  - 来源：Stage C `waterbody_area_km2_in_cell`
- 分母仍使用 `v_tot_km3_for_rates`

**(C) k_use（day⁻¹）**

脚本实现（Helmes Eq.9 结构）：

$$k_{use} = f_{WTA}\,(1-f_{DITW})\,k_{adv}\,(1-f_{soil})$$

其中：
- `f_soil`（无量纲，0–1）：脚本变量 `f_soil`
  - 来源：Stage C `runoff_m_per_year` 计算得出（使用 Online Resource 的经验公式）：
    - `f_dip = 0.29 / (1 + (R/0.85)^(-2))`
    - `f_dop = 0.01 * R^(0.95)`
    - `f_soil = clip(f_dip + f_dop, 0, 1)`
  - 备注：当前实现明确不包含颗粒态 P 的土壤转移（脚本 notes 里有说明）。
- `f_WTA`（无量纲，0–500）：脚本变量 `f_wta`
  - 用水总需水量：`q_total_m3_day` 来自 HSWUD `q_total_m3_per_day`
  - 供水能力：`q_main_m3_day = q_cell_cms * SECONDS_PER_DAY`
  - 计算：`f_wta = q_total_m3_day / q_main_m3_day`（若 `q_main_m3_day>0`）
  - 特殊处理：当 `q_total_m3_day>0` 且 `q_main_m3_day≈0` 导致非有限时，设为 500（供水受限上限）；当 `q_total_m3_day<=0` 时设为 0；最后 `clip(0,500)`。
- `f_DITW`（无量纲，0–1）：脚本变量 `f_ditw`
  - 计算：`ditw_num = q_dom_m3_day + q_manu_m3_day + q_ele_m3_day`
  - `f_ditw = ditw_num / q_total_m3_day`（若 `q_total_m3_day>0`，否则 0），最后 clip 到 [0,1]。
- `k_adv`：来自 (A)

**(D) tau（day）**

$$\tau = \frac{1}{k_{adv}+k_{ret}+k_{use}}$$

脚本变量：`tau_day`。

#### D1.4 D 阶段输出变量清单（核心 + 解释性）
- 核心：`k_adv_day`, `k_ret_day`, `k_use_day`, `tau_day`
- 进入 k_use 的中间量：`f_dip`, `f_dop`, `f_soil`, `f_wta`, `f_ditw`
- k_adv 输入诊断：`q_cell_cms`, `q_cell_km3_per_day`, `v_tot_km3`
- 用于排错的对照 Q：`q_river_main_cms`（HydroRIVERS 主河段），`q_lake_disavg_cms`（HydroLAKES Dis_avg 面积加权均值）
- 其他 diagnostics：`hydrolakes_res_time_day_wmean`, `river_width_m_main`, `river_depth_m_main`

### D2. 速率计算（按脚本顺序）
本节目标：按脚本执行顺序，把“读取哪些数据 → 计算哪些中间量 → 代入哪些公式 → 得到哪些结果”写清楚。

对应脚本：scripts/modeling/compute_k_params_grid_0p1.py

#### D2.1 读取输入并建立对齐索引
1) 读取网格底座：
  - `grid_cells_china_0p1.nc` 提供 `grid_id(lat,lon)`, `in_china(lat,lon)` 与坐标轴。
  - 构建 `gid_to_flat`（grid_id → 扁平索引），作为所有“按 grid_id 聚合的表”散射到 (lat,lon) 的统一索引。
2) 读取 Stage C 权威输入：
  - `grid_hydro_geom_china_0p1.nc`。
  - 检查其 shape 与 grid_cells 一致，否则报错（防止错网格对齐）。
3) 读取 mapping parquet（HydroRIVERS/HydroLAKES/BasinATLAS）：
  - 这些在 D 阶段主要用于 diagnostics（例如 `q_river_main_cms`、HydroLAKES 的诊断项），不作为 k 主公式的权威来源。
4) 读取用水数据（HSWUD）：
  - `hswud_0p1_2010_2020_mean_clean_m3_per_day.parquet`
  - 用 lat/lon 乘 10 后四舍五入映射回网格坐标轴，得到每条记录的 `grid_id`，再按 grid_id 汇总。

#### D2.2 组装 df_all（按 grid_id 的综合表）
1) 以 `gid_to_flat.index`（所有有效 grid_id）作为主索引建表。
2) 合并（outer join）：
  - HydroRIVERS：主河段 Q（按 `overlap_length_km` 最大选取）、河长、基于 overlap 的河流体积（仅 diagnostics）。
  - HydroLAKES：水体面积/体积拆分（`v_wb/v_res/v_lake`）与诊断 `Dis_avg`、`Res_time`（面积加权）。
  - BasinATLAS：`run_mm_syr` 按 overlap 面积加权得到 `runoff_m_yr`（注意：在主公式里最终仍使用 Stage C 的 runoff）。
  - HSWUD：`q_*_m3_per_day` 各分项与 `q_total_m3_per_day`。

#### D2.3 读取 Stage C 权威变量（真正进入 k 公式的输入）
脚本通过 `gid_to_flat` 把 Stage C 的 2D 栅格变量抽成 1D（顺序与 df_all.index 一一对应）。必需变量：
- `q_best_cms` → `q_cell_cms`
- `runoff_m_per_year` → `runoff_m_yr`
- `cell_area_km2`
- `v_river_km3` → `v_riv_km3`
- `waterbody_area_km2_in_cell` → `a_wb_km2`
- `v_waterbody_km3_in_cell` → `v_wb_km3`
- `v_lake_km3_in_cell` → `v_lake_km3`
- `v_reservoir_km3_in_cell` → `v_res_km3`
- `v_tot_km3` → `v_tot_km3`

同时脚本保留两类 diagnostics：
- `q_river_main_cms`：来自 HydroRIVERS mapping 的主河段 Q
- `q_lake_disavg_cms`：来自 HydroLAKES 的 `Dis_avg` 面积加权均值

#### D2.4 单位换算与数值稳定处理
1) 流量单位：
- `q_km3_day = q_cell_cms * 86400 / 1e9`
- `q_km3_yr  = q_cell_cms * 31557600 / 1e9`
2) 体积稳定掩膜：
- `v_tot_km3_for_rates = v_tot_km3` 若 `v_tot_km3 >= V_TOT_MIN_KM3_FOR_RATES`，否则 NaN。
- 记录被掩膜数量 `n_cells_masked_due_to_tiny_v_tot` 写入输出 attrs。

#### D2.5 计算 k_adv
公式与实现：
- `k_adv_day = q_km3_day / v_tot_km3_for_rates`（若分母 NaN 则 NaN）。

#### D2.6 计算 k_ret
1) 先由 `q_km3_yr` 得到河道滞留 `kriv_day`：
- 若 `q_km3_yr < 0.0882` → `kriv_yr = 71.2`
- 若 `0.0882 ≤ q_km3_yr < 0.4473` → `kriv_yr = 25.0`
- 若 `q_km3_yr ≥ 0.4473` → `kriv_yr = 4.4`
- `kriv_day = kriv_yr/365.25`
2) 代入简化 k_ret：
- `k_ret_day = (v_riv_km3*kriv_day + VF_KM_PER_DAY*a_wb_km2) / v_tot_km3_for_rates`

#### D2.7 计算 f_soil（进入 k_use）
1) 使用 Stage C 的 `runoff_m_yr`（m/yr）计算：
- `f_dip = 0.29/(1 + (R/0.85)^(-2))`
- `f_dop = 0.01 * R^(0.95)`
- `f_soil = clip(f_dip + f_dop, 0, 1)`
2) 备注：当前实现明确省略颗粒态 P（脚本 notes）。

#### D2.8 计算 f_wta 与 f_ditw（来自 HSWUD）
1) `q_main_m3_day = q_cell_cms * 86400`
2) `f_wta = q_total_m3_day / q_main_m3_day`（仅当 `q_main_m3_day>0`）
  - 若需求存在但 `q_main_m3_day≈0` → 置为 500
  - 若无需求 → 置为 0
  - 最后 `clip(0,500)`
3) `f_ditw`：
  - `ditw_num = q_dom_m3_day + q_manu_m3_day + q_ele_m3_day`
  - `f_ditw = ditw_num / q_total_m3_day`（若 `q_total_m3_day>0`，否则 0）
  - `clip(0,1)`

#### D2.9 计算 k_use
公式与实现：
- `k_use_day = f_wta * (1 - f_ditw) * k_adv_day * (1 - f_soil)`

#### D2.10 计算 tau
1) `denom = k_adv_day + k_ret_day + k_use_day`
2) `tau_day = 1/denom`（仅当 `denom>0`，否则 NaN）

#### D2.11 写出 NetCDF（含解释性变量）
1) 把 1D（按 df_all.index）结果散射回 (lat,lon)。
2) 用 `in_china` 掩膜输出。
3) 写出 attrs：包括所有常量（VF, KRIV_* 等）、输入文件路径、体积掩膜阈值与被掩膜数量。

### D3. HydroLAKES 的 Res_time 单位
- HydroLAKES TechDoc：`Res_time` 单位为 **days**。
- 脚本输出诊断变量为 `hydrolakes_res_time_day_wmean`（面积加权平均，仅作为诊断，不直接进入 tau 计算）。

## 五、Stage E：FF/CF（grid_ff_cf）

- 脚本：scripts/modeling/compute_ff_cf_grid_0p1.py
- 输出：data/processed/grid_0p1/grid_ff_cf_china_0p1.nc
- 输入：
  - grid_cells（网格掩膜与 grid_id）
  - grid_topology（`hydrorivers_next_grid_id` 或 `riveratlas_next_grid_id`）
  - grid_k_params（k_adv,k_ret,k_use,tau）

### E1. 递推公式与实现细节
- `f_transfer = k_adv/(k_adv+k_ret+k_use)`，并裁剪到 [0,1]。
- 递推：`ff = tau + f_transfer * ff_next`。
- `export_frac_to_outlet`：路径上 f 的连乘。
- `steps_to_outlet`：到 outlet 的步数。
- cycle-breaking：若检测到环，在局部断边并记录 `cycle_break_flag`。

### E2. CF 的状态
- 当前仅支持 `--effect-factor` 标量，输出 `cf = ff_day * effect_factor`。
- EF 尚未在本仓库参数化，因此“学术意义上的 CF”还需要后续定义 EF。

## 六、回答你的 4 个问题

### 1) 结果对不对：我们如何避免“理解偏差”导致错算
高风险点清单（我们已处理/未处理）：
- 单位：HydroLAKES 体积 mcm→km³（已修复）；Res_time day（已修复输出名与说明）。
- 拓扑：self-loop 与 cycles（已修复/兜底；并在产物 attrs 或变量里留痕）。
- 支撑域不一致：河道线属性 vs 流域面属性 vs 湖库面属性（这是常态，不必然错误；关键是聚合方式正确：深度按面积加权、线属性按长度/主河段、体积按面积分数）。
- 时间口径：Q、runoff、用水的多年平均/时期可能不同（当前属于“climatology/long-term mean”假设；需要在论文中明确）。
- 水量闭合：HydroRIVERS 的 Q 与 runoff 累积 Q 在某些区域可能不一致（当前用 `q_best` 优先级策略解决，但应做诊断图/统计）。

### 2) 在口径正确前提下，准确性/科学性主要受什么限制
- 0.1° 网格不是水文响应单元：河道与分水岭会被切割，三角洲/分汊区域会被强制单出口。
- k_ret 的简化：目前采用 VF×水体面积 + 河道 kriv 的简化形式，未显式区分不同水体类型/水深/温度/季节。
- 用水与 P 去向参数：f_WTA, f_DITW, f_soil 等（如果来自文献默认或粗尺度产品）会带来结构性不确定性。
- 过程为“稳态一阶”：忽略季节波动、洪峰、冰冻期等。

### 3) 如何提升精度（在不推翻框架情况下）
优先级从高到低：
1) 拓扑不确定性显式化：输出每格 outlet 候选数、主河段 id、分数差距等诊断层，避免“黑盒 next_grid”。
2) Q 口径改进：
   - 在河道无 Q 的格子，runoff→Q 的累积可加入湖库调蓄或分区校准。
   - 对 `q_best` 引入“与下游一致性”约束，减少局部异常。
3) 水体体积/面积质量控制：对异常水深（V/A）做 flag；对小水体的 subgrid 处理。
4) 过程参数区域化：VF、kriv、用水参数按气候带/土地利用/流域类型分区而不是全国统一常数。
5) 若允许改变内部计算单元：先在 reach/子流域单元上路由，再汇总回 0.1° 输出（兼顾水文一致性与栅格交付）。

### 4) 如何验证结果准确性（对外说服）
建议做三层验证：
- 机制/守恒层：
  - 检查 `f_transfer` ∈ [0,1]，`tau>0`，无大范围 NaN；cycle 数量与空间分布可解释。
  - 质量守恒：对任意源点 i，`export_frac_to_outlet` 应等于沿路径 f 的乘积。
- 观测/文献对标层：
  - 选几个大流域（长江/黄河/珠江/松花江）比较 outlet 的 Q 与公开水文统计量级（只做数量级/相对关系）。
  - 与 Helmes/Henderson 等文献中 FF 的典型范围对比（分布形态、p50/p90/p99）。
- 反事实/敏感性层：
  - 对关键常数（VF、kriv 分段阈值、用水去向系数）做 ±30% 扰动，看 FF 分布/空间格局是否稳健。
  - 对拓扑（hydrorivers vs riveratlas 指针）做替换对比，检查结果对拓扑依赖程度。

## 七、建议立刻补齐的“审计输出”（最能消除不确定）
- 一张“来源占比图”：`q_source`（HydroRIVERS vs runoff 累积）空间分布。
- 一组一致性散点：`q_hydrorivers_main_cms` vs `q_accum_runoff_cms`（log-log，按流域分组）。
- 一张拓扑不确定性图：每格 outlet 候选数（需要在拓扑导出脚本里额外输出）。

