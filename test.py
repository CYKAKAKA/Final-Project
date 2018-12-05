# import networkx as nx
# import pylab
# import numpy as np
# import matplotlib.pyplot as plt
#
#
#
#
# def mod_pert_random(low, likely, high, confidence=4, samples=10000):
#     """Produce random numbers according to the 'Modified PERT'
#     distribution.
#
#     :param low: The lowest value expected as possible.
#     :param likely: The 'most likely' value, statistically, the mode.
#     :param high: The highest value expected as possible.
#     :param confidence: This is typically called 'lambda' in literature
#                         about the Modified PERT distribution. The value
#                         4 here matches the standard PERT curve. Higher
#                         values indicate higher confidence in the mode.
#                         Currently allows values 1-18
#     :param samples: random number size
#
#     Formulas from "Modified Pert Simulation" by Paulo Buchsbaum.
#     """
#     # Check minimum & maximum confidence levels to allow:
#     if confidence < 1 or confidence > 18:
#         raise ValueError('confidence value must be in range 1-18.')
#
#     mean = (low + confidence * likely + high) / (confidence + 2)
#
#     a = (mean - low) / (high - low) * (confidence + 2)
#     b = ((confidence + 1) * high - low - confidence * likely) / (high - low)
#
#     beta = np.random.beta(a, b, samples)
#     beta = beta * (high - low) + low
#     return beta
#
#
#
# G = nx.grid_2d_graph(5,5)
#
# nx.draw(G)
# plt.show()
#
# position={1:(1,0),2:(2,0),3:(3,0),4:(4,0)}
# nx.draw(G,pos=position)

import networkx as nx
from pylab import show
import matplotlib.pyplot as plt
position={}
for i in range(25):
    G = nx.Graph()
    if i<24:
        G.add_node(i+1)
        G.add_edge(i+1,i+2)
# for i in range(25):
#     position[i+1]=(i,0)
# print(position)
# nx.draw(G,pos=position)
# plt.xlim(0,20)
# plt.ylim(0,20)
# plt.show()
nx.draw(G)
plt.show()
