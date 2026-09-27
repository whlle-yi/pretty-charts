# -*- coding: utf-8 -*-
"""散点 + 回归线 + 95% 置信带 + 相关系数标注（relationship.md 规范 1/2）。"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

STYLE = Path(__file__).resolve().parents[3] / "references" / "assets" / "matplotlib"
plt.rcParams.update(plt.rcParamsDefault)
# 取色唯一来源：references/assets/palettes/academic.json（references/spec.md「取色与配色」§1：禁止硬编码色值）
SKILL_ROOT = Path(__file__).resolve().parents[3]
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "academic.json")
    .read_text(encoding="utf-8"))
plt.style.use(STYLE / "academic.mplstyle")

rng = np.random.default_rng(3)
n = 120
ad = rng.uniform(10, 100, n)                      # 广告投入
sales = 18 + 0.62 * ad + rng.normal(0, 8, n)      # 销售额

r, p = stats.pearsonr(ad, sales)
slope, inter, _, _, stderr = stats.linregress(ad, sales)
xs = np.linspace(ad.min(), ad.max(), 100)
yhat = inter + slope * xs
conf = stats.t.ppf(0.975, n - 2) * stderr * np.sqrt(
    1 / n + (xs - ad.mean()) ** 2 / np.sum((ad - ad.mean()) ** 2))

fig, ax = plt.subplots(figsize=(4.8, 3.2))
ax.fill_between(xs, yhat - conf, yhat + conf, color=PALETTE["primary"], alpha=0.18, lw=0, label="95% 置信带")
ax.scatter(ad, sales, s=18, color=PALETTE["primary"], alpha=0.55, linewidths=0, label="门店")
ax.plot(xs, yhat, color=PALETTE["accent"], lw=1.8, label="线性拟合")
ax.set_xlabel("广告投入（万元）")
ax.set_ylabel("月销售额（万元）")
ax.set_title(f"广告投入与销售额正相关（r = {r:.2f}，p < 0.001，n = {n}）")
ax.legend(loc="upper left")
fig.savefig(Path(__file__).with_suffix(".png"))
