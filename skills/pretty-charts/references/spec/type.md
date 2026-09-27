# 规范：字体与文字（type）

> 本文件是**字体的唯一定义处**。图型文件、工具文件只引用本文件，不得复述字体方案。
> 机器可读资产：`references/style/matplotlib/*.mplstyle`（`font.family`/`font.sans-serif`/字号）、`references/style/echarts/*.json`（`fontFamily`/`fontSize`）、`references/style/tikz/preamble.tex`。

## 1. 中西文分字体

中文与西文/数字用不同字体族：不要让中文字体顺便渲染西文（其西文字形间距偏宽、数字非等宽）。

| 场景 | 中文 | 西文 / 数字 |
|---|---|---|
| 数据图（matplotlib / ECharts） | 思源黑体 Source Han Sans SC / Noto Sans SC | Arial |
| TikZ 论文版（流程图、示意图） | 宋体 SimSun | Times New Roman |
| TikZ 演示版 | 黑体 Microsoft YaHei | Arial |

**TikZ 的模式宏不含字体**：`\pcPaperMode` / `\pcPPTMode` 只切配色、线宽、字号。字体必须由你自己的文档用 `\setmainfont` / `\setCJKmainfont` 声明——只切宏而不声明字体，中文会变成豆腐块。示例见 `examples/diagram/flowchart/paper_flow.tex` 与 `ppt_flow.tex`（两者仅"1 行模式 + 2 行字体"之差）。

**跨平台字体层（TikZ）**：两种搭配各封装为可 `\input` 的片段，按字体是否存在自动回退，**文档里不要写死字体名**：
- [`fonts-serif.tex`](../style/tikz/fonts-serif.tex)：宋体 + Times New Roman（与论文正文一致的图）
- [`fonts-sans.tex`](../style/tikz/fonts-sans.tex)：黑体 + Arial（演示版，以及黑体系的示意图）

  回退顺序：Windows 原生字体 → Noto CJK → **Fandol**（TeX Live 自带，故无需系统字体包）。

**回退链**（已内置在 `.mplstyle`）：`Source Han Sans SC → Noto Sans SC → Microsoft YaHei → Arial → Helvetica → DejaVu Sans`。
数学符号用 STIX（`mathtext.fontset: stix`）。

## 2. 字号层级

同一张图内层级 ≤4 级：标题 / 轴标题 / 刻度与图例 / 数据标注。

| 元素 | T1 | T2 | T3 |
|---|---|---|---|
| 图标题 | 11 bold | 13 bold | 15 bold |
| 轴标题 | 10 | 11 | 12 |
| 刻度 / 图例 | 9 | 10 | 11 |
| 数据标注 | 8–9 | 10 | 11 |
| **绝对下限** | **7**（印刷可读） | 9 | 11（最后一排可读） |

ECharts（px，已内置主题）：T1 14/12/11、T2 16/13/12、T3 20/15/14（标题/图例/刻度）。
TikZ：轴标题 `\small`、刻度与图例 `\footnotesize`。

**下限约束的是"最终成品上的等效字号"，不是代码里的数字。** 如果图会被缩放排版（例：122mm 宽的原图放进 90mm 单栏，缩放比 0.74），等效字号 = 设定值 × 缩放比，必须按缩放后的值判断是否仍 ≥7pt。这与 `layout.md` §2.5 的 tight bbox 问题是同一个陷阱的两面。

## 3. 两个必须知道的坑

1. **Windows 的 Noto Sans SC 是可变字体（VF）**，两条管线都会翻车：
   - **XeLaTeX / xdvipdfmx 无法嵌入** → 报 `fatal: Invalid font`。TikZ 出 PDF 改用 Microsoft YaHei 或静态版思源黑体（`preamble.tex` 已按此设 `\chartcjk{Microsoft YaHei}`）。
   - **matplotlib 导出的 PDF 子集经 Ghostscript 渲染会丢字形**（PDF 本身在 Adobe/浏览器正常，但出版系统的 gs 管线会掉字）→ 把静态字体 Microsoft YaHei 提到回退链首位。
   - 对策（示例 `examples/data/paper/make_paper_figures.py`）：

     ```python
     sans = list(plt.rcParams["font.sans-serif"])
     if "Microsoft YaHei" in sans:      # 回退链可能被外部覆盖，先判存在
         sans.remove("Microsoft YaHei")
     sans.insert(0, "Microsoft YaHei")
     plt.rcParams["font.sans-serif"] = sans
     ```
2. **Linux 服务器缺中文字体** → 中文变豆腐块。先装 `fonts-noto-cjk`；SVG 交付若文字未转路径，接收方也需有同名字体。

## 4. 强调

图内强调用**加粗**（同字体 Bold/Medium 字重）或强调色；不用下划线，不堆颜色。只强调关键结论、关键数据、警告。
负号：主题已设 `axes.unicode_minus: False`，即使用 ASCII 连字符代替 U+2212，避免缺字形的中文字体画不出来。

## 5. 换字体方案

项目要求衬线（部分中文期刊）时，在**项目内**覆盖 `font.family: serif` + SimSun / Times New Roman，**不要修改本仓库的主题文件**——改了会影响所有使用者。
