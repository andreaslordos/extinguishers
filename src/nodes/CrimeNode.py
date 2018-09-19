from nodes.Node import Node

class CrimeNode(Node):
    def __init__(self,lat,long):
        super().__init__(lat,long)

    def calculateWeight(self):
        '''
        Need to calculate weight
        '''
