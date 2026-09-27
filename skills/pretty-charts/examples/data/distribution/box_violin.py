# -*- coding: utf-8 -*-
"""箱线图 + 抖动散点：多组分布比较，个体可见（distribution.md 规范 2/3）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[3] / "references" / "style" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")

rng = np.random.default_rng(11)
groups = ["对照组", "低剂量", "中剂量", "高剂量"]
means = [52, 56, 63, 70]
data = [rng.normal(m, 6, 40) for m in means]

fig, ax = plt.subplots(figsize=(4.8, 2.9))
bp = ax.boxplot(data, tick_labels=groups, showfliers=False, patch_artist=True, widths=0.5)
for patch in bp["boxes"]:
    patch.set_facecolor("#0072B2")
    patch.set_alpha(0.35)
    patch.set_edgecolor("#333333")
for i, vals in enumerate(data, start=1):
    ax.scatter(rng.uniform(i - 0.12, i + 0.12, len(vals)), vals,
               s=9, color="#0072B2", alpha=0.6, zorder=3, linewidths=0)
ax.set_ylabel("反应时间（min）")
ax.set_title("剂量越高反应越快（n=40/组）")
fig.savefig(Path(__file__).with_suffix(".png"))
