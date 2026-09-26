# 工具栈：mermaid（tool-mermaid）

> 非数据图默认首选：文本生成、版本可控、覆盖流程/时序/状态/甘特/思维导/类图。本仓库主题配置 `assets/mermaid/mermaid-config.json`（学术基调：浅蓝节点、蓝边框、灰连线）。

## 1. 命令行渲染

```bash
# 标准渲染（PNG 2x，白底）
mmdc -i diagram.mmd -o diagram.png -c mermaid-config.json -b white -s 2

# 矢量（网页/印刷优先）
mmdc -i diagram.mmd -o diagram.svg -c mermaid-config.json -b white
```

- `-s 2`：2 倍缩放，位图插入文档必开（默认 1x 太糊）。
- `-b white`：透明底在深色环境会"隐身"，交付位图固定白底（或指定色）。

**chrome-headless-shell 缺失报错时**，用系统 Edge/Chrome：写 puppeteer 配置（见 `examples/diagram/puppeteer-edge.json`）并加 `-p` 参数：

```json
{ "executablePath": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", "args": ["--no-sandbox"] }
```

或安装：`npx puppeteer browsers install chrome-headless-shell`。

## 2. 主题与内联样式纪律

- **默认只靠主题文件**，不在图源里写 `style`/`classDef`；个别强调节点（关键路径）才用 classDef 覆盖，且颜色从 `assets/palettes/` 取。
- 中文与西文字体由主题 fontFamily 决定；不要在图源里指定字体。
- 深色 PPT：换深色 themeVariables（底深字浅），不改节点结构。

## 3. 布局调优（mermaid 布局不理想时的顺序）

1. 换方向：`flowchart TD` ↔ `flowchart LR`（TD 窄高，LR 宽扁）。
2. 连线防交叉：调整节点声明顺序（mermaid 按声明顺序就近摆放）。
3. 分组：`subgraph` 强制聚类；子图标题写在 `subgraph id[标题]`。
4. 长文字换行：节点内用 `<br/>`，或 `wrappingWidth`（主题已设 220）。
5. 以上都救不了 → 转 Graphviz（`tool-graphviz.md`）。

## 4. 常见坑

1. 节点文字含特殊字符（括号、引号）用引号包裹：`A["文本 (带括号)"]`。
2. 边标签含 `/` 与 `|` 会截断，同样引号处理：`-->|"是/通过"|`。
3. 思维导图（mindmap）缩进敏感，Tab 与空格不能混用。
4. 甘特图日期默认从今天滚动的写法（`:0, 3d`）不稳定，交付图写死起始日期。
5. 序列图 participant 过多时图超宽——用 `box` 分组或拆图。
6. mmdc 渲染中文需要系统字体（Windows 自带雅黑；Linux 服务器装 fonts-noto-cjk）。
