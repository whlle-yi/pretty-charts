# -*- coding: utf-8 -*-
"""折线图 + 线端直接标注：代替图例（trend.md 规范 3/2）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[3] / "references" / "style" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")

x = np.arange(2020, 2026)
series = {"新能车": [40, 65, 95, 140, 185, 230], "燃油车": [420, 400, 380, 355, 330, 305],
          "混动车": [25, 38, 60, 90, 125, 160]}
palette = {"新能车": "#0072B2", "燃油车": "#999999", "混动车": "#D55E00"}

fig, ax = plt.subplots(figsize=(5.2, 3.0))
for name, y in series.items():
    ax.plot(x, y, color=palette[name], lw=2, marker="o", markersize=4)
    ax.annotate(f"{name} {y[-1]}", (x[-1], y[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", fontsize=9,
                color=palette[name], fontweight="bold")
ax.set_xlim(x[0], x[-1] + 0.9)  # 右侧留白给线端标注
ax.set_xticks(x)
ax.set_ylabel("销量（万台）")
ax.set_title("新能与混动挤压燃油车份额（2020–2025）")
fig.savefig(Path(__file__).with_suffix(".png"))
