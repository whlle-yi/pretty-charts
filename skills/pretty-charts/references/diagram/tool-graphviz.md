# 工具栈：Graphviz（tool-graphviz）

> mermaid 布局爆炸时的退路：模块多、边乱、需要自动最小化交叉的**有向图**。引擎 dot（分层，架构图）、neato/fdp（力导向，网络）、circo（环状）。

## 1. 基本用法

```bash
dot -Tpdf input.dot -o output.pdf    # 矢量优先
dot -Tpng -Gdpi=200 input.dot -o output.png
```

## 2. 风格规范（与本仓库主题对齐）

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

## 3. 与 mermaid 的取舍

| 场景 | 选 |
|---|---|
| ≤20 节点、常见图型 | mermaid（语法更快） |
| 节点 20+ 或 mermaid 布局交叉严重 | Graphviz（dot 引擎布局质量更高） |
| 需要精确 rank 控制、端口锚点（箭头从节点指定边出入） | Graphviz（`:port` 语法） |
| 需要时序图/甘特图/思维导图 | mermaid（Graphviz 无这些图型） |

## 4. 常见坑

1. 记得 `fontname` 逐处声明（graph/node/edge 各自独立，不会继承渲染器的字体回退）。
2. `splines=ortho` 与 `xlabel`、边标签同用时常溢出——有边标签就换 `splines=polyline`。
3. 大图 dpi 调节用 `-Gdpi`，不要缩放输出 PNG（会糊）。
4. 节点固定尺寸 `fixedsize=true` + `width/height`（英寸）防文字溢出框。
