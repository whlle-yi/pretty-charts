# inference

## 统计推断类


> 核心问题："这个结果可信吗？差异是真的还是噪声"。T1 出版级的核心章节；T2/T3 至少做到"不确定度可见"。
> **横切规范只在本技能 `references/common.md` 定义一次**：红线九条见 [`../common.md`](../common.md)，取色见 [`../common.md`](../common.md)，字体字号见 [`../common.md`](../common.md)，尺寸导出与落盘见 [`../common.md`](../common.md)。本文件**只列本图型特有规范**，不复述上述任何内容。

### 图型清单

| 图型 | 适用 | 关键规范 |
|---|---|---|
| 误差棒（error bar） | 均值/比例的点估计 | 注明类型：SD / SE / 95%CI 三选一并写进图注 |
| 置信带（confidence band） | 回归线、时间序列平滑 | 带宽 = 95%CI；半透明填充（alpha 0.15–0.25） |
| 显著性标注（bracket + 星号） | 组间比较 | 星号规范见下；括号不与数据重叠 |
| 配对连线图（paired lines） | 配对/前后测设计 | 每个受试一条线，n 可见 |
| 森林图（forest plot） | meta 分析、多模型系数 | 竖线 = 无效应参考（0 或 1）；菱形 = 合并效应 |
| 回归诊断图 | 拟合质量 | 残差图必带零参考线 |
| 生存曲线 | 生存分析 | 注明 n（risk table）；censoring 标记 |

### 画法骨架

#### 误差棒 + 95%CI + 显著性括号 + 个体散点

```python
ax.bar(groups, means, yerr=ci, capsize=4, width=0.5, color=...)   # 均值 + 95%CI
for i, v in enumerate(raw_groups):                       # 个体散点叠加：n 可见
    ax.scatter(rng.uniform(i - 0.16, i + 0.16, len(v)), v, s=7,
               color=PAL["text"]["tick"], alpha=0.55, zorder=3)
for x1, x2, text in significant_pairs:                   # 显著性括号：跨组画 Π 形
    y = 顶部预留高度
    ax.plot([x1, x1, x2, x2], [y, y + 1.5, y + 1.5, y], lw=0.9, color=PAL["text"]["label"])
    ax.text((x1 + x2) / 2, y + 1.8, text, ha="center", fontsize=9)
ax.set_ylim(0, max(顶部 + ci) * 1.22)                    # 柱状从 0 起 + 括号余量
```
身份元素：CI 误差棒 + 个体散点 + Π 形显著性括号；星号定义写进图注。按数据调整：组多时括号分级排；不显著标 ns。

### 必守规范

1. **不确定度不可省略**：点估计没有误差棒 = T1 审稿直接退回。SD/SE/95%CI 是三个不同概念，混用是最常见的学术图错误；95%CI 最常被要求。
2. **星号规范**：`* p<0.05，** p<0.01，*** p<0.001，ns = 不显著`；检验方法与 n 写进图注（"双侧 t 检验，n=32"）。
3. 显著性括号：从最高星排起，括号尽量不跨组；比较对象清晰（哪两组）。
4. 误差棒存在时避免叠加数据标签（双重表达拥挤）；小样本（n<30）叠加原始散点。
5. 箱线 + 显著性：星号标在箱线上方，y 轴顶部预留星号空间（防裁切）。
6. 效应量优先于 p 值：展示差异大小（组间差、Cohen's d）而不只是星号。

### 常见错误

- ❌ "均值 ± 误差棒" 不说明是什么误差
- ❌ 用 SE 让误差棒看起来小（变相美化）——用 95%CI 更诚实
- ❌ 星号满天飞但不做多重比较校正说明
- ❌ 截断轴 + 误差棒（视觉夸大差异）

### 示例

`examples/data/statistical/errorbar_ci.py`（分组均值 + 95%CI + 显著性标注）
