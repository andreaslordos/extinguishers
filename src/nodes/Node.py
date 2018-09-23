import math

class Node:
    #Abstract class for all nodes
    def __init__(self,lat,long,type,popDens):
        types=("event","hub")
        if type not in types:
            raise TypeError
        self.type=type
        self.lat=lat
        self.long=long
        self.populationDistribution=popDens
        self.weight=0
        self.nearest_hub=None


    def getLat(self):
        return self.lat

    def getLong(self):
        return self.long

    def getDistance(self,target_node):
        '''
        Input: target_node, Node, node to calculate distance to
        Output: d, float, distance to node in meters
        '''
        lat1, lon1 = self.getLat(),self.getLong()
        lat2, lon2 = target_node.lat,target_node.long
        radius = 6371 # km radius of earth

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return d

    def calculateWeight(self):
        raise NotImplementedError

    def getNearestX(self,x,listOfNodes):
        '''
        Input: x, Integer, number of nearest nodes to retrieve
               listOfNodes, List, list of nodes on the map
        Output: nearest, List, list of nearest X nodes
                copyList, List, list of all nodes - nearest
        '''
        distances=[]
        distances_to_nodes={}
        copyOfList=listOfNodes[:]
        original_len=len(copyOfList)
        while 0<len(copyOfList):
            node=copyOfList[0]
            distance_from_new_node=self.getDistance(node)
            distances.append(self.getDistance(node))
            copyOfList.remove(node)
            try:
                distances_to_nodes[distance_from_new_node].append(node)
            except:
                distances_to_nodes[distance_from_new_node]=[node]
        distances.sort()
        #print(distances)
        nearest=[]
        for number in distances[:x]:
            nearest+=distances_to_nodes[number]
        nearest=nearest[:x]
        #print(copyOfList)
        return nearest,copyOfList

    def determineNearestHub(self,listOfNodes):
        '''
        Input: listOfNodes, List, list of all nodes in hub
        Output: None
        Sets self.nearest_hub to the nearest hub of this node.
        '''
        lowest=9999999999999999
        nearest=None
        for node in listOfNodes:
            distance=self.getDistance(node)
            if distance<lowest:
                lowest=distance
                nearest=node
        self.nearest_hub=nearest
