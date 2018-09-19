from nodes.Node import Node

class IncidentNode(Node):
    def __init__(self,lat,long,type,popDist):
        super().__init__(lat,long)

    def calculateWeight(self):
        '''
        Need to calculate weight
        '''
