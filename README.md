<div align="center">

# 📊 pretty-charts

**高质量绘图技能库 —— AI Agent 与人类共用的统一图表风格体系**

[![CI](https://github.com/whlle-yi/pretty-charts/actions/workflows/ci.yml/badge.svg)](https://github.com/whlle-yi/pretty-charts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-0072B2.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-%E2%89%A53.9-4E79A7.svg)](#依赖与环境)
[![Platform](https://img.shields.io/badge/Platform-ZCode%20%2F%20Claude%20Code-4E79A7.svg)](#1-作为-ai-skill-安装)
[![Charts](https://img.shields.io/badge/%E5%9B%BE%E5%9E%8B%E6%96%B9%E6%B3%95%E8%AE%BA-14%20%E7%B1%BB-009E73.svg)](#示例)
[![Verified](https://img.shields.io/badge/%E5%AE%9E%E6%B5%8B-2026--09%20%C2%B7%20Win%20%C2%B7%20TeXLive%202026-2E7D32.svg)](#质量保障)
[![Status](https://img.shields.io/badge/%E7%8A%B6%E6%80%81-%E6%8C%81%E7%BB%AD%E5%AE%8C%E5%96%84-F28E2B.svg)](#路线图)

[简介](#简介) · [特性](#特性) · [示例](#示例) · [快速开始](#快速开始) · [验证](#验证与依赖) · [文档](#文档索引) · [贡献](#贡献) · [路线图](#路线图)

</div>

---

> **English abstract** — `pretty-charts` is a charting skill for AI agents (ZCode / Claude Code skills) plus a set of reusable, tool-agnostic style assets. It covers data charts and diagrams across three quality tiers (print / report / presentation), ships three colour-blind-safe themes as machine-readable assets (matplotlib, ECharts, TikZ), and enforces a self-checking documentation structure. Every example is runnable code with its rendered output committed.
> Install: `cp -r pretty-charts/skills/pretty-charts ~/.zcode/skills/` (or `~/.claude/skills/`).

## 简介

给 AI Agent 用的图表规范，通常有两个失败模式：**规范写在散文里，Agent 读不完也记不住**；以及**同一个事实被复述在十几个文件里，改一处漏三处**。本项目针对这两点设计：

1. **规格单一来源**。红线、取色、字体、尺寸、非数据图布局只在 [`references/spec/`](skills/pretty-charts/references/spec/) 定义一次；14 份图型文件与 6 份工具文件只**引用**，不复述。
2. **参数化落到机器可读资产**。三档质量差异（色板、字号、线宽、DPI、画布）全部落在 `.mplstyle` / ECharts 主题 JSON / TikZ 模式宏里——散文不再重复描述它们，因此也不会与实现对不上。
3. **结构可机器校验**。[`scripts/check_refs.py`](scripts/check_refs.py) 校验引用完整性、孤儿方法论、孤儿示例；示例索引 [`examples/INDEX.md`](skills/pretty-charts/examples/INDEX.md) 由脚本生成，杜绝"文档说画廊里没有、其实早做完了"这类漂移。

人类也可以直接取用风格资产（见 [快速开始 §2](#2-只用风格资产)），不必走 Agent 流程。

## 特性

| | 能力 |
|---|---|
| **三档质量标准** | T1 出版级 / T2 报告级 / T3 展示级，**按输出介质判定**（印刷 / 屏幕文档 / 投影），而非"学术 vs 商务"这类社交标签 |
| **三套色盲友好主题** | academic（Okabe-Ito）· business（Tableau 10）· showcase（Paul Tol Vibrant），各自落成 matplotlib `.mplstyle`、ECharts 主题 JSON、TikZ 配色/模式宏 |
| **14 类图型方法论** | 数据图 9 类（比较 / 分布 / 构成 / 趋势 / 关系 / 层次网络 / 地理 / 热图矩阵 / 统计推断）+ 非数据图 5 类（流程与时序 / 系统架构 / 层级与逻辑 / 科研示意 / 信息图） |
| **防误导红线** | 九条硬规则（柱状零起点、不确定度不省略、气泡面积编码、样本归一…）+ 诚实原则：**图注里的 n、置信区间、p 值必须由脚本真实计算，不得编造** |
| **示例可跑** | 16 个 Python 脚本 + 16 个 LaTeX 源文件，成图全部由仓库内代码实际渲染并提交 |
| **可校验结构** | 五项自检脚本（引用完整性 / 孤儿方法论 / 孤儿示例 / 硬编码颜色 / 产出存在性） + 生成式示例索引 + GitHub Actions CI |
| **跨平台** | LaTeX 字体层按字体存在性自动回退（Windows 宋体/雅黑 → Noto CJK → TeX Live 自带 Fandol），同一份示例在 Windows 与 Linux 均可编译 |
| **降级路径** | 无 XeLaTeX、缺中文字体、只能出位图时怎么办，写在 [`routing.md` §5](skills/pretty-charts/references/routing.md)，不允许"默默出一张不合规的图" |

## 示例

每个图型文件对应一种类型：这里是**每种类型的一张代表成图**（类型名可点击跳转到对应方法论），全部成图由仓库内代码实际渲染。完整对照见 [examples/INDEX.md](skills/pretty-charts/examples/INDEX.md)。

### 数据图（9 类）

| | | |
|:---:|:---:|:---:|
| **[比较](skills/pretty-charts/references/data/comparison.md)** | **[分布](skills/pretty-charts/references/data/distribution.md)** | **[构成](skills/pretty-charts/references/data/composition.md)** |
| ![](skills/pretty-charts/examples/data/comparison/sorted_bar.png) | ![](skills/pretty-charts/examples/data/distribution/box_violin.png) | ![](skills/pretty-charts/examples/data/composition/donut.png) |
| **[趋势](skills/pretty-charts/references/data/trend.md)** | **[关系](skills/pretty-charts/references/data/relationship.md)** | **[层次与网络](skills/pretty-charts/references/data/network.md)** |
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

**三套主题的观感对照**——同一份数据在三个档位下的渲染差异（由 [demo_styles.py](skills/pretty-charts/examples/style-demo/demo_styles.py) 生成）：

| academic（T1 出版级） | business（T2 报告级） | showcase（T3 展示级） |
|:---:|:---:|:---:|
| ![](skills/pretty-charts/examples/style-demo/output/academic.png) | ![](skills/pretty-charts/examples/style-demo/output/business.png) | ![](skills/pretty-charts/examples/style-demo/output/showcase.png) |

更多论文内嵌效果：[科研流程图](skills/pretty-charts/examples/diagram/flowchart/research_flow.pdf) · [流程图演示版](skills/pretty-charts/examples/diagram/flowchart/ppt_flow.png) · [流程图论文版](skills/pretty-charts/examples/diagram/flowchart/paper_flow.png) · [数据图内嵌](skills/pretty-charts/examples/data/paper/paper_embedded_data.pdf) · [地理图内嵌](skills/pretty-charts/examples/data/geo/paper_embedded_geo.pdf) · [关系图内嵌](skills/pretty-charts/examples/data/relationship/paper_embedded_relationship.pdf) · [层级图内嵌](skills/pretty-charts/examples/diagram/hierarchy/paper_embedded_hierarchy.pdf) · [管线示意图](skills/pretty-charts/examples/diagram/schematic/pipeline_schematic.pdf)

## 快速开始

### 1. 作为 AI Skill 安装

```bash
git clone https://github.com/whlle-yi/pretty-charts.git

# ZCode
cp -r pretty-charts/skills/pretty-charts ~/.zcode/skills/

# Claude Code（skills 目录结构相同）
cp -r pretty-charts/skills/pretty-charts ~/.claude/skills/
```

装好后直接对 Agent 说话即可，例如：

> 画一张论文用的训练流程图
> 这张季度销售数据该怎么展示？给我三种方案

Agent 会按 [`SKILL.md`](skills/pretty-charts/SKILL.md) 的四步契约执行：**定性（画什么图）→ 定档（按输出介质）→ 按 `routing.md` 加载对应方法论 → 交付前过清单自查**，并在交付说明里给出所用档位、导出规格与清单结论。

### 2. 只用风格资产

不装 skill 也能直接复用主题资产：

| 工具 | 用法 |
|---|---|
| matplotlib | `plt.style.use("<技能根>/references/style/matplotlib/academic.mplstyle")`（`academic` / `business` / `showcase` 三选一） |
| ECharts | `echarts.registerTheme("pc", theme)` —— 主题 JSON 见 [references/style/echarts/](skills/pretty-charts/references/style/echarts/) |
| TikZ | `\input{references/style/tikz/preamble.tex}` + `\input{references/style/tikz/flowchart-styles.tex}`（模式宏 `\pcPaperMode` / `\pcPPTMode`） |
| 色板（任意工具） | [references/style/palettes/](skills/pretty-charts/references/style/palettes/) 三份 JSON：`categorical` / `sequential` / `diverging` / `neutral` / `missing` / `semantic` 等 token |

### 3. 跑示例与自检

```bash
pip install -r requirements.txt        # 见下方"依赖与环境"
python scripts/check_refs.py           # 校验引用完整性、孤儿方法论、孤儿示例
python scripts/check_refs.py --write-index   # 重新生成 examples/INDEX.md
```

## 验证与依赖

### 依赖

示例只依赖下列第三方库（**无 pandas / seaborn 依赖**）：

| 库 | 版本（实测） | 用于 |
|---|---|---|
| matplotlib | 3.11.2（要求 ≥3.6） | 全部数据图；`legend(ncols=)`、`set_xticks(ticks, labels)` 需 3.5/3.6+ |
| numpy | 2.5.3 | 数据生成与统计 |
| scipy | 1.18.1 | `t` 分布置信区间、线性回归、KDE、t 检验 |
| geopandas | 0.14.4 | 地理图；底层 shapely/fiona（不依赖已移除的 `geopandas.datasets`） |
| squarify | — | 树图布局 |
| cmcrameri | 1.8 | 感知均匀色图（batlow / vik） |
| scienceplots | — | 期刊尺寸与细节（T1 深化） |

LaTeX 示例需要 **XeLaTeX**（TeX Live 2026 实测），宏包：`pgfplots`、`pgf`、`xeCJK`、`fontspec`、`standalone`、`pgfgantt`，TikZ 库：`shapes.geometric`、`arrows.meta`、`positioning`、`fit`、`backgrounds`、`calc`、`mindmap`。

`~/.zcode/skills/` 与 `~/.claude/skills/` 的 skill 本体**无运行时依赖**，可单独拷贝分发。

### 质量保障

| 检查 | 结果 |
|---|---|
| 16 个 Python 示例执行 | 16/16 通过（exit 0） |
| 16 个 LaTeX 源文件编译 | 16/16 `xelatex` 通过 |
| 五项自检 `scripts/check_refs.py` | 通过：无悬空引用 · 无孤儿方法论 · 无孤儿示例 · 无硬编码颜色 · 产出齐备 |
| 主题 ↔ 色板一致性 | [`demo_styles.py`](skills/pretty-charts/examples/style-demo/demo_styles.py) 断言三套主题的循环色逐色等于 `palettes/*.json` |
| 规格单一来源 | 横切事实仅存在于 `references/spec/`；14 份图型文件与 6 份工具文件只引用不复述 |
| **CI** | GitHub Actions 三个作业：结构与引用自检 · Python 示例 · LaTeX 编译（[.github/workflows/ci.yml](.github/workflows/ci.yml)） |

**已知限制（不隐瞒）**：

- TikZ 侧目前只实现了 **academic（论文版）** 与 PPT 两种模式，**没有 business 模式**；[`routing.md`](skills/pretty-charts/references/routing.md) 与 `spec/` 已如实标注。
- CI 只验证"能跑通、能编译、结构自洽"，**不做成图字节比对**——matplotlib 的字体光栅化与 xelatex 的 PDF ID/时间戳跨平台必然不同，字节比对只会产生噪声失败。
- Windows 原生的宋体/雅黑与 Times New Roman/Arial 在 Linux 上不存在，字体由 [`fonts-serif.tex`](skills/pretty-charts/references/style/tikz/fonts-serif.tex) / [`fonts-sans.tex`](skills/pretty-charts/references/style/tikz/fonts-sans.tex) 逐级回退（Windows 原生 → Noto CJK → Fandol → 最后只发警告不报错，故缺字体不会中断编译）。该回退链**已由 CI（Ubuntu + TeX Live）实测通过**，Linux 前置包为 `fonts-noto-cjk fonts-noto-cjk-extra fonts-texgyre`——其中 `fonts-texgyre` 容易漏，漏了会报 `The font "TeX Gyre Termes" cannot be found`（TeX Live 自带的那份对 fontconfig 不可见）。
- PNG 转换命令（Ghostscript）未在本机实测——环境未安装 `gs`；PDF 产物本身已验证。

## 质量分档

| 档位 | 介质 / 场景 | 主题（色板来源） | 关键约束 |
|:---:|---|:---:|---|
| T1 出版级 | 印刷：期刊 / 学位论文 | academic（Okabe-Ito） | 流程图无底色、黑白可辨、误差与显著性规范、矢量导出 |
| T2 报告级 | 屏幕文档：咨询 / 商务文档 | business（Tableau 10） | 标题即结论、关键数值直标、语义色可用 |
| T3 展示级 | 投影 / 远距离：PPT / 海报 / 大屏 | showcase（Tol Vibrant） | 一图一结论、系列 ≤3、远距离可读 |

**档位由输出介质判定**（印刷 / 屏幕文档 / 投影），不是"学术 vs 商务"这类社交标签——完整判定表与参数差异见 [`routing.md` §1](skills/pretty-charts/references/routing.md)。档位是**场景标准而非质量排名**，质量以 [`checklist.md`](skills/pretty-charts/references/checklist.md) 对应清单衡量。

## 目录结构

```
pretty-charts/
├── README.md / LICENSE / .gitignore / requirements.txt
├── .github/workflows/ci.yml    # CI：结构与引用自检 · Python 示例 · LaTeX 编译
├── scripts/check_refs.py       # 仓库维护工具（不属于 skill 本体）：五项自检 + 生成示例索引
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
        └── examples/
            ├── INDEX.md        # 示例索引：脚本 ↔ 成图（脚本生成）
            ├── data/           # 10 个数据图示例目录
            ├── diagram/        # 8 个非数据图示例目录
            └── style-demo/     # 三主题风格验证样张
```

## 文档索引

**按需读取（Agent 视角）**

| 时机 | 文件 |
|---|---|
| ① 每次任务必读 | [`SKILL.md`](skills/pretty-charts/SKILL.md)（设计哲学 + 四步契约） |
| ② 定档 | [`routing.md`](skills/pretty-charts/references/routing.md)（档位 · 工具 · 读取顺序 · 降级） |
| ③ 图型未定时选型 | [`selection.md`](skills/pretty-charts/references/selection.md) |
| ④ 画什么读什么 | 图型专属：`references/data/`（9 类）· `references/diagram/`（5 类） |
| ⑤ 横切规范 | `references/spec/{integrity,color,type,layout,diagram}.md` |
| ⑥ 按工具栈读 | `data/tool-{matplotlib,echarts}.md` · `diagram/tool-{tikz,graphviz,svg}.md` |
| ⑦ 交付前查 | [`checklist.md`](skills/pretty-charts/references/checklist.md) 对应档位 |
| ⑧ 参照模仿 | [`examples/INDEX.md`](skills/pretty-charts/examples/INDEX.md) |
| ⑨ 被代码加载，不必通读 | `references/style/`（palettes / matplotlib / echarts / tikz） |

**核心文档**

| 文档 | 内容 |
|---|---|
| [SKILL.md](skills/pretty-charts/SKILL.md) | 入口：设计哲学 + 四步契约 + 交付要求 |
| [routing.md](skills/pretty-charts/references/routing.md) | 档位（按输出介质）· 工具选择 · 读取顺序 · 降级路径 |
| [selection.md](skills/pretty-charts/references/selection.md) | 要不要画 · 数据图/非数据图 · 目的+修饰维度 · 归属判定 |
| [checklist.md](skills/pretty-charts/references/checklist.md) | 三档自查清单（交付前逐项过） |
| [spec/integrity.md](skills/pretty-charts/references/spec/integrity.md) | 防误导九条红线 · 图注自含 · 诚实原则 · 统计呈现最低要求 |
| [spec/color.md](skills/pretty-charts/references/spec/color.md) | 取色唯一来源 · 色板/token 表 · 使用规则 · 多图一致性 |
| [spec/type.md](skills/pretty-charts/references/spec/type.md) | 字体与字号层级 · 可变字体与 Ghostscript 两个坑 |
| [spec/layout.md](skills/pretty-charts/references/spec/layout.md) | 尺寸速查 · 导出参数 · 落盘与命名 |
| [spec/diagram.md](skills/pretty-charts/references/spec/diagram.md) | 非数据图通用布局（对齐 / 流向 / 节点文字 / 克制着色） |
| [paper-data.md](skills/pretty-charts/references/data/paper-data.md) | 论文数据图深化：期刊规格 / SciencePlots / Crameri 色图 / 退稿清单 |
| [examples/INDEX.md](skills/pretty-charts/examples/INDEX.md) | 示例索引：脚本 ↔ 成图（脚本自动生成） |

## 贡献

欢迎提交图型、示例与规范改进。提交前请确保：

1. **自检通过**：`python scripts/check_refs.py` 退出码为 0（五项校验，CI 会重复执行）。
2. **新增示例必须被引用**：新脚本要在对应图型方法论文件的「示例」节里**按名**出现，否则自检会判定为孤儿示例。
3. **改完示例重跑索引**：`python scripts/check_refs.py --write-index`。
4. **遵守规格单一来源**：字体/配色/尺寸/红线只在 `references/spec/` 定义；图型与工具文件**引用而不复述**。新增横切事实请加进 `spec/` 并同步 `checklist.md`。
5. **示例必须真跑**：成图提交前重新渲染；图注里出现的统计量必须由脚本真实计算（见 `spec/integrity.md` §3）。
6. **文件组织**：脚本与成图同目录；输出路径用 `Path(__file__)` 推导，不依赖当前工作目录；中间产物不入库。

提交信息建议采用 `类型: 摘要` 的形式（如 `fix:`、`docs:`、`refactor:`、`feat:`）。

## 路线图

- [x] 风格基建：三套色盲友好主题 + matplotlib / ECharts / TikZ 资产（TikZ 目前只有 academic 模式）
- [x] 数据图方法论 + 画廊：9 类全部有代表成图
- [x] 非数据图方法论 + 画廊：13 个 `.tex` 源文件，5 类图型全部有成图
- [x] 地理可视化、信息图整页版式、树图、哑铃图
- [x] 文档结构重构：横切规范单一来源 + 唯一路由 + 生成式示例索引 + 引用自检
- [x] 取色单一来源收尾：16 个示例全部从 palette JSON 读色；`demo_styles.py` 兼作主题↔色板一致性校验
- [x] CI：结构与引用自检 + Python 示例执行 + `.tex` 编译（GitHub Actions 三作业）
- [x] LaTeX 字体层跨平台回退（Windows 原生字体 → Noto CJK → Fandol）
- [ ] TikZ business / showcase 模式
- [ ] 插件清单（`.zcode-plugin/` / `.claude-plugin/`），安装从手动拷贝变为一条命令
- [ ] 数据图第二批画廊：桑基、山脊图、ECDF、日历热图
- [ ] 双语 README（英文全量版）
- [ ] `requirements.txt` 锁定版本区间

## 致谢

配色基于 [Okabe-Ito](https://jfly.uni-koeln.de/color/)、[Tableau 10](https://www.tableau.com/) 与 [Paul Tol](https://personal.sron.nl/~pault/) 色板，顺序/发散色图取自 [ColorBrewer](https://colorbrewer2.org/) 与 [Crameri Scientific Colour Maps](https://www.fabiocrameri.ch/colourmaps/)；非数据图渲染依赖 [TikZ/pgfplots](https://ctan.org/pkg/pgfplots)、[pgfgantt](https://ctan.org/pkg/pgfgantt)；底图数据来自 [Natural Earth](https://www.naturalearthdata.com/)（公有领域）；期刊适配依赖 [SciencePlots](https://github.com/garrettj403/SciencePlots)。

## 许可

[MIT](LICENSE) © 2026 [whlle-yi](https://github.com/whlle-yi)
