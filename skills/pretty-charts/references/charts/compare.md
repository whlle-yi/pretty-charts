# compare

## 比较类


> 核心问题："谁大谁小、大多少"。视觉通道首选**长度**（条形/柱状），其次位置（点图）。
> **横切规范只在本技能 `references/common.md` 定义一次**：红线九条见 [`../common.md`](../common.md)，取色见 [`../common.md`](../common.md)，字体字号见 [`../common.md`](../common.md)，尺寸导出与落盘见 [`../common.md`](../common.md)。本文件**只列本图型特有规范**，不复述上述任何内容。

### 图型清单

| 图型 | 适用 | 关键规范 |
|---|---|---|
| 排序条形图 | 类别名较长、比大小（首选） | 数值**降序排列**；非重点系列用中性灰弱化 |
| 柱状图 | 类别名短（≤4 字）、类目少（≤8） | y 轴从 0 开始（红线）；柱宽 > 间距 |
| 分组柱状图 | 类别 × 多系列（系列 ≤3） | 组内柱紧贴、组间留白明显；图例顶部横排 |
| 堆叠条形（单条 100%） | 比构成占比（见本文件「构成类」） | — |
| 点图（dot plot） | 数值跨度大、或要看区间 | 从 0 起点约束消失，可用截断轴但须标注 |
| 雷达图 | 多维综合评分，**慎用** | 轴 ≤8、系列 ≤2、刻度统一；能不用就不用 |

### 画法骨架

骨架省略公共三件套：`plt.rcParams.update(plt.rcParamsDefault)` → `plt.style.use(<技能根>/references/assets/matplotlib/<档位>.mplstyle)` → 色值一律从 `palettes/<档位>.json` 读。完整可运行版见本节末尾的示例脚本。

#### 排序条形图

```python
order = sorted(zip(cats, vals), key=lambda kv: kv[1])   # y 轴自下而上 → 升序排
cats, vals = [c for c, _ in order], [v for _, v in order]
fig, ax = plt.subplots(figsize=(4.8, 0.55 * len(cats) + 1.0))
bars = ax.barh(cats, vals, height=0.62, color=PAL["primary"])
bars[vals.index(max(vals))].set_color(PAL["accent"])     # 最突出一项换强调色，其余保持主色
for y, v in enumerate(vals):                             # 条端直标数值，x 轴刻度整体删去
    ax.text(v + max(vals) * 0.02, y, f"{v:,.0f}",
            va="center", fontsize=9, color=PAL["text"]["tick"])
ax.set_xlim(0, max(vals) * 1.15)                         # 留出标注空间
ax.set_xticks([])
```
身份元素：按值排序、条端直标 + 隐藏 x 轴、强调色只给最突出一项。按数据调整：figsize 高度随类别数伸缩；标注格式随数据域加单位；出现负值时零基线画实线加粗。

#### 哑铃图

```python
for i, (a, b) in enumerate(zip(v24, v25)):               # 一行 = 一类别
    color = PAL["accent"] if i == star else PAL["primary"]
    ax.plot([a, b], [i, i], color=color, lw=2.2, solid_capstyle="round", zorder=2)
    ax.scatter(a, i, s=42, facecolor=PAL["background"],
               edgecolor=PAL["text"]["tick"], linewidth=1.1, zorder=3)   # 旧值空心
    ax.scatter(b, i, s=52, color=color, zorder=3)                          # 新值实心
    ax.text(b + 22, i, f"+{b - a}", va="center", fontsize=8, color=color)  # 增量直标
ax.set_yticks(range(len(names)), names)
```
身份元素：线连两时点、旧空心/新实心、增量直标在端点旁。按数据调整：xlim 两端各留标注空间；增量最大项用强调色。

#### 分组柱状图

```python
x = np.arange(len(groups)); width = 0.36
b1 = ax.bar(x - width / 2, y2024, width, label="2024", color=PAL["neutral"])  # 对照年份灰
b2 = ax.bar(x + width / 2, y2025, width, label="2025", color=PAL["primary"])
ax.bar_label(b2, fmt="%d", padding=2)                    # 只标关键系列，防拥挤
ax.set_ylim(0, max(y2025) * 1.22)                        # 柱状从 0 起 + 标注余量
ax.legend(loc="upper center", ncols=2)
```
身份元素：对照系列 neutral 灰、关键系列主色、只标关键系列数值。按数据调整：width 随系列数反比；系列 >3 拆小倍数。

### 必守规范

1. **排序**：条形/柱状默认按数值排序（时间序列除外）。字母序/乱序是最常见的错误。
2. **强调用色**：最重要的系列用主题主色，其余用 `neutral` 灰；"万绿丛中一点红"比十个颜色更醒目。
3. **直接标注数值**：T2/T3 档在柱顶标数值（千分位、去尾零）；T1 档如标注则字号 ≥7pt。
4. **类别数超限**：>8 根柱改条形图（横向放长类目名）；>15 类考虑 Top-N + "其他"。
5. 负值存在时：零基线画实线并加粗，正负分色（diverging 语义）。

### 常见错误

- ❌ 不排序的柱状图（读者被迫自己找最大值）
- ❌ 3D 柱状图（透视使前排柱显得更高，双重失真）
- ❌ 双色渐变柱（每根柱颜色不同但颜色无含义）
- ❌ 用柱状图画均值 ± 标准差（应改点图 + 误差棒，见 `charts/inference.md`）

### 示例

`examples/data/comparison/sorted_bar.py`（**哑铃图**：两时点 × 多类别，线长即变化量、端点直标；文件名为历史遗留）、`examples/data/comparison/grouped_bar.py`（分组柱）

---

## 构成类


> 核心问题："整体由哪些部分组成、各占多少、构成怎么变化"。
> **横切规范只在本技能 `references/common.md` 定义一次**：红线九条见 [`../common.md`](../common.md)，取色见 [`../common.md`](../common.md)，字体字号见 [`../common.md`](../common.md)，尺寸导出与落盘见 [`../common.md`](../common.md)。本文件**只列本图型特有规范**，不复述上述任何内容。

### 图型清单

| 图型 | 适用 | 关键规范 |
|---|---|---|
| 堆叠柱状图 | 构成 × 类别（绝对量） | 底块最重要（最易比较）；系列 ≤5 |
| 100% 堆叠柱 | 只关心占比不关心总量 | 每块直接标百分比；小到放不下就不标（示例阈值 ≥8%，见 `examples/data/composition/stacked_bar.py`） |
| 堆叠面积图 | 构成随时间变化 | y 轴从 0；系列 ≤4；波动大的不用 |
| 环图（donut） | 静态构成、块数 ≤5 | 中心放总量或关键指标；从 12 点起、按大小顺时针 |
| 饼图 | 同环图，能用环就不用饼 | 块数 ≤5；禁止 3D；差值小的相邻块避开相似色 |
| 瀑布图 | 增减分解（财务、预算） | 起点/终点实心，增减用 diverging 语义色 |
| 漏斗图 | 分阶段转化（注册→付费） | 阶段 ≤6；每阶段标绝对数与转化率；首阶段是分母，不按部分-整体解读 |
| 树图（treemap） | 层级构成（见 `charts/structure.md`） | 面积 ∝ 数值；标签防溢出 |

### 饼图/环图六规则（违反任一就换堆叠柱）

1. 块数 ≤5，超过必然读不动。
2. 从 12 点钟方向开始，按数值降序顺时针排列。
3. 每块直接标注（名称+百分比），不用小图例让读者对色找块。
4. 相邻两块差值 <3 个百分点时，颜色深浅必须明显不同（角度差人眼读不出）。
5. 禁止 3D、阴影、爆炸效果（透视扭曲角度）。
6. 有负值或合计 ≠100% 时禁用饼图。

### 画法骨架（构成类）

#### 堆叠柱状图

```python
bottom = np.zeros(len(quarters))
for (name, vals), c in zip(parts.items(), palette):      # 底块最易比较 → 主色，越往上越次要
    ax.bar(quarters, vals, bottom=bottom, label=name, color=c, width=0.55)
    for i, (v, b) in enumerate(zip(vals, bottom)):
        if v / totals[i] * 100 >= 8:                     # <8% 的块不放文字，防溢出
            ax.text(i, b + v / 2, f"{v / totals[i] * 100:.0f}%",
                    ha="center", va="center", fontsize=8, color=块内文字色)
    bottom += vals
for i, t in enumerate(totals):                           # 柱顶标总量
    ax.annotate(f"{t:,.0f}", (i, t), xytext=(0, 3), textcoords="offset points",
                ha="center", fontsize=9, fontweight="bold")
```
身份元素：块内占比直标（<8% 略去）、柱顶总量、底块用主色。按数据调整：块内文字色按底色亮度自动选深/浅；系列 ≤5。

#### 环图

```python
wedges, _ = ax.pie(vals, startangle=90, counterclock=False,     # 12 点起、顺时针、按值降序
                   colors=[PAL["primary"], *PAL["categorical"][1:4]],
                   wedgeprops={"width": 0.42, "edgecolor": PAL["background"], "linewidth": 2})
for w, name, v in zip(wedges, names, vals):              # 每块外侧直标：名称 + 占比
    ang = (w.theta1 + w.theta2) / 2
    x, y = np.cos(np.deg2rad(ang)) * 1.1, np.sin(np.deg2rad(ang)) * 1.1
    ax.annotate(f"{name} {v / total * 100:.0f}%", (x, y), ha="center", fontsize=9)
ax.text(0, 0.06, f"{total:,.0f}", ha="center", fontsize=15, fontweight="bold")   # 中心放总量
ax.text(0, -0.16, "单位说明", ha="center", fontsize=8, color=PAL["subtext"])
```
身份元素：中心总量、块外侧直标、缺口宽度 0.4 上下。按数据调整：相邻块占比差 <3 个百分点时拉开色深。

#### 雷达图（替代方案都被否后，确需多维画像对比再用）

```python
cats = ["可靠性", "成本", "易用性", "性能", "扩展性"]     # 轴 ≤8
N = len(cats)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
angles = np.concatenate([angles, angles[:1]])            # 多边形闭合：重复第一个点（最经典的坑，不闭合图会缺口）
fig, ax = plt.subplots(figsize=(4.2, 4.2), subplot_kw={"polar": True})
for name, vals, color in series:                         # 系列 ≤2
    v = np.concatenate([vals, vals[:1]])                 # 数据同样闭合
    ax.plot(angles, v, color=color, lw=1.6, label=name)
    ax.fill(angles, v, color=color, alpha=0.15)          # 填充透明，防互相遮挡
ax.set_xticks(angles[:-1], cats, fontsize=9)             # 类别名在轴端，过长换行防重叠
ax.set_ylim(0, 100)                                      # 各系列共用同一刻度
ax.grid(alpha=0.4)
ax.spines["polar"].set_visible(False)
ax.legend(loc="lower right", ncols=2, fontsize=8)
```
身份元素：多边形闭合（首点重复）、统一 0–100 刻度、系列 ≤2 且填充透明。按数据调整：T1 印刷场景雷达图灰度后几乎必然难辨——这正是它被标慎用的原因，动笔前再确认一次。

### 必守规范

- **堆叠图的分量比较陷阱**：堆叠柱中只有最底下的块能直接比大小（上方块底部不齐）。要比较上方分量：改小倍数图或换主题色标线。
- **占比与绝对量分开表达**：既有关总量又有构成 → 堆叠柱（绝对）+ 旁边或标签给百分比；只有百分比 → 100% 堆叠。
- 时间轴上：构成变化用堆叠面积/堆叠柱，**不用并排多饼图**（人眼无法跨饼比较角度）。

### 常见错误

- ❌ 饼图比较 7、8 个成分
- ❌ 堆叠面积图里中间系列忽高忽低被误读为"该系列变化大"（其实是底下系列在变）
- ❌ 两个 3D 饼图并排"对比"

### 示例

`examples/data/composition/stacked_bar.py`（堆叠柱+百分比标注）、`examples/data/composition/donut.py`（环图，中心总量）
