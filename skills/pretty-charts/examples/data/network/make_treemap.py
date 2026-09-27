# -*- coding: utf-8 -*-
"""树图（treemap）实战（charts/structure.md 指导）：层级构成，面积 ∝ 数值。

charts/structure.md：树图适合"层级 + 数量构成"（预算、磁盘、销售），面积必须 ∝ 数值，
层级 ≤3，标签放不下就留白。本例演示产品线两级构成的单层展开。
用法：python make_treemap.py
"""
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import squarify

SKILL_ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(SKILL_ROOT / "references" / "assets" / "matplotlib" / "business.mplstyle")
sans = list(plt.rcParams["font.sans-serif"])
if "Microsoft YaHei" in sans:
    sans.remove("Microsoft YaHei")
sans.insert(0, "Microsoft YaHei")
plt.rcParams["font.sans-serif"] = sans

# 取色唯一来源：references/assets/palettes/business.json（references/spec.md「取色与配色」§1：禁止硬编码色值）
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "business.json").read_text(encoding="utf-8")
)
palette = PALETTE["categorical"]

# 产品线构成：面积 ∝ 销售额
items = [
    ("旗舰产品线", 420), ("成长产品线", 310), ("平台服务", 240),
    ("行业方案", 180), ("生态合作", 120), ("硬件配件", 90), ("其他", 60),
]
sizes = [v for _, v in items]
total = sum(sizes)


def text_color(hexcolor):
    """按相对亮度自动选深/浅文字，保证对比度（不靠手工维护的色名白名单）。"""
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (1, 3, 5))
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return PALETTE["text"]["title"] if luminance > 0.5 else PALETTE["background"]


fig, ax = plt.subplots(figsize=(7.0, 4.2))
fig.canvas.draw()
# squarify 追求"方块"，故必须传坐标区真实宽高比：画布非正方形时若仍按 100×100
# 布局，方块会被拉成长条，树图的可读性随之丢失（面积仍 ∝ 数值，形状却失真）。
box = ax.get_window_extent()
W, H = 100.0, 100.0 * box.height / box.width
norm_sizes = squarify.normalize_sizes(sizes, W, H)
rects = squarify.squarify(norm_sizes, 0, 0, W, H)

for (name, v), r, c in zip(items, rects, palette):
    ax.add_patch(mpl.patches.Rectangle((r["x"], r["y"]), r["dx"], r["dy"],
                 facecolor=c, edgecolor=PALETTE["background"], linewidth=2))
    cx, cy = r["x"] + r["dx"] / 2, r["y"] + r["dy"] / 2
    share = f"{v} 亿（{v / total * 100:.0f}%）"
    if r["dx"] > 0.18 * W and r["dy"] > 0.15 * H:     # 大块：名称 + 数值
        ax.text(cx, cy, f"{name}\n{share}", ha="center", va="center",
                fontsize=10, color=text_color(c))
    elif r["dx"] > 0.08 * W:                           # 中块：只放名称
        ax.text(cx, cy, name, ha="center", va="center", fontsize=9,
                color=PALETTE["text"]["title"])
    # 小块：不放文字（图注与交互补足）

ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_title("2025 年产品线销售构成（合计 1 420 亿）", pad=10)  # 字号/字重取 business 主题
fig.savefig(OUT / "treemap.png")
print("treemap.png done")
