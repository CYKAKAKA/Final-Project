import networkx as nx
import random
import pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


class Order:
    """

    This is a class for order definition.

    Attributes:
        time (int): The time when the restaurant receive an order.
        size (int): 1 stands for small; 2 stands for medium and 3 stands for large.
        preparation_time (double): The time need for preparation
        order_location (tuple): The coordinate of the location of the order
        delivery_time (double): The time spend on the way to destination
        supposed_delivered_time(int): The time when the order should be delivered
        delivered_time (double): The time when the order arrives
        status (string): to define whether the order is cancelled
        mark (int): The job number of delivery man who delivers the order

    """

    def __init__(self, time, size, preparation_time=0, order_location=(0, 1), delivery_time=0,
                 supposed_delivered_time=0, delivered_time=0, status=0, mark=0):

        """
        The constructor for ComplexNumber class.

        Parameters:
            time (int): The time when the restaurant receive an order.
            size (int): 1 stands for small; 2 stands for medium and 3 stands for large.
            preparation_time (double): The time need for preparation
            order_location (tuple): The coordinate of the location of the order
            delivery_time (double): The time spend on the way to destination
            supposed_delivered_time(int): The time when the order should be delivered
            delivered_time (double): The time when the order arrives
            status (string): to define whether the order is cancelled
            mark (int): The job number of delivery man who delivers the order
        """
        self.time = time
        self.size = size
        self.preparation_time = preparation_time
        self.order_location = order_location
        self.mark = mark
        self.delivered_time = delivered_time
        self.delivery_time = delivery_time
        self.supposed_delivered_time = supposed_delivered_time
        self.status = status

    def set_preparation_time(self):
        """
        The function is to set the preparation time for an Order

        """
        self.preparation_time = 10
        if self.size == 1:
            pass
        elif self.size == 2:
            self.preparation_time *= 1.5
        else:
            self.preparation_time *= 2

    def set_order_location(self, length, width, i):
        """
        The function is to set the order location for an Order

        Parameters:
           length (int)：the length of the map
           width (int): the width of the map
           i: a randomly generated number
        """

        order_location = list(real_map(mapping(length, width)).nodes)[i]

        self.order_location = order_location

    def set_delivery_time(self, restaurant_loc, mapgrid):
        """
        The function is to set the delivery time for an Order

        Parameters:
           restaurant_loc (int)：the coordinate of the restaurant
           mapgrid (int): the map
        """

        delivery_time = nx.dijkstra_path_length(mapgrid, source=restaurant_loc, target=self.order_location,
                                                weight='time')

        self.delivery_time = delivery_time

    def set_supposed_delivered_time(self):
        """
        The function is to set the supposed delivered time for an Order

        """

        supposed_delivered_time = self.time + 100

        self.supposed_delivered_time = supposed_delivered_time

    def set_delivered_time(self, delivered_time):

        self.delivered_time = delivered_time

    def set_status(self):
        """
        The function is to set status for an Order

        Parameters:

        """

        if self.delivered_time < self.supposed_delivered_time:
            self.status = 'processing'
        else:
            self.status = 'cancelled'

    def set_mark(self, mark):
        """
        The function is to set mark for an Order

        Parameters:
            mark (int): the job number of a delivery man
        """

        self.mark = mark


class DeliveryMan:
    """

        This is a class for delivery man definition.

        Attributes:
            job_number (int): The time when the restaurant receive an order.
            arrived_time( double): The time when a delivery man return to the restaurant

    """

    def __init__(self, job_number, arrived_time=0):
        """
        The constructor for ComplexNumber class.

        Parameters:
            job_number (int): The time when the restaurant receive an order.
            arrived_time( double): The time when a delivery man return to the restaurant

        """
        self.job_number = job_number
        self.arrived_time = arrived_time

    def set_arrived_time(self, delivered_time, delivery_time):
        """
        The function is to set mark for an Order

        Parameters:
            delivered_time (int): The time when his last order is delivered
            delivery_time (int): The time he spend on his way back to the restaurant
        """
        self.arrived_time = delivered_time + delivery_time


if __name__ == '__main__':
    A = 1
    B = 720  # 8:00 am to 8 :00pm
    COUNT = 100  # total order number
    resultList = random.sample(range(A, B + 1), COUNT)
    order = []
    number = sorted(resultList)
    new_map = real_map(mapping(2, 2))
    map_size = len(list(real_map(mapping(2, 2)).nodes))

    # define the location of a resturant
    restaurant_loc = (int(2 / 2), int(2 / 2))

    for i in range(100):
        size = random.sample(range(1, 4), 1)[0]
        # order_location_index  is used to select a random node from the real_map
        order_location_index = random.sample(range(map_size), 1)[0]

        order.append(Order(number[i], size))

        order[i].set_preparation_time()
        order[i].set_order_location(2, 2, order_location_index)
        order[i].set_delivery_time(restaurant_loc, new_map)
        order[i].set_supposed_delivered_time()

    k = 3
    delivery_team = []
    delivery_man_timelist = []
    # (2)stands for the number of delivery man
    # create objects
    for i in range(k):
        delivery_team.append(DeliveryMan(i + 1))

    for i in range(100):
        if i <= k - 1:
            delivered_time = order[i].time + order[i].preparation_time + order[i].delivery_time + 0
            order[i].set_delivered_time(delivered_time)
            delivery_team[i].set_arrived_time(order[i].delivered_time, order[i].delivery_time)
            order[i].set_mark(i + 1)
            delivery_man_timelist.append(delivery_team[i].arrived_time)
        if i >= k:
            mark = delivery_man_timelist.index(min(delivery_man_timelist))
            #         print(mark)
            #         if delivery_team[0].arrived_time >= delivery_team[1].arrived_time:
            #             mark = 1

            #         else:
            #             mark = 0
            arrived_time_of_deliverman = delivery_team[mark].arrived_time
            if arrived_time_of_deliverman < order[i].time + order[i].preparation_time:

                delivered_time = order[i].time + order[i].preparation_time + order[i].delivery_time
            else:
                delivered_time = arrived_time_of_deliverman + order[i].delivery_time

            order[i].set_status()
            order[i].set_delivered_time(delivered_time)

            if order[i].status == 'processing':
                arrived_time_of_deliverman = delivered_time + order[i].delivery_time
                order[i].set_mark(mark + 1)

            else:
                for k in range(i)[::-1]:
                    if order[k].status == 'processing':
                        arrived_time_of_deliverman = order[k].delivered_time + order[k].delivery_time
                        break
            delivery_team[mark].arrived_time = arrived_time_of_deliverman
            delivery_man_timelist[mark] = delivery_team[mark].arrived_time
    status_list = []
    time_list = []
    delivered_list = []
    supposed_list = []
    mark_list = []
    for i in range(100):
        status_list.append(order[i].status)
        delivered_list.append(order[i].delivered_time)
        supposed_list.append(order[i].supposed_delivered_time)
        time_list.append(order[i].time)
        mark_list.append(order[i].mark)

    result = pd.DataFrame(
        {'time': time_list, 'delivered': delivered_list, 'supposed': supposed_list, 'status': status_list,
         'delivery_man': mark_list})
    print(result)