# distribution

## 分布类


> 核心问题："数值怎么分布的？集中在哪里、散多开、有没有离群值"。
> **横切规范只在本技能 `references/common.md` 定义一次**：红线九条见 [`../common.md`](../common.md)，取色见 [`../common.md`](../common.md)，字体字号见 [`../common.md`](../common.md)，尺寸导出与落盘见 [`../common.md`](../common.md)。本文件**只列本图型特有规范**，不复述上述任何内容。

### 图型清单

| 图型 | 适用 | 关键规范 |
|---|---|---|
| 直方图 | 单变量分布，n 较大 | bin 数 10–30；等距 bin；叠加 KDE 曲线 |
| 核密度图（KDE） | 平滑展示分布形态 | 必须与直方图/散点同呈现，防平滑掩盖多峰 |
| Q-Q 图（分位-分位） | 检验分布假设（正态、重尾） | 点贴参考线为符合；尾部偏离的模式本身就是诊断信息（上翘=重尾、S 形=偏态）；检验统计量写进图注 |
| 箱线图 | 多组分布比较、看离群值 | 标注 n；须叠加散点（抖动/蜂群）展示个体 |
| 小提琴图 | 多组分布形态比较 | 内嵌箱线（inner='box'）；样本极小（<20）时用蜂群代替 |
| 蜂群图（swarm） | 小样本展示每个点 | n ≤100 |
| ECDF 累积分布 | T1 论文推荐：无 bin 依赖、可读分位数 | 多组比较尤佳 |
| 山脊图（ridgeline） | 多组密度纵排（时间×分布） | 重叠留白足够，色渐变按序取 sequential |

### 画法骨架

#### 直方图 + KDE

```python
ax.hist(data, bins="auto", density=True, color=PAL["primary"], alpha=0.55,
        edgecolor=PAL["background"])                     # 白描边防块间粘连
xs = np.linspace(data.min(), data.max(), 200)
ax.plot(xs, gaussian_kde(data)(xs), color=PAL["accent"], lw=1.5, label="KDE")
ax.set_title("主峰与次峰的洞见写进标题", fontsize=10)      # 标题说分布形态
ax.legend(loc="upper left")
```
身份元素：直方 + KDE 叠加、density=True、标题说形态。按数据调整：bins 用 "auto" 或 Freedman–Diaconis 后人工复核多峰；偏态数据改报分位数。

#### 小提琴 + 箱线 + 个体散点

```python
ax.violinplot(data, positions=range(k), widths=0.82, showextrema=False)   # 外形
ax.boxplot(data, positions=range(k), widths=0.16, showfliers=False)       # 中位/四分位
for i, vals in enumerate(data):                          # 个体抖动散点：n 可见
    ax.scatter(rng.uniform(i - 0.09, i + 0.09, len(vals)), vals, s=7,
               color=PAL["primary"], alpha=0.55, linewidths=0, zorder=3)
ax.set_xticks(range(k), groups)
```
身份元素：小提琴外形 + 窄箱线 + 抖动散点三层叠加。按数据调整：n <20 改纯蜂群；每组必须共享同一 y 轴。

### 必守规范

1. **直方图 bin 宽决定一切**### 必守规范

1. **直方图 bin 宽决定一切**：bin 太粗掩盖双峰，太细噪声主导。默认 `bins='auto'` 或 Freedman–Diaconis；报告 bin 宽。
2. **个体可见**：任何箱线/小提琴都要能看到原始数据（叠加抖动散点，透明度 0.4–0.6），T1 尤其如此。
3. **多组比较 y 轴共享**：各组箱线/小提琴共享同一 y 轴，禁止各画各的。
4. **离群值处理透明**：标出离群值或说明剔除规则，不悄悄删。
5. 均值 vs 中位数：分布偏态时用中位数（箱线天然是中位数）；标均值要说明。

### 常见错误

- ❌ 用"均值 ± 2SD"近似区间画在偏态分布上（非对称分布该用分位数）
- ❌ 并排多个饼图比较构成（该用堆叠柱或箱线）
- ❌ KDE 带宽默认值直接用而不检查（多峰被抹平）
- ❌ 小提琴图样本量 <20（形状纯属误导）

### 示例

`examples/data/distribution/hist_kde.py`（直方图+KDE）、`examples/data/distribution/box_violin.py`（箱线+抖动散点）
