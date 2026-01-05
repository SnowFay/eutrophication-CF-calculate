# 阶段 A 工作进展汇报思路（PPT 详细建议）

> 适用场景：面向导师和同学的组会/阶段汇报（约 20–30 分钟），承接上次“整体研究目标”的报告。本次聚焦于：选择“水体富营养化”作为切入点，基于 Helmes / Henderson 方法学搭建中国本土化 CF 计算原型，并重点展示阶段 A 的数据准备与方法设计进展。

---

## 0. 开场与承接（1–2 页）

**目的**：自然承接上一次的“大目标”，说明这次是“从总体蓝图走向第一个具体试点”的进展汇报。

**PPT 建议：**

1. **标题页**  
   - 标题示例：
     - “中国本土化 LCIA 方法体系——水体富营养化试点的阶段性进展”  
   - 副标题：
     - “基于 Helmes / Henderson 方法学的特征化因子原型构建（阶段 A：数据准备）”  
   - 作者、单位、日期。

2. **承接上次整体目标**（1 页）  
   - 左侧放上次报告中的“总目标文字”或一个框图：
     - “**研究旨在构建一个多维时空动态化的中国本土化 LCIA 方法体系及 CF 数据库**”。
   - 右侧用 2–3 个要点说明本次报告的定位：
     - 本次聚焦 **一个影响类别：淡水富营养化** 作为切入点。  
     - 采用 **国际已有方法学（ReCiPe / TRACI / SDU）对比后，优先沿用 Helmes / Henderson 路线**。  
     - 当前处在 **方法学原型搭建的“阶段 A：数据准备”**，为后续 k 参数与 CF 计算打基础。

---

## 1. 影响类别选择与方法学框架（3–4 页）

**目的**：说明为什么选“淡水富营养化”，以及在众多方法中如何落到 Helmes/Henderson 的基本框架上。

### 1.1 为什么选“水体富营养化”（1 页）

**PPT 内容要点：**

- 列出几类常用 LCIA 影响类别（气候变化、酸化、富营养化、水资源消耗等），突出：
  - 富营养化 **与中国区域水环境治理、磷排放等问题高度相关**；
  - 有 **比较成熟的国际方法学** 可以借鉴（ReCiPe、TRACI、SDU、Helmes、Henderson 等）。
- 一张示意图：源（排放）→ 河网/湖泊 → 受体（富营养化风险）。

### 1.2 方法学选择：对比 ReCiPe / TRACI / SDU 等（1–2 页）

**建议做一个“对比表” + 一张简明示意图：**

- 表 1：不同方法学在淡水富营养化上的处理特点（示例）：
  - 维度：
    - 空间分辨率（全球/区域/格网）；
    - 时间分辨率（稳态/多年度平均/逐年）；
    - 传输与命运模型（是否显式河网/湖库、是否区分 k_adv, k_ret）；
    - 数据需求（河网、流量、湖库体积、用水量等）。
- 结论性一句话：
  - 本研究 **优先沿用 Helmes (2012) 与 Henderson (2021)** 提出的 **多媒体传输 + 河网/湖库过程显式化** 的方法学思路，
  - 在此基础上 **开发适合中国本土情况（数据、空间尺度、时间尺度）的实现方案与 CF 库**。

### 1.3 Helmes / Henderson 路线的核心思想（1–2 页）

**建议用“流程图 + 关键公式”形式：**

- 一张大流程示意图（可手绘风格）：
  1. **磷排放（源）**：来自点源/面源排放，落在某个空间单元（格网/流域）。
  2. **传输与稀释**：沿河网向下游传输，经历：
     - **对流 (advection)**：由流量驱动的输送，特征时间尺度 ~ $V/Q$；
     - **滞留/沉积 (retention)**：在河道和湖泊/水库中的滞留与沉积，用 $k_{ret}$ 或驻留时间 $\tau$ 描述；
     - **用水抽取与再排放 (water use & return)**：与 $f_{WTA}$，$f_{DITW}$ 等因子相连。  
  3. **中间介质浓度**：计算河段/湖库中的平均浓度或暴露量。  
  4. **受体与效应**：通过 effect factor（如 P 负荷→富营养化风险/受影响水体体积），得到 CF：
     $$ \text{CF} = \sum_\text{path} \text{fate factor} \times \text{effect factor} $$

- 关键参数标注：
  - $k_{adv}$：与河网拓扑、流量、体积、驻留时间相关；
  - $k_{ret}$：反映 P 在河道/湖泊中被滞留的概率；
  - $f_{WTA}$：水体抽取对污染物输送的影响（Water Transfer to Another basin）；
  - $f_{DITW}$：排放进入不同类型水体（河流/湖泊/海洋）比例。

**结论**：
- 这部分要给老师一个直观感觉：**你选的是一个“有物理过程基础”的命运-效应模型，而不是黑箱 CF**。
- 同时说明：
  - **本次阶段工作主要在“输入数据与过程参数”的准备上**（河网、湖库、用水量等），
  - 正在搭建适合中国的 k_adv / k_ret / f_WTA 计算框架。

---

## 2. 研究整体路线与阶段划分（2–3 页）

**目的**：把全项目的路线图说清楚，再突出目前所处的“阶段 A：数据准备”。

### 2.1 整体路线图（1–2 页）

**建议画一张“从原始数据到 CF 数据库”的时间线或模块图：**

- 模块可以包括：
  1. **阶段 A：数据准备与空间基底搭建**  
     - HSWUD 用水数据标准化（格网化、单位统一）。
     - 河网/流域（HydroRIVERS / RiverATLAS / BasinATLAS）。
     - 湖库（水库）数据（HydroLAKES / LakeATLAS）。
  2. 阶段 B：**格网–河网–流域耦合与传输路径构建**  
     - 建立 0.1° 格网与河网/流域的映射关系。
     - 构建河网拓扑 DAG，识别下游路径和终端汇水点（入海/内陆湖）。
  3. 阶段 C：**参数计算原型（k_adv, k_ret, f_WTA, f_DITW 等）**  
     - 利用流量、体积、用水量、湖库驻留时间等推导参数。
     - 在若干试点流域上进行验证与敏感性分析。
  4. 阶段 D：**全国尺度 CF 计算与结果集成**  
     - 生成中国本土化富营养化 CF 库（按格网/流域/省级等不同空间单元）。
  5. 阶段 E：**动态化与多影响类别扩展**  
     - 引入时间维度（逐年/多时期），
     - 将方法推广到其他影响类别（如水资源消耗、毒性等）。

### 2.2 当前阶段的定位（1 页）

- 在路线图上 **高亮标记“阶段 A”**，并用一句话概括：
  - “当前工作重点：**搭建适合中国区域的水文与用水数据基底，为 Helmes/Henderson 路线计算 P 命运参数提供稳定输入**。”
- 简要列出阶段 A 的关键问题：
  - 如何把 **原始 HSWUD NetCDF** 变成 **0.1° 格网、多年平均、单位统一的用水数据？**
  - 如何从 HydroRIVERS / RiverATLAS / BasinATLAS 中 **筛出对中国区域有用的核心信息（core tables）？**
  - 如何把 **湖库体积/驻留时间信息** 整合进来，为后续 $V_{tot}$ 和 $k_{adv}$ 做准备？

---

## 3. 阶段 A：数据准备——HSWUD 用水数据（3–4 页）

**目的**：展示你在 HSWUD 处理上的完整链条（数据→清洗→聚合→结果检验），说明已经得到可靠的中国用水空间格局输入。

### 3.1 数据来源与目标产物（1 页）

- 左侧：列出 4 个原始 HSWUD 文件（可以用代码块或表格展示）：
  - `HSWUD_irr_.nc`（农业灌溉）
  - `HSWUD_manu.nc`（工业制造）
  - `HSWUD_ele.nc`（电力冷却）
  - `HSWUD_dom.nc`（生活用水）
- 右侧：展示目标产物（可以直接用当前 `phase_a_data_prep_tasks.md` 中的清单）：
  - 多年平均 0.1° 网格：
    - 年单位：`hswud_0p1_2010_2020_mean_clean.parquet` / `.nc`（m³/year）。
    - 日单位：`hswud_0p1_2010_2020_mean_clean_m3_per_day.parquet` / `.nc`（m³/day）。
- 说明：
  - 年单位版本 → 方便和统计年鉴、总量对比；
  - 日单位版本 → 方便与 **日尺度驻留时间和 k_adv 公式** 对接。

### 3.2 处理流程与关键决策（1–2 页）

**建议用一个流程图 + 少量伪代码截图来说明 `hswud_aggregate.py` 的逻辑：**

1. **读取与单位统一**：
   - 使用 `xarray` 读取 4 个 NetCDF。  
   - 掩蔽 `_FillValue` / `missing_value` 和小于 `-1e20` 的异常值；  
   - 将所有值统一转换为 **m³**（原始单位约为 10⁸ m³/时段）。
2. **时间聚合（2010–2020 多年平均）**：
   - 对 time 维度按年求和，再对多年求平均；  
   - 得到每个格网格点上 2010–2020 的 **平均年总用水量（m³/year）**。
3. **行业聚合**：
   - 计算 `q_total_m3 = q_irr_m3 + q_manu_m3 + q_ele_m3 + q_dom_m3`。  
4. **格网展开与导出**：
   - 将 `Dataset` 转换成 `DataFrame`，保留 `lat`, `lon`，必要时引入 `grid_id`。  
   - 导出为 Parquet 和 NetCDF。
5. **单位转换到 m³/day（新工作）**：
   - 脚本 `hswud_convert_to_m3_per_day.py`：对 `q_*_m3` 除以 365 → `q_*_m3_per_day`。

可以插入一小段代码截图（例如 `_harmonise_units_to_m3_per_year` 的核心部分），展示你对极端值和缺失值的处理是**有意识设计**的，而不是“黑箱跑一下”。

### 3.3 Sanity check 与空间可视化（1–2 页）

- **总量检查结果页**：
  - 引用 `hswud_sanity_check.py` 结果：
    - 2010–2020 多年平均全国总用水量约 $5.96 \times 10^{12} \, m^3/yr$（~5962 km³/yr），灌溉占比最高。  
  - 与公开统计数据的数量级对比（6000 亿 m³ 左右），说明 **量级合理**。
- **空间分布图页**：
  - 嵌入 `plot_hswud_maps.py` 生成的图：
    - 总用水量空间分布；
    - 分行业（灌溉/工业/生活）分布对比（可选 1–2 张）。
  - 简要解读：
    - 高值集中在华北平原、长江中下游、部分灌溉区；
    - **符合对中国用水空间格局的直觉认知**。

---

## 4. 阶段 A：数据准备——河网与流域（HydroRIVERS / RiverATLAS / BasinATLAS）（3–4 页）

**目的**：说明你已经有了一套“为河网传输建模准备的干净骨架数据”，包括拓扑、流量、坡度、流域面积等。

### 4.1 原始数据与 core 子集思路（1 页）

**PPT 建议：**

- 原始数据列表：
  - HydroRIVERS v1.0 Asia shapefile；
  - RiverATLAS v1.0 geodatabase；
  - BasinATLAS v1.0 lev10 geodatabase；
  - 中国边界：`gadm41_CHN_0.shp`。
- 设计思路：
  - 不一上来就处理全量全球数据，而是**先做“轻量 core 子集”**：
    - 只保留：
      - 拓扑（如 HYRIV_ID, NEXT_DOWN, HYBAS_ID）；
      - 少数关键水文/地形属性（如流量、坡度、runoff）；
      - geometry。  
  - 再使用中国边界 + buffer 裁剪出 **中国及近邻区域** 的 core 表，减轻后续计算负担。

### 4.2 各 core 脚本与输出（2–3 页）

可以用表格 + 小段文字形式逐一介绍：

1. **HydroRIVERS Asia core**（`build_hydrorivers_asia_core.py`）
   - 核心字段示例：
     - `HYRIV_ID`, `NEXT_DOWN`, `LENGTH_KM`, `DIS_AV_CMS`, `HYBAS_L12` 等；
   - 输出：`data/processed/hydrology/hydrorivers_asia_core.parquet`。

2. **RiverATLAS v10 core**（`build_riveratlas_v10_core.py`）
   - 字段：
     - `HYRIV_ID` + 一些水文气候属性（`run_mm_cyr`, `pre_mm_cyr`, `aet_mm_cyr`, `ele_mt_cav`, `sgr_dk_rav` 等）；
   - 输出：`data/processed/hydrology/riveratlas_v10_core.parquet`。

3. **BasinATLAS lev10 core**（`build_basinatlas_lev10_core.py`）
   - 字段：
     - `HYBAS_ID`, `PFAF_ID`, `NEXT_DOWN`, `SUB_AREA`, `UP_AREA`, `run_mm_syr` 等；
   - 输出：`data/processed/hydrology/basinatlas_lev10_core.parquet`。

4. **裁剪到中国 + buffer**（`clip_hydro_to_china.py`）
   - 思路：
     - 使用 GADM 中国边界 + ~1° buffer；
     - 通过 `geometry.intersects()` 筛选与缓冲区相交的河段/流域；
   - 输出：
     - `hydrorivers_china_core.parquet`
     - `riveratlas_china_core.parquet`
     - `basinatlas_lev10_china_core.parquet`
   - 可以放一张小地图：展示裁剪前后河网密度差异，直观看出“只保留了与中国相关的部分”。

**强调一点**：
- 这些 core 表已经为后续构建 **河网拓扑、上游-下游路径、流域汇水关系** 提供了标准化输入。

---

## 5. 阶段 A：数据准备——湖库（HydroLAKES / LakeATLAS）（3–4 页）

**目的**：说明你已经为“湖库体积/驻留时间”准备好了核心数据，这是 k_adv / V_tot 等参数的关键输入之一。

### 5.1 构建湖库 global core（2 页）

1. **HydroLAKES global core**（`build_hydrolakes_core.py`）
   - 输入：`HydroLAKES_polys_v10.shp`。
   - 保留字段：
     - 识别与元数据：`Hylak_id`, `Lake_name`, `Country`, `Continent`, `Poly_src`, `Lake_type`, `Grand_id`；
     - 体积与面积：`Lake_area` (km²), `Vol_total` (km³), `Vol_res` (km³), `Depth_avg` (m)；
     - 水文：`Dis_avg` (m³/s), `Res_time` (years)；
     - 背景：`Elevation`, `Wshd_area` (km²)；
   - 输出：`hydrolakes_global_core.parquet`（约 142 万个湖库多边形）。

2. **LakeATLAS global core**（`build_lakeatlas_core.py`）
   - 输入：`LakeATLAS_v10.gdb` 中 `LakeATLAS_v10_pol` 图层。
   - 保留字段：
     - 识别：`Hylak_id`, `Lake_name`, `Country`, `Continent`, `Poly_src`, `Lake_type`, `Grand_id`；
     - 连接字段：`HYBAS_L12`, `HYRIV_RCH`, `HYRIV_CAT`（连接流域与河段）；
     - 其他：`Elevation`, `Pour_long`, `Pour_lat`, `run_mm_vyr`, `Res_time`；
   - 输出：`lakeatlas_global_core.parquet`（同样约 142 万条记录）。

**可以插入一页 schema 表或字段列表截图，让老师看到你**很清楚地挑选了与后续建模相关的字段**。

### 5.2 湖库 China+buffer 裁剪（1–2 页）

- 脚本：`clip_lakes_to_china.py`（与 `clip_hydro_to_china.py` 同模式）。
- 逻辑：
  - 使用 GADM 中国边界 + 1° buffer；
  - 对 `hydrolakes_global_core` 和 `lakeatlas_global_core` 分别做 `intersects()` 筛选；
  - 输出：
    - `hydrolakes_china_core.parquet`
    - `lakeatlas_china_core.parquet`
  - 结果（当前运行）：
    - 从 ~1,427,688 条记录裁剪到 ~26,567 条湖库（与中国+邻近区域有关）。

- 可以放一张简易地图：展示中国及周边湖库分布，突出高密度区域（青藏高原湖泊、东部平原水库等）。

---

## 6. 当前阶段的小结与已有“原型条件”（1–2 页）

**目的**：告诉老师“现在桌面上已经有哪些干净的数据积木”，已经可以开始搭一个简化方法学原型。

**建议一张“数据资产总览表”**：

| 模块 | 主要数据资产 | 分辨率 | 状态 |
| --- | --- | --- | --- |
| 用水 (HSWUD) | `hswud_0p1_2010_2020_mean_clean.parquet/.nc` (m³/yr), `*_m3_per_day.parquet/.nc` | 0.1°×0.1°，2010–2020 多年平均 | ✅ |
| 河网 (HydroRIVERS) | `hydrorivers_asia_core.parquet`, `hydrorivers_china_core.parquet` | 矢量河段，带 HYRIV_ID/流量/长度等 | ✅ |
| 河网属性 (RiverATLAS) | `riveratlas_v10_core.parquet`, `riveratlas_china_core.parquet` | 河段属性（runoff、降水、坡度等） | ✅ |
| 流域 (BasinATLAS lev10) | `basinatlas_lev10_core.parquet`, `basinatlas_lev10_china_core.parquet` | lev10 流域边界/拓扑/面积/径流 | ✅ |
| 湖库 (HydroLAKES) | `hydrolakes_global_core.parquet`, `hydrolakes_china_core.parquet` | 湖库面，含体积/面积/驻留时间 | ✅ |
| 湖库连接 (LakeATLAS) | `lakeatlas_global_core.parquet`, `lakeatlas_china_core.parquet` | Hylak↔HYBAS/HYRIV 连接信息 | ✅ |

**强调：**
- 这些资产已经 **满足在一个或多个试点流域上线“简化版 k_adv / f_WTA 原型”的前置条件**。

---

## 7. 下一步工作计划（2–3 页）

**目的**：让老师看到你有清晰的后续技术路线，不只是“做完数据就停住”。

### 7.1 阶段 B 近期重点（1–2 页）

可以用条列 + 简单框图：

1. **格网–河网映射构建**：
   - 将 0.1° HSWUD 格网与 HydroRIVERS / RiverATLAS 河段进行空间叠加；
   - 构建 `grid_id → HYRIV_ID` 的映射表（可能是一对多关系）。

2. **河网拓扑与路径识别**：
   - 基于 `HYRIV_ID`, `NEXT_DOWN`, `HYBAS_ID` 构建有向无环图（DAG）；
   - 对每个河段识别：上游贡献区、下游路径、汇流终点（出海/入湖/内陆终止）。

3. **在试点流域上尝试计算 k_adv**：
   - 选一个或少数流域（例如长江/黄河某上游子流域）；
   - 利用：
     - 河段长度与流量（HydroRIVERS+RiverATLAS），
     - 河道/湖库体积（结合河长/断面假设 + HydroLAKES/LakeATLAS），
     - HSWUD 日均 Q（m³/day），
   - 先实现一个 **极简 k_adv 公式**，验证数值是否合理、敏感性如何。

### 7.2 阶段 C 及以后展望（1 页）

- **阶段 C：参数体系完整化**  
  - 对 k_ret、f_WTA、f_DITW 做区域化；
  - 增加环境变量（坡度、气候、土地利用）以支持回归或分类型参数化。
- **阶段 D：全国 CF 计算**  
  - 把试点经验推广到全国河网与湖库系统；
  - 生成全国 CF 表，并与现有国际方法（ReCiPe、TRACI 等）结果进行对比。
- **阶段 E：时间维度与多影响类别扩展**  
  - 引入逐年或多时期的气候与用水变化，研究 **CF 的时间敏感性**；
  - 将方法扩展至其他影响类别，为“多维时空动态化 LCIA”蓝图添砖加瓦。

---

## 8. 面临的问题与需要讨论的点（1–2 页）

**目的**：主动抛出技术和策略问题，让老师参与决策，而不是只报喜不报忧。可以放在报告末尾，作为讨论环节。

**建议列出 3–5 个核心问题：**

1. **时间尺度的选择**：
   - 目前 HSWUD 是 2010–2020 多年平均；
   - k_adv / k_ret 计算采用多年度平均是否足够，还是需要逐年变化？
   - 与“多维时空动态化 LCIA”的长期目标如何平衡？

2. **空间分辨率与计算负担**：
   - 目前采用 0.1° 格网 + 全球河网/湖库子集；
   - 是否需要在重点区域（如太湖流域）采用更高分辨率？

3. **参数化策略**：
   - k_ret, f_WTA, f_DITW 等参数是采用文献经验值，还是做统计学习/回归建模？
   - 需要多少观测数据或文献校验点？

4. **试点流域选择**：
   - 建议导师一起讨论选择 1–2 个试点流域（数据和案例都相对丰富的地区）；
   - 先在试点中跑通全链路，再推广到全国。

5. **其他技术问题**（可根据你近期思考补充）：
   - CRS 与 buffer 的精度问题（目前在经纬度上简单 buffer，后续是否要用投影 CRS？）；
   - 与中国本地统计数据对接的策略（行政区聚合 vs 流域聚合）。

---

## 9. 汇报节奏与展示建议（简要）

**时间建议（30 分钟左右）：**

- 0–3 分钟：开场与承接（整体目标 + 本次聚焦内容）。
- 3–10 分钟：方法学选择与 Helmes/Henderson 路线（影响类别选择 + 大框架）。
- 10–20 分钟：阶段 A 数据准备三大块：
  - HSWUD 用水数据处理链；
  - 河网/流域 core + China 裁剪；
  - 湖库 core + China 裁剪；
  - 穿插 2–3 张空间分布图和流程图。
- 20–25 分钟：当前阶段小结 + 已具备的原型条件。
- 25–30 分钟：下一步计划 + 面临问题与讨论。

**风格建议：**

- 图 > 表 > 文字：尽量多用流程图、空间分布图、简洁表格，文字精炼；
- 每个技术细节后面都接一句“**为什么这样设计**”（例如：为什么做 m³/day 转换，为什么先做 China+buffer 裁剪）；
- 对老师可能关心的问题提前埋点：
  - 计算负担、可落地性、与中国数据的匹配，以及和“多维时空动态化 LCIA 总目标”的衔接。

---

> 备注：如果需要，我可以在下一步帮你把这些内容进一步拆成“每页 PPT 的标题 + 要点 + 建议插图/图表类型”的清单，方便你直接做 PPT。
