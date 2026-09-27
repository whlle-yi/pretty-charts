# 路由（routing）

> 本文件是**档位定义**、**工具选择**与**"该读哪些文件"规则**的唯一定义处。
> `SKILL.md` 定完性之后进本文件；图型未定则先看 [`selection.md`](selection.md)。

## 1. 档位：由输出介质决定

档位不是"学术 / 商务"这类社交标签——学术海报算学术还是演示？边界必然含混。改为看**输出介质的物理属性**：

| 判据 | T1 出版级 | T2 报告级 | T3 展示级 |
|---|---|---|---|
| 介质 | **印刷**（可能只有黑白） | 屏幕文档，逐字阅读 | 投影 / 远距离 / 一屏一结论 |
| 典型场景 | 期刊、学位论文、正式报告 | 咨询与商务报告、Word 配图、邮件插图 | PPT、海报、社交媒体、大屏 |
| 观看距离 | ~30cm 手持 | 50–70cm | 2m+ |
| 色彩可靠性 | 可能只有灰度 | 彩色可靠 | 彩色可靠，可能深色底 |
| 默认色板 | academic | business | showcase |
| 画布 | 期刊栏宽（90 / 190mm） | 16:9 或版心宽度 | 16:9（与页面等大） |
| 字号下限 | 7pt | 9pt | 11pt 等效 |
| 线宽 | 细（0.8–1.5pt） | 中（1–2pt） | 粗（2–2.5pt） |
| 位图 DPI | ≥600（线图 ≥1200 更佳） | 200 | 200 |
| 装饰余量 | 几乎为零 | 克制 | 可用强调色块 / 大标注 |

**用户已说明档位则遵从。** 没说时按介质判：要印刷 → T1；进文档给人读 → T2；投影或远距离 → T3。仍不确定就问一句，不要猜。

**档位差异只有上表这些项，且已全部落在机器可读资产里**（`references/style/matplotlib/*.mplstyle`、`references/style/echarts/*.json`、`references/style/tikz/*.tex` 的模式宏）。**其余规范与档位无关**——不要因为换档去改写字体、防误导等规范。

同一交付物内所有图必须**同档同色板**；多图交付还须做到语义 → 颜色全局一致（`spec/color.md` §5）。档位是**场景标准而非质量排名**，质量以 [`checklist.md`](checklist.md) 对应清单衡量。

## 2. 工具选择

**数据图**

| 交付形态 | 工具 | 说明 |
|---|---|---|
| T1 / T2 静态出图 | matplotlib | 主栈；seaborn 做统计图；plotly 仅用于交互探索 |
| T3 网页 / 交互 | ECharts | 内置主题；D3 仅在需要完全自定义视觉时 |

**非数据图**

| 工具 | 何时用 |
|---|---|
| **TikZ / pgfplots** | 交付级一律用它；流程图、时序图有预置双模式样式，其余按方法论手写 |
| Graphviz | 自动布局的复杂有向图（节点多、边乱），TikZ 手摆驾驭不了时 |
| SVG 手绘 | 完全自定义的示意图 / 插画，最后手段、成本最高 |

每个工具栈都有专属文件，按名读对应的一份：
- 数据图：`references/data/tool-matplotlib.md`、`references/data/tool-echarts.md`
- 非数据图：`references/diagram/tool-tikz.md`、`references/diagram/tool-graphviz.md`、`references/diagram/tool-svg.md`

**不使用 mermaid。**

## 3. 读取顺序（唯一规则）

```
1. 定档              → 本文件 §1（得到档位与色板）
2. 选型（图型未定时）  → selection.md
3. 加载三类文件：
   a. 图型专属        → references/data/<目的>.md 或 references/diagram/<图型>.md
   b. 工具专属        → references/data/tool-<工具>.md 或 references/diagram/tool-<工具>.md
   c. 横切规范        → references/spec/{color,type,layout,diagram,integrity}.md
4. 作图              → 代码里显式加载主题资产；禁止硬编码样式常量
5. 交付前            → checklist.md 对应档位逐项过
```

`spec/` 的横切规范**只在一处定义**：图型文件与工具文件提到字体、配色、尺寸、落盘、红线时，一律**引用而不得复述**。

## 4. 场景特例

**T1**：figsize 按期刊栏宽换算（90mm = 3.54in，190mm = 7.48in）；精确栏宽时关掉 tight bbox（`spec/layout.md` §2.5）；流程图用 `\pcPaperMode`；需经 Ghostscript 管线时先换静态字体（`spec/type.md` §3）。另读 `references/data/paper-data.md`（期刊规格、SciencePlots 集成、Crameri 色图、退稿清单）。

**T2**：Word 配图宽度对齐版心（15–16cm）；网页交付用 ECharts business 主题；允许 `semantic` 语义色（`spec/color.md` §3）。

**T3**：深色背景需检查对比度；ECharts 动画仅入场；导出尺寸 = 插入位置等大，位图不缩放；整页信息图读 `references/diagram/infographic.md`。

## 5. 降级路径（环境缺失时）

技能规定了主力工具栈，但环境不一定齐备。**不要因为缺工具就默默出一张不合规的图**——按下面处理，并在交付说明里写明降级了什么。

| 缺什么 | 怎么办 |
|---|---|
| 无 XeLaTeX / 字体 | 先确认是否真缺（`xelatex --version`、`fc-list`，Windows 用字体名核对）。TikZ 无法编译时**问用户**：装 TeX 发行版，或降级为 matplotlib 手绘示意图（降级产物必须在交付说明里标注"非交付级"） |
| 无中文字体（Linux） | 装 `fonts-noto-cjk` 后重试；**不要**用西文字体硬渲染中文 |
| 只能出位图 | 至少 600dpi，并在交付说明写明"非矢量" |
| 缺地图 / 底图数据 | 用随仓库分发的数据（如 `examples/data/geo/naturalearth_lowres.geojson`）；不要静默改成非地图图型 |
