# 场景入口（scenarios）

> 三档档位的**唯一定义处**：定档依据、各档阅读路径与场景专属规则都在这里。SKILL.md 第 2 步定档后进入对应节。
> 阅读顺序是编码前置条件（SKILL.md 执行顺序契约）；通用规范（配色/字体/导出/防误导）统一见 `style-guide.md`，本文件只列场景特例。

## 三档定义

| | T1 出版级 | T2 报告级 | T3 展示级 |
|---|---|---|---|
| 场景 | 期刊论文、学位论文、正式报告 | 咨询/商务报告、文档配图、邮件插图 | PPT、海报、社交媒体 |
| 默认主题（色板来源） | academic（Okabe-Ito） | business（Tableau 10） | showcase（Tol Vibrant） |
| 画布 | 期刊栏宽决定（90/190mm） | 16:9 或版心宽度 | 16:9（PPT 页面等大） |
| 字号逻辑 | 印刷可读即可（最小 7pt） | 屏幕舒适阅读（最小 9pt） | 远距离可读（最小 11pt） |
| 线条 | 细（0.8–1.5pt） | 中（1–2pt） | 粗（2–2.5pt） |
| 位图 DPI | ≥600（线图 ≥1200 更佳） | 200 | 200 |
| 装饰余量 | 几乎为零 | 克制 | 可用强调色块/大标注 |

用户未指定档位时：学术语境 → T1，工作文档 → T2，演示/宣传 → T3。同一交付物内**所有图必须同一档位**。档位是场景标准而非质量排名，质量以 `style-guide.md` §7 对应清单衡量。

## T1 论文

**阅读顺序**：① `style-guide.md` §3 配色、§4 字体、§5 尺寸导出 → ② 数据图读 `data/` 对应目的文件 + `data/tool-matplotlib.md`；流程图读 `diagram/flowchart.md` + `tool-tikz.md`，示意图读 `diagram/schematic.md` → ③ 示例：`examples/data/`、`examples/diagram/flowchart/paper_embedded*.tex` → ④ 交付前过 `style-guide.md` §7.1。

**场景特例**：
- figsize 按期刊栏宽换算：单栏 90mm = 3.54in，双栏 190mm = 7.48in
- 流程图 `\pcPaperMode`（无底色），文档层声明中文宋体 + 西文 Times New Roman

## T2 报告

**阅读顺序**：① `style-guide.md` §3、§4、§5 → ② `data/` 对应目的文件 + `data/tool-matplotlib.md` / `tool-echarts.md`；结构图读 `diagram/` 对应文件 → ③ `examples/`（换 business 主题）→ ④ §7.2。

**场景特例**：
- Word 配图宽度对齐版心（15–16cm）；网页交付 ECharts 用 business 主题
- 允许语义色（success/warning/danger，见 `style-guide.md` §3.2 语义色条目）

## T3 演示

**阅读顺序**：① `style-guide.md` §3、§4、§5 → ② `data/` 对应目的文件 + `data/tool-echarts.md`（网页/交互）；流程图 `flowchart.md`（TikZ `\pcPPTMode`）；信息图整页 `diagram/infographic.md` → ③ `examples/diagram/flowchart/ppt_flow.tex` → ④ §7.3。

**场景特例**：
- 深色背景（大屏）需检查对比度；ECharts 动画仅入场
- 导出尺寸 = 插入位置等大（PPT 半页 15×8.4cm），位图不缩放

## 通用收尾（三档都要）

画完按 `style-guide.md` §7 对应档位清单**逐项自查**。交付说明必须写明三项（SKILL.md 执行顺序契约第 5 步）：**已读文件列表、所用主题与档位、自查清单逐项结论**。
