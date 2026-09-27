# 规范：取色与配色（color）

> 本文件是**取色的唯一定义处**。图型文件、工具文件、示例代码只引用本文件，不得复述色值。
> 机器可读资产：`references/style/palettes/{academic,business,showcase}.json`。

## 1. 唯一来源

三套色板 JSON 是**唯一取色来源**：禁止临时凑色，禁止凭印象写 hex，禁止"看起来差不多"的近似色。代码里出现的每一个颜色都必须来自：

- `categorical[]` —— 类别色，**按顺序取**，不自选、不跳取
- `sequential[]` / `diverging[]` —— 连续映射（热图、色带、相关矩阵）
- 下表 token —— 按角色取

```python
import json
from pathlib import Path

PALETTE = json.loads(
    (SKILL_ROOT / "references/style/palettes/academic.json").read_text(encoding="utf-8"))
COLOR = PALETTE["categorical"]      # 类别色按序取用
MISSING = PALETTE["missing"]        # 无数据区域（地图等）
```

## 2. 色板选择

| 色板 | 档位 | 来源 | 特征 |
|---|---|---|---|
| academic | T1 | Okabe-Ito（色盲安全金标准，去黄、黑换灰） | 低饱和、印刷友好 |
| business | T2 | Tableau 10 | 蓝色锚定，专业克制 |
| showcase | T3 | Paul Tol Vibrant | 高饱和高对比，远距离清晰 |

同一交付物内所有图**必须同一色板**。档位与介质的对应见 `routing.md` §1。

三套主题的实际观感对照见风格验证样张：`examples/style-demo/demo_styles.py`（生成 `examples/style-demo/output/{academic,business,showcase}.png`）。

## 3. token（按角色取色）

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

## 4. 使用规则

1. **类别色按顺序取**，上限 = 色板容量（academic 7 / business 10 / showcase 7）。超了就做**小倍数图**或合并类别，**绝不加色**。前 4 色覆盖绝大多数场景。
2. **顺序色编码大小**：浅 = 小。方向约定：academic/business 的 `sequential` 是浅→深；**showcase 是 viridis 反向**（索引 0 最亮 = 最大值）。同一交付物内方向必须统一——换色板时先确认方向，别把"高值"在一张图里画成深色、在另一张里画成亮色。
3. **发散色编码偏离**：中心必须是"无意义点"（0 或均值），两侧对称；`vmin`/`vmax` 取等绝对值（如 `-1`/`1`），否则零点会漂。
4. **中性灰**用于背景参照、上年同期、次要系列，让主数据突出。
5. **色盲安全冗余**：不用红/绿单独编码关键信息；T1 必须叠加线型/标记/直接标注，保证**灰度打印仍可分辨**。
6. **语义色仅 T2/T3**：T1 印刷可能失真，改用色板色 + 文字标注。
7. **禁用彩虹 jet**。**无数据区域**用 `missing`，且必须与 `sequential` 最浅端可区分（地图类尤其重要，否则读者读成"最小值"）。

## 5. 多图一致性（同一交付物）

同一篇论文/报告里的所有图不仅共用色板，**语义 → 颜色的映射也必须只分配一次并全局复用**：

1. 先列出整份交付物会出现的"语义系列"清单（如：处理组、对照组、基线、预测值、缺失）。
2. 一次性分配颜色，写进交付物级配置，所有脚本 import 同一份。
3. 同一语义在任何一张图里都必须是同一颜色；**不要每张图各自从 `categorical[0]` 开始取**。

反例：图 1 用 `primary` 表示"处理组"，图 3 用 `primary` 表示"对照组"——读者必然误读。
这条比任何单图细节都更影响观感，且是演示/报告评审最常挑的问题。
