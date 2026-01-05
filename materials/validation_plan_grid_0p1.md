# 0.1° 网格 FF/CF 结果验证方案（建议稿）

本文档用于“从结果角度说服别人”：在不改变现有模型框架（B→C→D→E）的前提下，如何系统地验证输出的可靠性与科学性。

验证分三层：
1) 机制与守恒（必须做，能排除大部分实现/口径错误）
2) 外部对标（推荐做，能建立数量级与空间格局可信度）
3) 敏感性与稳健性（强烈推荐，最能说服审稿人/答辩）

---

## 0. 验证对象与关键产物

核心 NetCDF：
- Stage C：data/processed/grid_0p1/grid_hydro_geom_china_0p1.nc
- Stage D：data/processed/grid_0p1/grid_k_params_china_0p1.nc
- Stage E：data/processed/grid_0p1/grid_ff_cf_china_0p1.nc

关键变量（最低集合）：
- 拓扑：`hydrorivers_next_grid_id`
- 水文几何：`q_best_cms`, `v_tot_km3`, `waterbody_area_km2_in_cell`
- 速率与时间：`k_adv_day`, `k_ret_day`, `k_use_day`, `tau_day`
- 递推输出：`ff_day`, `f_transfer`, `export_frac_to_outlet`, `steps_to_outlet`, `cycle_break_flag`

推荐新增“验证产物”（图/表）：
- `Q一致性散点`：`q_hydrorivers_main_cms` vs `q_accum_runoff_cms`（来自 Stage C）
- `拓扑问题格子地图`：cycle/self-loop/多出口候选（如果输出 diagnostics）
- `FF分布与分区统计表`：p50/p90/p99/max（全国+分流域/分区）

---

## 1) 机制与守恒验证（必须做）

### 1.1 变量域与基本约束检查
检查项（对中国范围 in_china）：
- `f_transfer` 必须在 [0, 1]（数值误差允许极少量越界，但应在 clip 后为 [0,1]）
- `tau_day` 必须 > 0（或 NaN：代表本格子在当前口径下不可计算）
- `k_adv_day,k_ret_day,k_use_day` 必须 ≥ 0（或 NaN）
- `v_tot_km3` 必须 ≥ 0
- `q_best_cms` 必须 ≥ 0

判定标准：
- 若出现系统性负值/大面积 NaN，优先视为口径/单位/映射错误。

### 1.2 递推恒等式抽样复算（最关键）
对于随机抽样的 N 个格子（建议 N=200 或按流域分层抽样）：
- 从 Stage E 取 `ff_day(i)`、从 Stage D 取 `tau_day(i)` 与 `f_transfer(i)`、从拓扑取 `next(i)`。
- 计算：
  - 预测值：`ff_pred = tau_i + f_i * ff_day(next(i))`（若 next 无效则 `ff_pred = tau_i`）
- 断言：`abs(ff_day(i) - ff_pred)` 在很小容差内（建议 1e-6～1e-4 day，取决于 float32/float64 和输出精度）。

判定标准：
- 抽样通过率应接近 100%。
- 若失败集中在 `cycle_break_flag=True` 或边界格子，可解释；若随机分布则表示递推实现或拓扑对齐存在问题。

### 1.3 拓扑图性质检查（无环/步数合理）
检查项：
- `cycle_break_flag` 的数量与空间位置是否集中在可解释区域（分汊/湖区/内流区），而非随机散布。
- `steps_to_outlet` 的分布是否合理：
  - 极端大步数应主要出现在长干流上游；
  - 若大量格子出现“异常短步数”，可能是下游指针跳跃/断裂。

如果可以补一个统计：
- 对每个格子沿 `next` 追踪，验证路径最终结束（-1/出界/非中国），并统计“终止类型”。

### 1.4 水量/量纲一致性检查（强烈建议）
- `k_adv_day = Q_km3_day / V_tot_km3` 必须满足量纲。
- 检查典型量级：
  - `Q_km3_day`：由 `q_best_cms` 转换，必须与 `q_best_cms` 成正比
  - `V_tot_km3`：典型应在 1e-12～1e4 km³ 的合理范围（依区域而定），极端值应可追溯（大湖/大库）

备注：此前 HydroLAKES 体积单位错误（mcm vs km³）会直接导致该层检查失败，因此这是“能抓大 bug”的必做项。

---

## 2) 外部对标验证（推荐做）

### 2.1 与公开水文统计的数量级对标（Q 侧）
目的：证明 Stage C 的 Q 口径没有离谱。

做法：
- 选取几个中国主要流域出口附近格子（长江、黄河、珠江、松花江等），读取 `q_best_cms`。
- 与公开的多年平均流量数量级对比（不追求精确到个位数；强调“数量级与相对大小”）。

判定标准：
- 量级正确（例如长江口显著大于黄河口），且不会出现“出口 Q 比上游小很多”的反常现象（除非有明显调水/用水影响且模型中可解释）。

### 2.2 与文献 FF 范围对标（FF 侧）
目的：证明 FF 分布形态合理。

做法：
- 汇总全国 `ff_day` 的 p50/p90/p99/max
- 与 Helmes/Henderson/TRACI 等文献中 FF 的典型范围/空间格局描述对比

判定标准：
- 不出现明显违背常识的量级（例如大面积百万天级别）
- 长尾集中在大湖库/低流区符合物理直觉

### 2.3 空间格局合理性检视
目的：非定量但对沟通很有效。

检查点：
- 高 FF 是否沿“湖库密集、流量小、滞留强”的区域分布
- 低 FF 是否集中在“高流量主干、河道体积相对小”的区域

---

## 3) 敏感性与稳健性验证（强烈推荐）

### 3.1 参数扰动敏感性（±30%）
建议扰动的关键常数（一次一个，保持其余不变）：
- `VF_KM_PER_DAY`（水体吸收速度）
- `KRIV_LOW/MID/HIGH`（河道滞留）
- `f_wta` 的 cap（目前 0–500）

比较指标：
- 全国 `ff_day` 分位数变化（p50/p90/p99）
- Top100 极端格子的稳定性（是否还是同一批格子）
- 空间相关（base vs perturbed 的 Spearman/Pearson 或栅格相关）

判定标准：
- 空间格局不应在小扰动下完全翻转；若翻转，说明结果过度依赖某个单一假设。

### 3.2 拓扑替换稳健性（hydrorivers vs riveratlas）
做法：
- 在 Stage E 用 `--pointer hydrorivers` 与 `--pointer riveratlas` 各算一遍
- 比较 `ff_day` 差异图与分布差异

判定标准：
- 拓扑差异带来的变化应集中在“拓扑不确定区域”（分汊/湖区/数据稀疏区）。

### 3.3 数据源替换/一致性（runoff 侧）
若允许：
- runoff 来源从 BasinATLAS→RiverATLAS 或其它产品替换
- 检查 `q_accum_runoff_cms` 与 `q_best_cms` 的变化

目的：评估“面尺度驱动”对结果的影响范围。

---

## 4) 最小可交付的验证清单（MVP）

如果只做最小集合，建议至少完成：
1) `f_transfer` 范围检查 + `tau_day>0` 检查 + NaN 覆盖率统计
2) 递推恒等式抽样复算（200 点）
3) `q_hydrorivers_main_cms` vs `q_accum_runoff_cms` 的一致性散点（log-log）
4) `ff_day` 全国分位数与 Top100 表（用于快速发现异常单位/异常水体）

