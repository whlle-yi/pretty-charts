---
name: pretty-charts
description: 高质量图表绘制技能。当用户需要绘制、美化或选型任何图形时使用——数据图（折线、柱状、散点、箱线、热图、分布、相关、网络、地理等）与非数据图（流程图、时序图、架构图、思维导图、科研示意图、信息图等）。内置三套色盲友好主题（学术/商务/展示）与三档质量标准（出版级/报告级/展示级），覆盖 matplotlib/seaborn/plotly、ECharts/D3、TikZ/Graphviz、SVG 手绘。凡涉及"画图、作图、可视化、示意图、图表配色、图表美化"一律使用本技能。
---

# pretty-charts —— 高质量绘图技能

本技能是一棵决策树：先定性（什么类型的图、给谁看），再按需加载参考文件，最后按检查清单自查。**不要跳过第 1、2 步直接画图。**

## 第 1 步：定性——数据图还是非数据图？

判断规则：**有"数值 → 视觉通道"的映射（长度、角度、位置、颜色深浅编码数量）就是数据图；表达结构、流程、层级、概念的就是非数据图。**

- **用户直接指定了图型** → 按图型走第 3 步；
- **用户只给了内容，没说画什么图** → 先读 `references/content-analysis.md` 做内容审读：析出核心信息 → 三分类 → 给出推荐图型与理由，确认后进入对应分支；
- 数据图 → 读 `references/data/` 下对应文件；
- 非数据图 → 读 `references/diagram/` 下对应文件；
- 混合体（信息图、带数据的海报）按**最终交付形态**归类，两边的规范都要遵守。

## 第 2 步：定档——质量标准分三档

档位决定默认主题与自查清单的严格程度。用户未说明时按下表默认，已说明则遵从用户：

| 档位 | 名称 | 默认主题 | 典型场景 | 自查清单 |
|------|------|----------|----------|----------|
| T1 | 出版级 | academic | 期刊论文、学位论文、正式报告 | `references/style-guide.md` §7.1 |
| T2 | 报告级 | business | 咨询报告、文档配图、商务汇报 | `references/style-guide.md` §7.2 |
| T3 | 展示级 | showcase | PPT、海报、社交媒体 | `references/style-guide.md` §7.3 |

**定档后先读 `references/scenarios.md` 对应节**——那里有该场景的精确阅读顺序（接下来看哪几个文件）与场景专属规则（期刊尺寸、论文流程图无底色、远距离可读等），再按其清单加载方法论文件。

主题资产在 `references/style/`：色板 `references/style/palettes/*.json`、matplotlib `references/style/matplotlib/*.mplstyle`、ECharts `references/style/echarts/*.json`、TikZ `references/style/tikz/`、字体方案 `references/style/fonts.md`。

## 第 3 步：加载对应参考文件后作图

### 数据图（references/data/）

先按**分析目的**选图型（读 `chart-selection.md` 做选型决策），再按工具栈读对应文件：

- 比较类 / 分布类 / 构成类 / 趋势类 / 关系类 / 层次网络类 / 地理类 / 热图矩阵类 / 统计推断类（误差棒、置信区间、显著性）
- 工具栈：`tool-matplotlib.md`、`tool-echarts.md`（seaborn/plotly/D3 并入各自主线讲）

### 非数据图（references/diagram/）

按图型加载：流程与时序（流程图、时序图、甘特图）、系统架构图、层级与逻辑（思维导图、组织架构）、概念示意/科研示意图、信息图。

- 工具栈：`tool-tikz.md`（主力）、`tool-graphviz.md`（复杂自动布局备用）、`tool-svg.md`
- **非数据图交付级一律 TikZ，不使用 mermaid**：流程图 `references/style/tikz/flowchart-styles.tex`、时序图 `references/style/tikz/sequence-styles.tex`，均双模式——`\pcPaperMode` 论文版（无底色，中文宋体+Times New Roman）/ `\pcPPTMode` 演示版（showcase 彩色，中文黑体+Arial）；甘特图用 pgfgantt、思维导图用 TikZ mindmap，同为论文风格。

## 执行顺序契约（防跳步，强制）

以下顺序不可调换，**上一步未完成不得进入下一步**：

1. **定性定档**（读本文件完成）；
2. **读 `references/scenarios.md` 对应档位一节**，拿到阅读清单与场景规则；
3. **按清单读完列出的方法论文件**——在此之前**禁止写出任何绘图代码**，哪怕你已经"知道"怎么画；
4. **作图**：代码中必须显式引用主题资产路径（如 `plt.style.use(".../academic.mplstyle")`），禁止硬编码样式常量；
5. **交付**：交付说明必须包含三项，缺一视为不合规——
   - 本次实际读取的文件列表；
   - 所用主题与档位（如 academic / T1）；
   - 对应自查清单（style-guide §7.x）的逐项结论。

## 通用规则（任何图、任何档都适用）

1. **防误导优先于美观**：柱状图 y 轴必须从 0 开始；不滥用双轴；截断轴必须显式标注；不确定度（误差棒/置信区间）不能省略。详见 `references/style-guide.md` §6。
2. **颜色只从色板取**：三套色板全部色盲友好，禁止临时凑色；类别数超过色板容量时做小倍数图或合并，不加色。
3. **字体**：中文思源黑体（Noto Sans SC），西文/数字 Arial；最小字号按档位，见 `references/style/fonts.md`。
4. **导出**：矢量优先（PDF/SVG）；位图 DPI 按档位；尺寸按交付场景（期刊单栏 90mm/双栏 190mm、PPT 16:9、网页自适应）。
5. **画完必自查**：对照第 2 步选定的检查清单逐项过，发现问题先修再看下一项。
6. **示例画廊**：`examples/` 下每类图附可运行代码与成图，作图前可先找相近示例改。

## 仓库/资产索引

```
SKILL.md                  ← 本文件，入口与路由
references/
  ├── content-analysis.md ← 内容审读（用户未指定图型时的选型入口）
  ├── scenarios.md        ← 场景入口（定档后的阅读路径 + 场景专属规则）
  ├── style-guide.md      ← 风格规范总纲（配色/字体/导出/防误导/三档清单）
  ├── data/               ← 数据图方法论（按分析目的 + 工具栈）
  └── diagram/            ← 非数据图方法论（按图型 + 工具栈）
references/style/
  ├── palettes/           ← 三套色板 JSON（唯一取色来源）
  ├── matplotlib/         ← 三个 .mplstyle
  ├── echarts/            ← 三个 ECharts 主题
  ├── tikz/               ← TikZ/pgfplots 导言区模板
  └── fonts.md            ← 字体方案与回退链
examples/
  ├── data/               ← 数据图示例（代码 + 成图）
  ├── diagram/            ← 非数据图示例（代码 + 成图）
  └── style-demo/         ← 三主题风格验证样张
```
