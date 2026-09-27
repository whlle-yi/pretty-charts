# -*- coding: utf-8 -*-
"""哑铃图：两个时点的类别对比（比较类，点图变体）。

charts/compare.md：比大小首选位置/长度编码；两时点多类别对比时，哑铃图比双柱
更清晰地呈现"变化量"——线长即增幅，端点直接标注，无需图例查色。
文件名 sorted_bar 为历史遗留，实际图型是哑铃图。
用法：python sorted_bar.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

plt.rcParams.update(plt.rcParamsDefault)
# 取色唯一来源：references/assets/palettes/academic.json（references/spec.md「取色与配色」§1：禁止硬编码色值）
SKILL_ROOT = Path(__file__).resolve().parents[3]
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "academic.json")
    .read_text(encoding="utf-8"))
plt.style.use(Path(__file__).resolve().parents[3] /
              "references" / "assets" / "matplotlib" / "academic.mplstyle")

# 城市 → (2024, 2025) 销售额（亿元）
data = {
    "武汉": (1050, 1280), "成都": (930, 1160), "杭州": (905, 990),
    "南京": (820, 870), "西安": (700, 760), "沈阳": (700, 540),
}
# 按 2025 值降序（y 轴自下而上，故升序排列）
items = sorted(data.items(), key=lambda kv: kv[1][1])
names = [k for k, _ in items]
v24 = [ab[0] for _, ab in items]
v25 = [ab[1] for _, ab in items]
gains = [b - a for a, b in zip(v24, v25)]
star = gains.index(max(gains))               # 增幅最大的城市

fig, ax = plt.subplots(figsize=(4.8, 3.1))
for i, (a, b) in enumerate(zip(v24, v25)):
    color = PALETTE["accent"] if i == star else PALETTE["primary"]
    ax.plot([a, b], [i, i], color=color, lw=2.2, solid_capstyle="round", zorder=2)
    ax.scatter(a, i, s=42, facecolor=PALETTE["background"], edgecolor=PALETTE["text"]["tick"],
               linewidth=1.1, zorder=3)
    ax.scatter(b, i, s=52, color=color, zorder=3)
    ax.text(b + 22, i, f"+{b - a}", va="center", fontsize=8,
            color=color, fontweight="bold" if i == star else "normal")

ax.set_yticks(range(len(names)), names)
ax.set_xlabel("销售额（亿元）")
ax.set_xlim(580, 1400)
ax.scatter([], [], s=42, facecolor=PALETTE["background"], edgecolor=PALETTE["text"]["tick"], linewidth=1.1,
           label="2024")
ax.scatter([], [], s=52, color=PALETTE["primary"], label="2025")
ax.legend(loc="lower right", fontsize=8)
fig.savefig(Path(__file__).with_suffix(".png"))
