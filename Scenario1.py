"""
Scenerio#1
One order is ready to be delivered and another order come in right now. In what locations of the new customer
we should wait for preparation of the food and deliver these two together or deliver the ready order right now
and then come back for the new?
"""


import Functions as fun
import networkx as nx
import numpy as np
import pandas as pd


def deliver_wait_time(queue_count) -> float:
    """
    Return the wait time of the deliver man for this specific order
    :param queue_count: The number of orders which is before this order
    :return: Certain wait time for this order

    >>> time = deliver_wait_time(10)
    >>> print(type(time))
    <class 'numpy.float64'>
    """
    # Check the type of queue_count
    if type(queue_count) is not int:
        raise ValueError('queue_count must be integer')
    wait_time = 0
    order_size = ['S', 'M', 'L']
    for i in range(queue_count + 1):
        # Set a random order size for each order
        order_num = np.random.randint(0, 3)
        preparation_time = fun.prep_time(order_size[order_num])
        number = np.random.randint(0, len(preparation_time))
        # Calculate total wait time
        wait_time += preparation_time[number]
    return wait_time


def judgement(mapgrid: nx.classes.graph.Graph, coordinate: tuple, new_delivery_point: tuple, queue_count: int,
              previous_order_location: tuple) -> dict:
    """
    Depending on the time that cost on wait and traffic to new delivery point, this function tells if we should wait
    for the second order and deliver together or deliver the first order now and then come back for the second
    :param mapgrid: Generated grid with restaurant location
    :param coordinate: The location of restaurant, i.e.:(2,2)
    :param new_delivery_point: Randomly generated location on grid, i,e,(3,2)
    :param queue_count:The number of orders which is before this order
    :param previous_order_location: Last order location, i.e.(1,1)
    :return: 'W'ait or leave 'N'ow

    >>> new_map = fun.real_map(fun.mapping(5,5))
    >>> judge = judgement(new_map,(2,2),(3,2),1,(1,1))
    >>> judge[(3,2)] in ['W','N']
    True
    """
    try:
        # This is the time from restaurant to new location
        new_time = nx.dijkstra_path_length(mapgrid, source=coordinate, target=new_delivery_point, weight='time') \
                   + fun.weather_effect()
        # This is the time from restaurant to previous location
        previous_time = nx.dijkstra_path_length(mapgrid, source=coordinate, target=previous_order_location, weight='time') \
                        + fun.weather_effect()
        # This is the time between two locations
        time_two_destination = nx.dijkstra_path_length(mapgrid, source=previous_order_location, target=new_delivery_point,
                                                       weight='time') + fun.weather_effect()
    except TypeError:
        print('parameter types are wrong ')
    else:
        if (new_time + previous_time) * 2 > \
                deliver_wait_time(queue_count) + new_time + time_two_destination + previous_time:
            return {new_delivery_point: 'W'}  # for 'wait'
        else:
            return {new_delivery_point: 'N'}  # for 'now'


def monte_carlo_scenario1(grid_length, grid_width, queue_number, previous_location: tuple) -> pd.DataFrame:
    """
    This function is to apply Monte Carlo Method to simulate scenario 1 with 1000 repeat times.
    The parameters here are mutable according to real needs.
    :param grid_length: The length of the map
    :param grid_width: The width of the map
    :param queue_number: The number of orders which is before this order
    :param previous_loc: Previous location, i.e. (1,1)
    :return: A dataframe which contains all possible locations of the new order and times and percentages
    for wait or now

    >>> result =  monte_carlo_scenario1(5, 5, 1, (1,1))
    >>> result.columns
    Index(['location', 'Wait', 'Now', 'Wait_percentage', 'Now_percentage'], dtype='object')
    """
    location_list = []
    decision_list = []
    restaurant_loc = (int(grid_length / 2), int(grid_width / 2))
    new_map = fun.mapping(grid_length, grid_width)
    # Repeat for 1000 times
    for repeat in range(1000):
        new_map = fun.real_map(new_map)
        # Test each node in the map
        for nodes in list(new_map.nodes()):
            for location, decision in judgement(new_map, restaurant_loc, nodes, queue_number,
                                                previous_location).items():
                location_list.append(location)
                decision_list.append(decision)
    result = pd.DataFrame({'location': location_list, 'decision': decision_list})
    temp = result.groupby('location')['decision'].sum().reset_index()
    list_now = []
    list_wait = []
    for i in list(range(grid_length * grid_width)):
        number_now = temp['decision'][i].count('N')
        number_wait = temp['decision'][i].count('W')
        list_now.append(number_now)
        list_wait.append(number_wait)
    result = pd.DataFrame({'location': list(temp['location']), 'Wait': list_wait, 'Now': list_now})
    result['Wait_percentage'] = result['Wait'] / 1000
    result['Now_percentage'] = result['Now'] / 1000
    return result


if __name__ == '__main__':
    # Check the input type
    while True:
        try:
            grid_length = int(input('Please input the length of the grid:\n'))
            grid_width = int(input('Please input the width of the grid:\n'))
            queue_number = int(input('Please input the number of orders in line:\n'))
        except ValueError:
            print('Length, width and orders in line must all be integers')
        else:
            break
    while True:
        previous_loc = input('Please input previous order location: (i.e. 1,1)\n')
        try:
            x, y = int(previous_loc.split(',')[0]), int(previous_loc.split(',')[1])
            previous_location = (x, y)
        except ValueError:
            print('Previous order location must be like 1,1')
        except IndexError:
            print('Previous order location must be like 1,1')
        else:
            break
    # Get the result
    scenario1_result = monte_carlo_scenario1(grid_length, grid_width, queue_number, previous_location)
    print(scenario1_result)
