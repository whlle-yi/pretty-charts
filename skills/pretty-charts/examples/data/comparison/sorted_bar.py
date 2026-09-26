# -*- coding: utf-8 -*-
"""排序条形图：按数值降序 + 主色强调冠军、其余灰化（comparison.md 规范 1/3/4）。"""
from pathlib import Path

import matplotlib.pyplot as plt

STYLE = Path(__file__).resolve().parents[3] / "assets" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")

data = {"武汉": 1280, "成都": 1160, "杭州": 990, "南京": 870, "西安": 760, "沈阳": 540}
items = sorted(data.items(), key=lambda kv: kv[1])  # 条形图 y 轴自下而上，升序=视觉降序
names, values = [k for k, _ in items], [v for _, v in items]
colors = ["#B3B3B3"] * (len(items) - 1) + ["#0072B2"]  # 灰化配角，主色强调第一名

fig, ax = plt.subplots(figsize=(4.5, 2.8))
bars = ax.barh(names, values, color=colors, height=0.62)
ax.bar_label(bars, fmt="%d", padding=3)
ax.set_title("2025 年六城市销售额（亿元）：武汉居首")
ax.set_xlabel("销售额")
ax.set_xlim(0, max(values) * 1.15)  # 顶部留白给数值标签
fig.savefig(Path(__file__).with_suffix(".png"))
