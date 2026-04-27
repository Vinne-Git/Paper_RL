# -*- coding: UTF-8 -*-
"""
@Project ：Paper_RL
@File    ：Fig-AE.py
@IDE     ：PyCharm
@Author  ：Vinne
@Date    ：2026/3/29
@Explain ：消融实验主图+附图可视化，凸显“本文机制缺一不可”
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.transforms as mtransforms
# 字体统一设置
from matplotlib import rcParams
config = {
    "font.family": 'Times New Roman',  # 设置字体类型
}
rcParams.update(config)
plt.rcParams['font.sans-serif'] = 'Times New Roman'

# ============================
# 配色方案
# ============================

model_colors = {
    "RL": "#2c6d99",#2c6d99
    "EPG": "#F2E1A4",#F2E1A4
    "NPA": "#E89B9B",#E89B9B
    "BA": "#797979",#797979
}

# ============================
# 参数设置（统一控制）
# ============================

FIGSIZE = (15, 5)        # 整个图的画布大小（宽度, 高度），影响主图+附图整体比例
TITLE_SIZE = 16          # 主标题字体大小（如雷达图标题）
radar_LABEL_SIZE = 16    # 雷达图轴标签字体大小
LABEL_SIZE = 12         # 轴标签字体大小
TICK_SIZE_radar = 10      # 雷达图刻度字体大小

radar_LEGEND_x = 0.523      # 图例位置
radar_LEGEND_y = -0.102     # 图例位置
radar_linewidth = 8     # 图例色条宽度（粗细）
radar_handlelength = 1.6    # 图例色条长度
LEGEND_SIZE = 14         # 图例字体大小（RL、EPG、NPA的说明）
LINE_WIDTH = 2           # 雷达图上的线条粗细
FILL_ALPHA = 0.32        # 雷达图曲线下的填充区域透明度
GRID_COLOR = "gray"      # 雷达图网格线颜色
GRID_STYLE = "--"        # 雷达图网格线样式
GRID_WIDTH = 0.5         # 雷达图网格线宽度
GRID_ALPHA = 0.7        # 雷达图网格线透明度


TICK_SIZE = 7            # 坐标轴刻度字体大小（如网络简称、数值刻度）
bar_width = 0.6             # 每个柱子的宽度
tick_spacing = bar_width*3  # 每个刻度的间隔距离（等于3倍的柱子宽度）
margin = 1                # 柱状图左右留白宽度



# ============================
# 参数设置
# ============================

file_path = "data/result/真实网络与计算结果.xlsx"
models_radar = ["RL", "EPG", "NPA", "BA"]
metrics_radar = ["SINS", "NLSD", "WD", "KS", "JS", "GDD"]
models_bar = ["RL", "EPG", "NPA"]
metrics_bar = ["NLSD", "WD", "SINS", "KS", "GDD", "JS"]
# 预定义子图标号
labels = ["(a)", "(d)", "(b)", "(e)", "(c)", "(f)"]
# 定义显示名称映射
display_names = {
    "RL": "Full",
    "EPG": "EPG",
    "NPA": "NPA",
    "BA": "BA"
}

# ============================
# 数据读取与处理
# ============================

df = pd.read_excel(file_path)
networks = df["简称"].tolist()

# 平均值计算（用于雷达图）
avg_scores = {model: [] for model in models_radar}
for model in models_radar:
    for metric in metrics_radar:
        col_name = f"{model}({metric})"
        if col_name in df.columns:
            avg_val = df[col_name].mean()
            avg_scores[model].append(avg_val)
        else:
            raise ValueError(f"列 {col_name} 不存在，请检查 Excel 文件")

score_matrix = np.array([avg_scores[m] for m in models_radar])  # shape: (4,6)

# ============================
# 指标归一化处理（雷达图用）
# ============================

score_matrix_norm = np.zeros_like(score_matrix)
for j, metric in enumerate(metrics_radar):
    col_vals = score_matrix[:, j]
    if metric == "GDD":
        score_matrix_norm[:, j] = col_vals / col_vals.max()
    else:
        inv_vals = col_vals.max() / col_vals
        score_matrix_norm[:, j] = inv_vals / inv_vals.max()

# ============================
# 绘制主图+附图
# ============================

fig = plt.figure(figsize=FIGSIZE)
# gs = gridspec.GridSpec(3, 3, figure=fig, width_ratios=[1, 1.2, 1.2])
outer_gs = gridspec.GridSpec(
    1, 2, figure=fig,
    width_ratios=[0.76, 2],   # 左右比例
    wspace=0.185                # ★ 左–右间距（你要精确控制的）
)


# 主图：雷达图占左侧三行
# ax_radar = fig.add_subplot(gs[:,0], polar=True)
ax_radar = fig.add_subplot(outer_gs[0], polar=True)

num_metrics = len(metrics_radar)
angles = np.linspace(0, 2*np.pi, num_metrics, endpoint=False).tolist()
angles += angles[:1]

zorders = {
    "RL": 2,
    "EPG": 4,
    "NPA": 5,
    "BA": 3
}
# 绘制曲线与填充
for i, model in enumerate(models_radar):
    values = score_matrix_norm[i].tolist()
    values += values[:1]
    ax_radar.plot(angles, values, label=display_names[model],
                  color=model_colors[model],
                  linewidth=LINE_WIDTH,
                  zorder=zorders[model] + 1  # 线条比填充高一层
                  )  # 更粗线条
    ax_radar.fill(angles, values,
                  color=model_colors[model],
                  alpha=FILL_ALPHA,     # 更淡填充
                  zorder=zorders[model]   # 填充层
                  )

# 设置角度刻度（指标标签）
ax_radar.set_xticks(angles[:-1])
ax_radar.set_xticklabels(metrics_radar, fontsize=radar_LABEL_SIZE)

import matplotlib.transforms as mtransforms

fig.canvas.draw()  # 必须先渲染一次

# 为每个标签设置不同的偏移量（单位：points）
# "SINS", "NLSD", "WD", "KS", "JS", "GDD"
offsets = [-15, -2, 4, 10, 5, -3]  # 每个指标独立设置

for label, offset in zip(ax_radar.get_xticklabels(), offsets):
    # 在文本自身坐标系基础上添加一个平移
    text_transform = (
        label.get_transform() +
        mtransforms.ScaledTranslation(0, offset / 72, fig.dpi_scale_trans)
    )
    label.set_transform(text_transform)



# 设置径向刻度（数值范围 0–1）
ax_radar.set_ylim(0, 1)
ax_radar.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # 环形刻度线位置
ax_radar.set_yticklabels(["20%", "40%", "60%", "80%", "100%"],
                         fontsize=TICK_SIZE_radar, color="gray")

# 调整角度，使 SINS 在顶部
ax_radar.set_theta_offset(np.pi/2)

# 标题与图例
legend = ax_radar.legend(loc="upper center",
                bbox_to_anchor=(radar_LEGEND_x, radar_LEGEND_y),
                ncol=4, frameon=False,
                fontsize=LEGEND_SIZE,
                handlelength=radar_handlelength,  # 控制色条的长度（更宽）
                handletextpad=0.8,  # 色条与文字之间的间距
                columnspacing=1.5,   # 各标签之间的间距
                )

# 修改图例色条的粗细
for legline in legend.legendHandles:
    legline.set_linewidth(radar_linewidth)  # 设置雷达图图例的色条粗细

# 美化网格与边框
ax_radar.spines["polar"].set_visible(False)
ax_radar.grid(True, color=GRID_COLOR, linestyle=GRID_STYLE,
              linewidth=GRID_WIDTH, alpha=GRID_ALPHA)


right_gs = gridspec.GridSpecFromSubplotSpec(
    3, 2,
    subplot_spec=outer_gs[1],
    # wspace=0.1,    # ★ 控制右侧两列之间的间距
    # hspace=0.35     # 控制上下间距
)

# 附图：右侧 3×2 柱状图
for idx, metric in enumerate(metrics_bar):
    # 计算子图所在的行和列位置（3行2列布局）
    # row = idx // 2
    # col = idx % 2 + 1  # 第0列是雷达图，所以这里从第1列开始
    row = idx // 2
    col = idx % 2

    if metric == "WD":

        # 将 WD 的格子再细分成上下两层
        # inner_gs = gridspec.GridSpecFromSubplotSpec(
        #     2, 1, subplot_spec=gs[row, col], height_ratios=[1, 3], hspace=0.05
        # )
        inner_gs = gridspec.GridSpecFromSubplotSpec(
            2, 1,
            subplot_spec=right_gs[row, col],
            height_ratios=[1, 3],
            hspace=0.05
        )

        ax_high = fig.add_subplot(inner_gs[0])  # 上层显示极大值
        ax_low = fig.add_subplot(inner_gs[1])  # 下层显示常规范围

        # 设置 y 轴范围
        ymax = df[[f"{m}(WD)" for m in models_bar]].values.max()
        ax_low.set_ylim(0, 52)
        ax_high.set_ylim(ymax - 200, ymax+20)

        # 横坐标
        x = np.arange(len(networks)) * tick_spacing

        # 绘制柱状图到两个子图
        for j, model in enumerate(models_bar):
            vals = df[f"{model}(WD)"].values
            ax_low.bar(x + j * bar_width, vals, bar_width,
                       color=model_colors[model], zorder=2)
            ax_high.bar(x + j * bar_width, vals, bar_width,
                        color=model_colors[model], zorder=2)

        # 设置横坐标刻度只在下侧显示
        ax_low.set_xticks(x + (len(models_bar) * bar_width) / 2 - bar_width / 2)
        ax_low.set_xticklabels(networks, fontsize=TICK_SIZE, rotation=50,
                               ha="right", va="top")
        plt.setp(ax_high.get_xticklabels(), visible=False)

        ax_low.set_yticks([0, 25, 50])

        # 添加断口符号（上下都加，统一粗细）
        d = 0.014
        width = 0.9
        ax_low.plot([-d, +d], [1, 1], transform=ax_low.transAxes,
                    color='k', linewidth=width, clip_on=False)
        ax_low.plot([1 - d, 1 + d], [1, 1], transform=ax_low.transAxes,
                    color='k', linewidth=width, clip_on=False)

        ax_high.plot([-d, +d], [0, 0], transform=ax_high.transAxes,
                     color='k', linewidth=width, clip_on=False)
        ax_high.plot([1 - d, 1 + d], [0, 0], transform=ax_high.transAxes,
                     color='k', linewidth=width, clip_on=False)

        ax_high.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)
        ax_high.spines["bottom"].set_visible(False)
        ax_low.spines["top"].set_visible(False)

        # 设置标签和网格
        ax_low.set_ylabel("WD", fontsize=LABEL_SIZE)
        ax_low.grid(True, axis="y", color="#E8E8E8", linestyle="-.", linewidth=0.5)
        ax_high.grid(True, axis="y", color="#E8E8E8", linestyle="-.", linewidth=0.5)

        # 子图标号
        ax_high.text(1.06, 0.935, labels[idx], transform=ax.transAxes,
                fontsize=LABEL_SIZE, va="top", ha="left")

        for label in ax_low.get_xticklabels():
            label.set_position((0, 0.03))
            # 在原有 transform 基础上加一个水平偏移
            offset = mtransforms.ScaledTranslation(4 / 72, 0, fig.dpi_scale_trans)
            label.set_transform(label.get_transform() + offset)

    else:
        # ax = fig.add_subplot(gs[row, col])
        ax = fig.add_subplot(right_gs[row, col])

        # 横坐标：每组的起始位置
        x = np.arange(len(networks)) * tick_spacing

        # 绘制 RL、EPG、NPA 三个模型的柱状图
        for j, model in enumerate(models_bar):
            col_name = f"{model}({metric})"
            vals = df[col_name].values
            ax.bar(x + j * bar_width, vals,
                   bar_width,
                   color=model_colors[model],
                   zorder=2
                   )

        # 设置横坐标刻度为网络简称（居中在每组柱子下方）
        ax.set_xticks(x + (len(models_bar) * bar_width) / 2 - bar_width / 2)
        ax.set_xticklabels(networks, fontsize=TICK_SIZE, rotation=50,
                               ha="right", va="top")

        # 每组柱子的总宽度（不含间隔）
        group_width = len(models_bar) * bar_width
        # 设置横坐标范围：从左边留 margin，到最后一组柱子结束再加 margin
        ax.set_xlim(-margin, x[-1] + 2/3*group_width + margin)

        # 设置纵坐标标签为指标名称
        ax.set_ylabel(metric, fontsize=LABEL_SIZE)

        # 子图标号
        ax.text(-0.115, 0.95, labels[idx], transform=ax.transAxes,
                fontsize=LABEL_SIZE, va="top", ha="center")

        # 设置背景网格线
        ax.grid(True, axis="y", color="#E8E8E8", linestyle="-.", linewidth=0.5)

        for label in ax.get_xticklabels():
            label.set_position((0, 0.03))
            # 在原有 transform 基础上加一个水平偏移
            offset = mtransforms.ScaledTranslation(4 / 72, 0, fig.dpi_scale_trans)
            label.set_transform(label.get_transform() + offset)


plt.subplots_adjust(
    top=0.97,
    bottom=0.118,
    left=0.037,
    right=0.989,
    hspace=0.412,
    wspace=0.196
)

# 保存
plt.rcParams['pdf.fonttype'] = 42   # 解决保存pdf的报错问题
plt.savefig("D:\科研论文文稿\Paper_RL\图\Figs\Fig_AE.pdf", format="pdf")
plt.savefig('D:\科研论文文稿\Paper_RL\图\Figs\Fig_AE.svg', format='svg')
plt.show()
