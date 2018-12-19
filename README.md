# 590PR Final_Project

# Title: 
Delivery Service Monte Carlo Simulation

## Team Member(s): 
Yekai Chen, Xiner Liu, Yue Xian

## Responsibilities:
Yue Xian: Developing the major part of scenario #2
Yekai Chen: Developing the most part in scenario1, brainstorming for scenario2 and warpping up.

# Monte Carlo Simulation Scenario & Purpose: 

For a resturant, it's increasingly necessary to have a delivery service. But the time of delivery time is hard to predict thus it's also hard to make management decision according to it. In this Monte Carlo Simulation, we'd like to help the manager to make decisions in two certain scenarios.

In our scenarios, we assume that the restaurant is at the center of a gird. The nodes in the grid represent the possible customer locations and the edges between nodes represent the roads with the weights representing the travel time.

In the restaurant, there are three different sizes of food (small, medium, large). Each is of different price and different preparation time.

- Scenario 1: 
  - One order is ready to be delivered and another order comes in right now. In what locations of the new order we should wait for preparation of the food and deliver these two together or deliver the ready order right now and then come back for the new?
  
- Scenario 2: 
  - The restaurant would receive a fixed number of orders throughout a day(8:00 am to 8:00 pm, 12 hours).
  - If the delivery time is more than 90 minutes, customers would cancel the order.
  - Profit = Total order revenue - number of the delivery man x 15(dollars/hour) x 12 (hours).
  - Therefore, how many delivery men should be employed to reach the highest profit, and what is the relationship between the profit and  the success order rate.

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
  - The further from restaurant the new order is, the more likely to wait. 
  - The further from the previous order the new order is, the more likely to deliver now.
  
- Scenario 2:
  - As the number of delivery men increases, the successful delivery rate will increase, so as the profit. However, after a certain number, the successful delivery rate will be stable, and the profit will start to drop.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

- Scenario 1: 

  The decision depends on the distance from the new order to the previous order more than the distance between the restaurant and the new order. If the location of the new order is closer to the previous order, it's more time-saving to wait and deliver them together. 
  
- Scenario 2:

  Based on the average number of orders a restaurant might receive a day, a manager of the restaurant could decide the number of delivery man they should hire to maximize the profit. In this case, we assume the total number of order is 100 and according to the results, we could conclude that this restaurant should employ 4 delivery men.
  
  Also, as our hypothesis, as the number of delivery men increases, the successful delivery rate will increase at first, then become stable. The profit will thus generally increase at first, reach the peak, then decrease.
  
  During the simulation, we find that if the road condition is too bad, which means it will take a long time to deliver, the stable successful delivery rate will be really low. This is because the travel time between the restaurant and the customer location is already more than 90 minutes and therefore no matter how many delivery men there are, the order cannot be delivered in time.
  
  
## Instructions on how to use the program:
### Only Scenario1.py and Scenario2.py are executable. 
- Scenario1.py:
  Input 'the map scale', 'number of orders are waiting' and 'the previous order location'. Then the program will form a panda DataFrame that includes the probability of wait and deliver now for each node on the map. 
  
- Scenario2.py:
  Input 'the map scale' and 'the number of order per day'. Then the program will form a panda DataFrame that indicates different number of delivery men, the profit and the order successful rate.
### Other files descriptions
- Function.py: Module used in these two programs. 
- IS590PR Final Presentation.pptx: Powerpoint file used in class progress presentation.
- Scenario 1 & 2 Visualization.ipynb: Visualizatoin work for result outputs.
- Weather.ipynb: Data analysis from Champaign weather historic data.


## All Sources Used:

1. Weather Data: https://www.isws.illinois.edu/statecli/urbana/urbana-monthly-2017.htm
2. NetworkX: https://networkx.github.io/documentation/stable/tutorial.html
3. BQPlot: https://bqplot.readthedocs.io/en/latest/
