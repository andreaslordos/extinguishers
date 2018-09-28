from util.distancetime import getDurationGMAPS
from random import uniform
from nodes.Node import Node

def calculate_score(nodes,hubs,api_key):
    '''
    Input: nodes, List, contains event nodes such as fire/crime events
           hubs, List, contains hubs such as fire stations/police stations
    Output: hub_score, Dictionary, a list of all hubs and their equivalent scores

    The lower the distance from hub to event and the higher the weight of the event,
    the higher the score of the hub!

    Score of hub = sum(weight_of_surrounding_events/((distance_to_event)^2))
    Objective needs to be to maximize hub score
    '''
    hub_score={}
    for hub in hubs:
        hub_score[hub]=0
    for node in nodes:
        if node.nearest_hub in hubs:
            source=str((node.nearest_hub).lat)+", "+str((node.nearest_hub).long)
            destination=str(node.lat)+", "+str(node.long)
            try:
                hub_score[node.nearest_hub]+=(node.weight/((node.getDistance(node.nearest_hub))**2))
            except Exception as e:
                #shouldn't be included in the score if you can't drive to it!
                pass
    total=0
    for hub in hub_score:
         total+=hub_score[hub]
    return total

def place_random_hubs(howManyHubs,minlat,maxlat,minlon,maxlon,number_to_try,existing_nodes,existing_hubs,api_key):
    '''
    Input: minlat, float, minimum latitude possible for randomly generated node
           maxlat, float, maximum latitude possible for randomly generated node
           minlon, float, minimum longitude possible for randomly generated node
           maxlon, float, maximum longitude possible for randomly generated node
           number_to_try, number of nodes to try a random walk on
           existing_nodes, Node, event nodes (e.g. fires) that already exist
           existing_hubs, Node, hub nodes (e.g. fire stations) that already exists
           api_key, String, api key for Google Maps API
    Output: best_hub, Node, a new hub node (generated from genNewNode()) that has
                            the highest score (generated from calculate_score())
                            out of number_to_try nodes that were generated
    '''
    def genNewNode():
        lat=uniform(minlat,maxlat) #determine new lat
        long=uniform(minlon,maxlon) #determine new long
        #print(lat,long)
        new_hub=Node(lat,long,"hub",0)
        return new_hub

    highscore=0
    best_hub=None
    new_score={}
    for x in range(number_to_try):
        new_hub=1
        new_score=0
        while new_score==0:
            new_hubs=[]
            for number_of_hubs in range(howManyHubs):
                new_hubs.append(genNewNode())
            total_hubs=new_hubs+existing_hubs
            for node in existing_nodes:
                node.determineNearestHub(total_hubs)
            new_score=calculate_score(existing_nodes,total_hubs,api_key)
        if new_score>highscore:
            best_hubs=new_hubs
            highscore=new_score
    return best_hubs
