# -*- coding: UTF-8 -*-
'''
@Project ：Paper_RL 
@File    ：Fig-NS.py
@IDE     ：PyCharm 
@Author  ：Vinne
@Date    ：2026/3/25 9:11 
@Explain ：
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import copy
import matplotlib.colors as mcolors

# ================== 全局字体设置 ==================
config = {"font.family": 'Times New Roman'}
rcParams.update(config)
plt.rcParams['font.sans-serif'] = 'Times New Roman'

plt.rc('axes', titlesize=11)    # 子图标题字体
plt.rc('axes', labelsize=16)    # 坐标轴标签字体
plt.rc('xtick', labelsize=11)   # x 轴刻度字体
plt.rc('ytick', labelsize=10)   # y 轴刻度字体
plt.rc('legend', fontsize=12)   # 图例字体
annotate_font = FontProperties(size=16) # 子图标号 (a)(b)(c) 字体

# 设置颜色点位
color_points = [
    (0.0, "#194775"),   # 最小值
    (0.11, "#9AB7DA"),
    (0.5, "#F1F5F8"),
    (0.89, "#F6B4C7"),
    (1.0, "#8c1414")    # 最大值
]
# 构造线性渐变 colormap
custom_cmap = mcolors.LinearSegmentedColormap.from_list("my_cmap", color_points)

# ================== 读取数据 ==================
df = pd.read_excel("data/result/真实网络与计算结果.xlsx")
net_names = df["简称"].astype(str).tolist()

# 指标列名
metrics = {
    "NLSD": [
        "ER(NLSD)", "WS(NLSD)", "BA(NLSD)", "DG(NLSD)", "GGDP(NLSD)", "GW(NLSD)", "RL(NLSD)"
    ],
    "SINS": [
        "ER(SINS)", "WS(SINS)", "BA(SINS)", "DG(SINS)", "GGDP(SINS)", "GW(SINS)", "RL(SINS)"
    ],
    "GDD": [
        "ER(GDD)", "WS(GDD)", "BA(GDD)", "DG(GDD)", "GGDP(GDD)", "GW(GDD)", "RL(GDD)"
    ]
}

model_names = ["ER", "WS", "BA", "DG", "GGDP", "GW", "RL"]
# 定义映射
rename_map = {
    "RL": "Our"
}
model_names = model_names = [rename_map.get(name, name) for name in model_names]

# ================== 绘图 ==================
fig, axes = plt.subplots(1, 3, figsize=(11.5, 5))

titles = [
    "NLSD",
    "SINS",
    "GDD"
]

labels = ["(a)", "(b)", "(c)"]

epsilon = 1e-12  # 防止除零

for idx, (metric_name, cols) in enumerate(metrics.items()):
    ax = axes[idx]

    data = df[cols].copy()
    data.columns = model_names

    # 差异性指标 → 取倒数
    if metric_name in ["NLSD", "SINS"]:
        data = 1.0 / (data + epsilon)

    # ========== 归一化处理（Min-Max） ==========
    dmin = data.min().min()
    dmax = data.max().max()
    data = (data - dmin) / (dmax - dmin)

    matrix = data.values

    sns.heatmap(
        matrix,
        ax=ax,
        cmap=custom_cmap,
        linewidths=0.4,
        linecolor="white",
        cbar=False,  # 所有子图都不显示 colorbar
        xticklabels=model_names,
        yticklabels=net_names,
        mask=np.isnan(matrix)
    )

    # 横轴刻度置于上方
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    if idx == 0:
        ax.set_ylabel("Empirical Networks")
    else:
        ax.set_ylabel("")

    ax.text(
        0.5017, -0.028, titles[idx],  # y 位置可微调
        transform=ax.transAxes,
        ha='center', va='top',
        fontproperties=annotate_font
    )

    # 子图标号置于下方
    ax.text(
        0.4556, -0.116, labels[idx],
        transform=ax.transAxes,
        fontproperties=annotate_font
    )

    import matplotlib.patches as patches

    # 缺失值填充灰色
    custom_cmap.set_bad(color="white")
    mask = np.isnan(matrix)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if mask[i, j]:
                # 单斜线
                ax.plot([j, j + 1], [i, i + 1], color="#E8E8E8", linewidth=0.8)
                # 双斜线
                ax.plot([j, j + 1], [i + 1, i], color="#E8E8E8", linewidth=0.8)
                # 四边框线
                rect = patches.Rectangle((j, i), 1, 1, linewidth=0.8,
                                         edgecolor='#E8E8E8', facecolor='none')
                ax.add_patch(rect)

plt.subplots_adjust(
    top=0.935,
    bottom=0.114,
    left=0.086,
    right=0.942,
    hspace=0.2,
    wspace=0.287
)

# ========== 独立 colorbar（自动与热力图等高） ==========
norm = mpl.colors.Normalize(vmin=0, vmax=1)
sm = mpl.cm.ScalarMappable(cmap=custom_cmap, norm=norm)
sm.set_array([])

# 自动读取第三个子图的位置
pos = axes[2].get_position()
cbar_left = pos.x1 + 0.01      # 色条紧贴右侧
cbar_bottom = pos.y0           # 与热力图底部对齐
cbar_height = pos.height       # 与热力图高度一致

# 创建 colorbar
cbar_ax = fig.add_axes([cbar_left, cbar_bottom, 0.015, cbar_height])
cbar = fig.colorbar(sm, cbar_ax)

# 去掉黑边
cbar.outline.set_visible(False)


# 保存
plt.savefig("D:\科研论文文稿\Paper_RL\图\Figs\Fig_NS.pdf", format="pdf")
plt.savefig('D:\科研论文文稿\Paper_RL\图\Figs\Fig_NS.svg', format='svg')
plt.show()



