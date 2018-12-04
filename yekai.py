import networkx as nx
import pylab
import numpy as np


def mod_pert_random(low, likely, high, confidence=4, samples=10000):
    """Produce random numbers according to the 'Modified PERT'
    distribution.

    :param low: The lowest value expected as possible.
    :param likely: The 'most likely' value, statistically, the mode.
    :param high: The highest value expected as possible.
    :param confidence: This is typically called 'lambda' in literature
                        about the Modified PERT distribution. The value
                        4 here matches the standard PERT curve. Higher
                        values indicate higher confidence in the mode.
                        Currently allows values 1-18
    :param samples: random number size

    Formulas from "Modified Pert Simulation" by Paulo Buchsbaum.
    """
    # Check minimum & maximum confidence levels to allow:
    if confidence < 1 or confidence > 18:
        raise ValueError('confidence value must be in range 1-18.')

    mean = (low + confidence * likely + high) / (confidence + 2)

    a = (mean - low) / (high - low) * (confidence + 2)
    b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta


def mapping(length, width):
    G = nx.grid_2d_graph(length, width)
    n = len(list(G.edges))
    for edge in list(range(n)):
        likely = np.random.randint(10, 20, 1)
        G.edges[G.edges[edge][0], G.edges[edge][1]]['time'] = np.mean(mod_pert_random(low=5, likely=likely, high=50, confidence=2))
    return G


# G = nx.DiGraph()
#
# for i in range(0, np.size(col) + 1):
#     G.add_node(i)
# print('在网络中添加带权中的边...')
# for i in range(np.size(row)):
#     G.add_weighted_edges_from([(row[i], col[i], value[i])])
#
# print('给网路设置布局...')
# pos = nx.shell_layout(G)
# print('画出网络图像：')
# nx.draw(G, pos, with_labels=True, node_color='white', edge_color='red', node_size=400, alpha=0.5)
# pylab.title('Self_Define Net', fontsize=15)
# pylab.show()
#
# '''
# Shortest Path with dijkstra_path
# '''
# print('dijkstra方法寻找最短路径：')
# path = nx.dijkstra_path(G, source=0, target=7)
# print('节点0到7的路径：', path)
# print('dijkstra方法寻找最短距离：')
# distance = nx.dijkstra_path_length(G, source=0, target=7)
# print('节点0到7的距离为：', distance)
