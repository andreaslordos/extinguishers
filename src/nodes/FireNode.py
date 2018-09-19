from nodes.Node import Node
#from utils import calculate_pop_density
class FireNode(Node):
    def __init__(self,lat,long,type,pop,acq_date,confidence,frp):
        super().__init__(lat,long,type,pop)
        self.acq_date=acq_date
        self.confidence=confidence
        self.frp=frp
        self.severity=1

    def calculateWeight(self, maxSeverity, maxFRP,maxPopDensity):
        severity_score=int(self.severity/maxSeverity*100)
        frp_score=int(self.frp/maxFRP*100)
        #pop_density=calculate_pop_density(self.lat,self.long,pop)
        #pop_density_score=int(self.pop/maxPopDensity*100)
        pop_density_score=50

        if self.confidence=="l":
            c_score=33
        elif self.confidence=="h":
            c_score=100
        else:
            c_score=67
        self.weight = (severity_score+frp_score+pop_density_score+c_score)/4
