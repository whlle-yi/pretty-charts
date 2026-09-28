# -*- coding: utf-8 -*-
"""环图：块数 ≤5、12 点起降序顺时针、块上直标、中心放总量（charts/compare.md 六规则）。"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SKILL_ROOT = Path(__file__).resolve().parents[3]
STYLE = SKILL_ROOT / "references" / "assets" / "matplotlib"
plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(STYLE / "academic.mplstyle")

# 取色唯一来源：references/assets/palettes/academic.json（references/common.md「取色与配色」§1：禁止硬编码色值）
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "academic.json").read_text(encoding="utf-8"))

data = {"华东": 386, "华南": 254, "华北": 190, "西部": 120, "东北": 85}
data = dict(sorted(data.items(), key=lambda kv: -kv[1]))  # 降序
values = list(data.values())
colors = PALETTE["categorical"][:len(values)]              # 按色板顺序取色，不自造

fig, ax = plt.subplots(figsize=(4.2, 3.6))
wedges, _ = ax.pie(
    values, colors=colors, startangle=90, counterclock=False,
    wedgeprops=dict(width=0.38, edgecolor=PALETTE["background"], linewidth=1.5),
)
total = sum(values)
for w, (name, v) in zip(wedges, data.items()):
    angle = (w.theta1 + w.theta2) / 2
    x, y = np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))
    ax.annotate(f"{name} {v / total * 100:.0f}%", (x, y),
                xytext=(1.15 * x, 1.15 * y), ha="center", va="center", fontsize=9)
ax.text(0, 0.06, f"{total}", ha="center", va="center", fontsize=15, fontweight="bold")
ax.text(0, -0.16, "总销量（万台）", ha="center", va="center", fontsize=8,
        color=PALETTE["subtext"])
ax.set_title("2025 年销量区域构成", pad=12)   # 字号/字重取 academic 主题
fig.savefig(Path(__file__).with_suffix(".png"))
