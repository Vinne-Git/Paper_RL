# -*- coding: UTF-8 -*-
'''
@Project ：Paper_模拟网络 
@File    ：Fig-PA-DD.py
@IDE     ：PyCharm 
@Author  ：Vinne
@Date    ：2025/6/16 15:12 
@Explain ：
'''
import networkx as nx
import pandas as pd
import numpy as np
import ren_lv_graph as rl
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

print("网络读取中..")
networks = {
    'n=2000, k=6, r=-10': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=6_r=-10.gexf"),
    'n=2000, k=6, r=-1': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=6_r=-1.gexf"),
    'n=2000, k=6, r=-0.5': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=6_r=-0.5.gexf"),
    'n=2000, k=6, r=0': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=6_r=0.gexf"),
    'n=2000, k=6, r=0.5': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=6_r=0.5.gexf"),
    'n=2000, k=6, r=1': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=6_r=1.gexf"),
    'n=2000, k=6, r=10': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=6_r=10.gexf"),

    'n=2000, k=4, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=4_r=0.8.gexf"),
    'n=2000, k=6, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=6_r=0.8.gexf"),
    'n=2000, k=8, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=8_r=0.8.gexf"),
    'n=2000, k=10, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=10_r=0.8.gexf"),
    'n=2000, k=12, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=2000_k=12_r=0.8.gexf"),

    'n=500, k=6, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=500_k=6_r=0.8.gexf"),
    'n=5000, k=6, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=5000_k=6_r=0.8.gexf"),
    'n=10000, k=6, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=10000_k=6_r=0.8.gexf"),
    'n=20000, k=6, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=20000_k=6_r=0.8.gexf"),
    'n=100000, k=6, r=0.8': nx.read_gexf("data/ParameterAnalysis-DD/RL_n=100000_k=6_r=0.8.gexf"),
}

print("度分布计算中..")
results = []  # 初始化结果列表用于保存每个网络的度分布数据
for name, G in networks.items():
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degree_count = np.bincount(degree_sequence)  # 计算每个度的出现次数
    degree = np.arange(len(degree_count))  # 生成度的数组
    degree_distr = degree_count / degree_count.sum() # 归一化处理：将每个度的频数除以总节点
    results.append({'network': name, 'degree': list(degree), 'degree_distr': list(degree_distr)})  # 将结果保存到列表

# 将结果转换为 DataFrame，保存时以字符串形式保存列表
df = pd.DataFrame(results)
df['degree'] = df['degree'].apply(lambda x: ','.join(map(str, x)))
df['degree_distr'] = df['degree_distr'].apply(lambda x: ','.join(map(str, x)))

# 子图的网络列表
networks_a = [
    'n=500, k=6, r=0.8',
    'n=5000, k=6, r=0.8',
    'n=10000, k=6, r=0.8',
    'n=20000, k=6, r=0.8',
    'n=100000, k=6, r=0.8',
]
networks_b = [
    'n=2000, k=4, r=0.8',
    'n=2000, k=6, r=0.8',
    'n=2000, k=8, r=0.8',
    'n=2000, k=10, r=0.8',
    'n=2000, k=12, r=0.8',
]
networks_c = [
    'n=2000, k=6, r=10',
    'n=2000, k=6, r=1',
    'n=2000, k=6, r=0.5',
    'n=2000, k=6, r=0',
    'n=2000, k=6, r=-0.5',
    'n=2000, k=6, r=-1',
    'n=2000, k=6, r=-10',
]

# 绘图顺序（图层）
zorder_dict = {
    'n=2000, k=6, r=-10': 2,
    'n=2000, k=6, r=-1': 2,
    'n=2000, k=6, r=-0.5': 2,
    'n=2000, k=6, r=0': 2,
    'n=2000, k=6, r=0.5': 2,
    'n=2000, k=6, r=1': 2,
    'n=2000, k=6, r=10': 2,

    'n=2000, k=4, r=0.8': 2,
    'n=2000, k=6, r=0.8': 2,
    'n=2000, k=8, r=0.8': 2,
    'n=2000, k=10, r=0.8': 2,
    'n=2000, k=12, r=0.8': 2,

    'n=500, k=6, r=0.8': 2,
    'n=5000, k=6, r=0.8': 2,
    'n=10000, k=6, r=0.8': 2,
    'n=20000, k=6, r=0.8': 2,
    'n=100000, k=6, r=0.8': 2,
}
# 散点符号
marker_dict = {
    'n=2000, k=6, r=10': 'o',
    'n=2000, k=6, r=1': '^',
    'n=2000, k=6, r=0.5': 'v',
    'n=2000, k=6, r=0': '<',
    'n=2000, k=6, r=-0.5': '>',
    'n=2000, k=6, r=-1': 's',
    'n=2000, k=6, r=-10': 'p',

    'n=2000, k=4, r=0.8': 'o',
    'n=2000, k=6, r=0.8': '^',
    'n=2000, k=8, r=0.8': 'v',
    'n=2000, k=10, r=0.8': '<',
    'n=2000, k=12, r=0.8': '>',

    'n=500, k=6, r=0.8': 'o',
    'n=5000, k=6, r=0.8': '^',
    'n=10000, k=6, r=0.8': 'v',
    'n=20000, k=6, r=0.8': '<',
    'n=100000, k=6, r=0.8': '>',
}

# 配色方案
# red1 = "#f6a5a5"  # 红1
# red2 = "#f05454"  # 红2
# orange1 = "#F4A460"  # 橙1
# orange2 = "#ff9900"  # 橙2
# yellow1 = "#F4D03F"  # 黄1
# yellow2 = "#ffd54f"  # 黄2
# green1 = "#16A085"  # 绿1
# green2 = "#3b8c4f"  # 绿2
# cyan = "#16A085"  # 青
# blue1 = "#66b3e6"  # 蓝1
# blue2 = "#4aa6c8"  # 蓝2
# purple = "#7C83D3"  # 紫
# brown = "#8c564b"  # 棕
# pink = "#E6A0C4"  # 粉
# gray = "#757575"  # 灰

blue1 = "#66b3e6"  # 蓝1
purple = "#7C83D3"  # 紫

blue3 = "#124B7D"  # 蓝3
green1 = "#8fbf78"  # 绿1
yellow2 = "#f9c74f"  # 黄2
orange2 = "#ff9900"  # 橙2
red2 = "#F85C42"  # 红2
color_map = {
    'n=500, k=6, r=0.8': blue3,
    'n=5000, k=6, r=0.8': green1,
    'n=10000, k=6, r=0.8': yellow2,
    'n=20000, k=6, r=0.8': orange2,
    'n=100000, k=6, r=0.8': red2,

    'n=2000, k=4, r=0.8': blue3,
    'n=2000, k=6, r=0.8': green1,
    'n=2000, k=8, r=0.8': yellow2,
    'n=2000, k=10, r=0.8': orange2,
    'n=2000, k=12, r=0.8': red2,

    'n=2000, k=6, r=-10': red2,
    'n=2000, k=6, r=-1': orange2,
    'n=2000, k=6, r=-0.5': yellow2,
    'n=2000, k=6, r=0': green1,
    'n=2000, k=6, r=0.5': blue3,
    'n=2000, k=6, r=1': blue1,
    'n=2000, k=6, r=10': purple,
}

# 设置散点透明度
alpha_value = 0.88
# 设置散点边宽度
markeredgewidth_value = 0.1
# 子图号码位置
annotate_x = 0.5
annotate_y = -0.258
# 散点大小
markersize = 8
# 设置字体大小
# plt.rc('axes', titlesize=12)      # 子图标题字体大小
plt.rc('axes', labelsize=16.6)      # 轴标签字体大小
plt.rc('xtick', labelsize=13.5)     # x轴刻度字体大小
plt.rc('ytick', labelsize=13.5)     # y轴刻度字体大小
plt.rc('legend', fontsize=10.9)     # 图例字体大小
annotate_font = FontProperties(size=17.6)     # 定义注释的字体属性（子图序号标签）
# 创建一个图
fig, axs = plt.subplots(1, 3, figsize=(14, 4))

# 子图a
for network in networks_a:
    network_df = df[df['network'] == network]
    degree = list(map(int, network_df['degree'].values[0].split(',')))
    degree_distr = list(map(float, network_df['degree_distr'].values[0].split(',')))
    axs[0].loglog(
        degree, degree_distr,
        # 散点形状
        marker=marker_dict[network],
        linestyle='None',
        label=network,
        # 覆盖顺序
        zorder=zorder_dict[network],
        # 散点大小设置
        markersize=markersize,
        # 散点透明度
        alpha=alpha_value,
        # 散点边宽度
        markeredgewidth=markeredgewidth_value,
        # 颜色设置
        color=color_map[network],
    )
axs[0].spines['top'].set_visible(False)
axs[0].spines['right'].set_visible(False)
axs[0].set_xlabel('$d$')
axs[0].set_ylabel('$P(d)$')
# axs[0].set_xlim(4, )
axs[0].legend(
    handlelength=1,  # 左边界与色块之间的宽度
    handletextpad=0.4,
)
axs[0].grid(color="#E8E8E8", linestyle="-.", linewidth=0.4, zorder=0)
axs[0].annotate('(a)', xy=(annotate_x, annotate_y), xycoords='axes fraction', ha='center', fontproperties=annotate_font)

# 子图b
for network in networks_b:
    network_df = df[df['network'] == network]
    degree = list(map(int, network_df['degree'].values[0].split(',')))
    degree_distr = list(map(float, network_df['degree_distr'].values[0].split(',')))
    axs[1].loglog(
        degree, degree_distr,
        # 散点形状
        marker=marker_dict[network],
        linestyle='None',
        label=network,
        # 覆盖顺序
        zorder=zorder_dict[network],
        # 散点大小设置
        markersize=markersize,
        # 散点透明度
        alpha=alpha_value,
        # 散点边宽度
        markeredgewidth=markeredgewidth_value,
        # 颜色设置
        color=color_map[network]
    )
axs[1].spines['top'].set_visible(False)
axs[1].spines['right'].set_visible(False)
axs[1].set_xlabel('$d$')
# axs[1].set_ylabel('P(k)')
# axs[1].set_xlim(4, )
axs[1].legend(
    handlelength=1, # 左边界与色块之间的宽度
    handletextpad=0.4,
)
axs[1].grid(color="#E8E8E8", linestyle="-.", linewidth=0.4, zorder=0)
axs[1].annotate('(b)', xy=(annotate_x, annotate_y), xycoords='axes fraction', ha='center', fontproperties=annotate_font)

# 子图c
for network in networks_c:
    network_df = df[df['network'] == network]
    degree = list(map(int, network_df['degree'].values[0].split(',')))
    degree_distr = list(map(float, network_df['degree_distr'].values[0].split(',')))
    axs[2].loglog(
        degree, degree_distr,
        # 散点形状
        marker=marker_dict[network],
        linestyle='None',
        label=network,
        # 覆盖顺序
        zorder=zorder_dict[network],
        # 散点大小设置
        markersize=markersize,
        # 散点透明度
        alpha=alpha_value,
        # 散点边宽度
        markeredgewidth=markeredgewidth_value,
        # 颜色设置
        color=color_map[network]
    )
axs[2].spines['top'].set_visible(False)
axs[2].spines['right'].set_visible(False)
axs[2].set_xlabel('$d$')
# axs[2].set_ylabel('P(k)')
axs[2].legend(
    handlelength=1,  # 左边界与色块之间的宽度
    handletextpad=0.4,
)
axs[2].grid(color="#E8E8E8", linestyle="-.", linewidth=0.4, zorder=0)
axs[2].annotate('(c)', xy=(annotate_x, annotate_y), xycoords='axes fraction', ha='center', fontproperties=annotate_font)


# 设置整个图形的标题
# fig.suptitle('The distribution function of connectivities')
plt.subplots_adjust(
    top=0.973,
    bottom=0.226,
    left=0.054,
    right=0.993,
    hspace=0.2,
    wspace=0.145
)
# 保存
plt.rcParams['pdf.fonttype'] = 42   # 解决保存pdf的报错问题
plt.savefig("D:\科研论文文稿\Paper_RL\图\Figs\Fig-PA-DD.pdf", format="pdf")
plt.savefig('D:\科研论文文稿\Paper_RL\图\Figs\Fig-PA-DD.svg', format='svg')
plt.show()





