# -*- coding: utf-8 -*-
"""堆叠柱状图：构成 × 类别，绝对量 + 总量标注（composition.md）。

堆叠图中只有最底块可直接比大小；如需比较上方分量，改用分面小倍数图。
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[3] / "assets" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")

quarters = ["一季度", "二季度", "三季度", "四季度"]
parts = {
    "线上": np.array([420, 460, 510, 580]),
    "门店": np.array([300, 310, 330, 360]),
    "批发": np.array([180, 190, 210, 240]),
}
palette = ["#0072B2", "#56B4E9", "#999999"]  # 底块最易比较 → 主色；最次要 → 灰
totals = sum(parts.values())

fig, ax = plt.subplots(figsize=(4.8, 3.0))
bottom = np.zeros(len(quarters))
for (name, vals), c in zip(parts.items(), palette):
    ax.bar(quarters, vals, bottom=bottom, label=name, color=c, width=0.55)
    for i, (v, b) in enumerate(zip(vals, bottom)):  # 每块内标占比
        pct = v / totals[i] * 100
        if pct >= 8:  # 小于 8% 的块不放文字，防溢出
            ax.text(i, b + v / 2, f"{pct:.0f}%", ha="center", va="center",
                    fontsize=8, color="white" if c != "#56B4E9" else "#1A1A1A")
    bottom += vals

for i, t in enumerate(totals):  # 柱顶标总量
    ax.annotate(f"{t:,.0f}", (i, t), xytext=(0, 3), textcoords="offset points",
                ha="center", fontsize=9, fontweight="bold")
ax.set_ylabel("销售额（万元）")
ax.set_title("季度销售额构成：线上占比持续扩大")
ax.set_ylim(0, totals.max() * 1.15)
ax.legend(loc="upper center", ncols=3)
fig.savefig(Path(__file__).with_suffix(".png"))
