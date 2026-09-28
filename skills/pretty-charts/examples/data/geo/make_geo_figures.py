# -*- coding: utf-8 -*-
"""地理空间图实战（geo.md 指导）：choropleth 比率 + 比例符号绝对量 + 小倍数共享色标。

产出三个矢量 PDF（供 paper_embedded_geo.tex 引用）：
  fig1.pdf  世界 choropleth：研发人员密度（每百万人口，比率而非绝对数）
  fig2.pdf  比例符号地图：研发支出总额（气泡面积 ∝ 数值，绝对量）
  fig3.pdf  小倍数地图：2015 vs 2020 两期对比，共享色标

数据为演示用合成值；底图用随仓库分发的 Natural Earth 1:110m 低分辨率国界
（naturalearth_lowres.geojson，公有领域，离线可用），不依赖 geopandas 自带的
数据集接口——geopandas 1.0 已移除 geopandas.datasets。
用法：python make_geo_figures.py
"""
import json
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
import cmcrameri.cm as cmc

SKILL_ROOT = Path(__file__).resolve().parents[3]
STYLE = SKILL_ROOT / "references" / "assets" / "matplotlib"
OUT = Path(__file__).resolve().parent

# 取色唯一来源：references/assets/palettes/academic.json（references/common.md「取色与配色」§1：禁止硬编码色值）
PALETTE = json.loads(
    (SKILL_ROOT / "references" / "assets" / "palettes" / "academic.json").read_text(encoding="utf-8")
)

# ---- 演示用合成数据：ISO3 → (研发人员密度/百万, 支出总额 $B, 2015 密度, 2020 密度) ----
DATA = {  # iso3: (density, spend, d2015, d2020)
    "KOR": (8800, 190, 6500, 8800), "SWE": (7600, 150, 6800, 7600),
    "ISR": (10300, 160, 8500, 10300), "JPN": (5300, 170, 5100, 5300),
    "DEU": (4600, 160, 4200, 4600), "USA": (4800, 810, 4100, 4800),
    "CHN": (1700, 620, 700, 1700), "GBR": (3400, 120, 3000, 3400),
    "FRA": (3600, 110, 3300, 3600), "NLD": (3900, 60, 3400, 3900),
    "CHE": (5100, 90, 4600, 5100), "FIN": (6200, 30, 5900, 6200),
    "DNK": (5400, 40, 4900, 5400), "AUT": (3100, 40, 2900, 3100),
    "BEL": (2900, 30, 2700, 2900), "CAN": (2600, 70, 2400, 2600),
    "AUS": (2300, 60, 2100, 2300), "ITA": (1400, 60, 1300, 1400),
    "ESP": (1500, 50, 1200, 1500), "BRA": (700, 30, 600, 700),
    "IND": (260, 60, 150, 260), "IDN": (120, 20, 60, 120),
    "TUR": (1000, 20, 500, 1000), "ZAF": (500, 15, 400, 500),
    "MEX": (300, 15, 250, 300), "SGP": (6500, 40, 5300, 6500),
    "NOR": (5200, 30, 4800, 5200), "POL": (1800, 25, 1100, 1800),
    "RUS": (2100, 70, 1900, 2100), "IRL": (3200, 30, 2500, 3200),
}

# ---- 主题：T1 出版级 + gs 管线安全字体（可变字体 Noto Sans SC 经 gs 丢字形，见 tool-matplotlib 已知坑 1）----
plt.rcParams.update(plt.rcParamsDefault)
plt.style.use(STYLE / "academic.mplstyle")
sans = list(plt.rcParams["font.sans-serif"])
if "Microsoft YaHei" in sans:
    sans.remove("Microsoft YaHei")
sans.insert(0, "Microsoft YaHei")
plt.rcParams["font.sans-serif"] = sans

# ---- 底图与世界数据 ----
WORLD_FILE = OUT / "naturalearth_lowres.geojson"
if not WORLD_FILE.exists():
    raise SystemExit(
        f"缺少底图数据：{WORLD_FILE}\n"
        "该文件随仓库分发（Natural Earth 1:110m，公有领域）。"
        "如需重新获取，见 geo.md 的'底图来源'一节。"
    )
world = gpd.read_file(WORLD_FILE)   # iso_a3 已修正 FRA/NOR（原数据集为 -99）

world["density"] = world["iso_a3"].map({k: v[0] for k, v in DATA.items()})
world["spend"] = world["iso_a3"].map({k: v[1] for k, v in DATA.items()})
world["d2015"] = world["iso_a3"].map({k: v[2] for k, v in DATA.items()})
world["d2020"] = world["iso_a3"].map({k: v[3] for k, v in DATA.items()})

# Crameri 感知均匀顺序色图 Batlow（pip install cmcrameri），0–11 000 人/百万人
CMAP = LinearSegmentedColormap.from_list(
    "batlow", cmc.batlow(np.linspace(0, 1, 256)))
NORM = Normalize(vmin=0, vmax=11_000)
MISSING = PALETTE["missing"]      # 无数据地区：中性灰（≠ 色标最低色）
INK = PALETTE["text"]["label"]    # 气泡描边/参照圆：用文字墨色，避免引入色板外颜色
LIMITS = dict(xlim=(-168, 190), ylim=(-57, 83))


def draw_base(ax, column=None):
    """底图：无数据国家灰底 + 有数据国家按数值着色 + 白色国界。"""
    world.plot(ax=ax, color=MISSING, edgecolor=PALETTE["background"], linewidth=0.4)
    if column is not None:
        sub = world.dropna(subset=[column])
        sub.plot(ax=ax, column=column, cmap=CMAP, norm=NORM,
                 edgecolor=PALETTE["background"], linewidth=0.4)
    ax.set_xlim(LIMITS["xlim"]); ax.set_ylim(LIMITS["ylim"])
    # 非地图投影：等经纬（plate carrée）近似，按纬度拉伸 1.15 做粗略补偿；仅供示意
    ax.set_aspect(1.15)
    ax.set_axis_off()


# ---- 图 1：choropleth（比率指标，90mm 单栏）----
fig, ax = plt.subplots(figsize=(3.54, 2.75))
draw_base(ax, "density")
cb = fig.colorbar(ScalarMappable(norm=NORM, cmap=CMAP), ax=ax,
                  fraction=0.032, pad=0.01)
cb.set_label("人/百万人", fontsize=8)
cb.ax.tick_params(labelsize=7)
fig.subplots_adjust(right=0.85)
fig.savefig(OUT / "fig1.pdf")
fig.savefig(OUT / "fig1_preview.png", dpi=600)
plt.close(fig)

# ---- 图 2：比例符号地图（绝对量，90mm 单栏）----
fig, ax = plt.subplots(figsize=(3.54, 2.75))
draw_base(ax)
sub = world.dropna(subset=["spend"]).copy()
sub["pt"] = sub.geometry.representative_point()
sub["x"] = sub["pt"].x; sub["y"] = sub["pt"].y
ax.scatter(sub["x"], sub["y"], s=sub["spend"] * 1.9,             # 面积 ∝ 数值
           color=PALETTE["primary"], alpha=0.55, linewidths=0.6, edgecolors=INK)
# 参照气泡定标（南太平洋空白区，面积 ∝ 数值，半径 ∝ 平方根）
for v, xlon in [(200, -136), (50, -98)]:
    ax.scatter([xlon], [-34], s=v * 1.9, facecolors="none",
               edgecolors=INK, linewidths=0.6)
    ax.text(xlon, -34, str(v), ha="center", va="center", fontsize=7)
ax.text(-117, -58, "支出（10 亿美元）", ha="center", va="top", fontsize=7)
fig.savefig(OUT / "fig2.pdf")
fig.savefig(OUT / "fig2_preview.png", dpi=600)
plt.close(fig)

# ---- 图 3：小倍数地图（两期对比，190mm 双栏，共享色标）----
fig, axes = plt.subplots(1, 2, figsize=(7.48, 2.75))
for ax, col, year in zip(axes, ["d2015", "d2020"], ["2015", "2020"]):
    draw_base(ax, col)
    ax.set_title(year, fontsize=10, fontweight="bold", pad=2)
cb = fig.colorbar(ScalarMappable(norm=NORM, cmap=CMAP), ax=axes,
                  fraction=0.022, pad=0.01)
cb.set_label("人/百万人", fontsize=8)
cb.ax.tick_params(labelsize=7)
fig.subplots_adjust(wspace=0.05, right=0.86)
fig.savefig(OUT / "fig3.pdf")
fig.savefig(OUT / "fig3_preview.png", dpi=600)
plt.close(fig)
print("fig1/2/3 pdf + preview done")
