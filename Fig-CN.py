# -*- coding: UTF-8 -*-
"""
@Project ：Paper_模拟网络
@File    ：Fig-CN(可视化).py
@IDE     ：PyCharm
@Author  ：Vinne
@Date    ：2025/6/17 10:44
@Explain ：经典网络与RL网络的度分布（含误差棒）
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec

plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'   # ！数学符号也使用 Times New Roman

# ============================================================
# 统一样式配置（所有可调参数集中在这里）
# ============================================================

STYLE = {
    # 图尺寸
    "fig.size": (9, 6),

    # 字体
    "font.family": "Times New Roman",   # 全局字体
    "axes.labelsize": 12,               # 坐标轴标签字体大小
    "axes.titlesize": 12,               # 子图标题字体大小
    "xtick.labelsize": 11,              # x 轴刻度字体大小
    "ytick.labelsize": 11,              # y 轴刻度字体大小
    "legend.fontsize": 9.5,               # 图例字体大小

    # 散点样式
    "marker.size": 6,                   # 散点大小
    "marker.alpha": 0.9,                # 散点透明度
    "marker.edgewidth": 0.3,            # 散点边缘线宽

    # 误差棒样式
    "error.linewidth": 0.2,             # 误差棒线宽
    "error.capsize": 2,               # 误差棒帽子长度
    "error.capthick": 0.3,              # 误差棒帽子线宽

    # 子图标签样式
    "subplot.label.size": 14,           # (a)(b)(c) 字体大小
    "subplot.label.x_ab": 0.5007,
    "subplot.label.x_c": 0.5007,
    "subplot.label.y_ab": -0.253,
    "subplot.label.y_c": -0.2065,

    # 图例
    "legend_a_x": 0.24,
    "legend_a_y": 0.3,

    "legend_b_x": 0.75,
    "legend_b_y": 0.741,

    "legend_c_x": 0.97,
    "legend_c_y": 0.97,
}

STYLE_A = {
    "sample.step": 1,
}
STYLE_B = {
    "sample.step": 1,
}
STYLE_C = {
    "sample.step": 1,
}


# 应用字体设置
rcParams.update({"font.family": STYLE["font.family"]})
plt.rcParams['font.sans-serif'] = STYLE["font.family"]

# 子图标签字体
annotate_font = FontProperties(size=STYLE["subplot.label.size"])

# ============================================================
# 数据路径
# ============================================================

csv_dir = "data/ClassicalNetwork-200"

csv_files = {
    r'ER': "ER_degree_dist.csv",
    r'WS': "WS_degree_dist.csv",
    r'BA': "BA_degree_dist.csv",
    r'Our #1': "RL_#1_degree_dist.csv",
    r'Our #2': "RL_#2_degree_dist.csv",
    r'Our #3': "RL_#3_degree_dist.csv",
}

# ============================================================
# 绘图分组
# ============================================================

networks_a = [
    r'Our #1',
    r'ER',
]
networks_b = [
    r'Our #2',
    r'WS',
]
networks_c = [
    r'Our #3',
    r'BA',
]

# ============================================================
# 样式字典
# ============================================================

marker_dict = {
    r'Our #1': 's',
    r'Our #2': 's',
    r'Our #3': 's',
    r'ER': '^',
    r'WS': '^',
    r'BA': '^',
}

import matplotlib.colors as mcolors
def lighten_color(color, factor=0.5):
    """
    将颜色变浅，但保持不透明。
    factor < 1 变浅，factor > 1 变深
    """
    r, g, b = mcolors.to_rgb(color)
    h, s, v = mcolors.rgb_to_hsv([r, g, b])

    # 降低饱和度、提高亮度
    s *= factor
    v = 1 - (1 - v) * factor

    r2, g2, b2 = mcolors.hsv_to_rgb([h, s, v])
    return (r2, g2, b2, 1.0)  # 保持不透明
# lighten_color("#1168A3", factor=0.95)

color_map = {
    # #124B7D "#4B81BD"
    r'Our #1': "#124B7D",
    r'Our #2': "#124B7D",
    r'Our #3': "#124B7D",
    r'ER': "#ff6f61",#f05454
    r'WS': "#ffab40",#ff9900
    r'BA': "#16A085",#64B8A8
    # r'BA': "#F5C90F",
}

zorder_dict = {name: 2 for name in csv_files}

# ============================================================
# 绘图函数
# ============================================================

def plot_group(ax, group, label):
    # 判断
    is_panel_a = (label == "(a)")
    is_panel_b = (label == "(b)")
    is_panel_c = (label == "(c)")

    for name in group:
        df = pd.read_csv(os.path.join(csv_dir, csv_files[name]))

        # 转为数值类型（log 轴必须）
        degree = df["degree"].astype(int).values
        mean = df["mean"].astype(float).values
        std = df["std"].astype(float).values

        # log 轴过滤
        mask = (degree > 0) & (mean > 0)
        degree = degree[mask]
        mean = mean[mask]
        std = std[mask]

        # ----------- 散点抽样 -----------
        if is_panel_a:
            step = STYLE_A["sample.step"]
        if is_panel_b:
            step = STYLE_B["sample.step"]
        if is_panel_c:
            step = STYLE_C["sample.step"]
        degree = degree[::step]
        mean = mean[::step]
        std = std[::step]

        # 误差棒（含注释）
        ax.errorbar(
            degree, mean,
            yerr=std,                          # 误差：标准差
            fmt=marker_dict[name],             # 散点形状
            markersize=STYLE["marker.size"],   # 散点大小
            linestyle="None",                  # 不画连线
            color=color_map[name],             # 颜色
            alpha=STYLE["marker.alpha"],       # 散点透明度
            markeredgewidth=STYLE["marker.edgewidth"],

            # --- 误差棒透明度设置 ---
            ecolor=mcolors.to_rgba(color_map[name], alpha=0.01),
            elinewidth=STYLE["error.linewidth"],  # 误差棒线宽
            capsize=STYLE["error.capsize"],       # 误差棒帽子长度
            capthick=STYLE["error.capthick"],     # 误差棒帽子线宽

            zorder=zorder_dict[name],
            label=name
        )

    # 坐标轴设置
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(color="#E8E8E8", linestyle="-.", linewidth=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel("$d$", fontsize=STYLE["axes.labelsize"])

    if is_panel_c:
        ax.annotate(
            label,
            xy=(STYLE["subplot.label.x_c"], STYLE["subplot.label.y_c"]),  # 图下方中央
            xycoords='axes fraction',
            fontsize=STYLE["subplot.label.size"],
            ha='center',
            va='top'
        )
    else:
        ax.annotate(
            label,
            xy=(STYLE["subplot.label.x_ab"], STYLE["subplot.label.y_ab"]),  # 图下方中央
            xycoords='axes fraction',
            fontsize=STYLE["subplot.label.size"],
            ha='center',
            va='top'
        )

    # --- 图例 ---
    if label == "(a)":
        leg = ax.legend(
            bbox_to_anchor=(STYLE["legend_a_x"], STYLE["legend_a_y"]),  # 图例在坐标轴中的精确位置 (x, y)，0~1 相对坐标
            # frameon=True,  # 开启图例背景框
            handletextpad=0.4,  # 文字与 marker 距离
            handlelength=1.3,  # 图例中 marker 的长度
            borderpad=0.55,  # 控制框内边距
            fontsize=STYLE["legend.fontsize"],  # 图例字体大小
        )
    if label == "(b)":
        leg = ax.legend(
            bbox_to_anchor=(STYLE["legend_b_x"], STYLE["legend_b_y"]),  # 图例在坐标轴中的精确位置 (x, y)，0~1 相对坐标
            # frameon=True,  # 开启图例背景框
            handletextpad=0.4,  # 文字与 marker 距离
            handlelength=1.3,  # 图例中 marker 的长度
            borderpad=0.55,  # 控制框内边距
            fontsize=STYLE["legend.fontsize"],  # 图例字体大小
        )
    if label == "(c)":
        leg = ax.legend(
            bbox_to_anchor=(STYLE["legend_c_x"], STYLE["legend_c_y"]),  # 精确位置 (x, y)
            # frameon=True,  # 开启图例背景框
            handletextpad=0.4,  # 文字与 marker 距离
            handlelength=1.3,  # 图例中 marker 的长度
            borderpad=0.55,  # 控制框内边距
            fontsize=STYLE["legend.fontsize"],
        )

    # --- 设置图例边框线宽（legend() 不接受 linewidth，只能这样设置） ---
    leg.get_frame().set_linewidth(0.6)  # 图例边框线宽

    # ax.legend([emd_dummy], [emd_text],
    #                        loc='lower left',
    #                        bbox_to_anchor=(0.01, 0.01),  # 左下角微调
    #                        handletextpad=0.0,  # ← 关键：减少文字左边距
    #                        borderpad=0.45,  # ← 控制框内边距
    #                        handlelength=0,
    #                        labelspacing=0.2,
    #                        framealpha=0.45
    #                        )


# ============================================================
# 绘制图像
# ============================================================


fig = plt.figure(figsize=STYLE["fig.size"])
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1.2])

# 上排：a, b
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])

# 下排：c 占据整行
ax_c = fig.add_subplot(gs[1, :])

ax_a.set_ylabel("$P(d)$", fontsize=STYLE["axes.labelsize"])
ax_b.set_ylabel("$P(d)$", fontsize=STYLE["axes.labelsize"])
ax_c.set_ylabel("$P(d)$", fontsize=STYLE["axes.labelsize"])
plot_group(ax_a, networks_a, "(a)")
plot_group(ax_b, networks_b, "(b)")
plot_group(ax_c, networks_c, "(c)")


plt.subplots_adjust(
    top=0.983,
    bottom=0.123,
    left=0.07,
    right=0.993,
    hspace=0.335,
    wspace=0.145
)
# 保存
plt.rcParams['pdf.fonttype'] = 42   # 解决保存pdf的报错问题
plt.savefig("D:\科研论文文稿\Paper_RL\图\Figs\Fig_CN.pdf", format="pdf")
plt.savefig('D:\科研论文文稿\Paper_RL\图\Figs\Fig_CN.svg', format='svg')
plt.show()
