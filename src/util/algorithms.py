from util.distancetime import getDurationGMAPS
from random import randint
from nodes.Node import Node

def calculate_score(nodes,hubs):
    '''
    The lower the distance from hub to event and the higher the weight of the event,
    the higher the score of the hub!

    Score of hub = sum(weight_of_surrounding_events/((distance_to_event)^2))
    '''
    hub_score={}
    for hub in hubs:
        hub_score[hub]=0
    print(hub_score)
    for node in nodes:
        if node.nearest_hub in hubs:
            source=str((node.nearest_hub).lat)+", "+str((node.nearest_hub).long)
            destination=str(node.lat)+", "+str(node.long)
            print("Node weight:",node.weight)
            print("Source:",source)
            print("Destination:",destination)
            print("Nearest hub:",node.nearest_hub)
            try:
                hub_score[node.nearest_hub]+=(node.weight/((getDurationGMAPS(source,destination))**2))
            except Exception as e:
                print("Warning")
                hub_score[node.nearest_hub]+=(node.weight/((node.nearest_hub).getDistance(node))**2)
    return hub_score

def place_random_hubs(minlat,maxlat,minlon,maxlon,number_to_try,existing_nodes,existing_hubs):

    def genNewNode():
        minlat,maxlat=347,351
        minlon,maxlon=323,340
        lat=randint(minlat,maxlat)/10 #determine new lat
        long=randint(minlon,maxlon)/10 #determine new long
        print(lat,long)
        new_hub=Node(lat,long,"hub",0)
        return new_hub

    highscore=0
    best_hub=None
    new_score={}
    for x in range(number_to_try):
        new_hub=1
        new_score[new_hub]=0
        while new_score[new_hub]==0:
            new_hub=genNewNode()
            total_hubs=[new_hub]+existing_hubs
            for node in existing_nodes:
                node.determineNearestHub(total_hubs)
            new_score=calculate_score(existing_nodes,[new_hub])
        if new_score[new_hub]>highscore:
            best_hub=new_hub
            highscore=new_score[new_hub]
    return best_hub
