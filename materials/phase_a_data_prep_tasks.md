# 阶段 A：数据准备与 HSWUD 处理任务清单

**目标**：将原始的 HSWUD NetCDF 数据转换为标准化的、可直接用于模型的 0.1° 网格化年均用水数据表（Parquet 格式）。

**输入数据**：
- `data/water use data/27610524/HSWUD_irr_.nc` (农业灌溉)
- `data/water use data/27610524/HSWUD_manu.nc` (工业制造)
- `data/water use data/27610524/HSWUD_ele.nc` (电力冷却)
- `data/water use data/27610524/HSWUD_dom.nc` (生活用水)

**输出数据**：
**输出数据（当前已实现的标准产物）**：
- 多年平均 0.1° 网格用水表（Parquet）：
    - 年单位（m³/year，多年平均年总量）：`data/processed/water_use/hswud_0p1_2010_2020_mean_clean.parquet`
    - 日单位（m³/day，多年平均日均量）：`data/processed/water_use/hswud_0p1_2010_2020_mean_clean_m3_per_day.parquet`
- 多年平均 0.1° 网格用水场（NetCDF）：
    - 年单位（m³/year，多年平均年总量）：`data/processed/water_use/hswud_0p1_2010_2020_mean_clean.nc`
    - 日单位（m³/day，多年平均日均量）：`data/processed/water_use/hswud_0p1_2010_2020_mean_clean_m3_per_day.nc`

### 6. 数据输出与验证

- [x] **保存文件**
        - 将 DataFrame 保存为多年平均 Parquet 表 `data/processed/water_use/hswud_0p1_2010_2020_mean_clean.parquet`。
        - 同时导出 NetCDF 文件 `data/processed/water_use/hswud_0p1_2010_2020_mean_clean.nc`，便于与其它 NetCDF 数据集协同分析。
- [x] **基础验证 (Sanity Check)**
        - **总量检查**：使用 `scripts/analysis/hswud_sanity_check.py` 计算 2010–2020 多年平均的全国总用水量：约 $5.96 \times 10^{12}\,m^3/yr$（约 5962 km³/yr），其中灌溉用水占比最高；具体见脚本输出。
        - **可视化检查**：使用 `scripts/analysis/plot_hswud_maps.py` 生成空间分布图，确认高用水区主要集中在华北平原、长江中下游等人口/农业密集区域，图像说明见 `results/figures/hswud/README.md`。
- [ ] **创建目录结构**
    - 确保存在 `scripts/data_prep/` 目录。
    - 确保存在 `data/processed/water_use/` 目录用于存放输出结果。
- [ ] **创建脚本文件**
    - 创建 `scripts/data_prep/hswud_aggregate.py` 作为主处理脚本。
    - 确保 `requirements.txt` 中包含 `xarray`, `netCDF4`, `pandas`, `pyarrow` (用于 parquet)。

### 2. HSWUD 数据读取与清洗
- [ ] **读取 NetCDF 文件**
    - 使用 `xarray` 分别读取 4 个行业的 `.nc` 文件。
    - **检查点**：打印每个 dataset 的变量名、维度（time, lat, lon）和属性（units）。
- [ ] **单位标准化**
    - 依据 `state.md` 和元数据，确认原始单位（通常是 $10^8 m^3$ 或 $m^3$）。
    - 将所有数据统一转换为 **立方米 ($m^3$)**。
    - **注意**：`HSWUD_irr_.nc` 的单位可能需要特殊处理（参考 `state.md` 中的修正说明）。
- [ ] **缺失值处理**
    - 将 `NaN` 值填充为 0（假设无数据区域为无用水）。

### 3. 时间聚合 (Temporal Aggregation)
- [ ] **选定基准年份或时段**
    - 建议：计算 **2010-2020 年的平均值**，以代表近期稳态水平；或者提供参数选择特定年份（如 2015）。
- [ ] **执行聚合**
    - 对 `time` 维度进行求和（如果是月数据转年数据）或平均（如果是多年平均）。
    - 产出：每个行业在每个网格点上的年均用水量 ($m^3/yr$)。

### 4. 行业聚合 (Sectoral Aggregation)
- [ ] **计算总用水量**
    - 计算 $Q_{total} = Q_{irr} + Q_{manu} + Q_{ele} + Q_{dom}$。
    - 保留各分项数据，以便后续计算行业特定的 $f_{DITW}$。

### 5. 空间对齐与 ID 生成 (Spatial Alignment)
- [ ] **生成 Grid ID**
    - 为 0.1° 网格生成唯一的 `grid_id`。
    - **规则建议**：可以基于经纬度生成哈希值，或者简单的行主序编号（Row-major ordering），但必须保证与后续处理河流数据的 Grid ID 规则一致。
    - *注：如果暂时没有统一的 Grid ID 系统，可以先保留 `lat`, `lon` 列，后续再 join。*
- [ ] **格式转换**
    - 将 `xarray.Dataset` 转换为 `pandas.DataFrame`。
    - 展平数据，去除无用水（全 0）的网格以节省空间。

### 6. 数据输出与验证
- [ ] **保存文件**
    - 将 DataFrame 保存为 `data/processed/water_use/hswud_0p1_annual.parquet`。
- [ ] **基础验证 (Sanity Check)**
    - **总量检查**：计算全中国总用水量（Sum of all grids），与《中国水资源公报》或统计年鉴对比（数量级应在 6000亿 $m^3$ 左右）。
    - **可视化检查**（可选）：简单绘制一张热力图，确认高用水区是否在华北平原、长江中下游等人口密集区。

---

## 预期数据结构 (Schema)

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `grid_id` | int/str | 网格唯一标识 (可选，或保留 lat/lon) |
| `lat` | float | 网格中心纬度 |
| `lon` | float | 网格中心经度 |
| `q_irr_m3` | float | 农业灌溉年用水量 ($m^3$) |
| `q_manu_m3` | float | 工业制造年用水量 ($m^3$) |
| `q_ele_m3` | float | 电力冷却年用水量 ($m^3$) |
| `q_dom_m3` | float | 生活年用水量 ($m^3$) |
| `q_total_m3` | float | 总用水量 ($m^3$) |

---

## 7. 其他数据集预处理总览（阶段与目标）

> 目的：把“哪些数据什么时候处理到什么程度”说清楚，避免一开始就对所有数据做过度预处理。

### 7.1 数据集级别概览表

| 数据集 | 原始位置（示例） | 是否需要预处理 | 建议阶段 | 预处理目标（阶段 A） | 后续派生处理（阶段 B–E） |
| --- | --- | --- | --- | --- | --- |
| HSWUD 用水数据 | `data/water use data/27610524/*.nc` | 必须 | **阶段 A / 近期优先任务 1** | - 统一时间（年尺度或多年平均）<br>- 统一单位到 $m^3/yr$<br>- 与 0.1° 网格对齐（lat/lon 或 `grid_id`）<br>- 输出 `hswud_0p1_annual.parquet` | - 与可利用水量组合计算 $f_{WTA}$<br>- 按行业结构推导 `f_DITW`、`k_use` 等 |
| HydroRIVERS v1.0 | `.../HydroRIVERS_v10_as.shp` | 建议 | **阶段 A（HSWUD 之后）** | - 只保留中国范围河段<br>- 保留核心字段：`HYRIV_ID`, `NEXT_DOWN`, `LENGTH_KM`, `DIS_AV_CMS`, `HYBAS_L12` 等<br>- 统一 CRS 为 WGS84 (EPSG:4326)<br>- 保存为 `rivers_china_core.parquet` | - 阶段 B：与 0.1° 网格叠加，生成 `grid_river_mapping.parquet`<br>- 阶段 C：结合流量、长度等计算河段/格网的 $Q$, $V_{river}$, $\tau$ |
| RiverATLAS v1.0 | `.../RiverATLAS_v10.gdb` | 建议 | **阶段 A（与 HydroRIVERS 同步）** | - 从 GDB 中按 `HYRIV_ID` 选取与中国相关的河段记录<br>- 提取少量关键属性：runoff、湖库体积相关字段等（见 `materials/dataset_field_inventory.md`）<br>- 存为 `riveratlas_china_core.parquet` | - 阶段 C：与 HydroRIVERS 通过 `HYRIV_ID` 合并，派生 `runoff`, `k_adv` 等<br>- 阶段 D：为 `k_use`, `k_ret` 的区域化提供环境背景变量 |
| BasinATLAS v1.0 | `.../BasinATLAS_v10.gdb` | 建议 | **阶段 A（轻量）** | - 按层级（如 lev10）选取中国覆盖范围<br>- 提取 `HYBAS_ID`, `PFAF_ID`, `run_mm_syr`, `UP_AREA` 等关键字段<br>- 存为 `basins_lev10_china_core.parquet` | - 阶段 B：用于辅助构建流域级拓扑、检查网格-河网一致性<br>- 阶段 C/D：聚合到流域或行政区尺度，做对比与敏感性分析 |
| HydroLAKES / LakeATLAS | `HydroLAKES_*`, `LakeATLAS_v10.gdb` | 建议（但可稍后） | **阶段 A 末 / 阶段 C 前** | - 构建全球 core：`hydrolakes_global_core.parquet`, `lakeatlas_global_core.parquet`，只保留必要字段（如 `Hylak_id`, `Lake_area`, `Vol_total`, `Res_time`, `HYBAS_L12`, `HYRIV_RCH` 等）<br>- 后续按中国及近邻区域（按 `Country` 或空间裁剪）派生 `*_china_core.parquet` | - 阶段 C：与 0.1° 网格叠加，计算每格 `Vlake`, `Vres`，用于 $k_{ret}$、$\tau$ 估算 |
| HydroBASINS / hybas_lake / pour points | `hybas_lake_as_lev10_v1c.shp` 等 | 视需求 | **阶段 B 开始前后** | - 验证 `HYBAS_ID`, `PFAF_ID`, `NEXT_DOWN` 拓扑<br>- 可只保留中国及相关主流域<br>- 存为 `hybas_lev10_china_core.parquet` | - 阶段 B/E：用于构建流域级 DAG，辅助河网拓扑、终端汇水点判断（出海/内流等） |

### 7.2 阶段 A 内部的预处理优先级建议

在阶段 A 中，可以按下面顺序逐步推进预处理（避免一上来就“全数据开干”）：

1. **优先级 1：HSWUD（当前任务）**  
    - 目标：`hswud_0p1_annual.parquet`。  
    - 完成后即可支撑 $f_{WTA}$、用水相关分析。

2. **优先级 2：河网与流域的核心子集（轻量标准化）**  
    - HydroRIVERS → `rivers_china_core.parquet`  
    - RiverATLAS → `riveratlas_china_core.parquet`  
    - BasinATLAS（选一个合理层级，如 lev10）→ `basins_lev10_china_core.parquet`  
    - 目标：为阶段 B 的“0.1° 网格与河网对接”提供干净输入。

3. **优先级 3：湖泊/水库子集（为体积与速率原型做准备）**  
    - HydroLAKES / LakeATLAS → `lakeatlas_china_core.parquet`。  
    - 可以在开始做“体积与速率原型（试点流域）”之前、或者同时进行。

4. **优先级 4：HydroBASINS / pour points**  
    - 若在网格/河网拓扑构建中需要 Pfafstetter 编码和流域级 DAG，再针对性地为中国区域做裁剪和字段筛选。  

> 小结：阶段 A 只做“一次性的、可复用的轻量标准化预处理”（统一 CRS、空间范围、单位、字段子集，并存入 `data/processed/`）；真正绑定到 0.1° 网格、计算 k 参数、构建传输矩阵的派生处理，放在阶段 B–E 按任务推进。
