# 论文数据图深化指南（paper-data）

> T1 数据图的出版级深化规范，补充 `style-guide.md` 与 `tool-matplotlib.md`。来源：SciencePlots（garrettj403，★9.3k）、Rougier《Scientific Visualisation: Python + Matplotlib》（★11.6k）、Scientific Colour Maps（Crameri）与各期刊投稿要求。

## 1. 期刊规格速查

| 期刊/出版社 | 单栏 | 双栏 | 位图 DPI | 图内字号 |
|---|---|---|---|---|
| Nature 系列 | 89mm | 183mm | 300（线图矢量） | 缩放后 5–7pt |
| IEEE | 88.9mm（3.5in） | 181.6mm（7.16in） | ≥600 | 缩放后 ≥8pt |
| Elsevier | 90mm | 190mm | 300（矢量优先） | ≥7pt |
| ACS | ≈82.6mm | ≈177.8mm | 300–600 | ≥4.5pt（建议 ≥7） |

**以当期 Guide for Authors 为准**——上表是快速起点，投稿前必须核对最新版。通用硬规则：**缩放打印后**字号 ≥6pt、线宽 ≥0.5pt；先按栏宽设 figsize，再定字号，顺序不能反。

## 2. SciencePlots 配合使用（期刊仿真）

```python
import matplotlib.pyplot as plt
import scienceplots                      # pip install SciencePlots
plt.style.use(["science", "ieee"])       # 期刊变体：ieee / nature / apa
```

- `science` 是主样式（细框、无顶右刺、窄栏宽）；`ieee`（3.5in 栏宽、衬线）、`nature`（无网格）等变体叠加在后覆盖前者；
- **中文必须加 `no-latex`**：`plt.style.use(["science", "no-latex", "../references/style/matplotlib/academic.mplstyle"])`——`science` 默认 `text.usetex=True` 会因缺 LaTeX/中文配置直接报错；
- 与本仓库主题叠加时，**本仓库主题写在最后**（保持取色与字体纪律，SciencePlots 只负责期刊尺寸与默认细节）；
- 环境：`pip install SciencePlots`；无 LaTeX 环境永远带 `no-latex`。

## 3. 色图标准（Scientific Colour Maps）

感知均匀色图已是出版界事实标准（Crameri, Shephard & Heron, 2020, *Nature Communications*——使用需引用该文）：

- **禁用** jet / rainbow / hsv：感知不均匀、色盲不友好、黑白打印产生虚假条纹；
- **顺序数据**：viridis / cividis / magma（matplotlib 内置），或 Crameri `batlow`；Crameri 色图安装：`pip install cmcrameri` → `import cmcrameri.cm as cmc; cmap="cmc.batlow"`；
- **发散数据**：RdBu_r / coolwarm，或 Crameri `vik` / `roma`（中心必须对齐语义零点）；
- **循环数据**（角度、周期）：twilight_shifted 或 Crameri `romero`——顺序色图画循环数据会在 0/360 处产生虚假断崖；
- 色盲自检：交付前用色盲模拟（colorspacious 或系统工具）过一遍，或直接用 cividis/batlow 这类天然安全的。

## 4. 多面板组合规范

- 面板标签 **a / b / c**（Nature 系小写粗体，左上角外侧统一对齐）或 (a)(b)，全篇统一一种；
- 组合用 `fig.subplot_mosaic` 或 GridSpec；同列面板共享 x 轴时 `sharex=True` 并删中间重复刻度；
- 面板间距不小于标签高度，标签不得压轴；
- caption 与面板一一对应，每面板可独立理解。

## 5. 细节退稿清单（审稿人常挑）

1. **字体未嵌入**：PDF 用 `pdffonts` 检查，非内嵌字体（TrueType 以外）会被出版系统打回——主题已设 fonttype 42，勿覆盖；
2. **该矢量的用了位图**：线图/柱状/散点一律 PDF/EPS 矢量；仅热图、>1 万点散点、图像用位图且 ≥600dpi（主题 savefig.dpi 已按档位设置）；
3. **标签重叠**：密数据标签用 `adjustText` 库（`pip install adjustText`）自动避让，不许手工挪了事；
4. **量级记法**：轴用 ×10ⁿ 标注（`ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 3))`），不出现 1e6 裸记数；SI 词头优先（μ、m、k）；
5. **图例压数据**：图例置顶框外或线端直标；误差棒类型（SD/SE/95%CI）在图注明示；
6. **usatex 与正文不一致**：中文期刊或中文图注慎用 `text.usetex`（中文配置繁琐且易与模板冲突），用 no-latex + 主题字体即可；
7. **一图一信息**：panel 数量克制（≤6），超了拆图；每张图在正文中必须被引用和讨论。

## 6. 与本仓库工作流的整合

走 `scenarios.md` T1 路径：本文件排在 `tool-matplotlib.md` 之后、作图之前；主题仍用 academic.mplstyle（取色与字体纪律不变），SciencePlots 与 cmcrameri 是**期刊适配层**，不替代本仓库主题。
