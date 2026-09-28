# -*- coding: utf-8 -*-
"""直方图 + KDE：单变量分布，bin 数与 KDE 同图（distribution.md 规范 1）。"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

SKILL_ROOT = Path(__file__).resolve().parents[3]
STYLE = SKILL_ROOT / "references" / "assets" / "matplotlib"
plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(STYLE / "academic.mplstyle")

# 取色唯一来源：references/assets/palettes/academic.json（references/common.md「取色与配色」§1：禁止硬编码色值）
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "academic.json").read_text(encoding="utf-8"))

rng = np.random.default_rng(7)
data = np.concatenate([rng.normal(168, 5.5, 900), rng.normal(178, 5.0, 300)])  # 双峰

fig, ax = plt.subplots(figsize=(4.6, 2.9))
# density=True 得到的是概率密度，纵轴单位是 1/cm，故标签写"概率密度"而非"频数密度"
ax.hist(data, bins="auto", density=True, color=PALETTE["primary"], alpha=0.55,
        label="概率密度")
xs = np.linspace(data.min() - 4, data.max() + 4, 300)
ax.plot(xs, gaussian_kde(data)(xs), color=PALETTE["accent"], lw=1.5, label="KDE")
ax.set_xlabel("身高（cm）")
ax.set_ylabel("概率密度（1/cm）")
ax.set_title("某校男生身高分布：168cm 附近为主峰，178cm 存在次峰")
ax.legend(loc="upper left")
fig.savefig(Path(__file__).with_suffix(".png"))
