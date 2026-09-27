# spec

## 红线与诚实原则


> 本文件是**红线**的唯一定义处。任何档位都不得违反。
> 总优先级：**准确 > 易读 > 简洁 > 美观**——任何与更高优先级冲突的美化都要舍弃。

### 1. 九条红线

1. **柱状图 y 轴必须从 0 开始**——柱高编码数量，截断等于撒谎。确需截断就改用点图。折线图可以截断（编码的是位置趋势），但**任何非零起点的轴都必须显式标注**（轴中断标记或图注说明）。
2. **不滥用双轴**：双轴只允许"单位相同的两个量"且两轴刻度对齐，系列颜色与所属轴同色；不同单位的关联改用双图 + 分色，并在标题中说明"相关 ≠ 因果"。
3. **不确定度不能省略**：有误差/波动/样本量的数据必须有误差棒、置信带或箱线，并说明 n 与统计口径。
4. **样本归一**：比较不同规模的总体用比例/人均，不用绝对数制造"碾压"错觉。
5. **完整个体**：箱线/直方图隐藏了个体时，建议叠加散点（T1 论文越来越常见的审稿要求）。
6. **面积/圆角不编码**：饼图只用角度比较（块数 ≤5，否则改堆叠条形）；禁止 3D 饼图（透视扭曲角度）；**气泡面积 ∝ 数值（半径 ∝ 平方根），不按半径线性**。
7. **图例完整**：每条线/每块色都要有可对应的图例或直接标注；**direct labeling 优先于图例**。
8. **图片不变形**：改尺寸等比例缩放，拉伸是最常见的事故。
9. **拟合要说清**：回归线只在数据范围内画（不外推），并声明置信带是**均值 CI** 还是**预测区间**。

### 2. 图注自含

图注必须不看正文也能看懂，至少包含：样本量 n、统计口径、误差类型（SD/SEM/95%CI）、显著性标注的定义（`* p<0.05, ** p<0.01, *** p<0.001`）、数据来源与时间范围。

### 3. 诚实原则（不画不该画的图）

- **一句话测试**：写不出"这张图要让读者 5 秒内得到 ______"，说明内容不适合画图。
- 信息量 ≤3 个数字：直接写进标题或正文，不画图。
- 内容里**没有数据**就不要数据图，**没有结构**就不要流程图；只有结论没有数字时，先要原始数据。
- 图只是装饰、数据不支撑任何结论：不画。
- 两种图型难分伯仲时，选**信息损耗更小**的一种。
- **不得编造统计量**：图注里出现的 n、置信区间、p 值、检验方法，必须由脚本真实计算得出。示例 `examples/data/paper/make_paper_figures.py` 已按此重写（真抽样、真 t 检验）。

### 4. 统计呈现最低要求

| 场景 | 必须给出 |
|---|---|
| 组间比较 | 误差棒或 CI + 每组 n + 检验方法 + 显著性 |
| 时间序列 | 波动来源（SD / SEM / 95%CI）说明 + 样本量 |
| 相关 / 回归 | r 或 R² + 置信带 + 是否外推 |
| 多组多重比较 | 校正方法（Bonferroni / FDR 等），或显式注明"未校正" |

---

## 取色与配色


> 本文件是**取色的唯一定义处**。图型文件、工具文件、示例代码只引用本文件，不得复述色值。
> 机器可读资产：`references/assets/palettes/{academic,business,showcase}.json`。

### 1. 唯一来源

三套色板 JSON 是**唯一取色来源**：禁止临时凑色，禁止凭印象写 hex，禁止"看起来差不多"的近似色。代码里出现的每一个颜色都必须来自：

- `categorical[]` —— 类别色，**按顺序取**，不自选、不跳取
- `sequential[]` / `diverging[]` —— 连续映射（热图、色带、相关矩阵）
- 下表 token —— 按角色取

```python
import json
from pathlib import Path

PALETTE = json.loads(
    (SKILL_ROOT / "references/assets/palettes/academic.json").read_text(encoding="utf-8"))
COLOR = PALETTE["categorical"]      # 类别色按序取用
MISSING = PALETTE["missing"]        # 无数据区域（地图等）
```

### 2. 色板选择

| 色板 | 档位 | 来源 | 特征 |
|---|---|---|---|
| academic | T1 | Okabe-Ito（色盲安全金标准，去黄、黑换灰） | 低饱和、印刷友好 |
| business | T2 | Tableau 10 | 蓝色锚定，专业克制 |
| showcase | T3 | Paul Tol Vibrant | 高饱和高对比，远距离清晰 |

同一交付物内所有图**必须同一色板**。档位与介质的对应见 `../SKILL.md` §第 2 步。

三套主题的实际观感对照见风格验证样张：`examples/style-demo/demo_styles.py`（生成 `examples/style-demo/output/{academic,business,showcase}.png`）。

### 3. token（按角色取色）

| token | 用途 | academic | business | showcase |
|---|---|---|---|---|
| `primary` / `accent` | 主色 / 强调色 | `#0072B2` / `#D55E00` | `#4E79A7` / `#F28E2B` | `#0077BB` / `#EE7733` |
| `neutral` | 中性参照、次要系列 | `#B3B3B3` | `#BAB0AC` | `#BBBBBB` |
| `text.{title,label,tick}` | 图标题 / 轴标题 / 刻度文字 | `#1A1A1A` / `#333333` / `#4D4D4D` | 同左 | 同左 |
| `grid` / `axis` | 网格线 / 轴线与边框 | `#CCCCCC` / `#333333` | `#D9D9D9` / `#D0D0D0` | `#D9D9D9` / `#C0C0C0` |
| `subtext` | 副标题、脚注、次要文字 | `#666666` | `#666666` | `#666666` |
| `missing` | 无数据区域填充 | `#E8E8E8` | `#E8E8E8` | `#E8E8E8` |
| `semantic` | success / warning / danger / info（**仅 T2/T3**） | 不提供 | `#2E7D32` / `#ED6C02` / `#C62828` / `#0288D1` | 同 business |
| `background` | 画布底色 | `#FFFFFF` | `#FFFFFF` | `#FFFFFF` |

TikZ 侧同名颜色为 `pcNeutral`。**注意 `pcGray` 是 academic 的第 7 个类别色（`#999999`），不是中性灰**。
`business`/`showcase` 的 `neutral` 与各自 `categorical` 末位同值（色板原生灰）；同图同时用到最后一个类别色与中性参照时，参照改用 `text.tick`。

### 4. 使用规则

1. **类别色按顺序取**，上限 = 色板容量（academic 7 / business 10 / showcase 7）。超了就做**小倍数图**或合并类别，**绝不加色**。前 4 色覆盖绝大多数场景。
2. **顺序色编码大小**：浅 = 小。方向约定：academic/business 的 `sequential` 是浅→深；**showcase 是 viridis 反向**（索引 0 最亮 = 最大值）。同一交付物内方向必须统一——换色板时先确认方向，别把"高值"在一张图里画成深色、在另一张里画成亮色。
3. **发散色编码偏离**：中心必须是"无意义点"（0 或均值），两侧对称；`vmin`/`vmax` 取等绝对值（如 `-1`/`1`），否则零点会漂。
4. **中性灰**用于背景参照、上年同期、次要系列，让主数据突出。
5. **色盲安全冗余**：不用红/绿单独编码关键信息；T1 必须叠加线型/标记/直接标注，保证**灰度打印仍可分辨**。
6. **语义色仅 T2/T3**：T1 印刷可能失真，改用色板色 + 文字标注。
7. **禁用彩虹 jet**。**无数据区域**用 `missing`，且必须与 `sequential` 最浅端可区分（地图类尤其重要，否则读者读成"最小值"）。

### 5. 多图一致性（同一交付物）

同一篇论文/报告里的所有图不仅共用色板，**语义 → 颜色的映射也必须只分配一次并全局复用**：

1. 先列出整份交付物会出现的"语义系列"清单（如：处理组、对照组、基线、预测值、缺失）。
2. 一次性分配颜色，写进交付物级配置，所有脚本 import 同一份。
3. 同一语义在任何一张图里都必须是同一颜色；**不要每张图各自从 `categorical[0]` 开始取**。

反例：图 1 用 `primary` 表示"处理组"，图 3 用 `primary` 表示"对照组"——读者必然误读。
这条比任何单图细节都更影响观感，且是演示/报告评审最常挑的问题。

---

## 字体与文字


> 本文件是**字体的唯一定义处**。图型文件、工具文件只引用本文件，不得复述字体方案。
> 机器可读资产：`references/assets/matplotlib/*.mplstyle`（`font.family`/`font.sans-serif`/字号）、`references/assets/echarts/*.json`（`fontFamily`/`fontSize`）、`references/assets/tikz/preamble.tex`。

### 1. 中西文分字体

中文与西文/数字用不同字体族：不要让中文字体顺便渲染西文（其西文字形间距偏宽、数字非等宽）。

| 场景 | 中文 | 西文 / 数字 |
|---|---|---|
| 数据图（matplotlib / ECharts） | 思源黑体 Source Han Sans SC / Noto Sans SC | Arial |
| TikZ 论文版（流程图、示意图） | 宋体 SimSun | Times New Roman |
| TikZ 演示版 | 黑体 Microsoft YaHei | Arial |

**TikZ 的模式宏不含字体**：`\pcPaperMode` / `\pcPPTMode` 只切配色、线宽、字号。字体必须由你自己的文档用 `\setmainfont` / `\setCJKmainfont` 声明——只切宏而不声明字体，中文会变成豆腐块。示例见 `examples/diagram/flowchart/paper_flow.tex` 与 `ppt_flow.tex`（两者仅"1 行模式 + 2 行字体"之差）。

**跨平台字体层（TikZ）**：两种搭配各封装为可 `\input` 的片段，按字体是否存在自动回退，**文档里不要写死字体名**：
- [`fonts-serif.tex`](../style/tikz/fonts-serif.tex)：宋体 + Times New Roman（与论文正文一致的图）
- [`fonts-sans.tex`](../style/tikz/fonts-sans.tex)：黑体 + Arial（演示版，以及黑体系的示意图）

  回退顺序：Windows 原生字体 → Noto CJK → **Fandol**（TeX Live 自带）。
  Linux 上还需让 fontspec（经 fontconfig）能找到西文回退字体，前置包为：
  `apt install fonts-noto-cjk fonts-noto-cjk-extra fonts-texgyre`（缺 `fonts-texgyre` 会报 `The font "TeX Gyre Termes" cannot be found`——TeX Live 自带的那份对 fontconfig 不可见）。
  两级回退都找不到时只发 `\PackageWarning` 而**不报错**，因此缺字体不会中断编译。

**回退链**（已内置在 `.mplstyle`）：`Source Han Sans SC → Noto Sans SC → Microsoft YaHei → Arial → Helvetica → DejaVu Sans`。
数学符号用 STIX（`mathtext.fontset: stix`）。

### 2. 字号层级

同一张图内层级 ≤4 级：标题 / 轴标题 / 刻度与图例 / 数据标注。

| 元素 | T1 | T2 | T3 |
|---|---|---|---|
| 图标题 | 11 bold | 13 bold | 15 bold |
| 轴标题 | 10 | 11 | 12 |
| 刻度 / 图例 | 9 | 10 | 11 |
| 数据标注 | 8–9 | 10 | 11 |
| **绝对下限** | **7**（印刷可读） | 9 | 11（最后一排可读） |

ECharts（px，已内置主题）：T1 14/12/11、T2 16/13/12、T3 20/15/14（标题/图例/刻度）。
TikZ：轴标题 `\small`、刻度与图例 `\footnotesize`。

**下限约束的是"最终成品上的等效字号"，不是代码里的数字。** 如果图会被缩放排版（例：122mm 宽的原图放进 90mm 单栏，缩放比 0.74），等效字号 = 设定值 × 缩放比，必须按缩放后的值判断是否仍 ≥7pt。这与 本文件 §画布、尺寸、导出与落盘 §2.5 的 tight bbox 问题是同一个陷阱的两面。

### 3. 两个必须知道的坑

1. **Windows 的 Noto Sans SC 是可变字体（VF）**，两条管线都会翻车：
   - **XeLaTeX / xdvipdfmx 无法嵌入** → 报 `fatal: Invalid font`。TikZ 出 PDF 改用 Microsoft YaHei 或静态版思源黑体（`preamble.tex` 已按此设 `\chartcjk{Microsoft YaHei}`）。
   - **matplotlib 导出的 PDF 子集经 Ghostscript 渲染会丢字形**（PDF 本身在 Adobe/浏览器正常，但出版系统的 gs 管线会掉字）→ 把静态字体 Microsoft YaHei 提到回退链首位。
   - 对策（示例 `examples/data/paper/make_paper_figures.py`）：

     ```python
     sans = list(plt.rcParams["font.sans-serif"])
     if "Microsoft YaHei" in sans:      # 回退链可能被外部覆盖，先判存在
         sans.remove("Microsoft YaHei")
     sans.insert(0, "Microsoft YaHei")
     plt.rcParams["font.sans-serif"] = sans
     ```
2. **Linux 服务器缺中文字体** → 中文变豆腐块。先装 `fonts-noto-cjk`；SVG 交付若文字未转路径，接收方也需有同名字体。

### 4. 强调

图内强调用**加粗**（同字体 Bold/Medium 字重）或强调色；不用下划线，不堆颜色。只强调关键结论、关键数据、警告。
负号：主题已设 `axes.unicode_minus: False`，即使用 ASCII 连字符代替 U+2212，避免缺字形的中文字体画不出来。

### 5. 换字体方案

项目要求衬线（部分中文期刊）时，在**项目内**覆盖 `font.family: serif` + SimSun / Times New Roman，**不要修改本仓库的主题文件**——改了会影响所有使用者。

---

## 画布、尺寸、导出与落盘


> 本文件是**尺寸 / DPI / 导出参数 / 文件落盘**的唯一定义处。
> 机器可读资产：`references/assets/matplotlib/*.mplstyle`（`figure.figsize`/`savefig.*`/`pdf.fonttype`）。

### 1. 尺寸速查

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

### 2. 导出

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

   留白用 `subplots_adjust` 控制。否则排版时一旦缩放，等效字号跟着变，可能跌破 本文件 §字体与文字 的下限。

### 3. 落盘（输出目录与命名）

1. **图必须落在项目内的专用目录**（如 `<项目>/figures/`），不要散落在根目录，也不要写进系统临时目录。仓库示例落在各自示例目录，因为示例本身就是交付物。
2. 命名 `图名_主题_日期.png`（如 `sales_trend_business_20260926.png`）；不用"新建图像.png"这类默认名。
3. 生成脚本与成图放同一目录；脚本内输出路径必须用 `Path(__file__)` 推导，**不依赖当前工作目录**（仓库示例统一用 `SKILL_ROOT = Path(__file__).resolve().parents[3]`）。
4. **中间产物不入库**：LaTeX 的 `.aux/.log/.out/.toc/.fls/.synctex.gz`、`temp/`、`*.tmp` 已被仓库 `.gitignore` 覆盖；一次性调试脚本用完即删，不留仓库。

### 4. 多面板与留白

- 用 `fig.subplots_adjust` 或 `constrained_layout=True` 防标签被裁切；多面板共享轴必须 `sharex`/`sharey=True`，比较类子图的轴范围必须一致。
- 面板标签用小写粗体（a/b/c），放在坐标区左上角外侧（`transform=ax.transAxes`，约 `(-0.18, 1.06)`）。
- 共享色标时把 colorbar 放在子图外侧一次，不要每个面板各放一个。

---

## T1 期刊规格与退稿清单


> T1 数据图的出版级深化规范，补充 ``spec.md`` 与 `tools/python.md`。来源：SciencePlots（garrettj403，★9.3k）、Rougier《Scientific Visualisation: Python + Matplotlib》（★11.6k）、Scientific Colour Maps（Crameri）与各期刊投稿要求。
> **横切规范只在本技能 `spec/` 定义一次**（红线 [`../spec.md`](../spec.md)、取色 [`../spec.md`](../spec.md)、字体 [`../spec.md`](../spec.md)、尺寸与落盘 [`../spec.md`](../spec.md)）；本文件**只讲本工具栈的用法与坑**，不复述上述内容。

### 1. 期刊规格速查

| 期刊/出版社 | 单栏 | 双栏 | 位图 DPI | 图内字号 |
|---|---|---|---|---|
| Nature 系列 | 89mm | 183mm | 300（线图矢量） | 缩放后 5–7pt |
| IEEE | 88.9mm（3.5in） | 181.6mm（7.16in） | ≥600 | 缩放后 ≥8pt |
| Elsevier | 90mm | 190mm | 300（矢量优先） | ≥7pt |
| ACS | ≈82.6mm | ≈177.8mm | 300–600 | ≥4.5pt（建议 ≥7） |

**以当期 Guide for Authors 为准**——上表是快速起点，投稿前必须核对最新版。通用硬规则：**缩放打印后**字号 ≥6pt、线宽 ≥0.5pt；先按栏宽设 figsize，再定字号，顺序不能反。

### 2. SciencePlots 配合使用（期刊仿真）

```python
import matplotlib.pyplot as plt
import scienceplots                      # pip install SciencePlots
plt.style.use(["science", "ieee"])       # 期刊变体：ieee / nature / apa
```

- `science` 是主样式（细框、无顶右刺、窄栏宽）；`ieee`（3.5in 栏宽、衬线）、`nature`（无网格）等变体叠加在后覆盖前者；
- **中文必须加 `no-latex`**：`plt.style.use(["science", "no-latex", "../../../references/assets/matplotlib/academic.mplstyle"  # 相对脚本所在目录，见 spec/本文件 §画布、尺寸、导出与落盘 §3.3；该路径相对脚本目录，非本文件 check-refs: skip])`——`science` 默认 `text.usetex=True` 会因缺 LaTeX/中文配置直接报错；
- 与本仓库主题叠加时，**本仓库主题写在最后**（保持取色与字体纪律，SciencePlots 只负责期刊尺寸与默认细节）；
- 环境：`pip install SciencePlots`；无 LaTeX 环境永远带 `no-latex`。

### 3. 色图标准（Scientific Colour Maps）

感知均匀色图已是出版界事实标准（Crameri, Shephard & Heron, 2020, *Nature Communications*——使用需引用该文）：

- **禁用** jet / rainbow / hsv：感知不均匀、色盲不友好、黑白打印产生虚假条纹；
- **顺序数据**：viridis / cividis / magma（matplotlib 内置），或 Crameri `batlow`；Crameri 色图安装：`pip install cmcrameri` → `import cmcrameri.cm as cmc; cmap="cmc.batlow"`；
- **发散数据**：RdBu_r / coolwarm，或 Crameri `vik` / `roma`（中心必须对齐语义零点）；
- **循环数据**（角度、周期）：twilight_shifted 或 Crameri `romero`——顺序色图画循环数据会在 0/360 处产生虚假断崖；
- 色盲自检：交付前用色盲模拟（colorspacious 或系统工具）过一遍，或直接用 cividis/batlow 这类天然安全的。

### 4. 多面板组合规范

- 面板标签 **a / b / c**（Nature 系小写粗体，左上角外侧统一对齐）或 (a)(b)，全篇统一一种；
- 组合用 `fig.subplot_mosaic` 或 GridSpec；同列面板共享 x 轴时 `sharex=True` 并删中间重复刻度；
- 面板间距不小于标签高度，标签不得压轴；
- caption 与面板一一对应，每面板可独立理解。

### 5. 细节退稿清单（审稿人常挑）

1. **字体未嵌入**：PDF 用 `pdffonts` 检查，非内嵌字体（TrueType 以外）会被出版系统打回——主题已设 fonttype 42，勿覆盖；
2. **该矢量的用了位图**：线图/柱状/散点一律 PDF/EPS 矢量；仅热图、>1 万点散点、图像用位图且 ≥600dpi（主题 savefig.dpi 已按档位设置）；
3. **标签重叠**：密数据标签用 `adjustText` 库（`pip install adjustText`）自动避让，不许手工挪了事；
4. **量级记法**：轴用 ×10ⁿ 标注（`ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 3))`），不出现 1e6 裸记数；SI 词头优先（μ、m、k）；
5. **图例压数据**：图例置顶框外或线端直标；误差棒类型（SD/SE/95%CI）在图注明示；
6. **usatex 与正文不一致**：中文期刊或中文图注慎用 `text.usetex`（中文配置繁琐且易与模板冲突），用 no-latex + 主题字体即可；
7. **一图一信息**：panel 数量克制（≤6），超了拆图；每张图在正文中必须被引用和讨论。

### 6. 与本仓库工作流的整合

走 `../SKILL.md` T1 路径：本文件排在 `tools/python.md` 之后、作图之前；主题仍用 academic.mplstyle（取色与字体纪律不变），SciencePlots 与 cmcrameri 是**期刊适配层**，不替代本仓库主题。

---

## 非数据图通用布局


> 非数据图的质量核心不是"防误导"（那是 本文件 §红线与诚实原则），而是**布局清晰、对齐、视觉动线**。
> 本文件适用于流程图、时序图、甘特图、架构图、层级图、示意图、信息图——所有非数据图共用。

### 1. 六条通用规范

1. **对齐即秩序**：同类节点对齐同一网格（水平/垂直居中）；连线只用正交线或平滑曲线，**两者不混用**。
2. **流向一致**：全图只有一条主轴（从左到右，或从上到下）；回流/反馈线用虚线并绕外侧，不横穿其他节点。
3. **节点文字极短**：框内 ≤10 字，细节放图注；动词 + 名词（"审核订单"），不写整句。
4. **分支显式标注**：判断分支必须标条件（是/否、达标/未达标），不留无标签箭头。
5. **克制着色**：默认单色系（主题蓝），颜色只用于区分**类别**或强调**关键路径**；流程/时序/架构/示意类**不超过 3 种颜色**，分类树（`diagrams.md`）按一级分支数取色，上限为色板容量（见 本文件 §取色与配色 §4.1）。跨图交付时符号约定保持一致（菱形 = 判断、圆柱 = 数据库、平行四边形 = 输入输出）。
6. **画完逐项过**：斜线、交叉线、无标签箭头、节点文字溢出、子图嵌套层级混乱。

### 2. 工具与尺寸

- 工具选择见 `../SKILL.md` §第 3 步；交付级非数据图一律 TikZ（**不使用 mermaid**）。
- 尺寸、字号下限、矢量导出、落盘命名统一遵守 本文件 §画布、尺寸、导出与落盘；着色统一遵守 本文件 §取色与配色。
- TikZ 出单图用 `\documentclass[border=6pt]{standalone}`；论文内嵌时把 `tikzpicture` 整体放进正文的 `figure` 环境，并删掉 `\documentclass`、`\begin{document}`、`\end{document}` **三行**（只删 `\documentclass` 会留下孤立的 `\begin{document}`），`\input{preamble.tex}` 移到正文导言区。
- `\input` 路径基准是**当前 .tex 文件所在目录**；仓库示例位于 `examples/<类>/<图型>/`，距技能根 3 层，故写作 `../../../references/assets/tikz/…`。

### 3. 图注与符号

- 非标准符号必须在图注说明（菱形、圆柱、T 形汇流点、虚线 = 异步/回流）。
- 术语在整份交付物内统一：不要同一份报告里"泳道 / 车道 / 阶段虚线框"混用。
