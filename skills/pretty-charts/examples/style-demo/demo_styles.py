# -*- coding: utf-8 -*-
"""pretty-charts 风格验证样张：三个主题各渲染一张图，验证字体/配色/主题生效。

用法：python demo_styles.py
输出：output/{academic,business,showcase}.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SKILL_ROOT = Path(__file__).resolve().parents[2]
STYLES = SKILL_ROOT / "assets" / "matplotlib"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)

rng = np.random.default_rng(42)
x = np.arange(2021, 2026)
series = {
    "华东": np.array([120, 145, 138, 172, 205]),
    "华南": np.array([90, 102, 118, 126, 158]),
    "华北": np.array([75, 80, 88, 96, 110]),
}
groups = ["一季度", "二季度", "三季度", "四季度"]
bars = rng.uniform(30, 90, (3, 4))


def render(theme: str) -> None:
    plt.style.use(STYLES / f"{theme}.mplstyle")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.2), gridspec_kw={"wspace": 0.28})

    for name, y in series.items():
        ax1.plot(x, y, marker="o", label=name)
        ax1.annotate(f"{y[-1]}", (x[-1], y[-1]), xytext=(6, 0),
                     textcoords="offset points", va="center")
    ax1.set_title("近五年区域销量趋势（万台）")
    ax1.set_ylabel("销量")
    ax1.set_xticks(x)
    ax1.set_xlim(2020.6, 2026.2)
    ax1.legend(loc="upper left")

    width = 0.26
    for i, name in enumerate(series):
        ax2.bar(np.arange(4) + (i - 1) * width, bars[i], width, label=name)
    ax2.set_title("各季度平均库存（万件）")
    ax2.set_xticks(np.arange(4), groups)
    ax2.set_ylabel("库存")
    ax2.set_ylim(0, bars.max() * 1.28)  # 顶部留白给图例，避免图例压柱
    ax2.legend(loc="upper center", ncols=3)

    fig.savefig(OUT / f"{theme}.png")
    plt.close(fig)
    print(f"done: {theme}")


for theme in ("academic", "business", "showcase"):
    render(theme)
