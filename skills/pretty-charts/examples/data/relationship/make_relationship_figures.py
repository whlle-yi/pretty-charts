# -*- coding: utf-8 -*-
"""关系类数据图实战（relationship.md 指导）：分组回归带 + 过绘处理 + 气泡图。

产出矢量 PDF（供 paper_embedded_relationship.tex 引用，双栏 190mm）：
  fig1.pdf  (a) 分组散点 + 各自线性回归 + 95%CI 带（不外推）
            (b) 大样本散点的二维密度处理（n=6000，防过绘）
            (c) 气泡图：面积 ∝ 第三变量，附参照气泡定标

用法：python make_relationship_figures.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

SKILL_ROOT = Path(__file__).resolve().parents[3]
STYLE = SKILL_ROOT / "references" / "assets" / "matplotlib"
OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(11)

# 取色唯一来源：references/assets/palettes/academic.json（references/common.md「取色与配色」§1：禁止硬编码色值）
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "academic.json").read_text(encoding="utf-8"))
CAT = PALETTE["categorical"]
INK = PALETTE["text"]["label"]      # 描边/参照圆用文字墨色，不再引入色板外颜色

# ---- 主题：T1 出版级 + gs 管线安全字体（可变字体 Noto Sans SC 经 gs 丢字形）----
plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(STYLE / "academic.mplstyle")
sans = list(plt.rcParams["font.sans-serif"])
if "Microsoft YaHei" in sans:
    sans.remove("Microsoft YaHei")
sans.insert(0, "Microsoft YaHei")
plt.rcParams["font.sans-serif"] = sans

# Crameri Batlow 顺序色图（密度着色用）
CMAP = LinearSegmentedColormap.from_list(
    "batlow", cmc.batlow(np.linspace(0, 1, 256)))

fig, axes = plt.subplots(1, 3, figsize=(7.48, 2.65),
                         gridspec_kw={"wspace": 0.34})

# ================= (a) 分组散点 + 回归带 =================
ax = axes[0]
for name, slope, color, inter in [("线下渠道", 0.32, CAT[1], 8),      # 强调色 = 次要系列
                                  ("线上渠道", 0.58, CAT[0], 12)]:    # 主色 = 重点系列
    n = 55
    ad = rng.uniform(10, 95, n)
    sales = inter + slope * ad + rng.normal(0, 6.5, n)
    ax.scatter(ad, sales, s=13, color=color, alpha=0.55, linewidths=0)
    lr = stats.linregress(ad, sales)
    xs = np.linspace(ad.min(), ad.max(), 60)          # 不外推出数据范围
    yhat = lr.intercept + lr.slope * xs
    se = lr.stderr
    conf = stats.t.ppf(0.975, n - 2) * se * np.sqrt(
        1 / n + (xs - ad.mean()) ** 2 / np.sum((ad - ad.mean()) ** 2))
    ax.plot(xs, yhat, color=color, lw=1.2)
    ax.fill_between(xs, yhat - conf, yhat + conf, color=color, alpha=0.18, lw=0)
    ax.annotate(f"{name}\n(r = {lr.rvalue:.2f})", (xs[-1], yhat[-1]),
                xytext=(2, -6), textcoords="offset points",
                fontsize=7, color=color, va="top")    # T1 字号下限 7pt
ax.set_xlabel("广告投入（万元）")
ax.set_ylabel("月销售额（万元）")
ax.set_xlim(5, 100)

# ================= (b) 大样本：二维密度防过绘 =================
ax = axes[1]
n = 6000
mx = rng.normal(52, 15, n)
my = 12 + 0.45 * mx + rng.normal(0, 11, n)
hb = ax.hexbin(mx, my, gridsize=26, cmap=CMAP, mincnt=1,
               linewidths=0.2, edgecolors=INK)
ax.set_xlabel("用户活跃度（次/周）")
ax.set_ylabel("留存天数")
cb = fig.colorbar(hb, ax=ax, shrink=0.9, pad=0.02)
cb.set_label("样本数", fontsize=7)
cb.ax.tick_params(labelsize=7)

# ================= (c) 气泡图：面积编码第三变量 =================
ax = axes[2]
techs = rng.uniform(2, 8.5, 14)
growth = 4 + 2.2 * techs + rng.normal(0, 5, 14)
revenue = rng.uniform(20, 320, 14)
ax.scatter(techs, growth, s=revenue * 1.35, color=CAT[2],
           alpha=0.5, linewidths=0.6, edgecolors=INK)
ax.set_xlabel("研发强度（%）")
ax.set_ylabel("营收增速（%）")
ax.set_xlim(1, 9.5)
ax.set_ylim(-12, 34)
# 参照气泡定标（面积 ∝ 营收，半径 ∝ 平方根）
for v, xref, yref in [(50, 2.0, -6.5), (200, 3.6, -6.5)]:
    ax.scatter([xref], [yref], s=v * 1.35, facecolors="none",
               edgecolors=INK, linewidths=0.6)
    ax.text(xref, yref, str(v), ha="center", va="center", fontsize=7)
ax.text(2.8, -9.6, "营收（百万元）", ha="center", fontsize=7)

# ---- 面板标签：小写粗体，左上角外侧 ----
for ax, lab in zip(axes, "abc"):
    ax.text(-0.22, 1.05, lab, transform=ax.transAxes,
            fontsize=11, fontweight="bold", va="bottom")

fig.savefig(OUT / "fig1.pdf")
fig.savefig(OUT / "fig1_preview.png", dpi=200)
plt.close(fig)
print("fig1.pdf + preview done")
