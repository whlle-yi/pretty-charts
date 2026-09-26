# 工具栈：TikZ / pgfplots（tool-tikz）

> T1 出版级示意图主力：矢量、字体与 LaTeX 正文一致、几何精确。编译 XeLaTeX。导言区与配色模板：`assets/tikz/preamble.tex`。

## 1. 何时用 TikZ（而不是 mermaid）

- 论文正文里的示意图（字体必须与正文一致）；
- 需要精确坐标、循环阵列、镜像对称的装置/结构图；
- 需要与 pgfplots 数据图混排（示意元素 + 真实数据同图）。
- 普通流程图/时序图：mermaid 更快，别用 TikZ 折磨自己。

## 2. 模板接入

```latex
\documentclass{standalone}   % 单图输出；论文内嵌时去掉本行改 figure 环境
\input{assets/tikz/preamble.tex}  % 主题配色 pcBlue... 与轴风格
\begin{document}
\begin{tikzpicture}
  ...
\end{tikzpicture}
\end{document}
```

编译：`xelatex -interaction=nonstopmode file.tex`。

## 3. 示意图常用技法（高质量的关键）

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

## 4. 常见坑

1. **Windows 的 Noto Sans SC 是可变字体，xdvipdfmx 无法嵌入**（报 `fatal: Invalid font`）→ TikZ 出 PDF 用 Microsoft YaHei 或静态版思源黑体；matplotlib/ECharts 不受影响。
2. standalone 中文：文档类选项加 `varwidth` 或直接用 `standalone` + xeCJK（模板已含）。
2. 节点距离用 `positioning` 库的 `right=of`，**不用 `at (x,y)` 手摆**（改一处全崩）。
3. 箭头 `->` 与 `-{Stealth}` 混用会导致全场箭头不一致——统一在 tikzset 定义。
4. pgfplots 混排时坐标系：示意图元素放 `axis description cs` 或画在 axis 外层 tikzpicture。
5. 编译慢/循环深：`\usetikzlibrary{positioning, arrows.meta, calc, fit, backgrounds}` 按需加，别全量。
