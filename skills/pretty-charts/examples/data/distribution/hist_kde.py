# -*- coding: utf-8 -*-
"""直方图 + KDE：单变量分布，bin 数与 KDE 同图（distribution.md 规范 1）。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

STYLE = Path(__file__).resolve().parents[3] / "assets" / "matplotlib"
plt.style.use(STYLE / "academic.mplstyle")

rng = np.random.default_rng(7)
data = np.concatenate([rng.normal(168, 5.5, 900), rng.normal(178, 5.0, 300)])  # 双峰

fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.hist(data, bins="auto", density=True, color="#0072B2", alpha=0.55, label="频数密度")
xs = np.linspace(data.min() - 4, data.max() + 4, 300)
ax.plot(xs, gaussian_kde(data)(xs), color="#D55E00", lw=1.5, label="KDE")
ax.set_xlabel("身高（cm）")
ax.set_ylabel("密度")
ax.set_title("某校男生身高分布：168cm 附近为主峰，178cm 存在次峰")
ax.legend(loc="upper left")
fig.savefig(Path(__file__).with_suffix(".png"))
