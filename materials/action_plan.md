# 区域化淡水富营养化 CF 行动方案

更新日期：2025-11-21

## 1. 背景与目标
- **研究目的**：依据 Helmes (2012) 的淡水磷命运模型及 Henderson (2021) 在 TRACI 中的区域化实现，构建面向中国（可扩展全球）的 0.1° 网格化淡水富营养化特征化因子（CF）。
- **成果要求**：生成可追溯的数据管线、可复现的计算脚本/模型、并输出格网/流域/行政区等多尺度 CF 结果，为 LCIA 使用者提供本地化的淡水富营养化评价能力。
 - **当前进度**：HydroSHEDS/HydroATLAS 与 HSWUD 数据已下载并整理入库，完成字段清单与检查脚本（`scripts/inspect_hydro_datasets.py`），即将进入阶段 A/B 的脚本化实现。

## 2. 关键参考与约束
| 类别 | 说明 |
| --- | --- |
| 方法学 | Helmes et al. (2012) fate 公式（Eq.4–6），Henderson et al. (2021) 的 TRACI 区域化框架（P 控制淡水、N 控制海洋）。|
| 受体单元 | 采用 **0.1° 规则网格** 作为 receptor unit，需映射全部水文变量与下游拓扑；可与 HydroBASINS 子流域互作。|
| 数据现状 | 所有 HydroSHEDS/HydroATLAS 数据已位于 `data/HydroSHEDS data/`，水资源利用数据位于 `data/water use data/27610524/`。`materials/dataset_field_inventory.md` 提供字段清单。|
| 计算限制 | 优先利用现有流量、径流、湖泊体积等属性，避免重复构建水文模型；必要时再补充 runoff / land-use 数据。|

### 2.1 关键符号工作定义（本项目约定）
- `f_WTA`：单元内年平均总取水量 / 可利用水资源量（可按行业细分：dom/ele/irr/manu），用于表征水量压力。
- `f_DITW`：排放到淡水受体（河流/湖泊）的比例，考虑污水处理前后与海排情形。
- `k_use`：由 `f_WTA` 与 `f_DITW` 综合得到的人类用水相关去除速率，代表在用水和污水处理过程中从水体移除的 P 份额。
- `k_adv`：由流量与几何特征决定的平流（输送）速率，近似 $Q/V$。
- `k_ret`：由湖库/河道滞留与沉积决定的保留速率，依赖水体体积、停留时间与经验系数。
- `f_soil`：排放到土壤/陆地后最终进入淡水的比例，可基于 NEWS/区域经验式估算。
- `FF_i`：格网/单元 $i$ 的 fate factor，定义为从 $i$ 到所有下游单元 $j$ 的暴露时间加权和：$FF_i = \sum_j f_{i,j} 
   	au_j$。

## 3. 数据资产概览（精选）
| 数据集 | 位置 | 主要用途 | 当前状态 |
| --- | --- | --- | --- |
| HydroRIVERS v1.0 Asia | `.../HydroRIVERS_v10_as.shp` | 河段几何、`DIS_AV_CMS`、`NEXT_DOWN`，用于构建河网拓扑、河段长度。| 已在 inventory 中检查字段 |
| RiverATLAS v1.0 | `.../RiverATLAS_v10.gdb` | 提供丰富的河段属性（流量、径流、土地利用、人口等），可按 `HYRIV_ID` 与 HydroRIVERS 对应。| 已在 inventory 中检查字段 |
| BasinATLAS v1.0 | `.../BasinATLAS_v10.gdb` | 各级 HydroBASINS 子流域属性（`dis_m3_pyr`, `run_mm_syr`, `pop_ct`, `dor_pc_pva` 等）。| 已在 inventory 中检查字段 |
| HydroLAKES / LakeATLAS | `HydroLAKES_*`, `LakeATLAS_v10.gdb` | 湖泊/水库面、体积、均深，用于 Vtot、kret 计算。| 已下载，待体积/面积派生脚本 |
| HydroBASINS level 10 & pour points | `hybas_*` | 流域拓扑、Pfafstetter 码，与网格/河段映射。| 已在 inventory 中检查字段 |
| HSWUD 水资源利用 | `data/water use data/27610524/*.nc` | 1965–2022 月尺度行业取水（dom/ele/irr/manu），支撑 `f_WTA`、`f_DITW`、水资源压力估算。| 已读取元数据，待 0.1° 聚合与校验 |
| 参考文献/笔记 | `materials/articles/*.md` | Helmes/Henderson 原文 & 摘要，可直接引用公式与参数。| 已整理，随用随查 |

## 4. 行动路线
### 阶段划分概览
| 阶段 | 核心任务 | 关键输入 | 产出 |
| --- | --- | --- | --- |
| A. 数据准备 | 统一路径、版本、投影；生成数据字典；必要时抽取子区域 | `dataset_field_inventory.md`、原始数据 | 规范化的数据仓库、读取脚本模板 |
| B. 网格与河网对接 | 构建 0.1° 网格；将 HydroRIVERS/HydroBASINS 属性映射到网格；定义唯一下游单元 | HydroRIVERS、BasinATLAS、HydroBASINS | 网格属性表（ID、面积、河段/流域映射、流向）|
| C. 水文量与几何量 | 利用 River/BasinATLAS 字段直接赋值或插值：`Q`, `runoff`, `river length`；结合 HydroLAKES 估算湖/库体积、河宽深 | RiverATLAS、HydroLAKES、HydroRIVERS | 每格 `Vriver`, `Vlake`, `Vres`, `Q`, `Ai` |
| D. 过程速率计算 | 依据 Helmes 公式计算 `k_adv`, `k_ret`, `k_use`；整合 HSWUD 估算 `f_WTA`、`f_DITW`、行业结构；估算 `f_soil` (NEWS/区域经验式) | 阶段 B/C 输出、HSWUD、文献参数 | 速率系数表、停留时间 `τ_j` |
| E. 传输与 CF 计算 | 构建河网 DAG，沿主流向递推 `f_{i,j}` 并累积 `FF_i = Σ f_{i,j} τ_j`；输出格网/子流域/行政区 CF；叠加 effect factor | k 系数表、hydro topology、Helmes EF | 0.1° CF 栅格 + 汇总表（省、流域、活动类型）|
| F. 校核与敏感性 | 与 Helmes 0.5° 结果、Henderson 国家级结果对比；评估数据缺口（如污水处理、fsoil 不确定度） | 阶段 E 结果、文献 | 误差分析、改进清单 |
| G. 产品化与文档 | 打包脚本、参数、数据接口；撰写方法手册、使用示例；准备未来扩展（更高分辨率/全球） | 全部成果 | 可复现 repo、技术报告、CF 产品 |

> 代码组织建议：
- A–C 阶段主要放在 `scripts/data_prep/` 与 `scripts/modeling/geometry/` 下，如 `build_grid.py`, `build_grid_river_mapping.py`, `derive_flow_volume.py`。
- D–E 阶段主要放在 `scripts/modeling/fate/`，例如 `compute_k_params.py`, `compute_ff_cf.py`。
- F–G 阶段主要放在 `scripts/analysis/` 与 `scripts/viz/`，例如 `compare_with_helmes.py`, `plot_ff_maps.py`。

> 关键中间数据建议统一存放在 `data/processed/` 目录，命名规则：`data/processed/<theme>/<resolution>_<name>.<parquet|nc>`。

### 近期优先任务（建议顺序）
1. **HSWUD 数据处理**：
   - 统一单位（10^8 m³ → km³/yr 或 m³/s）。
   - 计算 0.1° 网格内按行业的平均取水量及季节性，得到 `f_WTA` 与行业占比（推得 `f_DITW`）。
   - **Done 判据**：生成 `data/processed/water_use/hswud_0p1_annual.parquet`，字段至少包含 {`grid_id`, `year`, `q_dom`, `q_ele`, `q_irr`, `q_manu`, `q_total`}，并在 2–3 个省与官方统计年鉴总量对比误差 < 10%。
2. **网格-河段对齐脚本**：
   - 建立 0.1° 网格索引（含 `grid_id`, `lat`, `lon`, `area_km2`）。
   - 将 HydroRIVERS `HYRIV_ID` 依据线段与网格的空间交集写入映射表；提取 `NEXT_DOWN` 形成网格级拓扑。
   - **Done 判据**：得到 `data/processed/grid_0p1/grid_cells.parquet` 与 `data/processed/grid_0p1/grid_river_mapping.parquet`（含 `grid_id`, `hyriv_id`, `length_in_grid_km`），并在一个小区域（如长江上游子域）通过可视化人工检查网格-河段匹配正确。
3. **体积与速率原型**：
   - 选取试点流域（如长江上游）验证从 RiverATLAS/BasinATLAS 字段即可计算 `k_adv`、`k_ret`。
   - 将 HydroLAKES/LakeATLAS 多边形与网格叠加，检验体积守恒。
   - **Done 判据**：在试点流域生成 `results/prototype/k_params_yangtze_0p1.parquet`，包含 `grid_id`, `k_adv`, `k_ret`, `k_use` 等字段，并完成至少 1–2 张对比图（如 `k_adv` vs. 流量等级）。
4. **f_soil 参数源**：
   - 复核 Helmes 使用的 NEWS 回归（Mayorga 2010）；准备 runoff、土地利用输入；设计中国区替代方案（如 SWAT、GLEAM 数据）。
   - **Done 判据**：整理形成 `materials/f_soil_assumptions.md`，明确中国区 `f_soil` 的参数来源、公式与不确定性范围。
5. **代码框架**：
   - 以 `scripts/` 目录为基础，新增 `data_prep/`, `modeling/`, `analysis/` Python 包，拆分为“数据抽取、参数计算、CF 计算、可视化”四大模块。
   - **Done 判据**：完成基础包结构（含 `__init__.py`）、至少一个 CLI 入口脚本（例如 `scripts/main.py` 或若干 `python -m scripts.data_prep.xxx` 可直接运行），并在 `README` 或本文件中记录调用示例。
6. **验证策略**：
   - 规划与 Helmes 0.5° 网格对比流程：聚合 0.1° 结果→0.5°，对比 `FF` 分布；记录偏差原因（数据替换 vs. 分辨率差异）。
   - **Done 判据**：设计并记录一套对比流程（脚本草案 + 步骤说明），包括：0.1°→0.5° 聚合规则、对比指标（如 RMSE、偏差因子）、输出图/表清单，保存为 `materials/validation_plan.md`。

## 5. 风险与对策
| 风险 | 可能影响 | 缓解措施 |
| --- | --- | --- |
| HSWUD 数据覆盖/质量不一 | `f_WTA` 失真，影响 `k_use` | 与官方统计（年鉴、省级）交叉校验；必要时按流域比对总量。 |
| 0.1° 网格拓扑复杂，存在多出口 | 传输矩阵 `f_{i,j}` 难以稳定 | 借助 HydroBASINS Pfafstetter 码进行层级约束；为河湖单元设置“超级节点”。 |
| retention 参数仅基于美国 SPARROW | 热带/高寒地区偏差 | 参考区域研究（如湖泊沉积速率、河道自净），建立校正系数；进行敏感性分析。 |
| 缺少污水处理效率数据 | `k_use` 可能高估 | 先按 Helmes 假设（忽略污水处理），再从中国城市污水处理率统计中补充校正。 |
| 全国 0.1° 计算的算力与内存压力 | 大规模传输递推计算时间过长或内存溢出 | 优先按流域/区域分块计算（分批加载河网与网格），必要时引入 `dask`/`xarray` 的分布式/惰性计算，并提前做小区域性能测试。 |

## 6. 里程碑（建议）
1. **M1 – 数据底座**（~2 周）：完成 HSWUD 处理、网格-河段映射、体积/流量变量抽取；交付数据字典与样例网格表。 
2. **M2 – 速率/传输原型**（~4 周）：在试点流域完成 `k` 参数与 `FF` 试算，验证流程与性能。 
3. **M3 – 全国 0.1° 计算**（~6 周）：跑通全国模型，输出格网/流域/省级 CF；完成与 Helmes/Henderson 的对比分析。 
4. **M4 – 文档与发布**（~2 周）：整合代码、方法说明、数据产品，形成可共享的 LCIA CF 套件。 

---
该行动方案可随进展迭代，建议在完成每个阶段后更新 `materials/action_plan.md` 与 `materials/dataset_field_inventory.md`，并在 `scripts/` 中记录对应代码入口。