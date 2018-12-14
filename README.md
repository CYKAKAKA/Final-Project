# 590PR Final_Project

# Title: 
Delivery Service Monte Carlo Simulation

## Team Member(s): 
Yekai Chen, Xiner Liu, Yue Xian

# Monte Carlo Simulation Scenario & Purpose: 
For a resturant, it's increasingly necessary to have a delivery service. But the time of delivery time is hard to predict thus it's also hard to make management decision according to it. In this Monte Carlo Simulation, we'd like to help the manager to make decisions in two certain scenarios.
- Scenario 1: 
  One order is ready to be delivered and another order come in right now. In what locations of the new customer we should wait for preparation of the food and deliver these two together or deliver the ready order right now and then come back for the new?
- Scenario 2: 
  The restaurant would receive a fixed number of orders throughout a day (8:00 am to 8:00 pm, 12 hours).
If the delivery time is more than 90 minutes, customer would cancel the order.
Profit = Total order revenue - number of the delivery man x 15(dollars/hour) x12 (hours).
Therefore, how many delivery men should be employed to reach the highest profit, and what is the relationship between the profit and the success order rate.

## Simulation's variables of uncertainty
- Scenario 1:
  - The location of the new order
  - The location of the previous order
  - Weather impact on traffic
  - Traffic condition on roads
  - Preparation time for one order
- Scenario 2:
  - The location of delivery destination 
  - Traffic condition on roads
  - Preparation time for one order
  - Total orders per day
  - Number of delivery men
  
## Hypothesis or hypotheses before running the simulation:
- Scenario 1:
  - The further from resturant the new order is, the more likely to wait. 
  - The further from the previous order is, the more likely to deliver now.
- Scenario 2:
  - As the number of delivery men increases, the successful delivery rate will increase, so as the profit. However, after a certain number, the successful delivery rate will be stable, and the profit will start to drop.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
- Scenario 1: 
  The decision depend on the distance from new order to previous order more than the one between restaurant and new order. If the location of new order is closer to the previous order, it's more likely to wait and deliver them together. 
- Scenario 2:
  Based on the average number of orders a restaurant might receive a day, a manager of the restaurant could decide the number of delivery man they should hire to maximize profit. In this case, we assume the total number of order is 100 and according to the results, we could conclude that this restaurant should employ 4 delivery men.
  
## Instructions on how to use the program:
- Scenario 1:
  Input the map scale, number of orders are waiting and the previous order location. Then the program will form a panda DataFrame that includes the probability of wait and deliver now for each node on the map. 
- Scenario 2:
  Input the map scale and the number of order per day. Then the program will form a panda DataFrame that indicates different number of delivery men, the profit and the order successful rate.

## All Sources Used:
1. Weather Data: https://www.isws.illinois.edu/statecli/urbana/urbana-monthly-2017.htm
2. NetworkX: https://networkx.github.io/documentation/stable/tutorial.html
3. BQPlot: https://bqplot.readthedocs.io/en/latest/
