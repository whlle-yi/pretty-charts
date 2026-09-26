# pretty-charts

一套面向 **AI Agent（ZCode skills）与人类** 的高质量绘图技能库：统一风格体系 + 分类图型方法论 + 代码与成图齐全的示例画廊。

## 项目结构

```
pretty-charts/                # 仓库
├── README.md / LICENSE / .gitignore
└── skills/
    └── pretty-charts/        # ★ skill 本体：一个自包含的整体，拷走即用
        ├── SKILL.md          #   入口与路由（数据图 / 非数据图 / 三档质量标准）
    ├── references/           #   方法论参考文件，按需加载
    │   ├── style-guide.md    #     风格规范总纲（配色/字体/导出/防误导/三档清单）
    │   ├── data/             #     数据图：选型决策 + 按分析目的与工具栈
    │   └── diagram/          #     非数据图：按图型与工具栈
    ├── assets/               #   风格资产（skill 内自包含，单一取色来源）
    │   ├── palettes/         #     三套色板：academic / business / showcase（均色盲友好）
    │   ├── matplotlib/       #     三个 .mplstyle 主题文件
    │   ├── echarts/          #     三个 ECharts 主题 JSON
    │   ├── mermaid/          #     mermaid 全局配置
    │   ├── tikz/             #     TikZ/pgfplots 导言区模板
    │   └── fonts.md          #     字体方案
    ├── examples/             #   示例画廊：每类图 = 可运行代码 + 实际成图
    └── scripts/              #   辅助脚本（色板预览、字体检查等）
```

> **安装**：把 `skills/pretty-charts/`（skill 文件夹整体）复制到你的 skills 目录即可；仓库其余文件只是说明文档，运行时不需要。

## 质量分档

同一套风格体系，三档严格程度，档位决定默认主题与检查清单：

| 档位 | 名称 | 默认主题 | 典型场景 |
|------|------|----------|----------|
| T1 | 出版级 | academic | 期刊论文、学位论文 |
| T2 | 报告级 | business | 咨询报告、商务汇报、文档配图 |
| T3 | 展示级 | showcase | PPT、海报、社交媒体 |

## 当前状态

- [x] 仓库骨架 + skill 本体（自包含单元）
- [x] 风格基建（色板 / 字体 / matplotlib / ECharts / mermaid / TikZ 主题）
- [x] 入口 SKILL.md（定性路由 + 分档 + 通用规则）
- [x] references/data（数据图方法论）+ examples/data 示例画廊第一批（10 图型）
- [x] references/diagram（非数据图方法论）+ examples/diagram 示例画廊第一批（mermaid 5 例 + TikZ 1 例）

## 使用

### matplotlib

```python
import matplotlib.pyplot as plt
plt.style.use("skills/pretty-charts/assets/matplotlib/academic.mplstyle")  # 路径按 skill 安装位置调整
```

### ECharts

```js
// 注册主题后使用
chart.setOption(option, { theme: "academic" });  // 主题文件见 skills/pretty-charts/assets/echarts/
```

## 许可

[MIT](LICENSE)
