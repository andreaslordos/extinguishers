# The Extinguisher Project

Empower governments to determine weaknesses in emergency response systems using historical data and Machine Learning.

### What

Visualization software to analyze current emergency-response hubs (e.g. fire stations, police stations, hospitals) and events related to the hubs (e.g. for fire stations that would be fires; for police stations, that would be car accidents and crime). 

Extinguisher then suggests locations for new emergency-response hubs so as to optimize the emergency response system.


### How

Step 1: Extinguisher plots historical data on an interactive map of the country using lat/long coordinates. Red dots are fires that occured in the past decade, while blue dots are fire stations. This data is collected via NASA's MODIS and VIIRS satellites.

![plots](https://i.imgur.com/XVVZ9og.png)

Step 2: Then, Extinguisher uses a clustering algorithm that takes into account the weight of each fire, it's importance, severity, confidence etc. in order to determine the mean location of a cluster. Mean locations are seen as grey dots below.

![clusters](https://i.imgur.com/Pc3qefy.png)

Step 3: Extinguisher then tries to determine the optimal location for a new fire station by trying to maximize the Total Score of the emergency response centers by using this equation:

![Equation](https://i.imgur.com/Juuretv.gif)

Essentially, when it's scoring a potential emergency response center location, the score is the sum of the weight of each cluster node divided by it's distance squared from the potential emergency response center location. Basically, the higher the weight of nodes a potential location affects the better, but the higher the distance of nodes from a potential location the worse.

Extinguisher attempts to optimize the sum of scores of all emergency response centers using the above equation.

Author: Andreas Lordos, 18 (andreasglordos@gmail.com)
