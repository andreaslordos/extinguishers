# extinguisher

Visualization software to analyze current emergency-response hubs (e.g. fire stations, police stations, hospitals) and events related to the hubs (e.g. for fire stations that would be fires; for police stations, that would be car accidents and crime). This repository empowers both national and local governments to determine the weak spots in any emergency response system based on historical data and graph theory.

Step 1: Extinguisher plots historical data on an interactive map of the country using lat/long coordinates. Red dots are fires that occured in the past 3 years, blue dots are fire stations.

![plots](https://i.imgur.com/XVVZ9og.png)

Step 2: Then, Extinguisher uses a clustering algorithm we wrote that takes into account the weight of each fire, it's importance, severity, confidence etc. in order to determine the mean location of a cluster. Mean locations are seen as grey dots below.

![clusters](https://i.imgur.com/Pc3qefy.png)

Step 3: Extinguisher then tries to determine the optimal location for a new fire station by trying to maximize the Total Score of the emergency response centers by using this equation:

![Equation](https://i.imgur.com/Juuretv.gif)

Essentially, when it's scoring a potential emergency response center location, the score is the sum of the weight of each cluster node divided by it's distance squared from the potential emergency response center location. Basically, the higher the weight of nodes a potential location affects the better, but the higher the distance of nodes from a potential location the worse.

Extinguisher attempts to optimize the sum of scores of all emergency response centers using the above equation.

Authors: Andreas Lordos, 17 (andreasglordos@gmail.com)
