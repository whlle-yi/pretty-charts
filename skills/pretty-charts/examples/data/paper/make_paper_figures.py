# -*- coding: utf-8 -*-
"""论文数据图实战（paper-data.md 指导）：期刊规格 + SciencePlots 叠加 + Crameri 色图。

产出两个矢量 PDF（供 paper_embedded_data.tex 引用）：
  fig1.pdf  单栏 90mm 折线图：均值±95%CI + 线端直标，无图内标题（caption 在论文里）
  fig2.pdf  双栏 190mm 多面板：(a) 分组柱+误差棒+显著性括号 (b) 相关矩阵热图（Crameri diverging）

用法：python make_paper_figures.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots
import cmcrameri.cm as cmc
from scipy import stats

SKILL_ROOT = Path(__file__).resolve().parents[3]
STYLE = SKILL_ROOT / "references" / "style" / "matplotlib"
OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(7)

def gs_safe_fonts():
    """Noto Sans SC 是可变字体，matplotlib PDF 子集经 Ghostscript 渲染会丢字形
    （PDF 本身正常，Adobe/浏览器可读；但出版系统的 gs 管线会翻车）。
    把静态字体 Microsoft YaHei 提到回退链首位即可。见 tool-matplotlib.md 已知坑。"""
    sans = list(plt.rcParams["font.sans-serif"])
    sans.remove("Microsoft YaHei"); sans.insert(0, "Microsoft YaHei")
    plt.rcParams["font.sans-serif"] = sans

# ---- 图 1：单栏 90mm = 3.54in（scenarios T1 场景特例）；SciencePlots 期刊仿真叠加本仓库主题 ----
plt.style.use(["science", "no-latex", STYLE / "academic.mplstyle"])
gs_safe_fonts()
fig, ax = plt.subplots(figsize=(3.54, 2.55))
x = np.arange(0, 8)
for name, y0, rate, color in [("对照组", 100, 0.9, "#B3B3B3"), ("处理组", 100, 1.12, "#0072B2")]:
    mean = y0 * rate ** x
    ci = 4 + 0.6 * x
    ax.plot(x, mean, color=color, lw=1.2, marker="o", markersize=2.8, label=name)
    ax.fill_between(x, mean - ci, mean + ci, color=color, alpha=0.18, lw=0)
    ax.annotate(name, (x[-1], mean[-1]), xytext=(4, 0), textcoords="offset points",
                va="center", fontsize=8, color=color, fontweight="bold")
ax.set_xlabel("时间（天）")
ax.set_ylabel("相对表达量（%）")
ax.set_xlim(-0.2, 9.2)
ax.set_xticks(x)
ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 3), useMathText=True)
fig.savefig(OUT / "fig1.pdf")
plt.close(fig)

# ---- 图 2：双栏 190mm = 7.48in 多面板，a/b/c 标签 ----
plt.style.use(["science", "no-latex", STYLE / "academic.mplstyle"])
gs_safe_fonts()
fig, axes = plt.subplot_mosaic(
    [["a", "a", "b", "b"]], figsize=(7.48, 2.6), gridspec_kw={"wspace": 0.38})

# (a) 分组柱：均值 ± 95%CI + 显著性括号
groups = ["安慰剂", "低剂量", "中剂量", "高剂量"]
raw = [rng.normal(m, s, 32) for m, s in [(50, 7), (54, 7), (62, 8), (74, 9)]]
means = np.array([v.mean() for v in raw])
ci = np.array([stats.t.ppf(0.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v)) for v in raw])
cols = ["#B3B3B3", "#56B4E9", "#0072B2", "#D55E00"]
axes["a"].bar(groups, means, yerr=ci, capsize=3, width=0.55, color=cols,
              error_kw=dict(lw=0.8, ecolor="#333333"))
axes["a"].set_ylim(0, (means + ci).max() * 1.24)
axes["a"].set_ylabel("疗效评分")
axes["a"].plot([0, 0, 3, 3], [86, 89, 89, 86], lw=0.8, color="#333333")
axes["a"].text(1.5, 90, "***", ha="center", fontsize=9)

# (b) 相关矩阵热图：Crameri diverging 色图（vik），中心对齐 0，格内标注
base = rng.normal(0, 1, (200, 4))
data = np.column_stack([base[:, 0], 0.8 * base[:, 0] + 0.6 * base[:, 1],
                        -0.7 * base[:, 0] + 0.7 * base[:, 2], base[:, 1]])
corr = np.corrcoef(data.T)
labels = ["V1", "V2", "V3", "V4"]
im = axes["b"].imshow(corr, cmap=cmc.vik_r if hasattr(cmc, "vik_r") else "RdBu_r",
                      vmin=-1, vmax=1)
axes["b"].grid(False)
axes["b"].set_xticks(range(4), labels)
axes["b"].set_yticks(range(4), labels)
for i in range(4):
    for j in range(4):
        axes["b"].text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center",
                       fontsize=7, color="white" if abs(corr[i, j]) > 0.55 else "#1A1A1A")
cb = fig.colorbar(im, ax=axes["b"], shrink=0.85, pad=0.02)
cb.ax.tick_params(labelsize=7)

for key, lab in [("a", "a"), ("b", "b")]:  # 面板标签：小写粗体，左上角外侧
    axes[key].text(-0.18, 1.06, lab, transform=axes[key].transAxes,
                   fontsize=11, fontweight="bold", va="bottom")

fig.savefig(OUT / "fig2.pdf")
plt.close(fig)
print("fig1.pdf / fig2.pdf done")
