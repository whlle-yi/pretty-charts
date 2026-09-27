# 规范：画布、尺寸、导出与落盘（layout）

> 本文件是**尺寸 / DPI / 导出参数 / 文件落盘**的唯一定义处。
> 机器可读资产：`references/style/matplotlib/*.mplstyle`（`figure.figsize`/`savefig.*`/`pdf.fonttype`）。

## 1. 尺寸速查

| 交付场景 | 尺寸 | 备注 |
|---|---|---|
| 期刊单栏 | 90mm（3.54in）宽 | T1 默认 |
| 期刊双栏 | 190mm（7.48in）宽 | |
| IEEE | 88.9mm / 181.6mm | 比 Elsevier 略窄；以目标期刊模板实测为准 |
| Word 文档配图 | 版心宽度 ≈ 15–16cm | |
| PPT 16:9 | 33.87×19.05cm，图按半页 15×8.4cm | T3 |
| 网页 / ECharts | 容器自适应，最小 320px 移动端可读 | 矢量导出 |
| **画廊示例** | 4.2–7.5in | **仅供屏幕观感，不是投稿尺寸** |

mm → inch 一律除以 25.4，不要凭感觉。仓库示例中只有 `examples/data/paper/`、`examples/data/geo/` 用的是投稿尺寸（3.54/7.48in），其余是画廊尺寸——复制示例代码时务必换掉 `figsize`。

## 2. 导出

1. **矢量优先**：PDF（印刷/投稿）、SVG（网页）。位图仅在交付渠道强制时使用（PPT 内嵌 PNG、社交媒体）。
2. 位图：T1 ≥600dpi（线图 ≥1200 更佳），T2/T3 200dpi；白底。
3. matplotlib 文字保持可编辑：`pdf.fonttype: 42`（主题已设）；SVG 用 `svg.fonttype: none`——注意这是 **matplotlib 的 rcParam**，不是 SVG 工具本身的设置，网页内嵌场景应改 `paths` 或直接用 ECharts。
4. 顺序：先 `savefig`，再 `plt.close`。
5. **T1 精确栏宽的例外**：主题默认 `savefig.bbox: tight`，会把留白裁掉，使成品宽度**不再等于** `figsize`。投稿要求精确栏宽时，必须把 rcParam 关掉：

   ```python
   plt.rcParams["savefig.bbox"] = None      # 正确：恢复固定画布尺寸
   fig.savefig("fig1.pdf")
   ```

   ⚠️ **`savefig(..., bbox_inches=None)` 关不掉**——它的语义是“沿用 `rcParams["savefig.bbox"]`”，所以仍然 tight；`bbox_inches="standard"` 会直接抛 `AttributeError`。已实测：4×3in @100dpi 在 tight 下输出 290×215，置 rcParam 为 `None` 后才是 400×300。

   留白用 `subplots_adjust` 控制。否则排版时一旦缩放，等效字号跟着变，可能跌破 `type.md` §2 的下限。

## 3. 落盘（输出目录与命名）

1. **图必须落在项目内的专用目录**（如 `<项目>/figures/`），不要散落在根目录，也不要写进系统临时目录。仓库示例落在各自示例目录，因为示例本身就是交付物。
2. 命名 `图名_主题_日期.png`（如 `sales_trend_business_20260926.png`）；不用"新建图像.png"这类默认名。
3. 生成脚本与成图放同一目录；脚本内输出路径必须用 `Path(__file__)` 推导，**不依赖当前工作目录**（仓库示例统一用 `SKILL_ROOT = Path(__file__).resolve().parents[3]`）。
4. **中间产物不入库**：LaTeX 的 `.aux/.log/.out/.toc/.fls/.synctex.gz`、`temp/`、`*.tmp` 已被仓库 `.gitignore` 覆盖；一次性调试脚本用完即删，不留仓库。

## 4. 多面板与留白

- 用 `fig.subplots_adjust` 或 `constrained_layout=True` 防标签被裁切；多面板共享轴必须 `sharex`/`sharey=True`，比较类子图的轴范围必须一致。
- 面板标签用小写粗体（a/b/c），放在坐标区左上角外侧（`transform=ax.transAxes`，约 `(-0.18, 1.06)`）。
- 共享色标时把 colorbar 放在子图外侧一次，不要每个面板各放一个。
