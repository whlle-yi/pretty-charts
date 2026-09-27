# -*- coding: utf-8 -*-
"""论文数据图实战（paper-data.md 指导）：期刊规格 + SciencePlots 叠加 + Crameri 色图。

产出两个矢量 PDF（供 paper_embedded_data.tex 引用）：
  fig1.pdf  单栏 90mm 折线图：均值±95%CI + 线端直标，无图内标题（caption 在论文里）
  fig2.pdf  双栏 190mm 多面板：(a) 分组柱+误差棒+显著性括号 (b) 相关矩阵热图（Crameri diverging）

图中所有统计量（95% 置信区间、显著性）都由本脚本按样本实际计算，
与 paper_embedded_data.tex 的图注逐项对应，不得写成硬编码数值。

用法：python make_paper_figures.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots  # noqa: F401  (提供 "science"/"no-latex" 样式名)
import cmcrameri.cm as cmc
from scipy import stats

SKILL_ROOT = Path(__file__).resolve().parents[3]
STYLE = SKILL_ROOT / "references" / "style" / "matplotlib"
OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(7)

# 取色唯一来源：references/style/palettes/academic.json（style-guide §3：禁止硬编码色值）
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "style" / "palettes" / "academic.json").read_text(encoding="utf-8"))
CAT = PALETTE["categorical"]
INK = PALETTE["text"]["label"]

N_PER_POINT = 8          # 图 1：每个时间点每组样本量（图注声明 n=8）
N_PER_GROUP = 32         # 图 2a：每组样本量（图注声明 n=32/组）


def gs_safe_fonts():
    """Noto Sans SC 是可变字体，matplotlib PDF 子集经 Ghostscript 渲染会丢字形
    （PDF 本身正常，Adobe/浏览器可读；但出版系统的 gs 管线会翻车）。
    把静态字体 Microsoft YaHei 提到回退链首位即可。见 tool-matplotlib.md 已知坑 1。"""
    sans = list(plt.rcParams["font.sans-serif"])
    if "Microsoft YaHei" in sans:
        sans.remove("Microsoft YaHei")
    sans.insert(0, "Microsoft YaHei")
    plt.rcParams["font.sans-serif"] = sans


def reset_style():
    plt.rcParams.update(plt.rcParamsDefault)
    plt.style.use(["science", "no-latex", STYLE / "academic.mplstyle"])
    gs_safe_fonts()


# ---- 图 1：单栏 90mm = 3.54in（scenarios T1 场景特例）；SciencePlots 期刊仿真叠加本仓库主题 ----
reset_style()
fig, ax = plt.subplots(figsize=(3.54, 2.55))
x = np.arange(0, 8)
for name, y0, rate, color in [("对照组", 100, 0.90, PALETTE["neutral"]),
                              ("处理组", 100, 1.12, PALETTE["primary"])]:
    # 每个时间点独立抽样 N_PER_POINT 次，再算均值与 95%CI（t 分布）——图注的统计口径由此成立
    samples = np.array([rng.normal(y0 * rate ** t, 0.05 * y0 * rate ** t, N_PER_POINT)
                        for t in x])
    mean = samples.mean(axis=1)
    half = stats.t.ppf(0.975, N_PER_POINT - 1) * samples.std(axis=1, ddof=1) / np.sqrt(N_PER_POINT)
    ax.plot(x, mean, color=color, lw=1.2, marker="o", markersize=2.8, label=name)
    ax.fill_between(x, mean - half, mean + half, color=color, alpha=0.18, lw=0)
    ax.annotate(name, (x[-1], mean[-1]), xytext=(4, 0), textcoords="offset points",
                va="center", fontsize=8, color=color, fontweight="bold")
ax.set_xlabel("时间（天）")
ax.set_ylabel("相对表达量（%）")
ax.set_xlim(-0.2, 9.2)
ax.set_xticks(x)
ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 3), useMathText=True)
fig.savefig(OUT / "fig1.pdf")
plt.close(fig)

# ---- 图 2：双栏 190mm = 7.48in 多面板，a/b 标签 ----
reset_style()
fig, axes = plt.subplot_mosaic(
    [["a", "a", "b", "b"]], figsize=(7.48, 2.6), gridspec_kw={"wspace": 0.38})

# (a) 分组柱：均值 ± 95%CI + 显著性括号（检验真实执行，星号由 p 值决定）
groups = ["安慰剂", "低剂量", "中剂量", "高剂量"]
raw = [rng.normal(m, s, N_PER_GROUP) for m, s in [(50, 7), (54, 7), (62, 8), (74, 9)]]
means = np.array([v.mean() for v in raw])
ci = np.array([stats.t.ppf(0.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v)) for v in raw])
cols = [PALETTE["neutral"], CAT[5], PALETTE["primary"], PALETTE["accent"]]
axes["a"].bar(groups, means, yerr=ci, capsize=3, width=0.55, color=cols,
              error_kw=dict(lw=0.8, ecolor=INK))
top = float((means + ci).max())
axes["a"].set_ylim(0, top * 1.24)
axes["a"].set_ylabel("疗效评分")

# 安慰剂 vs 高剂量：双侧独立样本 t 检验，星号按 p 值取（不硬编码）
_, p_value = stats.ttest_ind(raw[0], raw[3])
stars = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "n.s."
y_lo, y_hi = top * 1.10, top * 1.145
axes["a"].plot([0, 0, 3, 3], [y_lo, y_hi, y_hi, y_lo], lw=0.8, color=INK)
axes["a"].text(1.5, y_hi * 1.01, stars, ha="center", fontsize=9)

# (b) 相关矩阵热图：Crameri diverging 色图（vik），中心对齐 0，格内标注
if not hasattr(cmc, "vik_r"):
    raise SystemExit("cmcrameri 未提供 vik_r：请升级（pip install -U cmcrameri），"
                     "否则图注声明的 Crameri vik 色图不成立。")
base = rng.normal(0, 1, (200, 4))
data = np.column_stack([base[:, 0], 0.8 * base[:, 0] + 0.6 * base[:, 1],
                        -0.7 * base[:, 0] + 0.7 * base[:, 2], base[:, 1]])
corr = np.corrcoef(data.T)
labels = ["V1", "V2", "V3", "V4"]
im = axes["b"].imshow(corr, cmap=cmc.vik_r, vmin=-1, vmax=1)
axes["b"].grid(False)
axes["b"].set_xticks(range(4), labels)
axes["b"].set_yticks(range(4), labels)
for i in range(4):
    for j in range(4):
        axes["b"].text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", fontsize=7,
                       color=PALETTE["background"] if abs(corr[i, j]) > 0.55
                       else PALETTE["text"]["title"])
cb = fig.colorbar(im, ax=axes["b"], shrink=0.85, pad=0.02)
cb.ax.tick_params(labelsize=7)

for key, lab in [("a", "a"), ("b", "b")]:  # 面板标签：小写粗体，左上角外侧
    axes[key].text(-0.18, 1.06, lab, transform=axes[key].transAxes,
                   fontsize=11, fontweight="bold", va="bottom")

fig.savefig(OUT / "fig2.pdf")
plt.close(fig)
print(f"fig1.pdf / fig2.pdf done（图 2a 显著性：p={p_value:.2e} → {stars}）")
