"""
This module is our functions which are used in both scenarios.
For generating the map, we use networkx to create a grid and assume it to be the neighborhood, whose center
is the restaurant. Each node in the grid represents possible location of order and weight for each edge is
the time to travel.
Also, we consider weather influence. According to data from Champaign last year(2017), we calculate the
possibilities of rain,snow and too cold. With the possibilities, we will be able to add extra time to the
base deliver time because of the bad weather.
Moreover, we take the preparation time into consideration. We assume that there are three different types
of dishes and all apply to normal distribution.
"""
import networkx as nx
import numpy as np


def mod_pert_random(low, likely, high, confidence=4, samples=10000) -> np.ndarray:
    """Produce random numbers according to the 'Modified PERT' distribution.

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

    >>> beta = mod_pert_random(2,4,6)
    >>> print(len(beta))
    10000
    """
    # Check minimum & maximum confidence levels to allow:
    if confidence < 1 or confidence > 18:
        raise ValueError('confidence value must be in range 1-18.')
    # Check the relationship between the parameters.
    if low >= high:
        raise ValueError('low value should not be more than high value')
    if likely < low or likely > high:
        raise ValueError('likely value should be between low value and high value')

    mean = (low + confidence * likely + high) / (confidence + 2)

    a = (mean - low) / (high - low) * (confidence + 2)
    b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta


def mapping(length, width) -> nx.classes.graph.Graph:
    """
    With designated length and width, this function generate a length x width grid and
    assign each edge a low, likely and high weight. The function also define the middle
    point as the location of restaurant.

    :param length: The number of nodes vertically
    :param width: The number of nodes horizontally
    :return: A NetworkX 2D gird graph

    >>> g = mapping(4,4)
    >>> print(len(list(g)))
    16
    """

    # Check if the length and width are not normal
    if length <= 0 or width <= 0:
        raise ValueError('The length and the width of the grid must not be below 0')
    g = nx.grid_2d_graph(length, width)
    # Assign each edge with low, high and likely value
    for edge in list(g.edges):
        low = np.random.randint(1, 10)
        high = np.random.randint(low + 1, 30)
        likely = np.random.randint(low, high)
        g.edges[edge[0], edge[1]]['low'] = low
        g.edges[edge[0], edge[1]]['high'] = high
        g.edges[edge[0], edge[1]]['likely'] = likely
    g.nodes[int(length / 2), int(width / 2)]['name'] = 'RESTAURANT'
    return g


def real_map(g) -> nx.classes.graph.Graph:
    """
    With the generated graph, this function assign a real-time weight, which represents travel time according to
    the 'Modified PERT' distribution.

    :param g: the generated graph
    :return: the new graph with travel time at this moment

    >>> g = real_map(mapping(4,4))
    >>> print(type(g.edges[(0,0),(1,0)]['time']))
    numpy.float64
    """
    # Check the type of g
    if type(g) != 'nx.classes.graph.Graph':
        raise ValueError('The input is not a nx.classes.graph.Graph')
    # Assign the real-time weight to each edge
    for edge in list(g.edges):
        low = g.edges[edge[0], edge[1]]['low']
        high = g.edges[edge[0], edge[1]]['high']
        likely = g.edges[edge[0], edge[1]]['likely']
        distribution = mod_pert_random(low, likely, high, confidence=2)
        number = np.random.randint(0, len(distribution))
        g.edges[edge[0], edge[1]]['time'] = distribution[number]
    return g


def weather_effect():
    """
    With the data analysis before, the possibilities of different weather conditions are calculated.
    Therefore, the weather is assigned according to the possibilities, and the effect of weather
    is evaluated to extra time.

    :return: extra time depending on the weather

    >>> extra_time = weather_effect()
    >>> print(type(extra_time))
    int
    """

    # These are results of data analysis from weather data of Champaign in 2017
    possible_rain_types = np.random.multinomial(100, [0.109589, 0.112329, 0.208219, 0.569863])
    possible_snow_types = np.random.multinomial(100, [0.010959, 0.041096, 0.019178, 0.928767])
    rain_type = ['HR', 'LR', 'MR', 'NR']
    snow_type = ['HS', 'LS', 'MS', 'NS']
    rain_list, snow_list = [], []
    for i in list(range(len(possible_rain_types))):
        rain_list += [rain_type[i]] * possible_rain_types[i]
    for i in list(range(len(possible_snow_types))):
        snow_list += [snow_type[i]] * possible_snow_types[i]
    too_cold_list = np.random.binomial(1, 0.027397, 100)
    pick = int(np.random.randint(0, 100, 1))
    rain_effect = rain_list[pick]
    snow_effect = snow_list[pick]
    too_cold_effect = int(too_cold_list[pick])
    effect_result = 0
    # According to different weather, we will add extra time to the total time
    if rain_effect == 'HR':
        effect_result += 15
    elif rain_effect == 'LR':
        effect_result += 5
    elif rain_effect == 'MR':
        effect_result += 10
    if snow_effect == 'HS':
        effect_result += 20
    elif snow_effect == 'LS':
        effect_result += 10
    elif snow_effect == 'MS':
        effect_result += 15
    if too_cold_effect == 1:
        effect_result += 5
    return effect_result


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


