# -*- coding: UTF-8 -*-
'''
@Project ：Paper_RL 
@File    ：Fig-DD.py
@IDE     ：PyCharm 
@Author  ：Vinne
@Date    ：2026/3/21 15:43 
@Explain ：
'''
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D

# ================== 全局字体与样式 ==================
config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)
plt.rcParams['font.sans-serif'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'   # ！数学符号也使用 Times New Roman

alpha_value = 0.95
markeredgewidth_value = 0.1
markersize = 6.2

# plt.rc('axes', titlesize=8)        # 子图标题字体
plt.rc('axes', labelsize=16)     # 坐标轴标签字体
plt.rc('xtick', labelsize=13)     # x 轴刻度字体
plt.rc('ytick', labelsize=13)     # y 轴刻度字体
plt.rc('legend', fontsize=9.4)       # 图例字体
annotate_font = FontProperties(size=16)  # 子图标签 (a)(b)(c) 字体

def get_label(index):
    result = ''
    while True:
        result = chr(97 + index % 26) + result
        index = index // 26 - 1
        if index < 0:
            break
    return f'({result})'

# ================== 读取真实网络信息（顺序、颜色、RL 指标） ==================
real_net_info = pd.read_excel("data/result/真实网络与计算结果.xlsx", sheet_name=0)
net_order = real_net_info['网络名称'].dropna().astype(str).tolist()
color_map = dict(zip(real_net_info['网络名称'].astype(str), real_net_info['颜色']))

# 三个指标配置：名称、CSV 路径、Excel 中 RL 列名、显示前缀
metrics = [
    {
        "name": "WD",
        "csv": "data/result/RLvsReal_WD.csv",
        "rl_col": "RL(WD)",
        "text_prefix": "WD"
    },
    {
        "name": "KS",
        "csv": "data/result/RLvsReal_KS.csv",
        "rl_col": "RL(KS)",
        "text_prefix": "KS"
    },
    {
        "name": "JS",
        "csv": "data/result/RLvsReal_JS.csv",
        "rl_col": "RL(JS)",
        "text_prefix": "JS"
    },
]

# 只画这三组网络
target_nets = ["LesMisérables", "HumanProteins1", "CitHepPh1"]

# ================== 创建 3×3 子图 ==================
nrows, ncols = 3, 3
fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 4.1, nrows * 2.9))

annotate_x = -0.14
annotate_y = 0.95

panel_idx = 0

for row_idx, metric in enumerate(metrics):
    # 读取对应指标的 CSV
    df_all = pd.read_csv(metric["csv"])
    # 为该指标构建 RL 映射
    emd_map = dict(zip(real_net_info['网络名称'].astype(str),
                       real_net_info[metric["rl_col"]]))

    for col_idx, real_name in enumerate(target_nets):
        ax = axes[row_idx, col_idx]

        # 找到真实网络行
        real_row = df_all[df_all['network'] == f"Real_{real_name}"]
        if real_row.empty:
            print(f"[警告] 未找到真实网络 Real_{real_name} 在 {metric['name']} 的 CSV 中")
            continue
        real_row = real_row.iloc[0]

        # 找到对应实验网络（假设命名为 Exp_{real_name}_r...）
        exp_rows = df_all[df_all['network'].str.contains(f"Exp_{real_name}_r")]
        if exp_rows.empty:
            print(f"[警告] 未找到实验网络 Exp_{real_name}_r* 在 {metric['name']} 的 CSV 中")
            continue
        exp_row = exp_rows.iloc[0]

        # 提取 r 值
        match = re.match(r"Exp_(.+?)_r(-?\d+(?:\.\d+)?)", exp_row['network'])
        r_val = match.group(2) if match else "*"

        exp_legend = f"Our (r={r_val})"
        real_legend = f"Real ({real_name})"

        # 解析度分布
        exp_deg = list(map(int, exp_row['degree'].split(',')))
        exp_distr = list(map(float, exp_row['degree_distr'].split(',')))
        real_deg = list(map(int, real_row['degree'].split(',')))
        real_distr = list(map(float, real_row['degree_distr'].split(',')))

        # 去除 0
        exp_k = [k for k, p in zip(exp_deg, exp_distr) if k > 0 and p > 0]
        exp_p = [p for k, p in zip(exp_deg, exp_distr) if k > 0 and p > 0]
        real_k = [k for k, p in zip(real_deg, real_distr) if k > 0 and p > 0]
        real_p = [p for k, p in zip(real_deg, real_distr) if k > 0 and p > 0]

        # 绘制散点
        ax.plot(exp_k, exp_p, 's', label=exp_legend, color="#124B7D",
                alpha=alpha_value, markersize=markersize,
                markeredgewidth=markeredgewidth_value)

        real_color = color_map.get(real_name, "#000000")
        ax.plot(real_k, real_p, 'o', label=real_legend, color=real_color,
                alpha=alpha_value, markersize=markersize,
                markeredgewidth=markeredgewidth_value)

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(color="#E8E8E8", linestyle="-.", zorder=0, linewidth=0.4)
        ax.xaxis.set_major_locator(plt.LogLocator(base=10.0, numticks=10))
        ax.yaxis.set_major_locator(plt.LogLocator(base=10.0, numticks=10))

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # 轴标签：只在最左列画 y，只在最底行画 x
        if col_idx == 0:
            ax.set_ylabel("$P(d)$")
        else:
            ax.set_ylabel("")
        if row_idx == nrows - 1:
            ax.set_xlabel("$d$", labelpad=5.5)
        else:
            ax.set_xlabel("")

        # 主图例（真实 vs 实验）
        main_legend = ax.legend(
            # bbox_to_anchor=(1.05, 0.99),
            handlelength=1,
            labelspacing=0.35,
            handletextpad=0.42,  # ← 关键：减少文字左边距
            borderpad=0.45,  # ← 控制框内边距
            loc='upper right',
            framealpha=0.45
        )
        ax.add_artist(main_legend)

        # 指标值图例（WD/KS/JS）
        emd_value = emd_map.get(real_name, None)
        if emd_value is not None and not pd.isna(emd_value):
            emd_text = f"{metric['text_prefix']} : {emd_value:.4f}"
        else:
            emd_text = f"{metric['text_prefix']}: N/A"
        emd_dummy = Line2D([], [], linestyle='none', marker='', label=emd_text)

        emd_legend = ax.legend([emd_dummy], [emd_text],
                               loc='lower left',
                               bbox_to_anchor=(0.015, 0.015),  # 左下角微调
                               handletextpad=0.0,  # ← 关键：减少文字左边距
                               borderpad=0.45,  # ← 控制框内边距
                               handlelength=0,
                               labelspacing=0.2,
                               framealpha=0.45
                               )

        # 子图标识 (a)...(i)
        label_str = get_label(panel_idx)
        panel_idx += 1
        ax.annotate(label_str, xy=(annotate_x, annotate_y),
                    xycoords='axes fraction',
                    ha='center', va='center',
                    fontproperties=annotate_font)

# 布局调整
plt.subplots_adjust(
    top=0.988,
    bottom=0.071,
    left=0.061,
    right=0.988,
    hspace=0.245,
    wspace=0.23
)

# 保存
plt.rcParams['pdf.fonttype'] = 42   # 解决保存pdf的报错问题
plt.savefig("D:\科研论文文稿\Paper_RL\图\Figs\Fig_DD.pdf", format="pdf")
plt.savefig('D:\科研论文文稿\Paper_RL\图\Figs\Fig_DD.svg', format='svg')
plt.show()


