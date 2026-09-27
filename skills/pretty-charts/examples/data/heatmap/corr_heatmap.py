# -*- coding: utf-8 -*-
"""相关矩阵热图：diverging 色板中心对齐 0 + 数值标注（heatmap.md 规范 1/4）。"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[3] / "references" / "style" / "matplotlib"
plt.rcParams.update(plt.rcParamsDefault)
# 取色唯一来源：references/style/palettes/academic.json（spec/color.md §1：禁止硬编码色值）
SKILL_ROOT = Path(__file__).resolve().parents[3]
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "style" / "palettes" / "academic.json")
    .read_text(encoding="utf-8"))
plt.style.use(STYLE / "academic.mplstyle")

rng = np.random.default_rng(5)
# 造一组两两相关的指标
base = rng.normal(0, 1, (300, 5))
data = np.column_stack([base[:, 0],
                        0.8 * base[:, 0] + 0.6 * base[:, 1],
                        -0.7 * base[:, 0] + 0.7 * base[:, 2],
                        base[:, 1],
                        0.5 * base[:, 1] + 0.5 * base[:, 3]])
labels = ["指标 A", "指标 B", "指标 C", "指标 D", "指标 E"]
corr = np.corrcoef(data.T)

fig, ax = plt.subplots(figsize=(4.6, 3.8))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.grid(False)  # imshow 图关闭主题网格，防网格线透过色块
ax.set_xticks(range(5), labels, rotation=30, ha="right")
ax.set_yticks(range(5), labels)
for i in range(5):  # 格内标 r 值
    for j in range(5):
        v = corr[i, j]
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                color=PALETTE["background"] if abs(v) > 0.6 else PALETTE["text"]["title"])
cbar = fig.colorbar(im, ax=ax, shrink=0.82)
cbar.set_label("Pearson r", fontsize=9)
ax.set_title("指标相关矩阵（n = 300）")
fig.savefig(Path(__file__).with_suffix(".png"))
