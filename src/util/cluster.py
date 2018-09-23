from nodes.Node import Node

class Cluster:
    '''
    A cluster is a group of X nodes. The self.cluster_mean attribute means a
    cluster can also act as a node. All the nodes in the cluster are contained
    in self.nodes_in_cluster
    '''
    def __init__(self):
        self.nodes_in_cluster=[]
        self.cluster_mean=Node(0,0,"event",0)

    def form_cluster(self,starting_node,x,incident_nodes):
        '''
        Input: starting_node, Node, initial node to base off all measurements
               x, Integer, number of nodes per cluster
               incident_nodes, List, a list of all remaining nodes that are not
                                     yet in a cluster.
        Output: nextOne, Node, starting_node for the next cluster to be formed
                incident_nodes, List, list of remaining nodes to be used for next
                                      cluster
        Takes starting_node, finds x+1 nearest nodes to starting node. Last node
        found is the starting_node for the next cluster to be formed.
        '''
        nearest=starting_node.getNearestX(x+1,incident_nodes)
        nextOne=nearest[-1]
        (self.nodes_in_cluster)=nearest[:-1]
        self.calculate_mean_location()
        self.calculateWeight()
        return nextOne, incident_nodes

    def calculate_mean_location(self):
        '''
        Calculates the mean location of the cluster_mean (Node) by averaging lat/
        long of all nodes in the cluster.
        TODO: Factor in weight when calculating average location.
        '''
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
        '''
        Calculates weight of cluster_mean (Node) which is calculated by averaging
        all weights in the nodes_in_cluster
        '''
        sum_weight=0
        for node in self.nodes_in_cluster:
            sum_weight+=node.weight
        (self.cluster_mean).weight=sum_weight/len(self.nodes_in_cluster)
