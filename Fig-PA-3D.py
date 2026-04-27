# -*- coding: UTF-8 -*-
'''
@Project ：Paper_RL 
@File    ：Fig-PA-3D(可视化).py
@IDE     ：PyCharm 
@Author  ：Vinne
@Date    ：2026/1/8 11:48
@Explain ：
'''
import os
import string
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import matplotlib.colors as mcolors
from matplotlib import font_manager
import matplotlib.colors as mcolors

plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'   # ！数学符号也使用 Times New Roman


# ===== 绘图参数设置 =====
# 字体与尺寸
FONT_SIZE = 10        # 全局字体大小
TITLE_SIZE = 21       # 行列标题字体大小
LABEL_SIZE = 15       # 坐标轴标签字体大小
TICK_SIZE = 10        # 坐标刻度字体大小
# 子图标号设置
LABEL_FONT_SIZE = 18       # 子图标号字体大小
LABEL_POS_X = 0.1         # 子图标号横向位置（相对子图坐标系）
LABEL_POS_Y = 0.91         # 子图标号纵向位置（相对子图坐标系）

# 图像尺寸与间距
FIG_WIDTH = 8         # 整体图像宽度（英寸）
ROW_HEIGHT = 3        # 每一行高度（英寸）
COLUMN_NAME_PAD = 7   # 列名 与图的上下间距
ROW_NAME_SPACE = -0.20  # 行名 与图的左右间距

# 坐标轴
XTICK_STEP = 1   # k 轴刻度步长
YTICK_STEP = 1   # r 轴刻度步长
ZTICK_NUM = 5      # z 轴刻度数量（自动均分）
AXIS_LINEWIDTH = 0.8  # 坐标轴线条粗细
LABEL_PAD = -6       # 坐标轴标签距轴的距离
TICK_PAD = -4   # 坐标刻度值距轴的距离
# 网格标识线
GRID_LINEWIDTH = 0.4  # 网格线粗细
GRID_STYLE = "--"      # 网格线样式
GRID_COLOR = "#E8E8E8"      # 网格线颜色
FACE_COLOR = "#f9f9f9"  # 基面底色
# 散点样式参数
SCATTER_SIZE = 23          # 散点大小
SCATTER_ALPHA = 0.6       # 散点透明度 (0~1)
SCATTER_EDGE_WIDTH = 0.85      # 散点边框宽度
SCATTER_EDGE_WIDTH_ALPHA = 0.74     # 散点边框亮度（越小越深色）
# 设置颜色点位
color_points = [
    (0.0, "#1D5287"),   # 最小值
    (0.25, "#9AB7DA"),
    (0.5, "#F1F5F8"),
    (0.75, "#F6B4C7"),
    (1.0, "#8c1414")    # 最大值
]
# 构造线性渐变 colormap
custom_cmap = mcolors.LinearSegmentedColormap.from_list("my_cmap", color_points)

# 设置字体，避免乱码；同时解决负号显示问题
plt.rcParams['font.sans-serif'] = ['Times New Roman']   # 使用黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示问题
plt.rcParams['font.size'] = FONT_SIZE          # 全局字体大小
# 定义中英字体
cn_font_legend = font_manager.FontProperties(family='SimSun', size=FONT_SIZE)
en_font_legend = font_manager.FontProperties(family='Times New Roman', size=FONT_SIZE)

if __name__ == "__main__":

    # ===== 手动设置要绘制的三列网络规模 n =====
    ns_for_cols = [100, 1000, 10000]

    # ===== 实验设置，同时也是文件路径的一部分 =====
    k_min, k_max = 2.2, 8
    r_min, r_max = -2, 2
    step = 0.2
    repeats = 1

    # 行名（各网络属性）的映射字典
    attr_name_map = {
        "avg_degree": r"$\langle$d$\rangle$",
        "avg_clustering": r"$\langle$C$\rangle$",
        "avg_path_length": r"$\langle$L$\rangle$",
        "diameter": r"D",
        "density": r"$\rho$"
    }

    # 构造三个 CSV 文件路径，每个对应一个网络规模 n
    csv_files = [
        f"data/ParameterAnalysis-3D/k({k_min},{k_max})_r({r_min},{r_max})_step({step})/参数分析实验结果_{n}_{step}_{repeats}.csv"
        for n in ns_for_cols
    ]

    # ===== 读取数据 =====
    dfs = []
    for path in csv_files:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"未找到文件: {path}")
        dfs.append(pd.read_csv(path))

    # ===== 自动识别指标列 =====
    # 排除参数列 n, k, r，只保留数值型的网络属性列
    param_cols = {"n", "k", "r"}
    metric_cols = [
        c for c in dfs[0].columns
        if c not in param_cols and pd.api.types.is_numeric_dtype(dfs[0][c])
    ]
    # ===== 手动控制绘制顺序 =====
    # 行顺序【平均度 → 密度 → 平均路径长度 → 直径 → 平均聚类系数】
    desired_order = ["avg_degree", "density", "avg_path_length", "diameter", "avg_clustering"]
    # 只保留在 metric_cols 中存在的列，避免缺失报错
    metric_cols = [c for c in desired_order if c in metric_cols]

    total_rows = len(metric_cols)

    # ===== 创建总图像 =====
    # 行数 = 3（对应 n），列数 = 属性数
    fig = plt.figure(figsize=(15, 8.5))  # 横向更宽，纵向更矮
    gs = fig.add_gridspec(nrows=3, ncols=total_rows)

    # ===== 绘制每个属性 =====
    # 外层 i 遍历 n，内层 j 遍历属性
    for i, (n_val, df) in enumerate(zip(ns_for_cols, dfs)):
        for j, attr in enumerate(metric_cols):
            ax = fig.add_subplot(gs[i, j], projection="3d")

            # 数据抽取与空处理
            dfx = df.dropna(subset=["k", "r", attr])
            K = dfx["k"].values.astype(float)
            R = dfx["r"].values.astype(float)
            V = dfx[attr].values.astype(float)

            # 生成散点颜色
            norm = plt.Normalize(vmin=np.min(V), vmax=np.max(V))
            colors = custom_cmap(norm(V))
            # 生成散点边颜色
            fill_colors = custom_cmap(norm(V))
            edge_colors = []
            for fc in fill_colors:
                r, g, b, a = fc
                h, s, v = mcolors.rgb_to_hsv([r, g, b])
                v *= SCATTER_EDGE_WIDTH_ALPHA  # 降低亮度，得到更深的边框色
                edge_colors.append((*mcolors.hsv_to_rgb([h, s, v]), a))

            ssc = ax.scatter(
                K, R, V,
                c=colors,
                s=SCATTER_SIZE,
                alpha=SCATTER_ALPHA,
                edgecolors=edge_colors,
                linewidths=SCATTER_EDGE_WIDTH,
            )

            # 坐标范围与刻度精度
            ax.set_xlim(k_min, k_max)
            ax.set_ylim(r_min, r_max)
            ax.set_xticks(np.arange(k_min, k_max + 1e-9, XTICK_STEP))
            ax.set_yticks(np.arange(r_min, r_max + 1e-9, YTICK_STEP))

            v_min, v_max = float(np.min(V)), float(np.max(V))
            if v_min == v_max:
                # 避免 z 轴范围退化
                v_min -= 1e-6
                v_max += 1e-6
            ax.set_zlim(v_min, v_max)
            ax.set_zticks(np.linspace(v_min, v_max, ZTICK_NUM))
            # z刻度统一显示小数点后 2 位
            ax.zaxis.set_major_formatter(mticker.FormatStrFormatter("%.3f"))

            # 设置刻度字体大小和距轴距离
            ax.tick_params(axis='x', labelsize=int(TICK_SIZE), pad=int(TICK_PAD))
            ax.tick_params(axis='y', labelsize=int(TICK_SIZE), pad=int(TICK_PAD))
            ax.tick_params(axis='z', labelsize=int(TICK_SIZE), pad=int(TICK_PAD))

            # 设置 z 轴刻度标签左对齐，避免视觉偏移
            for lbl in ax.get_zticklabels():
                lbl.set_horizontalalignment("left")  # 左对齐
                lbl.set_fontproperties(en_font_legend)
                lbl.set_fontsize(TICK_SIZE)

            # 设置刻度字体为 Times New Roman
            for lbl in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
                lbl.set_fontproperties(en_font_legend)

            # 设置坐标轴标签
            ax.set_xlabel("k", fontproperties=en_font_legend, fontsize=LABEL_SIZE, labelpad=int(LABEL_PAD))
            ax.set_ylabel("r", fontproperties=en_font_legend, fontsize=LABEL_SIZE, labelpad=int(LABEL_PAD))
            ax.set_zlabel("")   # 不显示 z 轴标签

            # 坐标轴线条粗细（3D轴通过 _axinfo 控制）
            ax.w_xaxis.line.set_linewidth(AXIS_LINEWIDTH)
            ax.w_yaxis.line.set_linewidth(AXIS_LINEWIDTH)
            ax.w_zaxis.line.set_linewidth(AXIS_LINEWIDTH)

            # 设置三维面颜色
            ax.w_xaxis.set_pane_color((*mcolors.to_rgb(FACE_COLOR), 1.0))
            ax.w_yaxis.set_pane_color((*mcolors.to_rgb(FACE_COLOR), 1.0))
            ax.w_zaxis.set_pane_color((*mcolors.to_rgb(FACE_COLOR), 1.0))

            # 设置网格线样式
            for axis in [ax.w_xaxis, ax.w_yaxis, ax.w_zaxis]:
                axis._axinfo['grid']['linestyle'] = GRID_STYLE
                axis._axinfo['grid']['linewidth'] = GRID_LINEWIDTH
                axis._axinfo['grid']['color'] = ((*mcolors.to_rgb(GRID_COLOR), 1.0))

            # 每一行最左侧子图显示网络规模
            exp = int(math.floor(math.log10(n_val)))
            base = n_val / (10 ** exp)
            n_str = rf"10^{{{exp}}}"
            if j == 0:
                ax.text2D(ROW_NAME_SPACE, 0.5, f"n$={n_str}$",
                          fontproperties=en_font_legend, fontsize=TITLE_SIZE,
                          va="center", ha="center", transform=ax.transAxes)

            # 每一列最上方子图显示属性名
            if i == 0:
                ax.set_title(attr_name_map.get(attr, attr),
                             fontproperties=en_font_legend, fontsize=TITLE_SIZE,
                             pad=COLUMN_NAME_PAD)

            # i = 行索引 (对应 n)， j = 列索引 (对应属性)
            rows = len(ns_for_cols)  # 3
            cols = len(metric_cols)  # 5
            subplot_index = j * rows + i  # 竖向编号：先按列，再按行
            letters = string.ascii_lowercase
            label = ""
            idx = subplot_index
            while True:
                label = letters[idx % 26] + label
                idx //= 26
                if idx == 0:
                    break
                idx -= 1
            label = f"({label})"

            # 添加到子图
            ax.text2D(LABEL_POS_X, LABEL_POS_Y, label,
                      transform=ax.transAxes,
                      fontproperties=en_font_legend,  # 使用英文字体
                      fontsize=LABEL_FONT_SIZE,
                      # fontweight=LABEL_FONT_WEIGHT,
                      ha="left", va="top")

    plt.subplots_adjust(
        top=0.98,
        bottom=0.0,
        left=0.066,
        right=0.972,
        hspace=0.0,
        wspace=0.18
    )
    # 保存
    plt.rcParams['pdf.fonttype'] = 42  # 解决保存pdf的报错问题
    plt.savefig("D:\科研论文文稿\Paper_RL\图\Figs\Fig-PA-3D.pdf", format="pdf")
    plt.savefig('D:\科研论文文稿\Paper_RL\图\Figs\Fig-PA-3D.svg', format='svg')
    # 显示图像（交互式窗口）
    plt.show()




