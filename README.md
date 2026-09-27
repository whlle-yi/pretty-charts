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

| | | |
|:---:|:---:|:---:|
| **[比较](skills/pretty-charts/references/data/comparison.md)** | **[分布](skills/pretty-charts/references/data/distribution.md)** | **[构成](skills/pretty-charts/references/data/composition.md)** |
| ![](skills/pretty-charts/examples/data/comparison/sorted_bar.png) | ![](skills/pretty-charts/examples/data/distribution/box_violin.png) | ![](skills/pretty-charts/examples/data/composition/donut.png) |
| **[趋势](skills/pretty-charts/references/data/trend.md)** | **[关系](skills/pretty-charts/references/data/relationship.md)** | **[层次网络](skills/pretty-charts/references/data/network.md)** |
| ![](skills/pretty-charts/examples/data/trend/line_direct_label.png) | ![](skills/pretty-charts/examples/data/relationship/fig1_preview.png) | ![](skills/pretty-charts/examples/data/network/treemap.png) |
| **[地理](skills/pretty-charts/references/data/geo.md)** | **[热图矩阵](skills/pretty-charts/references/data/heatmap.md)** | **[统计推断](skills/pretty-charts/references/data/statistical.md)** |
| ![](skills/pretty-charts/examples/data/geo/fig1_preview.png) | ![](skills/pretty-charts/examples/data/heatmap/corr_heatmap.png) | ![](skills/pretty-charts/examples/data/statistical/errorbar_ci.png) |

### 非数据图（5 类）

| | |
|:---:|:---:|
| **[流程与时序](skills/pretty-charts/references/diagram/flowchart.md)** | **[系统架构](skills/pretty-charts/references/diagram/architecture.md)** |
| ![](skills/pretty-charts/examples/diagram/flowchart/research_flow.png) | ![](skills/pretty-charts/examples/diagram/architecture/three_tier.png) |
| **[层级与逻辑](skills/pretty-charts/references/diagram/hierarchy.md)** | **[科研示意图](skills/pretty-charts/references/diagram/schematic.md)** |
| ![](skills/pretty-charts/examples/diagram/hierarchy/org_chart.png) | ![](skills/pretty-charts/examples/diagram/schematic/signaling_schematic.png) |
| **[信息图](skills/pretty-charts/references/diagram/infographic.md)** | |
| ![](skills/pretty-charts/examples/diagram/infographic/infographic.png) | |

更多论文内嵌效果：[科研流程图](skills/pretty-charts/examples/diagram/flowchart/research_flow.pdf) · [流程图演示版](skills/pretty-charts/examples/diagram/flowchart/ppt_flow.png) · [流程图论文版](skills/pretty-charts/examples/diagram/flowchart/paper_flow.png) · [数据图内嵌](skills/pretty-charts/examples/data/paper/paper_embedded_data.pdf) · [地理图内嵌](skills/pretty-charts/examples/data/geo/paper_embedded_geo.pdf) · [关系图内嵌](skills/pretty-charts/examples/data/relationship/paper_embedded_relationship.pdf) · [层级图内嵌](skills/pretty-charts/examples/diagram/hierarchy/paper_embedded_hierarchy.pdf) · [管线示意图](skills/pretty-charts/examples/diagram/schematic/pipeline_schematic.pdf)

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
| matplotlib | `plt.style.use("<技能根>/references/style/matplotlib/academic.mplstyle")`（路径相对技能根；示例代码用 `Path(__file__)` 定位，不依赖当前工作目录） |
| ECharts | `echarts.registerTheme("pc", theme)` —— 主题 JSON 见 [references/style/echarts/](skills/pretty-charts/references/style/echarts/) |
| TikZ | `\input{references/style/tikz/preamble.tex}` + `\input{references/style/tikz/flowchart-styles.tex}` |

## 质量分档

| 档位 | 介质 / 场景 | 主题（色板来源） | 关键约束 |
|:---:|---|:---:|---|
| T1 出版级 | 期刊 / 学位论文 | academic（Okabe-Ito） | 流程图无底色、黑白可辨、误差与显著性规范、矢量导出 |
| T2 报告级 | 咨询 / 商务文档 | business（Tableau 10） | 标题即结论、关键数值直标、语义色可用 |
| T3 展示级 | PPT / 海报 / 大屏 | showcase（Tol Vibrant） | 一图一结论、系列 ≤3、远距离可读 |

**档位由输出介质判定**（印刷 / 屏幕文档 / 投影），不是“学术 vs 商务”这类社交标签——判定表与参数差异见 [routing.md](skills/pretty-charts/references/routing.md) §1。档位是场景标准而非质量排名，质量以 [checklist.md](skills/pretty-charts/references/checklist.md) 对应清单衡量。

## 文件地图

| 时机 | 文件 |
|---|---|
| ① 每次任务必读 | [`SKILL.md`](skills/pretty-charts/SKILL.md)（设计哲学 + 四步契约） |
| ② 定档 | [`routing.md`](skills/pretty-charts/references/routing.md)（档位 · 工具 · 读取顺序 · 降级） |
| ③ 图型未定时选型 | [`selection.md`](skills/pretty-charts/references/selection.md) |
| ④ 画什么读什么 | 图型专属：`references/data/`（9 类）· `references/diagram/`（5 类） |
| ⑤ 横切规范 | `references/spec/{integrity,color,type,layout,diagram}.md`（只定义一次） |
| ⑥ 按工具栈读 | `data/tool-{matplotlib,echarts}.md` · `diagram/tool-{tikz,graphviz,svg}.md` |
| ⑦ 交付前查 | [`checklist.md`](skills/pretty-charts/references/checklist.md) 对应档位 |
| ⑧ 参照模仿 | [`examples/INDEX.md`](skills/pretty-charts/examples/INDEX.md)（脚本 ↔ 成图） |
| ⑨ 被代码加载，不必通读 | `references/style/`（palettes / matplotlib / echarts / tikz） |

## 仓库结构

```
pretty-charts/
├── README.md / LICENSE / .gitignore
├── scripts/check_refs.py       # 仓库维护工具（不属于 skill 本体）：引用自检 + 生成示例索引
└── skills/
    └── pretty-charts/          # skill 本体：自包含，拷走即用
        ├── SKILL.md            # 入口：设计哲学 + 四步契约 + 交付要求
        ├── references/
        │   ├── routing.md      # 唯一路由：档位（按介质）+ 工具 + 读取顺序 + 降级路径
        │   ├── selection.md    # 唯一选型：要不要画 + 数据图/非数据图 + 归属判定
        │   ├── checklist.md    # 三档自查清单
        │   ├── spec/           # 横切规范（只定义一次）：integrity / color / type / layout / diagram
        │   ├── data/           # 数据图：9 类图型专属 + 2 工具栈 + paper-data.md
        │   ├── diagram/        # 非数据图：5 类图型专属 + 3 工具栈
        │   └── style/          # 机器可读资产：palettes / matplotlib / echarts / tikz
        ├── examples/           # 示例画廊：INDEX.md + 代码 + 成图
```

## 文档

| 文档 | 内容 |
|---|---|
| [SKILL.md](skills/pretty-charts/SKILL.md) | 入口：设计哲学 + 四步契约 + 交付要求 |
| [routing.md](skills/pretty-charts/references/routing.md) | 档位（按输出介质）· 工具选择 · 读取顺序 · 降级路径 |
| [selection.md](skills/pretty-charts/references/selection.md) | 要不要画 · 数据图/非数据图 · 目的+修饰维度 · 归属判定 |
| [checklist.md](skills/pretty-charts/references/checklist.md) | 三档自查清单（交付前逐项过） |
| [spec/integrity.md](skills/pretty-charts/references/spec/integrity.md) | 防误导九条红线 · 图注自含 · 诚实原则 |
| [spec/color.md](skills/pretty-charts/references/spec/color.md) | 取色唯一来源 · token 表 · 多图一致性 |
| [spec/type.md](skills/pretty-charts/references/spec/type.md) | 字体与字号层级 · VF 字体与 gs 管线两个坑 |
| [spec/layout.md](skills/pretty-charts/references/spec/layout.md) | 尺寸速查 · 导出参数 · 落盘与命名 |
| [spec/diagram.md](skills/pretty-charts/references/spec/diagram.md) | 非数据图通用布局 |
| [paper-data.md](skills/pretty-charts/references/data/paper-data.md) | 论文数据图深化：期刊规格 / SciencePlots / Crameri 色图 / 退稿清单 |
| [examples/INDEX.md](skills/pretty-charts/examples/INDEX.md) | 示例索引：脚本 ↔ 成图（脚本自动生成） |

## 路线图

- [x] 风格基建（三套色盲友好主题 + matplotlib / ECharts / TikZ 三套资产；TikZ 目前只落了 academic 一套）
- [x] 数据图方法论 + 首批画廊（9 类全有代表成图）
- [x] 非数据图方法论 + 首批画廊（TikZ 13 个源文件，5 类图型全部有成图）
- [x] 树图、哑铃图（`examples/data/network/make_treemap.py`、`examples/data/comparison/sorted_bar.py`）
- [ ] 数据图第二批画廊（余）：桑基、山脊图、ECDF
- [x] 地理可视化示例（choropleth / 比例符号 / 小倍数）
- [x] 信息图整页版式示例（简版）
- [ ] CI 自动渲染示例图
- [ ] 双语 README

## 致谢

配色基于 [Okabe-Ito](https://jfly.uni-koeln.de/color/)、[Tableau 10](https://www.tableau.com/) 与 [Paul Tol](https://personal.sron.nl/~pault/) 色板；非数据图渲染依赖 [TikZ/pgfplots](https://ctan.org/pkg/pgfplots) 与 [pgfgantt](https://ctan.org/pkg/pgfgantt)。

## 许可

[MIT](LICENSE) © 2026 [whlle-yi](https://github.com/whlle-yi)
