"""
Scenario#2
The restaurant would receive a fixed number of orders through out a day (8:00 am to 8:00 pm, 12 hours).
If the delivery time is more than 90 minutes, customer would cancel the order.
Profit = Total order revenue - number of the delivery man x 15(dollars/hour) x12 (hours)
Therefore, how many delivery man should be employed to reach the highest profit, and what is the
relationship between the profit and the success order rate.
"""


import networkx as nx
import random
import numpy as np
import Functions as fun
import pandas as pd


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
        self.preparation_time = random.choice(np.random.uniform(0, 10, size=1000))
        # 1 means small order, 2 means medium oder, else means large order
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
        The function is to set the supposed delivered time for an order

        """
        # Customer will wait for no more than 90 minutes, then will cancel the order
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
    while True:
        try:
            grid_length = int(input('Please input the length of the grid:\n'))
            grid_width = int(input('Please input the width of the grid:\n'))
            order_quantity = int(input('Please input the how many orders can be received from 8am to 8pm per day:\n'))
        except ValueError:
            print('Length, width and orders number must all be integers')
        else:
            break
    order = []
    new_map = fun.real_map(fun.mapping(grid_length, grid_width))
    map_size = len(list(new_map.nodes))
    profit_dic = {}
    successful_dic = {}
    # Set restaurant location
    restaurant_loc = (int(grid_length / 2), int(grid_width / 2))
    # The number of delivery man
    for k in [1, 2, 3, 4, 5, 6, 7, 8]:
        revenue_list = []
        # Cost = the number of delivery man x 15 (dollars/hour) x 12 (working hours)
        cost = k * 15 * 12
        successful_list = []
        # Repeat 1000 times
        for repeat in range(1000):
            # Assume the orders will equally come at any time during the working 12 hours (720 minutes)
            number = sorted(random.sample(range(1, 720 + 1), order_quantity))
            revenue = 0
            successful_times = 0
            for i in range(order_quantity):
                # Randomly set the order size
                size = random.sample(range(1, 4), 1)[0]
                # Randomly set the order location
                x_coordinate = np.random.randint(0, grid_length, size=1)
                y_coordinate = np.random.randint(0, grid_width, size=1)
                order.append(Order(number[i], size))
                order[i].set_preparation_time()
                order[i].set_order_location(x_coordinate, y_coordinate)
                order[i].set_delivery_time(restaurant_loc, new_map)
                order[i].set_supposed_delivered_time()
            delivery_team = []
            delivery_man_time_list = []
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

                if order[i].status == 'processing':
                    successful_times += 1
                    # Set different revenue to different size of orders
                    if order[i].order_size == 1:
                        revenue += 15
                    if order[i].order_size == 2:
                        revenue += 20
                    if order[i].order_size == 3:
                        revenue += 25
                else:
                    continue
            revenue_list.append(revenue)
            successful_list.append(successful_times)
        successful_dic[k] = np.mean(successful_list) / order_quantity
        profit_dic[k] = np.mean(revenue_list) - cost
    result = pd.DataFrame([profit_dic, successful_dic]).T.reset_index()
    result.columns = ['delivery man number', 'profit', 'success rate']
    print(result)
