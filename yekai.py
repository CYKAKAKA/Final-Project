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
    '''
    With designated length and width, this function generate a length x width grid. And define the middle point as
    the location of restaurant.

    :param length: The number of nodes vertically
    :param width: The number of nodes horizontally
    :return: A NetworkX 2D gird graph
    '''
    G = nx.grid_2d_graph(length, width)
    for edge in list(G.edges):
        low = np.random.randint(1, 10)
        high = np.random.randint(low + 1, 30)
        likely = np.random.randint(low, high)
        G.edges[edge[0], edge[1]]['time'] = np.mean(mod_pert_random(low, likely, high, confidence=2))
    G.nodes[int(length / 2), int(width / 2)]['name'] = 'RESTAURANT'
    return G


def prep_time(order_size):
    """
    Return the preparation time for the order based on its size
    :param size: size for the order
    :return: preparation time
    """
    prep_time = np.random.uniform(0, 10, size=100)
    if order_size == "S":
        return prep_time
    elif order_size == "M":
        return prep_time * 1.5
    else:
        return prep_time * 2


def deliver_wait_time():
    """
    Return the wait time of the deliver man for this specific order
    :param: none
    :return: wait time
    """
    wait_time = 0
    # When the order arrives, the total orders in the queue,maximum 10
    queue_count = np.random.randint(0, 11)
    order_size = ['S', 'M', 'L']
    for i in range(queue_count + 1):
        order_num = np.random.randint(0, 3)
        preparation_time = prep_time(order_size[order_num])
        number = np.random.randint(0, len(preparation_time))
        wait_time += preparation_time[number]
    return wait_time


def judgement(mapgrid, delivery_point):
    """
    Depend on the time that cost on wait and traffic to new delivery point, this function tells if we should wait or
    leave now

    :param mapgrid: Made grid with restaurant location
    :param delivery_point: Randomly generated location on grid
    :return: 'W'ait or leave 'N'ow
    """
    for location, name in nx.get_node_attributes(mapgrid, 'name').items():
        if name == 'RESTAURANT':
            coordinate = location
    time = nx.dijkstra_path_length(mapgrid, source=coordinate, target=delivery_point)
    if time * 2 > deliver_wait_time():
        return {delivery_point: 'W'}  # for 'wait'
    else:
        return {delivery_point: 'N'}  # for 'now'


if __name__ == '__main__':
    new_map = mapping(100, 100)
    print((judgement(new_map, (2, 3))))

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
