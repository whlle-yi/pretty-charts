# -*- coding: utf-8 -*-
"""分组均值 + 95%CI 误差棒 + 显著性标注（statistical.md 规范 1/2/3/5）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

STYLE = Path(__file__).resolve().parents[3] / "assets" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")

rng = np.random.default_rng(21)
groups = ["安慰剂", "低剂量", "中剂量", "高剂量"]
raw = [rng.normal(50, 7, 32), rng.normal(54, 7, 32),
       rng.normal(62, 8, 32), rng.normal(74, 9, 32)]
means = [v.mean() for v in raw]
ci = [stats.t.ppf(0.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v)) for v in raw]

fig, ax = plt.subplots(figsize=(4.8, 3.1))
ax.bar(groups, means, yerr=ci, capsize=4, width=0.5,
       color=["#B3B3B3", "#56B4E9", "#0072B2", "#D55E00"],
       error_kw=dict(lw=1, ecolor="#333333"))
# 顶部预留星号空间，防裁切
ax.set_ylim(0, (max(np.array(means) + np.array(ci))) * 1.22)

def sig_mark(ax, x1, x2, y, text):
    ax.plot([x1, x1, x2, x2], [y, y + 1.5, y + 1.5, y], lw=0.9, color="#333333")
    ax.text((x1 + x2) / 2, y + 1.8, text, ha="center", fontsize=9)

sig_mark(ax, 0, 1, 60, "ns")
sig_mark(ax, 0, 3, 88, "***")
ax.set_ylabel("疗效评分")
ax.set_title("高剂量组疗效显著高于安慰剂（95%CI，双侧 t 检验，n=32/组）")
fig.savefig(Path(__file__).with_suffix(".png"))
