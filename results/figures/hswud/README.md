# HSWUD 2010–2020 年平均用水空间分布图说明

本文件夹存放基于 HSWUD 数据集（dom/ele/irr/manu 四个行业）计算的 **2010–2020 年多年平均用水** 的空间分布图，用于快速检查数据合理性和向他人展示结果。

生成脚本：`scripts/analysis/plot_hswud_maps.py`

使用的数据：`data/processed/water_use/hswud_0p1_2010_2020_mean_clean.nc`

---

## 1. 图像列表与含义

本目录目前包含以下图像文件（PNG）：

- `hswud_dom_2010_2020_mean.png`
  - **生活用水（domestic）**多年平均空间分布图。
  - 每个 0.1° 网格的数值来自 HSWUD 中 domestic 部门 2010–2020 年间的年均取水量，单位为 m³/year，经对数变换后可视化。

- `hswud_ele_2010_2020_mean.png`
  - **电力用水（electricity）**多年平均空间分布图。
  - 反映电力生产相关的取水在空间上的分布和强度。

- `hswud_irr_2010_2020_mean.png`
  - **灌溉用水（irrigation）**多年平均空间分布图。
  - 往往在农田密集、灌溉发达区域呈现高值（例如华北平原、新疆绿洲灌区等）。

- `hswud_manu_2010_2020_mean.png`
  - **工业/制造业用水（manufacturing）**多年平均空间分布图。
  - 反映制造业活动的空间集聚，通常在发达工业带、城市群附近较高。

- `hswud_total_2010_2020_mean.png`
  - **总用水量（total）**多年平均空间分布图：
    $$q_{\text{total}} = q_{dom} + q_{ele} + q_{irr} + q_{manu}$$
  - 可以用来快速识别全国范围内用水压力较高的区域，是后续计算水量压力指标（如 $f_{WTA}$）的重要输入之一。

上述所有图均使用相同的颜色刻度（基于对数刻度的 5%–99% 分位），方便跨行业比较空间分布模式。

---

## 2. 数据来源与预处理简要说明

### 2.1 数据来源

- 原始数据：`data/water use data/27610524/HSWUD_*.nc`
  - HSWUD 数据集提供了 1965–2022 年的 0.1° 网格月尺度行业取水量，分为四个部门：
    - dom: 生活用水（domestic）
    - ele: 电力用水（electricity）
    - irr: 农业灌溉用水（irrigation）
    - manu: 工业/制造业用水（manufacturing）

- 边界数据：`data/boundary data/gadm41_CHN_shp/gadm41_CHN_0.shp`
  - 来自 GADM v4.1 的中国国家边界矢量数据，用于在图上叠加国界轮廓，便于识别地理位置。

### 2.2 预处理步骤（由 `hswud_aggregate.py` 完成）

1. **时间聚合（2010–2020 多年平均）**
   - 从原始 NetCDF 中读取 2010–2020 年间的月度数据。
   - 对所选时间段内的所有时间步进行求和，得到“该年段内总取水量”；
   - 根据模式 `mode="multi_year_mean"`，再将这一总量除以年数，得到**年平均取水量**（脚本中目前是通过总量直接表示该时段代表性年量）。

2. **单位统一与异常值处理**
   - 原始文件中 dom/irr/manu 的单位元数据为 `10^8 cubic meters`，ele 虽无单位标注，但数值量级与其他部门一致，因此约定四个部门数值均以 `10^8 m³` 为单位。
   - 在聚合过程中：
     - 所有部门统一乘以 $10^8$，得到单位为 `m³` 的体积；
     - 对极端负值（如 -1.7e308、-3.4e38 等）采用阈值过滤：
       $$ q < -10^{20} \Rightarrow \text{视为无效，记为 NaN} $$
     - 再将 NaN 视作“无数据”，在最终结果中填为 0（意味着该网格/时刻无用水或缺乏数据，不计入用水量）。
   - 聚合结果已确认：各列（dom/ele/irr/manu/total）均为非负，且不存在 inf 或 -inf。

3. **输出到 NetCDF**
   - 聚合后的结果被写入：
     - `data/processed/water_use/hswud_0p1_2010_2020_mean_clean.parquet`
     - `data/processed/water_use/hswud_0p1_2010_2020_mean_clean.nc`
   - NetCDF 文件采用维度结构：
     - `time`: 单值，代表 2010–2020 年间的多年平均（time 轴用于兼容 xarray 工作流）；
     - `lat`, `lon`: 0.1° 规则网格经纬度；
     - 数据变量：`q_dom_m3`, `q_ele_m3`, `q_irr_m3`, `q_manu_m3`, `q_total_m3`，单位均为 `m³/year`。

---

## 3. 绘图方法与颜色刻度

### 3.1 对数变换：为何使用 `log10(q + 1)`？

由于不同地点的用水量跨度很大（从接近 0 到约 $10^{10}$ m³/year），
如果直接以线性刻度绘制颜色图：

- 高用水区域会“亮爆”，低用水区域几乎不可见；
- 难以同时观察东部高值区和中西部低值区的细节。

为此，在绘图时对每个栅格的年用水量 $q$ 做了如下变换：

$$
\text{color value} = \log_{10}(q + 1)
$$

其中：
- $q$：原始年用水量，单位 $\mathrm{m^3\,year^{-1}}$；
- $+1$：避免对 0 取对数（$\log_{10}(0)$ 未定义），同时对大于 1 的值影响可以忽略；
- $\log_{10}$：以 10 为底的对数，使“每 10 倍差异”对应颜色上的一个大步长，更容易阅读。

**注意**：
- 图上的颜色数值并不是“直接的 m³/year”，而是 $\log_{10}(q+1)$；
- 但是这是一种**可逆的变换**，意味着每一种颜色仍然对应一个唯一的 $q$ 值，
  可以从 $\log_{10}(q+1)$ 反推回 $q$（近似为 $10^{x}$）。

颜色条标签在脚本中标记为：

> `log10(q + 1) [log10(m3/year)]`

含义可以理解为：

- 正在对“以 m³/year 为单位的用水量 $q$”进行 log10 变换；
- 颜色值的刻度是 $\log_{10}(q+1)$，其本身是无量纲的对数标度，
  但对应的原始物理量单位仍然是 m³/year。

### 3.2 颜色范围（vmin/vmax）

为了在各图之间保持可比性，脚本在计算颜色范围时：

1. 收集所有行业与总量变量在对数空间的值：
   $$ x = \log_{10}(q + 1) $$
2. 取其中有限值的第 5 个百分位和第 99 个百分位作为颜色刻度下/上限：
   - $v_\min = P_5(x)$
   - $v_\max = P_{99}(x)$

这样可以：

- 避免极个别极高值支配整个颜色范围；
- 又保留大部分区域的对比度；
- 且不同图（各行业和总量）使用同一对数刻度，便于视觉比较各行业的空间分布模式。

---

## 4. 如何在 Python 中重现或调整这些图？

### 4.1 重新运行现有脚本

在项目根目录下、激活虚拟环境后：

```bash
source cfcalculate/bin/activate
python -m scripts.analysis.plot_hswud_maps
```

脚本会：

- 重新读取 `hswud_0p1_2010_2020_mean_clean.nc`；
- 调用 `plot_hswud_maps()` 绘制并保存 5 张 PNG 图到本目录；
- 覆盖已有文件（方便迭代更新）。

### 4.2 在交互式环境中简单查看某个变量

示例：查看总用水量的原始线性值和对数值分布：

```python
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

path_nc = "data/processed/water_use/hswud_0p1_2010_2020_mean_clean.nc"

ds = xr.open_dataset(path_nc)
if "time" in ds.dims:
    da = ds["q_total_m3"].isel(time=0)
else:
    da = ds["q_total_m3"]

# 线性刻度（可能对比度不佳，但是真实值）
plt.figure(figsize=(8, 5))
plt.pcolormesh(da["lon"], da["lat"], da, shading="auto")
plt.colorbar(label="q_total_m3 [m³/year]")
plt.title("Total water use (linear scale)")
plt.show()

# 对数刻度（与本目录PNG类似）
plt.figure(figsize=(8, 5))
log_data = np.log10(da + 1.0)
plt.pcolormesh(da["lon"], da["lat"], log_data, shading="auto")
plt.colorbar(label="log10(q_total_m3 + 1)")
plt.title("Total water use (log10 scale)")
plt.show()
```

你可以根据需要修改变量名（例如 `q_dom_m3`、`q_irr_m3`），或者调整颜色映射和范围。

---

## 5. 如何在报告/文章中描述这些图？

在方法与结果章节中，可以类似这样描述：

> 使用 HSWUD 数据集（1965–2022 月尺度 0.1° 网格行业取水量），选取 2010–2020 年时间段，计算各网格与各行业的多年平均年取水量（单位 m³/year）。
> 为增强空间对比度，对每个网格的年取水量 $q$ 采用对数变换 $\log_{10}(q + 1)$ 进行可视化，其中 $q$ 的单位为 m³/year，$+1$ 用以避免零值的对数计算问题。图中颜色刻度基于 5%–99% 分位设置，以减少极端高值对整体颜色范围的影响。

这样既表达了图的数值基础（真实用水量），又解释了为何采用对数变换，有利于同行理解和复现。