# -*- coding: UTF-8 -*-
'''
@Project ：Paper_模拟网络 
@File    ：Fig-DD-JS(可视化).py
@IDE     ：PyCharm 
@Author  ：Vinne
@Date    ：2025/8/27 1:47
@Explain ：
'''
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 设置西文字体为新罗马字体
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
config = {
    "font.family": 'Times New Roman',  # 设置字体类型
}
rcParams.update(config)
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'   # ！数学符号也使用 Times New Roman
# # 启用 LaTeX 渲染
# plt.rcParams['text.usetex'] = True

# 子图标号函数
def get_label(index):
    result = ''
    while True:
        result = chr(97 + index % 26) + result
        index = index // 26 - 1
        if index < 0:
            break
    return f'({result})'


# 可视化参数设置
alpha_value = 0.9  # 设置散点透明度
markeredgewidth_value = 0.1     # 设置散点边宽度
markersize = 6    # 散点大小
# 子图号码位置
annotate_x = 0.5
annotate_y = -0.168
plt.rc('axes', titlesize=8)    # 子图标题字体大小
plt.rc('axes', labelsize=15)    # 轴标签字体大小
plt.rc('xtick', labelsize=12)   # x轴刻度字体大小
plt.rc('ytick', labelsize=12)   # y轴刻度字体大小
plt.rc('legend', fontsize=11)  # 图例字体大小
annotate_font = FontProperties(size=16)     # 定义注释的字体属性（子图标签）

# 读取保存的 CSV
df_all = pd.read_csv("data/result/RLvsReal_JS.csv")
# 提取所有真实-实验网络配对
network_pairs = set()
exp_pattern = re.compile(r"Exp_(.+?)_r([0-9.]+)")
for name in df_all['network']:
    if name.startswith("Exp_"):
        match = exp_pattern.match(name)
        if match:
            real_name = match.group(1)
            r_val = match.group(2)
            if f"Real_{real_name}" in df_all['network'].values:
                network_pairs.add(real_name)

# 从 Excel 中读取绘图顺序
real_net_info = pd.read_excel("data/result/真实网络与计算结果.xlsx", sheet_name=0)  # 默认读取第一个sheet
net_order = real_net_info['网络名称'].dropna().astype(str).tolist()
# 创建一个映射：网络名称 -> 颜色
color_map = dict(zip(real_net_info['网络名称'].astype(str), real_net_info['颜色']))
# 创建一个映射：网络名称 -> 最优JS
emd_map = dict(zip(real_net_info['网络名称'].astype(str), real_net_info['RL(JS)']))


# 保留存在于 df_all 中的网络
available_pairs = []
for real_name in net_order:
    if f"Real_{real_name}" in df_all['network'].values:
        available_pairs.append(real_name)
missing = set(net_order) - set(available_pairs)
if missing:
    print("以下网络在 CSV 数据中未找到：", missing)

# 设置子图布局
ncols = 4
nrows = int(np.ceil(len(available_pairs) / ncols))
fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 4, nrows * 3))
for i, real_name in enumerate(available_pairs):
    ax = axes[i // ncols, i % ncols]
    print(real_name)
    # 获取数据行
    exp_row = df_all[df_all['network'].str.contains(f"Exp_{real_name}_r")].iloc[0]
    real_row = df_all[df_all['network'] == f"Real_{real_name}"].iloc[0]

    # 提取 r 值
    match = re.match(r"Exp_(.+?)_r(-?\d+(?:\.\d+)?)", exp_row['network'])
    r_val = match.group(2) if match else "*"

    # 构造图例标签
    exp_legend = f"Our (r={r_val})"
    real_legend = f"Real ({real_name})"

    exp_deg = list(map(int, exp_row['degree'].split(',')))
    exp_distr = list(map(float, exp_row['degree_distr'].split(',')))
    real_deg = list(map(int, real_row['degree'].split(',')))
    real_distr = list(map(float, real_row['degree_distr'].split(',')))

    # 去除 0 值
    exp_k = [k for k, p in zip(exp_deg, exp_distr) if k > 0 and p > 0]
    exp_p = [p for k, p in zip(exp_deg, exp_distr) if k > 0 and p > 0]
    real_k = [k for k, p in zip(real_deg, real_distr) if k > 0 and p > 0]
    real_p = [p for k, p in zip(real_deg, real_distr) if k > 0 and p > 0]

    # 绘制实验和真实网络的散点图
    ax.plot(exp_k, exp_p, 's', label=exp_legend, color="#124B7D",
            alpha=alpha_value, markersize=markersize,
            markeredgewidth=markeredgewidth_value)

    real_color = color_map.get(real_name, "#000000")  # 若找不到则默认使用橙色
    ax.plot(real_k, real_p, 'o', label=real_legend, color=real_color,
            alpha=alpha_value, markersize=markersize,
            markeredgewidth=markeredgewidth_value)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid(color="#E8E8E8", linestyle="-.", zorder=0, linewidth=0.4)
    ax.xaxis.set_major_locator(plt.LogLocator(base=10.0, numticks=10))
    ax.yaxis.set_major_locator(plt.LogLocator(base=10.0, numticks=10))

    # 判断是否在最左边的列（第一列）
    is_left_col = (i % ncols == 0)
    # 判断是否在最底行
    is_bottom_row = (i // ncols == nrows - 1)
    if is_left_col:
        ax.set_ylabel("$P(d)$")
    else:
        ax.set_ylabel("")  # 保留刻度，但去掉标签
    if is_bottom_row:
        ax.set_xlabel("$d$", labelpad=17.5) #labelpad 控制标签与轴的距离
    else:
        ax.set_xlabel("")  # 保留刻度，但去掉标签

    # 构造图例
    # --- 根据子图编号调整图例位置 ---
    if i in [1, 3]:  # b、d 子图
        legend_loc = 'upper left'
    else:
        legend_loc = 'upper right'

    main_legend = ax.legend(handlelength=0.8, labelspacing=0.4,
                            loc=legend_loc, framealpha=0.45)
    ax.add_artist(main_legend)

    from matplotlib.lines import Line2D
    emd_value = emd_map.get(real_name, None)
    emd_text = f"JS: {emd_value:.4f}" if emd_value is not None else "JS: N/A"
    emd_dummy = Line2D([], [], linestyle='none', marker='', label=emd_text)

    emd_legend = ax.legend([emd_dummy], [emd_text],
                           loc='lower left',  # 可按需改为 'lower right' 等
                           bbox_to_anchor=(0.035, 0.034),  # 左下角微调
                           handletextpad=0.0,  # ← 关键：减少文字左边距
                           borderpad=0.45,  # ← 控制框内边距
                           handlelength=0,
                           labelspacing=0.2,
                           framealpha=0.45
                           )

    # 添加子图标识 (a), (b), ...
    label_str = get_label(i)
    ax.annotate(label_str, xy=(annotate_x, annotate_y), xycoords='axes fraction',
                ha='center', va='center', fontproperties=annotate_font)


# 移除多余子图
for j in range(i + 1, nrows * ncols):
    fig.delaxes(axes[j // ncols, j % ncols])

plt.subplots_adjust(
    top=0.993,
    bottom=0.032,
    left=0.043,
    right=0.99,
    hspace=0.25,
    wspace=0.132
)
# 保存为 SVG 格式
plt.rcParams['pdf.fonttype'] = 42   # 解决保存pdf的报错问题
plt.savefig("D:\科研论文文稿\Paper_RL\图\Figs\Fig-DD-JS.pdf", format="pdf")
plt.savefig('D:\科研论文文稿\Paper_RL\图\Figs\Fig-DD-JS.svg', format='svg')
# plt.show()


