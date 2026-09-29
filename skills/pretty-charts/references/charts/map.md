# map

## 地理空间类


> 核心问题："空间上哪里强哪里弱、怎么流动"。本质 = 地图底座 + 数据编码。
> **横切规范只在本技能 `references/common.md` 定义一次**：红线九条见 [`../common.md`](../common.md)，取色见 [`../common.md`](../common.md)，字体字号见 [`../common.md`](../common.md)，尺寸导出与落盘见 [`../common.md`](../common.md)。本文件**只列本图型特有规范**，不复述上述任何内容。

### 图型清单

| 图型 | 适用 | 关键规范 |
|---|---|---|
| 分级统计地图（choropleth） | 行政区 × 比率指标（人均、密度、率） | **必须用比率，不用绝对数**；sequential 色板；图例（色标）必备 |
| 比例符号地图（proportional symbol） | 行政区 × 绝对量 | 面积 ∝ 数值（半径 ∝ √值）；重叠用透明+描边 |
| 双变量地图 | 两个指标叠加（率 × 数量） | 谨慎：图例必须能自解释，否则拆两张 |
| 流向/迁移地图 | 空间流量 | 边宽 ∝ 流量；弧线弯曲统一方向 |
| 小倍数地图 | 多指标/多时期空间对比 | 共享色标（统一 legend 范围），否则不可比 |
| 密度热力图 | 点事件密度（POI、事故） | sequential；底图去饱和不抢数据 |

### 画法骨架

#### 分级统计地图（choropleth）

```python
fig, ax = plt.subplots(figsize=(3.54, 2.75))             # 90mm 单栏
gdf.plot(column="ratio", cmap=CMAP, norm=NORM, ax=ax,
         missing_kwds={"color": PAL["missing"]},         # 无数据区灰，勿用色板浅端
         edgecolor="white", linewidth=0.4)               # 白色细界线防区块粘连
cb = fig.colorbar(ScalarMappable(norm=NORM, cmap=CMAP), ax=ax,
                  fraction=0.032, pad=0.01)              # 色标必备
cb.set_label("人/百万人", fontsize=8)
ax.set_axis_off()
```
身份元素：比率指标 + 顺序色图 + 色标 + 灰底缺失区。按数据调整：分级数 5–7 并注明分级方法；中国地图用标准投影并声明。

### 必守规范

1. **choropleth 用比率不用绝对数**：绝对数上色 = 把"面积大"画成"数值大"（人口地图变成面积地图）。绝对量用比例符号。
2. **色标必须连续可见**：无图例的地图不可用；分级地图分级数 5–7，分级方法注明（等间距/分位数/自然断点 Jenks）。
3. **零/缺失区分**：无数据区域用灰色，不用色板最低色（最低色是"低"，不是"没有"）。
4. **投影声明**：中国地图用标准投影（如 Albers/Gauss-Krüger），Web 用 Web Mercator 并知晓其高纬面积膨胀；图注标注投影。
5. 全圆色板（rainbow）禁用；发散指标（对全国均值偏离）用 diverging。

### 常见错误

- ❌ GDP 总量 choropleth（广东永远最深，信息量为零）
- ❌ 无色标、无分级的"彩色地图"
- ❌ Web Mercator 上比较面积（格陵兰 ≈ 非洲的错觉）
- ❌ 地图色彩饱和度过高压过底图/边界

### 工具

- Python：geopandas + matplotlib（T1/T2 静态）、plotly choropleth（交互）
- 前端：ECharts（内置中国/世界地图 JSON）、D3 + topojson（T3）
- 注意地图边界合规：公开交付使用自然资源部标准地图服务的边界数据，不可用来源不明的边界文件

### 示例

`examples/data/geo/`：`make_geo_figures.py`（choropleth + 比例符号 + 小倍数三图）、`fig1–3.pdf` 与 `fig1_preview.png`、`paper_embedded_geo.tex`（论文内嵌）。底图用随仓库分发的 `naturalearth_lowres.geojson`（Natural Earth 1:110m，公有领域，离线可用），不依赖 `geopandas.datasets`（geopandas 1.0 已移除该模块）
