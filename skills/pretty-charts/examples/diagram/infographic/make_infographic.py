# -*- coding: utf-8 -*-
"""信息图实战（infographic.md 指导）：整页版式 = 标题带 + KPI 卡片 + 主图 + 落款。

infographic.md 三段式：标题说结论、主体 2-4 个视觉块（每块一个图型）、落款标来源；
关键数据放大 3-5 倍做 KPI 卡；配色来自 showcase 色板；字号有明确层级（画布 20in 宽时
标题 46pt / 副标题 15pt / KPI 数字 54pt / 正文 13pt）。
用法：python make_infographic.py
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent
plt.rcParams.update(plt.rcParamsDefault)
sans = ["Noto Sans SC", "Microsoft YaHei", "Arial"]
plt.rcParams["font.sans-serif"] = sans
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False

PRIMARY, ACCENT, GREY = "#0077BB", "#EE7733", "#C7C7C7"
INK, SUB, LINE = "#1A1A1A", "#666666", "#E3E3E3"
BARS = [("华南", 34), ("华东", 28), ("华北", 19), ("西部", 12), ("东北", 7)]

fig = plt.figure(figsize=(20, 11.25))          # 16:9，2000×1125 px @100dpi
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.set_xlim(0, 100); ax.set_ylim(0, 100)

# ---- 顶部强调条 + 标题区 ----
ax.add_patch(mpl.patches.Rectangle((0, 96.2), 100, 3.8, color=PRIMARY))
ax.text(4, 90.5, "华南区 Q3 增速第一", fontsize=46, fontweight="bold",
        color=INK, va="top")
ax.text(4, 83.8, "2025 年第三季度 · 各区域销售额同比增速 · 合计 1.2 亿元",
        fontsize=15, color=SUB, va="top")
ax.plot([4, 96], [80.5, 80.5], color=LINE, lw=1.5)

# ---- KPI 卡片（三张，圆角浅底）----
kpis = [("34%", "华南区同比增速", ACCENT), ("1.2 亿", "Q3 总销售额（元）", PRIMARY),
        ("6 倍", "较 2020 年同期", PRIMARY)]
for i, (num, label, color) in enumerate(kpis):
    x0 = 4 + i * 31.5
    ax.add_patch(FancyBboxPatch((x0, 61), 26, 15.5,
                 boxstyle="round,pad=0.6,rounding_size=1.2",
                 facecolor="#F4F7FA", edgecolor="none"))
    ax.text(x0 + 2.2, 71.5, num, fontsize=54, fontweight="bold", color=color, va="top")
    ax.text(x0 + 2.2, 64.2, label, fontsize=13.5, color=SUB, va="top")

# ---- 主图：区域增速条形（华南 = 强调色，其余灰；数值直标）----
ax.text(4, 55.5, "各区域同比增速", fontsize=17, fontweight="bold", color=INK, va="top")
bx = fig.add_axes([0.04, 0.12, 0.60, 0.40])
for i, (name, v) in enumerate(BARS):
    color = ACCENT if name == "华南" else GREY
    bx.barh(i, v, height=0.58, color=color)
    bx.text(v + 0.9, i, f"{v}%", va="center", fontsize=14,
            color=INK if name == "华南" else "#999999",
            fontweight="bold" if name == "华南" else "normal")
bx.set_yticks(range(5), [b[0] for b in BARS], fontsize=14, color=INK)
bx.invert_yaxis()
bx.set_xlim(0, 40)
bx.set_xticks([])
for s in bx.spines.values():
    s.set_visible(False)
bx.tick_params(length=0)

# ---- 右侧注释块（主图旁的解读）----
ax.text(72, 55.5, "要点", fontsize=17, fontweight="bold", color=INK, va="top")
notes = ["华南连续两个季度领跑，", "同比增速高出全国均值 21 个百分点；", "",
         "东北增长乏力，建议结合", "渠道政策专项评估。"]
for i, line in enumerate(notes):
    ax.text(72, 50.5 - i * 4.6, line, fontsize=13.5, color=SUB, va="top")

# ---- 落款区 ----
ax.plot([4, 96], [6.5, 6.5], color=LINE, lw=1.5)
ax.text(4, 3.5, "数据来源：示例数据（仅为版式演示） · 制图：pretty-charts",
        fontsize=11, color="#999999")

fig.savefig(OUT / "infographic.png", dpi=100)
print("infographic.png done")
