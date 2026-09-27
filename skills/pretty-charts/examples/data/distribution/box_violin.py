# -*- coding: utf-8 -*-
"""小提琴 + 箱线 + 抖动散点三层组合：分布形态、中位数与个体一并可见（distribution.md）。"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(plt.rcParamsDefault)
# 取色唯一来源：references/assets/palettes/academic.json（references/spec.md「取色与配色」§1：禁止硬编码色值）
SKILL_ROOT = Path(__file__).resolve().parents[3]
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "academic.json")
    .read_text(encoding="utf-8"))
plt.style.use(Path(__file__).resolve().parents[3] /
              "references" / "assets" / "matplotlib" / "academic.mplstyle")

rng = np.random.default_rng(11)
groups = ["对照组", "低剂量", "中剂量", "高剂量"]
data = [rng.normal(m, s, 40) for m, s in [(52, 6), (56, 6.5), (63, 7), (70, 8)]]

fig, ax = plt.subplots(figsize=(4.8, 3.0))
vp = ax.violinplot(data, positions=range(4), widths=0.82, showextrema=False)
for body in vp["bodies"]:
    body.set_facecolor(PALETTE["primary"]); body.set_alpha(0.18); body.set_edgecolor("none")
bp = ax.boxplot(data, positions=range(4), widths=0.16, showfliers=False,
                patch_artist=True, medianprops=dict(color=PALETTE["accent"], lw=1.4),
                boxprops=dict(facecolor=PALETTE["background"], edgecolor=PALETTE["text"]["label"], lw=0.8),
                whiskerprops=dict(color=PALETTE["text"]["label"], lw=0.8),
                capprops=dict(color=PALETTE["text"]["label"], lw=0.8))
for i, vals in enumerate(data):
    ax.scatter(rng.uniform(i - 0.09, i + 0.09, len(vals)), vals, s=7,
               color=PALETTE["primary"], alpha=0.55, linewidths=0, zorder=3)
ax.set_xticks(range(4), groups)
ax.set_ylabel("反应时间（min）")
ax.set_title("剂量越高反应越快（n=40/组）")
fig.savefig(Path(__file__).with_suffix(".png"))
