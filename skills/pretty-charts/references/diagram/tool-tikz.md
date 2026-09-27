# 工具栈：TikZ / pgfplots（tool-tikz）

> T1 出版级示意图主力：矢量、字体与 LaTeX 正文一致、几何精确。编译 XeLaTeX。导言区与配色模板：`references/style/tikz/preamble.tex`。

## 1. 定位

- 本仓库**全部非数据图的交付级工具**：流程图、时序图、甘特图、思维导图、架构图、示意图均由 TikZ 输出（各图型预置样式见 references/style/tikz/）；
- 论文正文插图（字体必须与正文一致）；
- 需要精确坐标、循环阵列、镜像对称的装置/结构图；
- 需要与 pgfplots 数据图混排（示意元素 + 真实数据同图）。

## 2. 模板接入

```latex
\documentclass{standalone}   % 单图输出；论文内嵌时去掉本行改 figure 环境
\input{references/style/tikz/preamble.tex}  % 主题配色 pcBlue... 与轴风格
\begin{document}
\begin{tikzpicture}
  ...
\end{tikzpicture}
\end{document}
```

编译：`xelatex -interaction=nonstopmode file.tex`。

## 3. 流程图预置样式（references/style/tikz/flowchart-styles.tex）

流程图**不要手写节点样式**，直接加载预置文件后选模式：

```latex
\input{references/style/tikz/preamble.tex}
\input{references/style/tikz/flowchart-styles.tex}
\setmainfont{Times New Roman}\setCJKmainfont{SimSun} % 论文版字体；演示版用 Arial+黑体
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
  \draw[pc flow back] (c.south) |- (n.east);   % 回流虚线
\end{tikzpicture}
```

可用样式：`pc start`（圆角起止）/ `pc process`（处理）/ `pc key`（关键路径：论文版粗边框、演示版主色实心）/ `pc decision`（菱形判断）/ `pc io`（平行四边形）/ `pc db`（圆柱）/ `pc sub`+`pc sub label`（阶段虚线框）/ `pc flow`、`pc flow back`（回流虚线）/ `pc label`（分支标签白底）。

两模式约定：**论文版无底色**（黑白印刷安全，中文宋体+西文 Times New Roman），**演示版 showcase 彩色**（中文黑体+西文 Arial）；同一结构只切模式与字体两行。完整示例见 `examples/diagram/flowchart/paper_flow.tex` 与 `ppt_flow.tex`。

## 4. 示意图常用技法（高质量的关键）

```latex
% 节点样式集中定义，全场复用
\tikzset{
  module/.style={draw=pcBlue, fill=pcBlue!15, rounded corners=2pt,
                 minimum width=2.2cm, minimum height=0.8cm,
                 font=\small\sffamily, align=center},
  data/.style={module, fill=pcGray!20, draw=pcGray},
  flow/.style={-{Stealth[length=2.5mm]}, thick, pcAxis},
}
% 箭头从指定锚点出入，防斜穿
\draw[flow] (a.east) -- node[above, font=\footnotesize]{特征} (b.west);
% 循环画阵列，不手摆
\foreach \i in {0,...,3} \node[module] at (\i*2.8, 0) {模块\i};
% scope 镜像对称
\begin{scope}[xscale=-1, x=-8cm] ... \end{scope}
```

- 颜色只用 `pcBlue` 系（来自 academic 色板），强调用 `pcOrange`；黑白可辨靠线型/填充图案补充。
- 箭头样式全场统一（`Stealth` 一致尺寸）；线宽：主线 `thick`（0.8–1pt），辅助线 `thin`。
- 文字节点 `align=center`，防长文本撑爆框。

## 5. 常见坑

1. **Windows 的 Noto Sans SC 是可变字体，xdvipdfmx 无法嵌入**（报 `fatal: Invalid font`）→ TikZ 出 PDF 用 Microsoft YaHei 或静态版思源黑体；matplotlib/ECharts 不受影响。
2. standalone 中文：文档类选项加 `varwidth` 或直接用 `standalone` + xeCJK（模板已含）。
2. 节点距离用 `positioning` 库的 `right=of`，**不用 `at (x,y)` 手摆**（改一处全崩）。
3. 箭头 `->` 与 `-{Stealth}` 混用会导致全场箭头不一致——统一在 tikzset 定义。
4. pgfplots 混排时坐标系：示意图元素放 `axis description cs` 或画在 axis 外层 tikzpicture。
5. 编译慢/循环深：`\usetikzlibrary{positioning, arrows.meta, calc, fit, backgrounds}` 按需加，别全量。
