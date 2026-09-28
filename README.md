<div align="center">

# 📊 pretty-charts

**AI Agent 与人类共用的图表风格体系**

数据图与非数据图的完整方法论 · 三档质量标准 · 三套色盲友好主题的机器可读资产

[![CI](https://github.com/whlle-yi/pretty-charts/actions/workflows/ci.yml/badge.svg)](https://github.com/whlle-yi/pretty-charts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-0072B2.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-%E2%89%A53.9-4E79A7.svg)](#依赖)
[![Platform](https://img.shields.io/badge/Platform-ZCode%20%2F%20Claude%20Code-4E79A7.svg)](#安装)
[![Charts](https://img.shields.io/badge/%E5%9B%BE%E5%9E%8B-40%2B-009E73.svg)](#示例)

*English — a charting skill for AI agents: methodology for 40+ chart types, three quality tiers, machine-readable style assets.*

[使用](#使用) · [效果展示](#效果展示) · [文件组织](#文件组织)

</div>

## 使用

### 装 Skill

一个自包含的绘图 Skill，无运行时依赖，拷走即用：

```bash
git clone https://github.com/whlle-yi/pretty-charts.git

# ZCode
cp -r pretty-charts/skills/pretty-charts ~/.zcode/skills/

# Claude Code（目录结构相同）
cp -r pretty-charts/skills/pretty-charts ~/.claude/skills/
```

装好后直接对 Agent 说话即可：

> 画一张论文用的训练流程图
> 这张季度销售数据该怎么展示？给我三种方案

Agent 按**五步契约**执行：**定性**（先看数据、过防误导判断）→ **定档**（按输出介质选 T1/T2/T3，判定表见 SKILL.md 第 2 步）→ **作图**（加载对应资产、按图型与工具规范执行）→ **目检**（渲染成图逐项检查）→ **交付**（写 chart-plan 决定记录、逐项过清单）。

防误导九条红线全程有效：图注里的 n、置信区间、p 值必须由脚本真实计算；语义 → 颜色映射一次分配、全交付物复用。

### 不装 Skill，只用风格资产

| 工具 | 用法 |
|---|---|
| matplotlib | `plt.style.use("<技能根>/references/assets/matplotlib/academic.mplstyle")`（academic / business / showcase 三选一） |
| ECharts | `echarts.registerTheme("pc", theme)` —— 主题 JSON 见 [references/assets/echarts/](skills/pretty-charts/references/assets/echarts/) |
| TikZ | `\input{.../preamble.tex}` + 模式宏 `\pcPaperMode` / `\pcPPTMode`，详见 [references/tools/tex.md](skills/pretty-charts/references/tools/tex.md) |
| 色板（任意工具） | [references/assets/palettes/](skills/pretty-charts/references/assets/palettes/) 三份 JSON：`categorical` / `sequential` / `diverging` / `neutral` / `missing` / `semantic` 等 token |

## 效果展示

每个示例都是可运行脚本，成图由仓库内代码实际渲染并提交；脚本 ↔ 成图 ↔ 方法论的完整对照见 [examples/INDEX.md](skills/pretty-charts/examples/INDEX.md)。

### 数据图（7 族代表）

| | | |
|:---:|:---:|:---:|
| **[比较](skills/pretty-charts/references/charts/compare.md)** | **[分布](skills/pretty-charts/references/charts/distribution.md)** | **[构成](skills/pretty-charts/references/charts/compare.md)** |
| ![](skills/pretty-charts/examples/data/comparison/sorted_bar.png) | ![](skills/pretty-charts/examples/data/distribution/box_violin.png) | ![](skills/pretty-charts/examples/data/composition/donut.png) |
| **[趋势](skills/pretty-charts/references/charts/trend.md)** | **[关系](skills/pretty-charts/references/charts/relationship.md)** | **[结构](skills/pretty-charts/references/charts/structure.md)** |
| ![](skills/pretty-charts/examples/data/trend/line_direct_label.png) | ![](skills/pretty-charts/examples/data/relationship/fig1_preview.png) | ![](skills/pretty-charts/examples/data/network/treemap.png) |
| **[地理](skills/pretty-charts/references/charts/map.md)** | **[热图矩阵](skills/pretty-charts/references/charts/relationship.md)** | **[统计推断](skills/pretty-charts/references/charts/inference.md)** |
| ![](skills/pretty-charts/examples/data/geo/fig1_preview.png) | ![](skills/pretty-charts/examples/data/heatmap/corr_heatmap.png) | ![](skills/pretty-charts/examples/data/statistical/errorbar_ci.png) |

### 非数据图（5 类）

| | |
|:---:|:---:|
| **[流程与时序](skills/pretty-charts/references/diagrams.md)** | **[系统架构](skills/pretty-charts/references/diagrams.md)** |
| ![](skills/pretty-charts/examples/diagram/flowchart/research_flow.png) | ![](skills/pretty-charts/examples/diagram/architecture/three_tier.png) |
| **[层级与逻辑](skills/pretty-charts/references/diagrams.md)** | **[科研示意图](skills/pretty-charts/references/diagrams.md)** |
| ![](skills/pretty-charts/examples/diagram/hierarchy/org_chart.png) | ![](skills/pretty-charts/examples/diagram/schematic/signaling_schematic.png) |
| **[信息图](skills/pretty-charts/references/diagrams.md)** | |
| ![](skills/pretty-charts/examples/diagram/infographic/infographic.png) | |

### 三档观感对照

同一份数据在三个档位下的渲染差异（[demo_styles.py](skills/pretty-charts/examples/style-demo/demo_styles.py) 生成）：

| academic（T1 出版级） | business（T2 报告级） | showcase（T3 展示级） |
|:---:|:---:|:---:|
| ![](skills/pretty-charts/examples/style-demo/output/academic.png) | ![](skills/pretty-charts/examples/style-demo/output/business.png) | ![](skills/pretty-charts/examples/style-demo/output/showcase.png) |


## 文件组织

```tree
pretty-charts/
├── README.md / LICENSE / requirements.txt / requirements-lock.txt
├── .github/workflows/ci.yml    # CI：八项自检 · Python 示例（从锁安装） · LaTeX 编译
├── scripts/check_refs.py       # 八项自检 + 生成示例索引（仓库维护工具，不属于 skill 本体）
└── skills/pretty-charts/       # Skill 本体：自包含，拷走即用
    ├── SKILL.md                # 唯一入口：五步契约 + 两张路由表
    ├── references/
    │   ├── common.md           # 公共规则唯一定义处：红线 / 取色 / 字体 / 尺寸落盘
    │   ├── select.md           # 选型（图型未定时读）
    │   ├── charts/  ×7         # 数据图方法论
    │   ├── diagrams.md         # 非数据图 5 类 + 通用布局
    │   ├── tools/   ×3         # python / web / tex
    │   └── assets/             # 机器可读资产：palettes / matplotlib / echarts / tikz
    └── examples/               # 16 个 Python 脚本 + 16 个 LaTeX 源 + 成图
```

Agent 一次任务的标准读取量 **4–5 个文件**：SKILL.md + common.md + 一份图型方法论 + 一份工具文件。依赖分两层（区间 + 锁），见根目录两个 requirements 文件与 CI 配置。

## 已知限制

- TikZ 只有论文 / 演示两种模式（business 模式待做）；
- CI 不做成图字节比对——字体光栅化与 PDF 时间戳跨平台必然不同；
- PDF→PNG 的 Ghostscript 管线未本机实测。

## 致谢

配色基于 [Okabe-Ito](https://jfly.uni-koeln.de/color/)、[Tableau 10](https://www.tableau.com/) 与 [Paul Tol](https://personal.sron.nl/~pault/) 色板，顺序 / 发散色图取自 [ColorBrewer](https://colorbrewer2.org/) 与 [Crameri Scientific Colour Maps](https://www.fabiocrameri.ch/colourmaps/)（使用需引用 Crameri, Shephard & Heron, 2020, *Nature Communications*）；非数据图渲染依赖 [TikZ/pgfplots](https://ctan.org/pkg/pgfplots)、[pgfgantt](https://ctan.org/pkg/pgfgantt)；底图数据来自 [Natural Earth](https://www.naturalearthdata.com/)（公有领域）；期刊适配依赖 [SciencePlots](https://github.com/garrettj403/SciencePlots)。

## 许可

[MIT](LICENSE) © 2026 [whlle-yi](https://github.com/whlle-yi)
