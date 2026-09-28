# -*- coding: utf-8 -*-
"""分组柱状图：类别 × 2 系列，图例置顶不压柱（charts/compare.md 规范 2/4）。"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[3] / "references" / "assets" / "matplotlib"
plt.rcParams.update(plt.rcParamsDefault)
# 取色唯一来源：references/assets/palettes/academic.json（references/common.md「取色与配色」§1：禁止硬编码色值）
SKILL_ROOT = Path(__file__).resolve().parents[3]
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "academic.json")
    .read_text(encoding="utf-8"))
plt.style.use(STYLE / "academic.mplstyle")

groups = ["产品 A", "产品 B", "产品 C", "产品 D"]
y2024 = np.array([320, 280, 190, 150])
y2025 = np.array([410, 300, 260, 180])

x = np.arange(len(groups))
width = 0.36
fig, ax = plt.subplots(figsize=(4.8, 2.9))
b1 = ax.bar(x - width / 2, y2024, width, label="2024", color=PALETTE["neutral"])
b2 = ax.bar(x + width / 2, y2025, width, label="2025", color=PALETTE["primary"])
ax.bar_label(b2, fmt="%d", padding=2)  # 只标注关键年份，防拥挤
ax.set_xticks(x, groups)
ax.set_ylabel("销量（万台）")
ax.set_title("四产品销量同比：全线增长，产品 C 增幅最大")
ax.set_ylim(0, max(y2025) * 1.22)
ax.legend(loc="upper center", ncols=2)
fig.savefig(Path(__file__).with_suffix(".png"))
