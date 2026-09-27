<div align="center">

# 📊 pretty-charts

**高质量绘图技能库 —— AI Agent 与人类共用的统一图表风格体系**

[![License: MIT](https://img.shields.io/badge/License-MIT-0072B2.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-ZCode%20%2F%20Claude%20Code-4E79A7.svg)](#快速开始)
[![Charts](https://img.shields.io/badge/图型-17%2B-009E73.svg)](#示例)
[![Status](https://img.shields.io/badge/状态-持续完善-F28E2B.svg)](#路线图)

[快速开始](#快速开始) · [示例](#示例) · [文档](#文档)

</div>

---

为 AI Agent（ZCode / Claude Code 等 skills 机制）提供图表绘制全流程指导，同时提供可直接复用的跨工具栈风格资产。覆盖数据图与非数据图，出版 / 报告 / 演示三档质量标准，方法论按需加载，全部示例附可运行代码与成图。

## 示例

每个图型文件对应一种类型：这里为**每种类型展示一张代表成图**（类型名可点击跳转到对应方法论），全部成图由仓库内代码实际渲染。

### 数据图（9 类）

| 比较 | 分布 | 构成 |
|:---:|:---:|:---:|
| **[比较](skills/pretty-charts/references/data/comparison.md)** | **[分布](skills/pretty-charts/references/data/distribution.md)** | **[构成](skills/pretty-charts/references/data/composition.md)** |
| ![](skills/pretty-charts/examples/data/comparison/sorted_bar.png) | ![](skills/pretty-charts/examples/data/distribution/box_violin.png) | ![](skills/pretty-charts/examples/data/composition/donut.png) |

| 趋势 | 关系 | 层次网络 |
|:---:|:---:|:---:|
| **[趋势](skills/pretty-charts/references/data/trend.md)** | **[关系](skills/pretty-charts/references/data/relationship.md)** | **[层次网络](skills/pretty-charts/references/data/network.md)** |
| ![](skills/pretty-charts/examples/data/trend/line_direct_label.png) | ![](skills/pretty-charts/examples/data/relationship/scatter_trend.png) | ![](skills/pretty-charts/examples/data/network/treemap.png) |

| 地理 | 热图矩阵 | 统计推断 |
|:---:|:---:|:---:|
| **[地理](skills/pretty-charts/references/data/geo.md)** | **[热图矩阵](skills/pretty-charts/references/data/heatmap.md)** | **[统计推断](skills/pretty-charts/references/data/statistical.md)** |
| ![](skills/pretty-charts/examples/data/geo/fig1_preview.png) | ![](skills/pretty-charts/examples/data/heatmap/corr_heatmap.png) | ![](skills/pretty-charts/examples/data/statistical/errorbar_ci.png) |

### 非数据图（5 类）

| 流程与时序 | 系统架构 | 层级与逻辑 |
|:---:|:---:|:---:|
| **[流程与时序](skills/pretty-charts/references/diagram/flowchart.md)** | **[系统架构](skills/pretty-charts/references/diagram/architecture.md)** | **[层级与逻辑](skills/pretty-charts/references/diagram/hierarchy.md)** |
| ![](skills/pretty-charts/examples/diagram/flowchart/ppt_flow.png) | ![](skills/pretty-charts/examples/diagram/architecture/three_tier.png) | ![](skills/pretty-charts/examples/diagram/hierarchy/org_chart.png) |

| 科研示意图 | 信息图 |
|:---:|:---:|
| **[科研示意图](skills/pretty-charts/references/diagram/schematic.md)** | **[信息图](skills/pretty-charts/references/diagram/infographic.md)** |
| ![](skills/pretty-charts/examples/diagram/schematic/pipeline_schematic.png) | ![](skills/pretty-charts/examples/diagram/infographic/infographic.png) |

更多论文内嵌效果：[流程图论文/演示双版](skills/pretty-charts/examples/diagram/flowchart/paper_flow.png) · [数据图内嵌](skills/pretty-charts/examples/data/paper/paper_embedded_data.pdf) · [地理图内嵌](skills/pretty-charts/examples/data/geo/paper_embedded_geo.pdf) · [关系图内嵌](skills/pretty-charts/examples/data/relationship/paper_embedded_relationship.pdf) · [层级图内嵌](skills/pretty-charts/examples/diagram/hierarchy/paper_embedded_hierarchy.pdf) · [管线示意图](skills/pretty-charts/examples/diagram/schematic/pipeline_schematic.pdf)

## 快速开始

**安装为 AI Skill**

```bash
git clone https://github.com/whlle-yi/pretty-charts.git
cp -r pretty-charts/skills/pretty-charts ~/.zcode/skills/
```

对 Agent 说"画一张论文用的训练流程图"，自动执行：定性 → 定档 → 按场景清单加载方法论 → 按主题作图 → 按清单自查交付。

**直接使用风格资产**

| 工具 | 用法 |
|---|---|
| matplotlib | `plt.style.use("references/style/matplotlib/academic.mplstyle")` |
| ECharts | `echarts.registerTheme("pc", theme)` —— 主题 JSON 见 [references/style/echarts/](skills/pretty-charts/references/style/echarts/) |
| TikZ | `\input{references/style/tikz/preamble.tex}` + `\input{references/style/tikz/flowchart-styles.tex}` |

## 质量分档

| 档位 | 场景 | 主题（色板来源） | 关键约束 |
|:---:|---|:---:|---|
| T1 出版级 | 期刊 / 学位论文 | academic（Okabe-Ito） | 流程图无底色、黑白可辨、误差与显著性规范、矢量导出 |
| T2 报告级 | 咨询 / 商务文档 | business（Tableau 10） | 标题即结论、关键数值直标、语义色可用 |
| T3 展示级 | PPT / 海报 / 大屏 | showcase（Tol Vibrant） | 一图一结论、系列 ≤3、远距离可读 |

档位是场景标准而非质量排名，质量以各档[自查清单](skills/pretty-charts/references/style-guide.md)衡量。

## 文件地图

| 时机 | 文件 |
|---|---|
| ① 被代码加载，不读 | `references/style/matplotlib/*.mplstyle` · `references/style/echarts/*.json` · `references/style/tikz/*.tex` |
| ② AI 每次任务必读 | `SKILL.md`（定性 + 定档） |
| ③ 定档后读一次 | [`references/scenarios.md`](skills/pretty-charts/references/scenarios.md)（对应档位一节） |
| ④ 画什么读什么 | `references/data/`（9 类分析目的 + 选型）· `references/diagram/`（5 类图型 + 选型） |
| ⑤ 按工具栈读 | `data/tool-{matplotlib,echarts}.md` · `diagram/tool-{tikz,graphviz,svg}.md` |
| ⑥ 交付前查 | `references/style-guide.md` §7 对应清单 · §4 字体 · §6 红线 |
| ⑦ 参照模仿 | `examples/`（代码 + 成图） |

## 仓库结构

```
pretty-charts/
├── README.md / LICENSE / .gitignore
└── skills/
    └── pretty-charts/          # skill 本体：自包含，拷走即用
        ├── SKILL.md            # 入口：定性路由 + 执行顺序契约
        ├── references/
        │   ├── scenarios.md    # 三档场景入口（阅读路径 + 专属规则）
        │   ├── style-guide.md  # 风格总纲（配色/字体/导出/防误导/清单）
        │   ├── data/           # 数据图：选型 + 9 类目的 + 2 工具栈
        │   └── diagram/        # 非数据图：5 类图型 + 4 工具栈
        │   └── style/          # 风格资产：palettes / matplotlib / echarts / tikz
        ├── examples/           # 示例画廊：代码 + 成图
```

## 文档

| 文档 | 内容 |
|---|---|
| [SKILL.md](skills/pretty-charts/SKILL.md) | 入口：内容审读 → 定档 → 执行顺序契约 |
| [scenarios.md](skills/pretty-charts/references/scenarios.md) | 三档场景：阅读顺序与专属规则 |
| [style-guide.md](skills/pretty-charts/references/style-guide.md) | 配色 / 字体 / 导出 / 防误导红线 / 三档清单（字体的唯一出处） |
| [chart-selection.md](skills/pretty-charts/references/data/chart-selection.md) | 数据图选型决策树 |
| [paper-data.md](skills/pretty-charts/references/data/paper-data.md) | 论文数据图深化：期刊规格 / SciencePlots / Crameri 色图 / 退稿清单 |
| [diagram-selection.md](skills/pretty-charts/references/diagram/diagram-selection.md) | 非数据图选型决策树 |

## 路线图

- [x] 风格基建（三套色盲友好主题 × 4 工具栈）
- [x] 数据图方法论 + 首批画廊（9 类全有代表成图）
- [x] 非数据图方法论 + 首批画廊（TikZ 9 例，全部 5 类图型有成图）
- [ ] 数据图第二批画廊：树图、桑基、山脊图、ECDF、哑铃图
- [x] 地理可视化示例（choropleth / 比例符号 / 小倍数）
- [x] 信息图整页版式示例（简版）
- [ ] CI 自动渲染示例图
- [ ] 双语 README

## 致谢

配色基于 [Okabe-Ito](https://jfly.uni-koeln.de/color/)、[Tableau 10](https://www.tableau.com/) 与 [Paul Tol](https://personal.sron.nl/~pault/) 色板；非数据图渲染依赖 [TikZ/pgfplots](https://ctan.org/pkg/pgfplots) 与 [pgfgantt](https://ctan.org/pkg/pgfgantt)。

## 许可

[MIT](LICENSE) © 2026 [whlle-yi](https://github.com/whlle-yi)
