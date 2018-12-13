import networkx as nx
import random
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
        order_size (int): 1 stands for small; 2 stands for medium and 3 stands for large.
        preparation_time (double): The time need for preparation
        order_location (tuple): The coordinate of the location of the order
        delivery_time (double): The time spend on the way to destination
        supposed_delivered_time(int): The time when the order should be delivered
        delivered_time (double): The time when the order arrives
        status (string): to define whether the order is cancelled
        delivery_man_number (int): The job number of delivery man who delivers the order

    """

    def __init__(self, time, order_size, preparation_time=0, order_location=(1, 1), delivery_time=0,
                 supposed_delivered_time=0, order_delivered_time=0, status=0, delivery_man_number=0):

        """
        The constructor for ComplexNumber class.

        Parameters:
            time (int): The time when the restaurant receive an order.
            order_size (int): 1 stands for small; 2 stands for medium and 3 stands for large.
            preparation_time (double): The time need for preparation
            order_location (tuple): The coordinate of the location of the order
            delivery_time (double): The time spend on the way to destination
            supposed_delivered_time(int): The time when the order should be delivered
            order_delivered_time (double): The time when the order arrives
            status (string): to define whether the order is cancelled
            delivery_man_number (int): The job number of delivery man who delivers the order
        """
        self.time = time
        self.order_size = order_size
        self.preparation_time = preparation_time
        self.order_location = order_location
        self.delivery_man_number = delivery_man_number
        self.delivered_time = order_delivered_time
        self.delivery_time = delivery_time
        self.supposed_delivered_time = supposed_delivered_time
        self.status = status

    def set_preparation_time(self):
        """
        The function is to set the preparation time for an Order

        """
        self.preparation_time = 10
        if self.order_size == 1:
            pass
        elif self.order_size == 2:
            self.preparation_time *= 1.5
        else:
            self.preparation_time *= 2

    def set_order_location(self, x, y):
        """
        The function is to set the order location for an Order

        Parameters:
           x (int)：the x coordinate of order location
           y (int): the y coordinate of order location
        """

        self.order_location = (int(x), int(y))

    def set_delivery_time(self, restaurant_location, mapgrid):
        """
        The function is to set the delivery time for an Order

        Parameters:
           restaurant_location (int)：the coordinate of the restaurant
           mapgrid (int): the map
        """
        self.delivery_time = nx.dijkstra_path_length(mapgrid, source=restaurant_location, target=self.order_location,
                                                     weight='time')

    def set_supposed_delivered_time(self):
        """
        The function is to set the supposed delivered time for an Order

        """
        self.supposed_delivered_time = self.time + 90

    def set_delivered_time(self, order_delivered_time):

        self.delivered_time = order_delivered_time

    def set_status(self):
        """
        The function is to set status for an Order

        Parameters:

        """
        if self.delivered_time < self.supposed_delivered_time:
            self.status = 'processing'
        else:
            self.status = 'cancelled'

    def set_mark(self, delivery_man_number):
        """
        The function is to set mark for an Order

        Parameters:
            delivery_man_number (int): the job number of a delivery man
        """

        self.delivery_man_number = delivery_man_number


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

    def set_arrived_time(self, order_delivered_time, delivery_time):
        """
        The function is to set mark for an Order

        Parameters:
            order_delivered_time (int): The time when his last order is delivered
            delivery_time (int): The time he spend on his way back to the restaurant
        """
        self.arrived_time = order_delivered_time + delivery_time


if __name__ == '__main__':
    grid_length = int(input('Please input the length of the grid:\n'))
    grid_width = int(input('Please input the width of the grid:\n'))
    order_quantity = int(input('Please input the how many orders can be received from 8am to 8pm per day:\n'))
    order = []
    new_map = real_map(mapping(grid_length, grid_width))
    map_size = len(list(real_map(mapping(grid_length, grid_width)).nodes))
    profit_dic = {}
    successful_dic = {}
    restaurant_loc = (int(grid_length / 2), int(grid_width / 2))  # set restaurant location
    for k in [1, 2, 3, 4, 5]:
        revenue_list = []
        cost = k * 15 * 12
        successful_list = []
        for repeat in range(1000):
            number = sorted(random.sample(range(1, 720 + 1), order_quantity))
            revenue = 0
            successful_times = 0
            for i in range(order_quantity):
                size = random.sample(range(1, 4), 1)[0]
                x_coordinate = np.random.randint(0, grid_length, size=1)
                y_coordinate = np.random.randint(0, grid_width, size=1)
                # order_location_index  is used to select a random node from the real_map
                order_location_index = random.sample(range(map_size), 1)[0]
                order.append(Order(number[i], size))
                order[i].set_preparation_time()
                order[i].set_order_location(x_coordinate, y_coordinate)
                order[i].set_delivery_time(restaurant_loc, new_map)
                order[i].set_supposed_delivered_time()
            delivery_team = []
            delivery_man_time_list = []
            # (2)stands for the number of delivery man
            # create objects
            for i in range(k):
                delivery_team.append(DeliveryMan(i + 1))
            for i in range(order_quantity):
                if i <= k - 1:
                    delivered_time = order[i].time + order[i].preparation_time + order[i].delivery_time + 0
                    order[i].set_delivered_time(delivered_time)
                    delivery_team[i].set_arrived_time(order[i].delivered_time, order[i].delivery_time)
                    order[i].set_mark(i + 1)
                    delivery_man_time_list.append(delivery_team[i].arrived_time)
                if i > k:
                    mark = delivery_man_time_list.index(min(delivery_man_time_list))
                    arrived_time_of_delivery_man = delivery_team[mark].arrived_time
                    if arrived_time_of_delivery_man < order[i].time + order[i].preparation_time:

                        delivered_time = order[i].time + order[i].preparation_time + order[i].delivery_time
                    else:
                        delivered_time = arrived_time_of_delivery_man + order[i].delivery_time

                    order[i].set_status()
                    order[i].set_delivered_time(delivered_time)

                    if order[i].status == 'processing':
                        arrived_time_of_delivery_man = delivered_time + order[i].delivery_time
                        order[i].set_mark(mark + 1)

                    else:
                        for j in range(i)[::-1]:
                            if order[j].status == 'processing':
                                arrived_time_of_delivery_man = order[j].delivered_time + order[j].delivery_time
                                break
                    delivery_team[mark].arrived_time = arrived_time_of_delivery_man
                    delivery_man_time_list[mark] = delivery_team[mark].arrived_time
                # for i in range(100):
                if order[i].status == 'processing':
                    successful_times += 1
                    if order[i].order_size == 1:
                        revenue += 10
                    if order[i].order_size == 2:
                        revenue += 20
                    if order[i].order_size == 3:
                        revenue += 30
                else:
                    continue
            revenue_list.append(revenue)
            successful_list.append(successful_times)
        successful_dic[k] = np.mean(successful_list) / order_quantity
        profit_dic[k] = np.mean(revenue_list) - cost
    print(profit_dic)
    print(successful_dic)
