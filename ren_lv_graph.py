# -*- coding: UTF-8 -*-
'''
@Project ：Paper_RL
@File    ：ren_lv_graph.py
@IDE     ：PyCharm 
@Author  ：Jinhu Ren
@Date    ：2025/4/28 14:27 
@Explain ：Core Code of Ren-Lü (RL) Vari-Linear Network Generation Model
'''
import random
import numpy as np
import networkx as nx


def ren_lv_graph(n, k, r, n0=3, seed=None):
    """
    Returns a Ren-Lü vari-linear graph (network).

    A graph of "n" nodes is grown by attaching new nodes, each with the number of edges connected follows an exponential
    probability governed by "k", and the existing nodes these edges connect to are determined by a variable linear
    preference controlled by "r".

    Parameters
    ----------
    n : int
        Set the number of nodes in the output graph.
    k : float
        Set the expected value of global average degree in the output graph.
    r : float
        Set the Control parameters for variable linear preferential attachment.
    n0 : int (3 default)
        Number of nodes in the initial complete graph created.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See [Randomness](https://networkx.org/documentation/stable/reference/randomness.html#randomness).

    Returns
    -------
    G : Graph

    Raises
    ------
    NetworkXError
        If `n<1`, or the `n0` does not satisfy `>= 1 and < n`, or the `initial_graph` number of nodes does not satisfy
        `>= 1 and < n`, or the `k` not satisfy `> 2`.

    References
    ----------
    Universal Network Generation Model via Exponential Probabilistic Growth and Vari-linear Preferential Attachment,
    Jinhu Ren, Linyuan Lü (https://arxiv.org/abs/2510.23041)
    """

    if n < 1:
        return print("Parameter n Setting Error !")
    if n0 < 1 or n0 >= n:
        return print("Parameter n0 Setting Error !")
    if not np.isfinite(k) or k <= 2:
        raise ValueError(f"Parameter k Setting Error !")

    # Initialize the random seed.
    # 初始化随机种子
    np.random.seed(seed)
    random.seed(seed)

    # Initialize a complete graph containing n0 nodes.
    # 初始化一个包含 n0 个节点的完全图
    G = nx.complete_graph(n0)
    # Use a list to store the degree of each node (indexed by node).
    # 使用列表存储每个节点的度数（按节点索引），初始空图每个节点的度为 n0-1
    degree_list = [n0 - 1] * n0
    initial_nodes_number = n0

    # Pre-compute the number of connections for all new nodes, following a discrete exponential distribution.
    # 预先生成所有新节点的连接边数，遵循离散指数分布
    # Parameter λ of the exponential distribution
    # 指数分布参数 λ
    lambda_value = -np.log(1 - 2.0 / k)
    # Sampling from a continuous exponential distribution and discretization.
    # 连续指数分布采样并离散化
    x_raw = np.random.exponential(scale=1.0 / lambda_value,
                                  size=n - initial_nodes_number)
    m_values_raw = np.floor(x_raw).astype(int) + 1

    # Limit the number of new nodes m_i to no more than the current number of available nodes (i.e., when adding the i-th new node, the existing number of nodes is i + initial_nodes_number).
    # 限制每个新节点的 m_i 不超过当前可选的节点数（即添加第 i 个新节点时，已有节点数为 i+initial_nodes_number）
    m_values = [int(min(m, i + 1)) for i, m in enumerate(m_values_raw)]

    # Network Evolution and Iteration
    # 网络演进与迭代
    for i, new_node in enumerate(range(initial_nodes_number, n)):

        # Add a new node.
        # 添加新节点
        G.add_node(new_node)

        # Calculate the adjusted priority connection probability based on the current degree of all nodes (stored in degree_list).
        # 根据当前所有节点的度（由 degree_list 保存）计算修正的优先连接概率
        weights = [float(d) ** r for d in degree_list]
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]

        # Weight-based sampling of m_i target nodes from the existing nodes (0 to len(degree_list)-1) (sampling without replacement).
        # 从当前已有节点（0 ~ len(degree_list)-1）中加权采样 m_i 个目标节点（不放回采样）
        m_i = m_values[i]

        # Form a set of target nodes for connection
        # 形成连接目标节点集
        targets = np.random.choice(len(degree_list), size=m_i, replace=False, p=probabilities)

        # Establish an edge between the new node and the target node, and update the degree of the target node.
        # 建立新节点与目标节点之间的边，并更新目标节点的度数
        for t in targets:
            G.add_edge(new_node, t)
            degree_list[t] += 1

        # Degree of the new node is denoted as m_i.
        # 新节点的度数记作 m_i
        degree_list.append(m_i)

        # Print progress information (printed approximately every 0.1% of new nodes generated).
        # 打印进度信息（每生成约0.1%新节点时打印一次）
        if new_node % max(1, n // 1000) == 0 or new_node == n - 1:
            progress = (new_node + 1) / n * 100
            print(f"\rGenerating: {new_node + 1}/{n} ({progress:.1f}%)", end="", flush=True)
    print("\r" + " " * 50 + "\r", end="", flush=True)

    return G


if __name__ == '__main__':

    # Test
    # 测试
    G = ren_lv_graph(n=2000, k=6, r=0.8, seed=None)

    print("\n" + "=" * 65)
    print("     Ren–Lü (RL) Vari-Linear Network Generation Completed !")
    print("=" * 65)

    print("Net Info:")
    num_nodes = G.number_of_nodes()
    print(f"Nodes: {num_nodes}")
    num_edges = G.number_of_edges()
    print(f"Edges: {num_edges}")
    avg_degree = 2 * num_edges / num_nodes
    print(f"Average degree: {avg_degree:.4f}")
    clustering = nx.average_clustering(G)
    print(f"Average clustering coefficient: {clustering:.4f}")
    if not nx.is_connected(G):
        G_lcc = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    else:
        G_lcc = G
    avg_path_length = nx.average_shortest_path_length(G_lcc)
    print(f"Average path length: {avg_path_length:.4f}")
    diameter = nx.diameter(G_lcc)
    print(f"Diameter: {diameter}")

    print("=" * 65)








