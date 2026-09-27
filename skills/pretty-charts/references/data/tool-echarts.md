# 工具栈：ECharts / D3（tool-echarts）

> 适用 T2/T3 网页交付：交互报告、dashboard、大屏。T1 出版级不用本栈。
> **横切规范只在本技能 `spec/` 定义一次**（红线 [`../spec/integrity.md`](../spec/integrity.md)、取色 [`../spec/color.md`](../spec/color.md)、字体 [`../spec/type.md`](../spec/type.md)、尺寸与落盘 [`../spec/layout.md`](../spec/layout.md)）；本文件**只讲本工具栈的用法与坑**，不复述上述内容。

## 0. 何时选本栈

- 交付形态是网页/大屏/可交互报告（hover 提示、缩放、联动）
- 数据量大（散点 >1 万点用 `large: true` 或 GL）
- 需要动画入场（克制使用：仅入场动画，`animationDuration: 600`）

静态导出选 matplotlib；两者都可用时，按交付渠道定，不按个人喜好。

## 1. 主题注册（每个页面第一件事）

```js
// academic.json / business.json / showcase.json 任选，fetch 后 echarts.registerTheme
const resp = await fetch("references/style/echarts/business.json");
const theme = await resp.json();
echarts.registerTheme("pretty-charts", theme);
const chart = echarts.init(dom, "pretty-charts", { renderer: "svg" });
```

- `renderer: "svg"`：网页内嵌首选（清晰、可缩放）；大数据量动画场景用默认 canvas。
- 主题已内置：色板、字体族、标题/图例/轴/tooltip 样式。**option 里不要再覆盖颜色与字体**，个别覆盖需注释原因。
- T3 大屏：底色深色时用 showcase 色板 + 容器深色背景，并按 `../checklist.md` 的 T3 一节 检查对比度。

## 2. 高频规范落地

```js
// 图例置顶不压数据
legend: { top: 0, left: "center" },
grid:   { top: 48, left: 56, right: 24, bottom: 40, containLabel: true },

// 柱状 y 轴从 0（红线）
yAxis: { min: 0 },

// 直接标注代替图例（系列少时）
series: [{ label: { show: true, position: "top", formatter: "{c}" } }],

// 环图：块 ≤5、从 12 点起、降序
series: [{ type: "pie", radius: ["55%", "78%"], startAngle: 90,
           label: { show: true, formatter: "{b} {d}%" } }],

// 折线线端直标（图例可关）
endLabel: { show: true, formatter: "{a}" },

// tooltip 统一
tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
```

## 3. 导出

- 静态图：`chart.getDataURL({ type: "png", pixelRatio: 3 })`（T2/T3 位图 ≥200dpi 等效）；矢量用 SVG 渲染器直接另存 DOM。
- 报告截图场景：先 `chart.resize()` 到目标尺寸再导出。
- 交付给无 JS 环境（Word/PDF）：老实用 matplotlib 重画同一张图，别截网页。

## 4. 常见坑

1. **颜色数组**：`color` 没显式给时 ECharts 用内置色板而不是本仓库主题——确认主题 JSON 的 `color` 字段已生效（init 第二参数传了主题名）。
2. **字体**：浏览器端主题 fontFamily 生效，但 canvas 渲染下中文回退链由 CSS 决定，页面 body 也要设置同链字体。
3. **resize**：容器尺寸变化后必须 `chart.resize()`，否则图糊/裁切；用 `window.addEventListener("resize", ...)` 或 ResizeObserver。
4. **数据集与编码**：`dataset.source` + `encode` 比逐系列 data 好，但注意 `dimensions` 顺序。
5. D3 场景（需要完全自定义视觉）：配色仍从 `references/style/palettes/*.json` 取值，禁止自造色；比例尺与轴参考 observable 标准写法。
