# -*- coding: utf-8 -*-
"""树图（treemap）实战（network.md 指导）：层级构成，面积 ∝ 数值。

network.md：树图适合"层级 + 数量构成"（预算、磁盘、销售），面积必须 ∝ 数值，
层级 ≤3，标签放不下就留白。本例演示产品线两级构成的单层展开。
用法：python make_treemap.py
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import squarify

OUT = Path(__file__).resolve().parent
plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(Path(__file__).resolve().parents[3] /
              "references" / "style" / "matplotlib" / "business.mplstyle")
sans = list(plt.rcParams["font.sans-serif"])
sans.remove("Microsoft YaHei"); sans.insert(0, "Microsoft YaHei")
plt.rcParams["font.sans-serif"] = sans

# 产品线构成：面积 ∝ 销售额
items = [
    ("旗舰产品线", 420), ("成长产品线", 310), ("平台服务", 240),
    ("行业方案", 180), ("生态合作", 120), ("硬件配件", 90), ("其他", 60),
]
sizes = [v for _, v in items]
total = sum(sizes)
palette = ["#4E79A7", "#76B7B2", "#59A14F", "#F28E2B",
           "#B07AA1", "#EDC948", "#BAB0AC"]

fig, ax = plt.subplots(figsize=(7.0, 4.2))
# 手动画矩形：布局只算一次，标签按块大小放，杜绝错位重叠
norm_sizes = squarify.normalize_sizes(sizes, 100, 100)
rects = squarify.squarify(norm_sizes, 0, 0, 100, 100)
for (name, v), r, c in zip(items, rects, palette):
    cx, cy = r["x"] + r["dx"] / 2, r["y"] + r["dy"] / 2
    share = f"{v} 亿（{v / total * 100:.0f}%）"
    if r["dx"] > 18 and r["dy"] > 15:          # 大块：名称 + 数值
        ax.text(cx, cy, f"{name}\n{share}", ha="center", va="center",
                fontsize=10, color="white" if c in ("#4E79A7", "#59A14F", "#B07AA1") else "#1A1A1A")
    elif r["dx"] > 8:                           # 中块：只放名称
        ax.text(cx, cy, name, ha="center", va="center", fontsize=8, color="#1A1A1A")
    # 小块：不放文字（README 图注与 hover 补足）
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("2025 年产品线销售构成（合计 1 420 亿）", fontsize=12, fontweight="bold", pad=10)
print("size in:", fig.get_size_inches(), "dpi:", fig.dpi, "savefig dpi:", fig.rcParamsNum if hasattr(fig,'rcParamsNum') else plt.rcParams["savefig.dpi"])
fig.savefig(OUT / "treemap.png", dpi=200, bbox_inches="tight")
print("treemap.png done")
