# -*- coding: utf-8 -*-
"""折线图 + 波动带 + 线端直标：季节性双系列趋势（trend.md 规范 2/3/5）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(Path(__file__).resolve().parents[3] /
              "references" / "style" / "matplotlib" / "academic.mplstyle")

rng = np.random.default_rng(5)
x = np.arange(24)                                    # 2024-01 至 2025-12
neu = 38 + 2.1 * x + 6 * np.sin(2 * np.pi * x / 12) + rng.normal(0, 2.5, 24)
fuel = 320 - 3.6 * x + 8 * np.sin(2 * np.pi * x / 12) + rng.normal(0, 4, 24)
band = 6 + 0.25 * x

fig, ax = plt.subplots(figsize=(5.4, 3.0))
ax.plot(x, neu, color="#0072B2", lw=1.6)
ax.fill_between(x, neu - band, neu + band, color="#0072B2", alpha=0.15, lw=0)
ax.plot(x, fuel, color="#999999", lw=1.6)
for name, y, c in [("新能车", neu, "#0072B2"), ("燃油车", fuel, "#999999")]:
    ax.annotate(f"{name} {y[-1]:.0f}", (x[-1], y[-1]), xytext=(5, 0),
                textcoords="offset points", va="center", fontsize=8.5,
                color=c, fontweight="bold")
ax.set_xticks(x[::3], [f"{1 + i % 12}月" for i in x[::3]], fontsize=8)
ax.set_xlim(-0.4, 25.8)
ax.set_ylabel("月销量（万台）")
fig.savefig(Path(__file__).with_suffix(".png"))
