# 590PR Final_Project

# Title: 
Delivery Service Monte Carlo Simulation

## Team Member(s): 
Yekai Chen, Xiner Liu, Yue Xian

# Monte Carlo Simulation Scenario & Purpose: 
For a resturant, it's increasingly necessary to have delivery service. But the time of order time is hard to predict thus it's also hard to make management decision on deliver or wait. In this Monte Carlo Simulation, we'd like to help the manager to make such decision.
- Scenario 1: One order is ready to be delivered and another order come in right now. In what condition of the locations of custmers we shoud wait and deliver these two together or deliver it right now and then come back for the other?
- Scenario 2: The restaurant would receive a fixed number of orders thorougout a day (8:00 am to 8:00 pm). How many delivery man should be employed to attain a trade-off between the cost of employemnt and the ratio of cancellation. (Customer would cancell the order within x minutes) 

## Simulation's variables of uncertainty
- The location of delivery destination 
- Weather impact on traffic
- Traffic condition on roads

## Hypothesis or hypotheses before running the simulation:
- The futher from resturant the new order is, the more likely to wait. 

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
- Scenario 1: 
The decision depend on the distance from new order to previous order more than the one between restaurant and new order. If the location of new order is closer to the previous order, it's the more likely to wait and deliver them together. 
- Scenario 2:
Based on the average number of  order a restaurant might receive a day, a manager of the restaurant could decdide the number of delivery man they should hire to maximize profit. In this case, we assume the total number of order is 100 and according to the results, we could conclude that this restaurant should employ 3 delivery men.
## Instructions on how to use the program:
- Scenario 1:
Input the map scale, number of orders are waiting and the previous order location. Then the program will form a panda DataFrame that includes the probability of wait and deliver now for each node on the map. 
- Scenario 2:
Input the map scale and the number of order per day. Then the program will form a dicionary that indicates the profit and order successful rate for different number of delivery men.

## All Sources Used:
1. Weather Data: https://www.isws.illinois.edu/statecli/urbana/urbana-monthly-2017.htm
2. NetworkX: https://networkx.github.io/documentation/stable/tutorial.html
3. BQPlot: https://bqplot.readthedocs.io/en/latest/
