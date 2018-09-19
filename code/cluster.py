from Node import Node

class Cluster:
    def __init__(self):
        self.nodes_in_cluster=[]
        self.cluster_mean=Node(0,0,"event",0)

    def form_cluster(self,starting_node,x,incident_nodes):
        nearest=starting_node.getNearestX(x+1,incident_nodes)
        nextOne=nearest[-1]
        (self.nodes_in_cluster)=nearest[:-1]
        self.calculate_mean_location()
        self.calculateWeight()
        return nextOne, incident_nodes

    def calculate_mean_location(self):
        cumulative_lat,cumulative_long=0,0
        self.nodes_in_cluster=self.nodes_in_cluster[0]
        for node in self.nodes_in_cluster:
            #print(node)
            cumulative_lat+=node.lat
            cumulative_long+=node.long
        average_lat=cumulative_lat/len(self.nodes_in_cluster)
        average_long=cumulative_long/len(self.nodes_in_cluster)
        (self.cluster_mean).lat,(self.cluster_mean).long=average_lat,average_long

    def calculateWeight(self):
        sum_weight=0
        for node in self.nodes_in_cluster:
            sum_weight+=node.weight
        (self.cluster_mean).weight=sum_weight/len(self.nodes_in_cluster)
