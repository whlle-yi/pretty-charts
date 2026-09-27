# python

## 工具栈：matplotlib 生态


> 适用 T1/T2 静态出版级与报告级出图。选型：**pandas.plot 快速探索 → seaborn 统计图 → matplotlib 手工精修 → plotly 需要交互时**。
> **横切规范只在本技能 `spec/` 定义一次**（红线 [`../spec.md`](../spec.md)、取色 [`../spec.md`](../spec.md)、字体 [`../spec.md`](../spec.md)、尺寸与落盘 [`../spec.md`](../spec.md)）；本文件**只讲本工具栈的用法与坑**，不复述上述内容。

### 0. 主题加载（每个脚本第一件事）

```python
from pathlib import Path
import matplotlib.pyplot as plt

SKILL_ROOT = Path(__file__).resolve().parents[3]   # examples/<类>/<图型>/x.py → 技能根，按脚本层级调整
STYLE = SKILL_ROOT / "references" / "style" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")   # 或 business / showcase
```

主题已内置：字体回退链、字号层级、色板循环、网格、去顶右刺、导出参数。**不要在代码里硬编码这些常量**；个别覆盖用临时 rcParams 并注释原因。

### 1. 库选择决策

| 场景 | 用什么 | 理由 |
|---|---|---|
| DataFrame 快速探索 | `df.plot()` | 一行出图，细节后续再修 |
| 分布/回归/分面等统计图 | seaborn | `histplot/kdeplot/boxplot/violinplot/regplot/lmplot/catplot` 自带统计语义 |
| 出版级精修、非常规图 | 纯 matplotlib OO 接口 | `fig, ax = plt.subplots()` 后全部 `ax.*`，不用 pyplot 状态机 |
| 交互探索（notebook） | plotly | hover、缩放 |
| 3D | matplotlib mplot3d 仅在必须时 | 大多数 3D 图该改成 2D 投影/分面 |

### 2. 高频配方

```python
# 数值标注（千分位、防重叠）
ax.bar_label(bars, fmt=lambda v: f"{v:,.0f}", padding=2)

# 直接标注线端（代替图例）
for name, y in series.items():
    ax.annotate(name, (x[-1], y[-1]), xytext=(6, 0), textcoords="offset points", va="center")

# 日期轴：自动稀疏刻度
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

# 千分位 y 轴
from matplotlib.ticker import FuncFormatter
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))

# 相关矩阵热图（diverging、中心 0）
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
fig.colorbar(im, ax=ax, shrink=0.8)

# 抖动散点叠加箱线（分布个体可见）
ax.boxplot(data, positions=..., showfliers=False)
ax.scatter(xs + jitter, vals, s=8, alpha=0.5, zorder=3)

# 共享图例置顶（多子图）
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc="outside upper center", ncols=len(labels))
```

### 3. 布局与导出

- 用 `fig.subplots_adjust`/`constrained_layout=True` 防标签裁切；保存默认 `bbox_inches="tight"`（主题已设）。
  **T1 投稿例外**：期刊要求精确栏宽时，`tight` 会裁掉留白、使成品宽度不再等于 `figsize`，投出去被缩放排版就会连带改变等效字号（可能跌破 7pt 下限）——此时 `plt.rcParams["savefig.bbox"] = None` 恢复固定画布，再用 `subplots_adjust` 留足边距。注意 `savefig(bbox_inches=None)` **不是**关闭它，而是“沿用 rcParams”（详见 `spec/`../spec.md` §画布、尺寸、导出与落盘` §2.5）。
- 子图共享轴必须 `sharex/sharey=True`；比较类子图 y 轴范围必须一致。
- 导出：`fig.savefig("name.pdf")` 矢量（T1 首选）、`fig.savefig("name.png")` 按 DPI 主题；**先 savefig 再 plt.close**。
- 图内中文与负号已由主题处理（Noto Sans SC + `axes.unicode_minus: False`）。

### 4. T1 出版级附加检查

> 期刊规格速查、SciencePlots 集成、Crameri 色图标准、多面板规范与退稿清单见 [`../spec.md` §T1 期刊规格](`../spec.md` §T1 期刊规格)；本节只列与 matplotlib 操作直接相关的检查。

- 字号 ≥7pt：缩小图后用 `fig.canvas.draw()` 后检查实际渲染，别只看代码参数。
- 灰度打印可辨：系列叠加线型/标记（linestyle + marker）冗余编码。
- 图注自含：n、统计口径、误差类型、显著性标注定义，全在 caption。
- 投稿要求单栏 90mm/双栏 190mm 时**按 mm 换算 figsize**（mm/25.4），不要凭感觉。

### 5. 已知坑（本仓库已替你处理，换环境时注意）

1. mplstyle 文件里 `#` 是行内注释 → 颜色写 RGB 元组，不写十六进制。
2. mplstyle 里循环色键名必须 `axes.prop_cycle`（下划线）；点号形式报 Bad key。
3. 中文字体在 Linux 服务器缺失 → 先装 fonts-noto-cjk，否则豆腐块。
4. seaborn 新版本用 `hue` 传系列后 legend 位置需手工收（`sns.move_legend`）。
5. **Noto Sans SC 是可变字体，matplotlib 导出的 PDF 子集经 Ghostscript 渲染会丢字形**（PDF 在 Adobe/浏览器中正常，但出版系统的 gs 管线会翻车）——需经 gs 转图或投给 gs 基管线的期刊时，把静态字体 Microsoft YaHei 提到回退链首位：`sans = rcParams["font.sans-serif"]; sans.insert(0, "Microsoft YaHei")`。实战案例见 `examples/data/paper/make_paper_figures.py` 的 `gs_safe_fonts()`。
