# 工具栈：SVG 手绘（tool-svg）

> 最后手段：信息图、海报、复杂插画、需要完全自定义视觉时。成本最高，先确认 TikZ/Graphviz 真不够用。

## 1. 何时用 SVG

- 信息图/海报整页版式（infographic.md）；
- 插画级示意图（渐变、圆角、阴影、图标组合）；
- 需要在网页中带交互（CSS hover、JS 动画）的示意图。

## 2. 尺寸与视图框

- `viewBox` 定坐标（如 `0 0 900 1600` 长图、`0 0 1280 720` 幻灯），`width/height` 留给交付渠道；
- 文字防溢出：`text` 估宽（中文 ≈ font-size × 字数），或用 `textLength` 约束；长文本拆 `tspan`。

## 3. 风格纪律（与其他主题对齐）

1. 颜色从 `assets/palettes/*.json` 取值写进 `:root` CSS 变量，禁止散落硬编码：
   ```svg
   <style> :root { --primary:#0072B2; --text:#1A1A1A; --grid:#CCCCCC; } </style>
   ```
2. 字体族统一：`font-family: 'Noto Sans SC','Microsoft YaHei',Arial,sans-serif`；交付前 `svg.fonttype` 等价处理——**关键文字转路径**（印刷）或确认目标机器有字体（网页）。
3. 网格与对齐：元素坐标落在 8px 栅格上；组用 `<g>` + `transform` 组织，不散放。
4. 线宽体系：主线 2px / 次线 1px / 辅助虚线 1px dashed，全图一致。
5. 信息图遵循 infographic.md 的三段式与防误导红线；示意图遵循 schematic.md 的三要素。

## 4. 校验与导出

- 浏览器打开目视（不同渲染器对 `text` 溢出、字体回退差异大）；
- 转 PNG：`resvg`/`cairosvg`/浏览器截图，2x 输出防糊；
- 投稿/印刷：转 PDF（`rsvg-convert -f pdf` 或浏览器打印），文字转曲。
- AI 生成 SVG 的自查：打开确认无文字溢出、无元素重叠、字体回退不炸版——**不渲染就交付 SVG 是本栈第一大事故来源**。

## 5. 常见坑

1. `text-anchor` 默认 start，居中要显式 `middle`；
2. 中文竖排/换行不支持自动——全靠 `tspan` 手排；
3. `em`/百分比尺寸在某些渲染器（Word 内嵌）失效，用绝对 px/pt；
4. 滤镜（drop-shadow）在非浏览器渲染器常被忽略，重要视觉别依赖滤镜。
