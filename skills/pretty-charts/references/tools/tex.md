# tex

## 工具栈：TikZ / pgfplots


> T1 出版级示意图主力：矢量、字体与 LaTeX 正文一致、几何精确。编译 XeLaTeX。导言区与配色模板：`references/assets/tikz/preamble.tex`。
> **横切规范只在本技能 `references/common.md` 定义一次**（红线 [`../common.md`](../common.md)、取色 [`../common.md`](../common.md)、字体 [`../common.md`](../common.md)、尺寸与落盘 [`../common.md`](../common.md)）；本文件**只讲本工具栈的用法与坑**，不复述上述内容。

### 1. 定位

- 本仓库**全部非数据图的交付级工具**：流程图、时序图、甘特图、思维导图、架构图、示意图均由 TikZ 输出。其中**流程图、时序图有预置样式文件**（`references/assets/tikz/flowchart-styles.tex`、`sequence-styles.tex`）；甘特图用 pgfgantt、思维导图用 TikZ `mindmap` 库、架构图/示意图按本文件与对应方法论章手写；
- 论文正文插图（字体必须与正文一致）；
- 需要精确坐标、循环阵列、镜像对称的装置/结构图；
- 需要与 pgfplots 数据图混排（示意元素 + 真实数据同图）。

### 2. 模板接入

**路径基准**：本文所有 `\input` 均相对**当前 .tex 文件所在目录**。仓库示例位于 `examples/<类>/<图型>/`，距技能根 3 层，故写作 `../../../references/assets/tikz/…`。若把片段搬进自己的项目，请把整个 `references/assets/tikz/` 拷入项目，并按实际层级调整前缀。 <!-- check-refs: skip -->

```latex
\documentclass[border=6pt]{standalone}                % 单图输出（示例用）
\input{../../../references/assets/tikz/preamble.tex}   % 配色 pcBlue… 与轴风格  % check-refs: skip
\begin{document}
\begin{tikzpicture}
  ...
\end{tikzpicture}
\end{document}
```

编译：`xelatex -interaction=nonstopmode file.tex`，**须在该文件所在目录执行**，否则 `\input` 解析不到。

**论文内嵌**：不是"删掉 `\documentclass` 那一行"——那样会留下孤立的 `\begin{document}`。正确做法是删掉 `\documentclass[…]{standalone}` 与 `\begin{document}`、`\end{document}` 三行，把 `tikzpicture` 整体放进正文的 `figure` 环境，并把 `\input{…preamble.tex}` 移到正文导言区。

### 3. 流程图预置样式（references/assets/tikz/flowchart-styles.tex）

流程图**不要手写节点样式**，直接加载预置文件后选模式：

```latex
\input{../../../references/assets/tikz/preamble.tex}        % check-refs: skip
\input{../../../references/assets/tikz/flowchart-styles.tex} % check-refs: skip
\setmainfont{Times New Roman}\setCJKmainfont{SimSun} % 论文版字体；演示版改 Arial + 黑体
% \pcPPTMode  % 演示版开关（默认 \pcPaperMode）
\begin{document}
\begin{tikzpicture}[node distance=7mm and 9mm]
  \node[pc start]                 (s) {开始};
  \node[pc process, below=of s]   (a) {处理};
  \node[pc decision, below=of a]  (b) {条件？};
  \node[pc key, below=of b]       (k) {关键步骤};
  \node[pc db, right=of k]        (d) {数据库};
  \node[pc io, right=of a]        (i) {输入输出};
  \draw[pc flow]      (s) -- (a);
  \draw[pc flow back] (k.west) -- ++(-1.0,0) |- (a.west);   % 回流虚线：绕主轴外侧
\end{tikzpicture}
\end{document}
```

可用样式：`pc start`（圆角起止）/ `pc process`（处理）/ `pc key`（关键路径：论文版粗边框、演示版主色实心）/ `pc decision`（菱形判断）/ `pc io`（平行四边形）/ `pc db`（圆柱）/ `pc sub`+`pc sub label`（阶段虚线框）/ `pc flow`、`pc flow back`（回流虚线）/ `pc label`（分支标签白底）。

TikZ 侧只有两种模式，**没有 business 模式**，资产也不按档位命名（`references/assets/tikz/` 里是 `preamble.tex` 加两个模式宏，不是 `academic/business/showcase` 三份文件）。

两模式约定：**论文版无底色**（黑白印刷安全，中文宋体 + 西文 Times New Roman），**演示版 showcase 彩色**（中文黑体 + 西文 Arial）。注意 `\pcPaperMode` / `\pcPPTMode` **只切换配色、线宽与字号，不含字体**——中英文字体由你文档里的 `\setmainfont` / `\setCJKmainfont` 自行决定；示例 `examples/diagram/flowchart/paper_flow.tex` 与 `ppt_flow.tex` 的结构完全相同，差异只有"模式行 1 行 + 字体 2 行"共 3 行。

### 4. 示意图常用技法（高质量的关键）

```latex
% 节点样式集中定义，全场复用
\tikzset{
  module/.style={draw=pcBlue, fill=pcBlue!15, rounded corners=2pt,
                 minimum width=2.2cm, minimum height=0.8cm,
                 font=\small\sffamily, align=center},
  data/.style={module, fill=pcNeutral!40, draw=pcNeutral},   % 中性/次要元素用 pcNeutral
  flow/.style={-{Stealth[length=2.5mm]}, thick, pcAxis},
}
% 箭头从指定锚点出入，防斜穿
\draw[flow] (a.east) -- node[above, font=\footnotesize]{特征} (b.west);
% 循环画阵列，不手摆
\foreach \i in {0,...,3} \node[module] at (\i*2.8, 0) {模块\i};
% scope 镜像对称：以竖直轴 x=-8cm 镜像（映射 x -> -16cm - x）
\begin{scope}[cm={-1,0,0,1,(-16cm,0cm)}] ... \end{scope}
```

- 颜色只用 `pcBlue` 系（来自 academic 色板），强调用 `pcOrange`，中性/次要元素用 `pcNeutral`；黑白可辨靠线型/填充图案补充。
- 箭头样式全场统一（`Stealth` 一致尺寸）；线宽：主线 `thick`（0.8–1pt），辅助线 `thin`。
- 文字节点 `align=center`，防长文本撑爆框。

### 5. 常见坑

1. **Windows 的 Noto Sans SC 是可变字体，xdvipdfmx 无法嵌入**（报 `fatal: Invalid font`）→ TikZ 出 PDF 用 Microsoft YaHei 或静态版思源黑体；matplotlib/ECharts 不受影响。
2. standalone 的中文支持：模板 `preamble.tex` 已 `\usepackage{xeCJK}`，无需另加；`standalone` 默认紧贴内容，故示例统一用 `\documentclass[border=6pt]{standalone}` 留白，中文不会被裁切。`varwidth` 是"按内容宽度折行"的选项，与中文无关，不要为中文去加它。
3. 节点距离用 `positioning` 库的 `below=of` / `right=of` 做**相对定位**；确需坐标定位时（如 `diagrams.md` 的"节点用坐标对齐车道"、并列终点同行）才用 `at (x,y)`，且同类节点必须共用同一套 x/y 基线，避免只为躲线而把图撑宽。
4. 箭头 `->` 与 `-{Stealth}` 混用会导致全场箭头不一致——统一在 tikzset 定义。
5. pgfplots 混排时坐标系：示意图元素放 `axis description cs` 或画在 axis 外层 tikzpicture。
6. **PDF → PNG 预览**：需要位图（网页橱窗、聊天展示）时用 TeX Live 自带的 rungs：
   `rungs -dBATCH -dNOPAUSE -sDEVICE=png16m -r300 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -sOutputFile=x.png x.pdf`。
   TikZ 展品为三件套（tex + pdf + png）：pdf 是矢量原件，png 由本命令生成、仅供网页内嵌（GitHub 不渲染 PDF）；300dpi 起步。
7. 编译慢/循环深：`\usetikzlibrary{positioning, arrows.meta, calc, fit, backgrounds}` 按需加，别全量。

---

## 工具栈：Graphviz


> TikZ 手摆无法驾驭时的退路：模块多、边乱、需要自动最小化交叉的**有向图**。引擎 dot（分层，架构图）、neato/fdp（力导向，网络）、circo（环状）。本机未安装 dot，本文件样式未经实测，使用前先验证。
> **横切规范只在本技能 `references/common.md` 定义一次**（红线 [`../common.md`](../common.md)、取色 [`../common.md`](../common.md)、字体 [`../common.md`](../common.md)、尺寸与落盘 [`../common.md`](../common.md)）；本文件**只讲本工具栈的用法与坑**，不复述上述内容。

### 1. 基本用法

```bash
dot -Tpdf input.dot -o output.pdf    # 矢量优先
dot -Tpng -Gdpi=200 input.dot -o output.png
```

### 2. 风格规范（与本仓库主题对齐）

```dot
digraph G {
  graph [rankdir=TB, splines=ortho, fontname="Noto Sans SC", bgcolor="white"];
  node  [shape=box, style="rounded,filled", fillcolor="#DCE8F2", color="#0072B2",
         fontname="Noto Sans SC", fontsize=11, fontcolor="#1A1A1A", margin="0.15,0.08"];
  edge  [color="#4D4D4D", fontcolor="#333333", fontname="Noto Sans SC", fontsize=9];
}
```

- `splines=ortho`：正交连线（架构图首选）；曲线图用默认 `splines=spline`。
- 形状语义：`box`=服务、`cylinder`=存储、`hexagon`=外部系统、`diamond`=判断。
- 颜色：节点填充浅蓝 `#DCE8F2` + 边框 `#0072B2`（学术档），强调节点用主色实心；**不自造颜色**。
- 分层/分组：`rank=same` 固定同层；`cluster_*` 子图表达物理/组织边界。
- 中文标签：确保系统装有中文字体（Windows 雅黑可用，Linux 装 fonts-noto-cjk）。

### 3. 与 TikZ 的取舍

| 场景 | 选 |
|---|---|
| ≤20 节点、常规结构图 | TikZ（预置样式 + 手工布局可控） |
| 节点 20+ 或连线交叉严重 | Graphviz（dot 引擎布局质量更高） |
| 需要精确 rank 控制、端口锚点（箭头从节点指定边出入） | Graphviz（`:port` 语法） |

### 4. 常见坑

1. 记得 `fontname` 逐处声明（graph/node/edge 各自独立，不会继承渲染器的字体回退）。
2. `splines=ortho` 与 `xlabel`、边标签同用时常溢出——有边标签就换 `splines=polyline`。
3. 大图 dpi 调节用 `-Gdpi`，不要缩放输出 PNG（会糊）。
4. 节点固定尺寸 `fixedsize=true` + `width/height`（英寸）防文字溢出框。

---

## 工具栈：SVG 手绘


> 最后手段：信息图、海报、复杂插画、需要完全自定义视觉时。成本最高，先确认 TikZ/Graphviz 真不够用。
> **横切规范只在本技能 `references/common.md` 定义一次**（红线 [`../common.md`](../common.md)、取色 [`../common.md`](../common.md)、字体 [`../common.md`](../common.md)、尺寸与落盘 [`../common.md`](../common.md)）；本文件**只讲本工具栈的用法与坑**，不复述上述内容。

### 1. 何时用 SVG

- 信息图/海报整页版式（`diagrams.md`「信息图与海报」）；
- 插画级示意图（渐变、圆角、阴影、图标组合）；
- 需要在网页中带交互（CSS hover、JS 动画）的示意图。

### 2. 尺寸与视图框

- `viewBox` 定坐标（如 `0 0 900 1600` 长图、`0 0 1280 720` 幻灯），`width/height` 留给交付渠道；
- 文字防溢出：`text` 估宽（中文 ≈ font-size × 字数），或用 `textLength` 约束；长文本拆 `tspan`。

### 3. 风格纪律（与其他主题对齐）

1. 颜色从 `references/assets/palettes/*.json` 取值写进 `:root` CSS 变量，禁止散落硬编码：
   ```svg
   <style> :root { --primary:#0072B2; --text:#1A1A1A; --grid:#CCCCCC; } </style>
   ```
2. 字体族统一：`font-family: 'Noto Sans SC','Microsoft YaHei',Arial,sans-serif`；交付前 `svg.fonttype` 等价处理——**关键文字转路径**（印刷）或确认目标机器有字体（网页）。
3. 网格与对齐：元素坐标落在 8px 栅格上；组用 `<g>` + `transform` 组织，不散放。
4. 线宽体系：主线 2px / 次线 1px / 辅助虚线 1px dashed，全图一致。
5. 信息图遵循 `diagrams.md`「信息图与海报」的三段式与防误导红线；示意图遵循 `diagrams.md`「科研示意图」的三要素。

### 4. 校验与导出

- 浏览器打开目视（不同渲染器对 `text` 溢出、字体回退差异大）；
- 转 PNG：`resvg`/`cairosvg`/浏览器截图，2x 输出防糊；
- 投稿/印刷：转 PDF（`rsvg-convert -f pdf` 或浏览器打印），文字转曲。
- AI 生成 SVG 的自查：打开确认无文字溢出、无元素重叠、字体回退不炸版——**不渲染就交付 SVG 是本栈第一大事故来源**。

### 5. 常见坑

1. `text-anchor` 默认 start，居中要显式 `middle`；
2. 中文竖排/换行不支持自动——全靠 `tspan` 手排；
3. `em`/百分比尺寸在某些渲染器（Word 内嵌）失效，用绝对 px/pt；
4. 滤镜（drop-shadow）在非浏览器渲染器常被忽略，重要视觉别依赖滤镜。
