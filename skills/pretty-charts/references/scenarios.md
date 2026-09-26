# 场景入口（scenarios）

> 按交付场景聚合的**阅读路径**与**场景专属规则**。SKILL.md 第 2 步定档后，先读本文件对应节，再按其清单加载方法论文件——避免漏读自查清单、漏看场景特例。

## T1 论文（学术出版）

**典型任务**：期刊论文、学位论文的数据图与流程图/示意图。

**阅读顺序**：
1. `style-guide.md` §2（三档定义）、§5.1（期刊尺寸）、§7.1（T1 自查清单）
2. `assets/fonts.md`（字号下限与中西文规则）
3. 数据图 → `references/data/` 对应分析目的文件 + `tool-matplotlib.md`
4. 流程图 → `references/diagram/flowchart.md` + `tool-tikz.md`；示意图 → `schematic.md`
5. 示例：`examples/data/`（academic 主题）、`examples/diagram/flowchart/paper_embedded*.tex`（论文内嵌写法）

**场景专属规则**：
- 尺寸按期刊栏宽：单栏 90mm（3.54in）、双栏 190mm（7.48in），matplotlib `figsize` 直接换算填入
- 主题锁定 `academic.mplstyle`；流程图用 `\pcPaperMode`（**无底色**），字体在文档层声明**中文宋体 + 西文 Times New Roman**
- 黑白可辨：数据图系列叠加线型/标记做冗余编码；流程图靠边框粗细区分关键路径，**不靠颜色**
- 不确定度与显著性：SD/SE/95%CI 必须注明类型，星号规范见 `data/statistical.md`
- 图注自含：n、统计口径、误差类型、检验方法全部写进 caption，不看正文也能懂
- 导出：矢量 PDF 优先（`pdf.fonttype: 42` 已在主题内置），位图兜底 ≥600dpi
- mermaid 只作流程草稿，**不进论文**

## T2 报告（商务/文档配图）

**典型任务**：咨询报告、工作文档、商务汇报的插图。

**阅读顺序**：
1. `style-guide.md` §2、§6（防误导红线）、§7.2（T2 自查清单）
2. 数据图 → `references/data/` 对应目的文件 + `tool-matplotlib.md` / `tool-echarts.md`
3. 流程/架构 → `references/diagram/` 对应文件 + `tool-mermaid.md`（交付可用）
4. 示例：`examples/` 各目录（换主题为 business 即可）

**场景专属规则**：
- 主题 `business.mplstyle` / ECharts `business.json`；Word 配图宽度对齐版心（15–16cm）
- 标题即结论（"Q3 华南区增速第一（+34% YoY）"），关键数值直接标注在图上
- 数字口径、单位、时间范围在图内可追溯；柱状 y 轴零起点，无违规双轴
- 允许语义色（success/warning/danger）表达达标/预警
- 导出 200dpi PNG 或 SVG；嵌入文档后图内文字 ≥9pt

## T3 演示（PPT/海报/社交媒体）

**典型任务**：幻灯片插图、海报版块、信息图数据块、网页大屏。

**阅读顺序**：
1. `style-guide.md` §2、§7.3（T3 自查清单）
2. 数据图 → `references/data/` 对应目的文件 + `tool-echarts.md`（网页/交互）或 `tool-matplotlib.md`（静态位图）
3. 流程/架构 → `references/diagram/flowchart.md`（TikZ `\pcPPTMode`）或 `tool-mermaid.md`；信息图整页 → `diagram/infographic.md`
4. 示例：`examples/diagram/flowchart/ppt_flow.tex`（演示版流程图）

**场景专属规则**：
- 主题 `showcase.mplstyle` / ECharts `showcase.json` / TikZ `\pcPPTMode`；深色背景检查对比度
- **一页一结论**：删掉与结论无关的系列，系列数 ≤3
- 远距离可读：等效字号 ≥11pt、线宽 ≥2pt；标注直接放数据旁，不用小图例
- 导出尺寸 = 插入位置等大（PPT 半页 15×8.4cm），位图不缩放；ECharts 动画仅入场

## 通用收尾（三档都要）

画完按 `style-guide.md` §7 对应档位清单**逐项自查**，修完再交付；交付时说明所用主题、档位、导出规格。
