# 字体方案

> 单一事实来源：所有工具栈的图表字体配置以本文件为准。

## 基本方案（默认）

| 用途 | 字体 | 说明 |
|------|------|------|
| 中文 | 思源黑体 / Noto Sans SC | 图表主流选择，笔画均匀、小字号清晰；本机已装 Noto Sans SC |
| 西文与数字 | Arial / Helvetica | 与思源黑体笔画风格协调，中性不抢戏 |
| 数学符号 | STIX（matplotlib `mathtext.fontset: stix`） | 与 Times 系数学风格一致 |

**规则：中西文分字体是常态，不要让中文字体顺便渲染西文**——思源黑体的西文字形间距偏宽，数字表格数字不等宽，混排会显松。

## 字体回退链

各主题文件中已写入如下回退链，缺失字体时逐级降级：

```
Source Han Sans SC → Noto Sans SC → Microsoft YaHei → Arial → Helvetica → DejaVu Sans
```

- Windows：通常命中 Noto Sans SC 或 Microsoft YaHei
- Linux 服务器：命中 Noto Sans SC / Source Han Sans SC；都没有时图表仍可出，但中文会回退到 DejaVu 的豆腐块，**必须先装字体**：`fonts-noto-cjk`（apt）或下载思源黑体 OTF 放入 `~/.fonts/`
- 分发给别人的 SVG：`svg.fonttype: none` 使文字保持可编辑，但对方机器需有同名字体；交付印刷/投稿请用 PDF（fonttype 42 内嵌 TrueType 子集）

## 字号层级

原则：**图内最小字号由"最远的读者"决定**，同一张图内层级不超过 4 级（标题 / 轴标题 / 刻度与图例 / 标注）。

| 元素 | T1 出版级 (pt) | T2 报告级 (pt) | T3 展示级 (pt) |
|------|------|------|------|
| 图标题 | 11 bold | 13 bold | 15 bold |
| 轴标题 | 10 | 11 | 12 |
| 刻度 / 图例 | 9 | 10 | 11 |
| 数据标注 | 8–9 | 10 | 11 |
| 绝对下限 | 7 pt（印刷可读） | 9 pt | 11 pt（投影最后一排可读） |

- ECharts（屏幕 px）：T1 ≈ 14/12/11，T2 ≈ 16/13/12，T3 ≈ 20/15/14（标题/图例/刻度），已在主题 JSON 内置
- matplotlib 数值已在 `.mplstyle` 内置；单独标注时用 `ax.annotate(..., fontsize=<档位数据标注字号>)`
- TikZ：模板 label `\small`、tick `ootnotesize`（见 `references/style/tikz/preamble.tex`）

## 强调规则

- 图内强调用**加粗**（同字体的 Bold/Medium 字重）或色板强调色，**不用颜色堆砌、不用下划线**
- 中文加粗：思源黑体 Medium/Bold 字重；matplotlib 中 `fontweight='bold'` 对 Noto Sans SC 生效（有 Bold 字重文件时）；若伪加粗发虚，改用 Medium 字重文件名显式指定
- 负号：matplotlib 已设 `axes.unicode_minus: False`，避免 U+2212 在中文字体缺字形

## 换字体方案

如果某个项目要求宋体/衬线图表（部分中文期刊如此）：matplotlib 中把 `font.sans-serif` 换为 `Source Han Serif SC, Noto Serif SC, SimSun`、`font.family: serif`，西文换 `Times New Roman`；其余规则不变。**不要修改本仓库默认主题文件，在项目内覆盖。**
