# -*- coding: utf-8 -*-
"""分组均值 + 95%CI + 个体散点 + 显著性标注（statistical.md 规范 1/2/4/5）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(Path(__file__).resolve().parents[3] /
              "references" / "style" / "matplotlib" / "academic.mplstyle")

rng = np.random.default_rng(21)
groups = ["安慰剂", "低剂量", "中剂量", "高剂量"]
raw = [rng.normal(m, s, 32) for m, s in [(50, 7), (54, 7), (62, 8), (74, 9)]]
means = [v.mean() for v in raw]
ci = [stats.t.ppf(0.975, 31) * v.std(ddof=1) / np.sqrt(len(v)) for v in raw]

fig, ax = plt.subplots(figsize=(4.8, 3.1))
ax.bar(groups, means, yerr=ci, capsize=4, width=0.5,
       color=["#B3B3B3", "#56B4E9", "#0072B2", "#D55E00"],
       error_kw=dict(lw=1, ecolor="#333333"))
rng2 = np.random.default_rng(3)
for i, v in enumerate(raw):          # 个体散点叠加：n 可见（statistical.md 规范 4）
    ax.scatter(rng2.uniform(i - 0.16, i + 0.16, len(v)), v, s=7,
               color="white", edgecolor="#333333", linewidth=0.5,
               alpha=0.85, zorder=3)
ax.set_ylim(0, (max(np.array(means) + np.array(ci))) * 1.22)

def sig(x1, x2, y, text):
    ax.plot([x1, x1, x2, x2], [y, y + 1.5, y + 1.5, y], lw=0.9, color="#333333")
    ax.text((x1 + x2) / 2, y + 1.8, text, ha="center", fontsize=9)

sig(0, 1, 62, "ns")
sig(0, 3, 90, "***")
ax.set_ylabel("疗效评分")
ax.set_title("高剂量组疗效显著高于安慰剂（95%CI，双侧 t 检验，n=32/组）")
fig.savefig(Path(__file__).with_suffix(".png"))
