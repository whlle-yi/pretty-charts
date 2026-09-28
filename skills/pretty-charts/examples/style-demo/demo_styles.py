# -*- coding: utf-8 -*-
"""pretty-charts 风格验证样张：三个主题各渲染一张图，并**校验主题循环色 = 色板 JSON**。

为什么要把"校验"放进来：`references/common.md`「取色与配色」§1 规定色板 JSON 是唯一取色来源，主题文件只是它的投影。
主题与色板一旦漂移（历史上出现过 showcase 循环色写成 `#CC3344`、色板是 `#CC3311` 这类问题），
本脚本会立即失败——因此它既是样张，也是 CI 里的色板一致性测试。

用法：python demo_styles.py
输出：output/{academic,business,showcase}.png
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_hex

SKILL_ROOT = Path(__file__).resolve().parents[2]
STYLES = SKILL_ROOT / "references" / "assets" / "matplotlib"
PALETTES = SKILL_ROOT / "references" / "assets" / "palettes"
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


def load_palette(theme):
    """取色唯一来源：references/assets/palettes/<theme>.json（references/common.md「取色与配色」§1）。"""
    return json.loads((PALETTES / f"{theme}.json").read_text(encoding="utf-8"))


def assert_cycle_matches_palette(theme):
    """断言主题的循环色与色板 categorical 逐色一致（含顺序与数量）。"""
    palette = load_palette(theme)
    expected = [c.lower() for c in palette["categorical"]]
    actual = [to_hex(c).lower() for c in plt.rcParams["axes.prop_cycle"].by_key()["color"]]
    if actual != expected:
        raise SystemExit(
            "%s.mplstyle 的循环色与色板 JSON 不一致（references/common.md「取色与配色」§1 要求二者同源）\n"
            "  主题: %s\n  色板: %s" % (theme, actual, expected))
    return palette


def render(theme: str) -> None:
    plt.rcParams.update(plt.rcParamsDefault)
    plt.style.use(STYLES / f"{theme}.mplstyle")
    palette = assert_cycle_matches_palette(theme)

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
    print(f"done: {theme}（循环色 = {len(palette['categorical'])} 色，与色板一致）")


for theme in ("academic", "business", "showcase"):
    render(theme)
