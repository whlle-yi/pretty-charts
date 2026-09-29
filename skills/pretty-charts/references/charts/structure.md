# structure

## 层次与网络类


> 核心问题："结构怎么组织、量怎么在结构间流动"。**与 diagram 分工**：本文件处理有数值编码的图（流量大小、节点权重）；纯结构表达（流程图、组织架构）走 `diagrams.md`。
> **横切规范只在本技能 `references/common.md` 定义一次**：红线九条见 [`../common.md`](../common.md)，取色见 [`../common.md`](../common.md)，字体字号见 [`../common.md`](../common.md)，尺寸导出与落盘见 [`../common.md`](../common.md)。本文件**只列本图型特有规范**，不复述上述任何内容。

### 图型清单

| 图型 | 适用 | 关键规范 |
|---|---|---|
| 树图（treemap） | 层级 + 数量构成（预算、磁盘、销售） | 面积 ∝ 数值；层级 ≤3；标签防溢出（放不下就留白+图注） |
| 桑基图（sankey） | 流量分解/迁移（渠道转化、能源流向） | 左源右汇；节点排序防边交叉；流量守恒要直观 |
| 弦图（chord） | 双向/成对流量（贸易、迁移） | 两侧弧段排序对齐；边 ≤30 |
| 力导向网络图 | 图结构（关系网、引用网） | 节点大小 ∝ 度数/权重；边 >500 先聚合社区（着色） |
| 河流图（streamgraph / alluvial） | 时期 × 构成的流动 | 类别 ≤6 |
| 上下游/依赖图 | 有向依赖 + 量 | 分层布局（hierarchical），防环路交叉 |
| UpSet 图 / 韦恩图 | 集合交集的规模 | >3 个集合必须用 UpSet（按交集大小排序）；韦恩仅限 ≤3 集合，且面积不编码数值 |

### 画法骨架

#### 树图（squarify）

```python
fig, ax = plt.subplots(figsize=(7.0, 4.2))
fig.canvas.draw()                                        # 先取坐标区真实宽高比
box = ax.get_window_extent()
W, H = 100.0, 100.0 * box.height / box.width             # 方块才不会被拉成长条
rects = squarify.squarify(squarify.normalize_sizes(sizes, W, H), 0, 0, W, H)
for (name, v), r, c in zip(items, rects, palette):       # 面积 ∝ 数值
    ax.add_patch(Rectangle((r["x"], r["y"]), r["dx"], r["dy"]),
                 facecolor=c, edgecolor=PAL["background"], linewidth=2)
    if r["dx"] > 0.18 * W and r["dy"] > 0.15 * H:        # 大块：名称 + 数值
        ax.text(cx, cy, f"{name}
{v / total * 100:.0f}%", ha="center", color=块内文字色)
    elif r["dx"] > 0.08 * W:                             # 中块：只放名称；小块留白
        ax.text(cx, cy, name, ha="center", fontsize=9)
ax.set_xticks([]); ax.set_yticks([])                     # spines 全关
```
身份元素：面积 ∝ 数值、按块大小分级标注、块间背景色描边。按数据调整：块内文字色按底色亮度自动选深/浅；层级 ≤3。

### 必守规范

1. **布局交给算法，不许手工摆点**：treemap 用 squarify，网络用 force/FR 布局，桑基自动排节点；手工摆放必然失真。
2. **数量编码一致**：节点大小、边宽都 ∝ 数值，且同一张图内只用一种比例规则，图注说明。
3. 边的数量克制：>30 条边先按流量排序取 Top-N 或聚合为"其他"。
4. 交互优先：桑基/网络在 T2/T3 网页交付（ECharts）体验远优于静态图，节点 hover 给数值。
5. 颜色：节点按社区/类别取 categorical；边用透明主色（alpha 0.3–0.5），防"毛线团"。

### 常见错误

- ❌ 力导向图 500 条边不做聚合（视觉噪声，无信息）
- ❌ treemap 面积不按数值（按栅格数），层级颜色随机
- ❌ 桑基节点顺序随意导致边大面积交叉
- ❌ 把网络图画进饼图（"占比"与"结构"混用）

### 示例

`examples/data/network/`：`make_treemap.py`（树图，面积 ∝ 数值）。桑基、弦图、力导向网络尚无示例，后续补充
