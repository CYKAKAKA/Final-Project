import numpy as np
import random


def generalLocatiob(total_number_of_node,n,map):
    """Produce random location of orders

      :param total_number_of_node: the total number of nodes in the map
      :param map: The graph generated from networkX
      :param map: number of orders appear at that time
      """
    # a = np.random.randint(0, total_number_of_node, n)
    a = random.sample(range(total_number_of_node),n)
    Location=[]
    for i in a:
        Location.append(list(map.nodes)[i])
    return Location
