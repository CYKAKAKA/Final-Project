import networkx as nx
import pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
    """
    With designated length and width, this function generate a length x width grid. And define the middle point as
    the location of restaurant.

    :param length: The number of nodes vertically
    :param width: The number of nodes horizontally
    :return: A NetworkX 2D gird graph
    """
    G = nx.grid_2d_graph(length, width)
    for edge in list(G.edges):
        low = np.random.randint(1, 10)
        high = np.random.randint(low + 1, 30)
        likely = np.random.randint(low, high)
        G.edges[edge[0], edge[1]]['low'] = low
        G.edges[edge[0], edge[1]]['high'] = high
        G.edges[edge[0], edge[1]]['likely'] = likely
    G.nodes[int(length / 2), int(width / 2)]['name'] = 'RESTAURANT'
    return G


def real_map(G):
    for edge in list(G.edges):
        low = G.edges[edge[0], edge[1]]['low']
        high = G.edges[edge[0], edge[1]]['high']
        likely = G.edges[edge[0], edge[1]]['likely']
        distribution = mod_pert_random(low, likely, high, confidence=2)
        number = np.random.randint(0, len(distribution))
        G.edges[edge[0], edge[1]]['time'] = distribution[number]
    return G


def prep_time(order_size):
    """
    Return the preparation time for the order based on its size
    :param order_size: size for the order
    :return: preparation time
    """
    preparation_time = np.random.uniform(0, 10, size=100)
    if order_size == "S":
        return preparation_time
    elif order_size == "M":
        return preparation_time * 1.5
    else:
        return preparation_time * 2


def deliver_wait_time(queue_count):
    """
    Return the wait time of the deliver man for this specific order
    :param: none
    :return: wait time
    """
    wait_time = 0
    # When the order arrives, the total orders in the queue,maximum 10
    order_size = ['S', 'M', 'L']
    for i in range(queue_count + 1):
        order_num = np.random.randint(0, 3)
        preparation_time = prep_time(order_size[order_num])
        number = np.random.randint(0, len(preparation_time))
        wait_time += preparation_time[number]
    return wait_time


def judgement(mapgrid, coordinate, new_delivery_point, queue_count, previous_order_location):
    """
    Depend on the time that cost on wait and traffic to new delivery point, this function tells if we should wait or
    leave now
    :param mapgrid: Made grid with restaurant location
    :param coordinate: The location of restaurant
    :param new_delivery_point: Randomly generated location on grid
    :param queue_count:how many orders are waiting to be prepared when the new order arrives
    :param previous_order_location: last order location
    :return: 'W'ait or leave 'N'ow
    """
    # coordinate = (0, 0)
    # for restaurant_location, name in nx.get_node_attributes(mapgrid, 'name').items():
    #     if name == 'RESTAURANT':
    #         coordinate = restaurant_location
    new_time = nx.dijkstra_path_length(mapgrid, source=coordinate, target=new_delivery_point, weight='time')
    previous_time = nx.dijkstra_path_length(mapgrid, source=coordinate, target=previous_order_location, weight='time')
    time_two_destination = nx.dijkstra_path_length(mapgrid, source=previous_order_location, target=new_delivery_point,
                                                   weight='time')
    if (new_time + previous_time) * 2 > deliver_wait_time(queue_count) + new_time + time_two_destination + previous_time:
        return {new_delivery_point: 'W'}  # for 'wait'
    else:
        return {new_delivery_point: 'N'}  # for 'now'


if __name__ == '__main__':
    location_list = []
    decision_list = []
    grid_length = int(input('Please input the length of the grid:\n'))
    grid_width = int(input('Please input the width of the grid:\n'))
    queue_number = int(input('Please input the number of orders in line:\n'))
    previous_loc = input('Please input previous order location: (i.e. 1,1)\n')
    x, y = int(previous_loc.split(',')[0]), int(previous_loc.split(',')[1])
    previous_location = (x, y)
    restaurant_loc = (int(grid_length/2), int(grid_width/2))
    for repeat in range(1000):
        new_map = mapping(grid_length, grid_width)
        for nodes in list(new_map.nodes()):
            for location, decision in judgement(new_map, restaurant_loc, nodes, queue_number, previous_location).items():
                location_list.append(location)
                decision_list.append(decision)
    result = pd.DataFrame({'location': location_list, 'decision': decision_list})
    temp = result.groupby('location')['decision'].sum().reset_index()
    list_N = []
    list_W = []
    for i in list(range(grid_length * grid_width)):
        n_N = temp['decision'][i].count('N')
        n_W = temp['decision'][i].count('W')
        list_N.append(n_N)
        list_W.append(n_W)
    result = pd.DataFrame({'location': list(temp['location']), 'Wait': list_W, 'Now': list_N})
    result['Wait_percentage'] = result['Wait'] / 1000
    result['Now_percentage'] = result['Now'] / 1000
    print(result)
