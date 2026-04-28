# Experimental Code for the Ren-L&uuml; (RL) Vari-linear Network Generation Model



The code necessary to reproduce the main figures and statistical analyses in the research on Ren-L&uuml; vari-linear network generation model.



------

## Core Code: ren_l&uuml;_graph.py

##### ren_l&uuml;_graph(n, k, r, n0=3, seed=None) 

Return a Ren-L&uuml; vari-linear graph (network). A graph of `n`nodes is grown by attaching new nodes, each with the number of edges connected follows an exponential probability governed by `k`, and the existing nodes these edges connect to are determined by a variable linear preference controlled by `r`.

##### **Parameters**

**n : int** Set the number of nodes in the output graph.

**k : float** Set the number of nodes in the output graph.

**r : float** Set the expected value of global average degree in the output graph.

**n0 : int (3 default)** Set the Control parameters for variable linear preferential attachment.

**seed : integer, random_state, or None (default)** Indicator of random number generation state. See [Randomness](https://networkx.org/documentation/stable/reference/randomness.html#randomness).

##### **Returns**

**G : Graph**

##### **Raises**

**NetworkXError**: If `n<1`, or the `m0` does not satisfy `>= 1 and < n`, or the `initial_graph` number of nodes does not satisfy `>= 1 and < n`, or the `k` not satisfy `> 2`.



------



## Experiment Code

Fig-NS.py : Comparison of the similarity between RL model results and the real network;

<!-- Fig-NS.py：RL模型结果与真实网络之间的相似性对比 -->

Fig-DD.py : Comparison of degree distributions between RL model results and the real network (three data sets shown; see Fig-DD-WD.py, Fig-DD-KS.py, and Fig-DD-JS.py for the full data comparison);

<!-- Fig-DD.py：RL模型结果与真实网络之间的度分布对比（三组数据的示例，完整数据对比见Fig-DD-WD.py，Fig-DD-KS.py和Fig-DD-JS.py） -->

Fig-CN.py : Comprehensive Analysis of the RL Model’s Coverage of the Classic Features Represented by Traditional Network Models;

<!-- Fig-CN.py：RL模型对传统网络模型所代表的经典特征的涵盖性的对比 -->

Fig-AE.py : Comparison of Ablation Experiments for RL Model;

<!-- Fig-AE.py：RL模型的消融实验对比 -->

Fig-PA-3D.py : Analysis of the basic attributes for the RL model's output network;

<!-- Fig-PA-3D.py：RL模型的结果网络基本属性分析 -->

Fig-PA-DD.py : Analysis of the degree distribution for the RL model's output network;

<!-- Fig-PA-DD.py：RL模型的结果网络度分布分析 -->

Fig-DD-WD.py : Comparison of degree distributions between RL model results and the real network (Wasserstein Distance metric);

<!-- Fig-DD-WD.py：RL模型结果与真实网络之间的度分布对比（Wasserstein Distance指标） -->

Fig-DD-KS.py : Comparison of degree distributions between RL model results and the real network (Kolmogorov-Smirnov metric);

<!-- Fig-DD-KS.py：RL模型结果与真实网络之间的度分布对比（Kolmogorov-Smirnov指标） -->

Fig-DD-JS.py : Comparison of degree distributions between RL model results and the real network (Jensen-Shannon metric).

<!-- Fig-DD-JS.py：RL模型结果与真实网络之间的度分布对比（Jensen-Shannon指标） -->

