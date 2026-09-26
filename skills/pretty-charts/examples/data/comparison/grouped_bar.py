# -*- coding: utf-8 -*-
"""分组柱状图：类别 × 2 系列，图例置顶不压柱（comparison.md 规范 2/4）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[3] / "assets" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")

groups = ["产品 A", "产品 B", "产品 C", "产品 D"]
y2024 = np.array([320, 280, 190, 150])
y2025 = np.array([410, 300, 260, 180])

x = np.arange(len(groups))
width = 0.36
fig, ax = plt.subplots(figsize=(4.8, 2.9))
b1 = ax.bar(x - width / 2, y2024, width, label="2024", color="#B3B3B3")
b2 = ax.bar(x + width / 2, y2025, width, label="2025", color="#0072B2")
ax.bar_label(b2, fmt="%d", padding=2)  # 只标注关键年份，防拥挤
ax.set_xticks(x, groups)
ax.set_ylabel("销量（万台）")
ax.set_title("四产品销量同比：全线增长，产品 C 增幅最大")
ax.set_ylim(0, max(y2025) * 1.22)
ax.legend(loc="upper center", ncols=2)
fig.savefig(Path(__file__).with_suffix(".png"))
