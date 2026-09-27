# -*- coding: utf-8 -*-
"""环图：块数 ≤5、12 点起降序顺时针、块上直标、中心放总量（composition.md 六规则）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[3] / "references" / "style" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")

data = {"华东": 386, "华南": 254, "华北": 190, "西部": 120, "东北": 85}
data = dict(sorted(data.items(), key=lambda kv: -kv[1]))  # 降序
values = list(data.values())
colors = ["#0072B2", "#56B4E9", "#009E73", "#CC79A7", "#999999"]

fig, ax = plt.subplots(figsize=(4.2, 3.6))
wedges, _ = ax.pie(
    values, colors=colors, startangle=90, counterclock=False,
    wedgeprops=dict(width=0.38, edgecolor="white", linewidth=1.5),
)
total = sum(values)
for w, (name, v) in zip(wedges, data.items()):
    angle = (w.theta1 + w.theta2) / 2
    x, y = np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))
    ax.annotate(f"{name} {v / total * 100:.0f}%", (x, y),
                xytext=(1.15 * x, 1.15 * y), ha="center", va="center", fontsize=9)
ax.text(0, 0.06, f"{total}", ha="center", va="center", fontsize=15, fontweight="bold")
ax.text(0, -0.16, "总销量（万台）", ha="center", va="center", fontsize=8, color="#666666")
ax.set_title("2025 年销量区域构成", fontsize=11, fontweight="bold", pad=12)
fig.savefig(Path(__file__).with_suffix(".png"))
