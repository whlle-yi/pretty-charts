# -*- coding: utf-8 -*-
"""信息图实战（infographic.md 指导）：整页版式 = 标题区 + KPI 大数字 + 主图 + 落款。

infographic.md 三段式：标题说结论、主体 2-4 个视觉块、落款标来源；
每块一个图型；关键数据放大 3-5 倍做 KPI 卡；配色来自 showcase 色板。
用法：python make_infographic.py
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(Path(__file__).resolve().parents[3] /
              "references" / "style" / "matplotlib" / "showcase.mplstyle")
sans = list(plt.rcParams["font.sans-serif"])
sans.remove("Microsoft YaHei"); sans.insert(0, "Microsoft YaHei")
plt.rcParams["font.sans-serif"] = sans

PRIMARY, ACCENT, GREY = "#0077BB", "#EE7733", "#BBBBBB"
BARS = [("华东", 34), ("华南", 28), ("华北", 19), ("西部", 12), ("东北", 7)]

fig = plt.figure(figsize=(10, 5.63))
fig.patch.set_facecolor("white")
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")

# ---- 标题区：结论式标题 + 口径 ----
ax.text(0.05, 0.92, "华南区 Q3 增速第一", fontsize=26, fontweight="bold",
        color="#1A1A1A", va="top")
ax.text(0.05, 0.845, "2025 年第三季度 · 各区域销售额同比增速 · 合计 1.2 亿元",
        fontsize=11, color="#666666", va="top")

# ---- KPI 大数字块（3 个）----
kpis = [("34%", "华南区同比增速", ACCENT), ("1.2 亿", "Q3 总销售额", PRIMARY),
        ("6 倍", "较 2020 年同期", PRIMARY)]
for i, (num, label, color) in enumerate(kpis):
    x = 0.05 + i * 0.24
    ax.text(x, 0.66, num, fontsize=34, fontweight="bold", color=color, va="top")
    ax.text(x, 0.56, label, fontsize=11, color="#666666", va="top")
ax.plot([0.05, 0.95], [0.51, 0.51], color="#E5E5E5", lw=1)

# ---- 主体：唯一一张图（区域增速条形，华南=强调色，其余灰）----
ax_bar = fig.add_axes([0.08, 0.13, 0.62, 0.33])
for i, (name, v) in enumerate(BARS):
    color = ACCENT if name == "华南" else GREY
    ax_bar.barh(i, v, height=0.62, color=color)
    ax_bar.text(v + 0.8, i, f"{v}%", va="center", fontsize=10,
                color="#1A1A1A" if name == "华南" else "#999999")
ax_bar.set_yticks(range(5), [b[0] for b in BARS], fontsize=11)
ax_bar.invert_yaxis()
ax_bar.set_xlim(0, 40)
ax_bar.set_xticks([])
for s in ax_bar.spines.values():
    s.set_visible(False)
ax_bar.tick_params(length=0)

# ---- 落款区 ----
ax.text(0.05, 0.03, "数据来源：示例数据（仅为版式演示） · 制图：pretty-charts",
        fontsize=9, color="#999999")

fig.savefig(OUT / "infographic.png", dpi=200)
print("infographic.png done")
