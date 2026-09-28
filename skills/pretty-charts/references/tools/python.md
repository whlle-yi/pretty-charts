# python

## 工具栈：matplotlib 生态


> 适用 T1/T2 静态出版级与报告级出图。选型：**pandas.plot 快速探索 → seaborn 统计图 → matplotlib 手工精修 → plotly 需要交互时**。
> **横切规范只在本技能 `references/common.md` 定义一次**（红线 [`../common.md`](../common.md)、取色 [`../common.md`](../common.md)、字体 [`../common.md`](../common.md)、尺寸与落盘 [`../common.md`](../common.md)）；本文件**只讲本工具栈的用法与坑**，不复述上述内容。

### 0. 主题加载（每个脚本第一件事）

```python
from pathlib import Path
import matplotlib.pyplot as plt

SKILL_ROOT = Path(__file__).resolve().parents[3]   # examples/<类>/<图型>/x.py → 技能根，按脚本层级调整
STYLE = SKILL_ROOT / "references" / "assets" / "matplotlib"
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
  **T1 投稿例外**：期刊要求精确栏宽时，`tight` 会裁掉留白、使成品宽度不再等于 `figsize`，投出去被缩放排版就会连带改变等效字号（可能跌破 7pt 下限）——此时 `plt.rcParams["savefig.bbox"] = None` 恢复固定画布，再用 `subplots_adjust` 留足边距。注意 `savefig(bbox_inches=None)` **不是**关闭它，而是“沿用 rcParams”（详见 [`../common.md`](../common.md)「画布、尺寸、导出与落盘」§2 第 5 条）。
- 子图共享轴必须 `sharex/sharey=True`；比较类子图 y 轴范围必须一致。
- 多面板：组合用 `fig.subplot_mosaic` 或 GridSpec；面板标签小写粗体 a/b/c，放坐标区左上角外侧（`transform=ax.transAxes`，约 `(-0.18, 1.06)`）；面板间距不小于标签高度；共享色标放子图外侧一次，不要每个面板各放一个；caption 与面板一一对应。
- 导出：`fig.savefig("name.pdf")` 矢量（T1 首选）、`fig.savefig("name.png")` 按 DPI 主题；**先 savefig 再 plt.close**。
- 图内中文与负号已由主题处理（Noto Sans SC + `axes.unicode_minus: False`）。

### 4. T1 出版级附加检查

> 期刊规格速查、SciencePlots 集成、Crameri 色图标准与退稿清单见下节；本节只列与 matplotlib 操作直接相关的检查。

- 字号 ≥7pt：缩小图后用 `fig.canvas.draw()` 后检查实际渲染，别只看代码参数。
- 灰度打印可辨：系列叠加线型/标记（linestyle + marker）冗余编码。
- 图注自含：n、统计口径、误差类型、显著性标注定义，全在 caption。
- 投稿要求单栏 90mm/双栏 190mm 时**按 mm 换算 figsize**（mm/25.4），不要凭感觉。

### 5. T1 期刊规格与退稿清单

> 来源：SciencePlots、Rougier《Scientific Visualisation: Python + Matplotlib》、Scientific Colour Maps（Crameri, *Nat. Commun.* 2020，使用需引用）与各期刊投稿要求。本节是 T1 数据图的期刊适配层，不替代本仓库主题。

#### 1. 期刊规格速查

| 期刊/出版社 | 单栏 | 双栏 | 位图 DPI | 图内字号 |
|---|---|---|---|---|
| Nature 系列 | 89mm | 183mm | 300（线图矢量） | 缩放后 5–7pt |
| IEEE | 88.9mm（3.5in） | 181.6mm（7.16in） | ≥600 | 缩放后 ≥8pt |
| Elsevier | 90mm | 190mm | 300（矢量优先） | ≥7pt |
| ACS | ≈82.6mm | ≈177.8mm | 300–600 | ≥4.5pt（建议 ≥7） |

**以当期 Guide for Authors 为准**——上表是快速起点。通用硬规则：**缩放打印后**字号 ≥6pt、线宽 ≥0.5pt；先按栏宽设 figsize，再定字号，顺序不能反。

#### 2. SciencePlots 配合使用（期刊仿真）

```python
import matplotlib.pyplot as plt
import scienceplots                      # pip install SciencePlots

plt.style.use(["science", "no-latex",    # science 默认 usetex=True，缺 LaTeX/中文配置会报错
               str(SKILL_ROOT / "references/assets/matplotlib/academic.mplstyle")])
```

- `science` 是主样式（细框、无顶右刺、窄栏宽）；`ieee`（3.5in 栏宽、衬线）、`nature`（无网格）等变体叠加在后覆盖前者；
- 与本仓库主题叠加时，**本仓库主题写在最后**（取色与字体纪律保持，SciencePlots 只负责期刊尺寸与默认细节）；
- 无 LaTeX 环境永远带 `no-latex`。

#### 3. 色图标准（Scientific Colour Maps）

感知均匀色图已是出版界事实标准：

- **禁用** jet / rainbow / hsv：感知不均匀、色盲不友好、黑白打印产生虚假条纹；
- **顺序数据**：viridis / cividis / magma（matplotlib 内置），或 Crameri `batlow`（`pip install cmcrameri` → `import cmcrameri.cm as cmc; cmap="cmc.batlow"`，用属性而非 `mpl.colormaps["…"]`）；
- **发散数据**：RdBu_r / coolwarm，或 Crameri `vik` / `roma`（中心必须对齐语义零点）；
- **循环数据**（角度、周期）：twilight_shifted 或 Crameri `romero`——顺序色图画循环数据会在 0/360 处产生虚假断崖；
- 色盲自检：交付前用色盲模拟（colorspacious 或系统工具）过一遍，或直接用 cividis/batlow 这类天然安全的。

#### 4. 细节退稿清单（审稿人常挑）

1. **字体未嵌入**：PDF 用 `pdffonts` 检查，非内嵌字体（TrueType 以外）会被出版系统打回——主题已设 fonttype 42，勿覆盖；
2. **该矢量的用了位图**：线图/柱状/散点一律 PDF/EPS 矢量；仅热图、>1 万点散点、图像用位图且 ≥600dpi（主题 savefig.dpi 已按档位设置）；
3. **标签重叠**：密数据标签用 `adjustText` 库（`pip install adjustText`）自动避让，不许手工挪了事；
4. **量级记法**：轴用 ×10ⁿ 标注（`ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 3))`），不出现 1e6 裸记数；SI 词头优先（μ、m、k）；
5. **图例压数据**：图例置顶框外或线端直标；误差棒类型（SD/SE/95%CI）在图注明示；
6. **usetex 与正文不一致**：中文期刊或中文图注慎用 `text.usetex`（中文配置繁琐且易与模板冲突），用 no-latex + 主题字体即可；
7. **一图一信息**：panel 数量克制（≤6），超了拆图；每张图在正文中必须被引用和讨论。

### 6. 已知坑（本仓库已替你处理，换环境时注意）

1. mplstyle 文件里 `#` 是行内注释 → 颜色写 RGB 元组，不写十六进制。
2. mplstyle 里循环色键名必须 `axes.prop_cycle`（下划线）；点号形式报 Bad key。
3. 中文字体在 Linux 服务器缺失 → 先装 fonts-noto-cjk，否则豆腐块。
4. seaborn 新版本用 `hue` 传系列后 legend 位置需手工收（`sns.move_legend`）。
5. **Noto Sans SC 是可变字体，matplotlib 导出的 PDF 子集经 Ghostscript 渲染会丢字形**（PDF 在 Adobe/浏览器中正常，但出版系统的 gs 管线会翻车）——需经 gs 转图或投给 gs 基管线的期刊时，把静态字体 Microsoft YaHei 提到回退链首位：`sans = rcParams["font.sans-serif"]; sans.insert(0, "Microsoft YaHei")`。实战案例见 `examples/data/paper/make_paper_figures.py` 的 `gs_safe_fonts()`。
