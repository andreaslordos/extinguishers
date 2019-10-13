import os, sys, json
from pathlib import Path

#To do: break it up into communities, find optimal fire station for each
#community
COUNTRY="cyprus"
NUMBER_OF_NEW=2 #Number of hubs to place
#Add paths to everything important for future reference
PATH_TO_SRC=os.path.dirname(os.path.abspath(__file__))
PATH_TO_UTIL=(Path(PATH_TO_SRC)).__str__()+"\\util"
PATH_TO_NODES=(Path(PATH_TO_SRC)).__str__()+"\\nodes"
PATH_TO_SAVE=(Path(PATH_TO_SRC).parent).__str__()+"\\saves"
PATH_TO_DATA=(Path(PATH_TO_SRC).parent).__str__()+"\\data\\"+COUNTRY
PATH_TO_SHP=Path(PATH_TO_DATA).__str__()+"\\shapefiles"
PATH_TO_ARCHIVES=Path(PATH_TO_DATA).__str__()+"\\emergencies"
PATH_TO_HUBS=Path(PATH_TO_DATA).__str__()+"\\hubs"

TRIALS=1000 #number of trials to run (e.g., how many potential hub locations to try?)

sys.path.insert(0, PATH_TO_NODES) #add nodes folder to path to be able to import
sys.path.insert(0, PATH_TO_UTIL) #add util folder to path to be able to import

from gmplot import gmplot
from nodes.FireNode import FireNode
from util.cluster import Cluster
from util.utils import removeDuplicates
from nodes.Node import Node
from util.algorithms import calculate_score
from util.algorithms import place_random_hubs

def loadEvents(PATH_TO_DATA,archiveName):
    '''
    Input: PATH_TO_DATA, String, defines path to events/incidents
           archiveName, String, the name of the .json file containing the events/incidents
    Output: event_dict, list, contains Dictionary of each event (each dictionary contains lat/long)
    '''
    os.chdir(PATH_TO_DATA)
    with open(archiveName, 'r') as f:
        event_dict = json.load(f)
    f.close()
    return event_dict


def plotAndSave(nodes,colors,gmap,filename="saved.html",sizes=[400,1600]):
    '''
    Input: nodes, List, list contains zipped tuples of multiple nodes each
           colors, List, defines colors for nodes in each zipped tuples in nodes
           gmap, GoogleMapPlotter, map object to write to
           filename, String, what filename to save to,
           sizes, List, default sizes for each zipped tuple
    Output: None
    '''
    if len(nodes)!=len(colors):
        print("Erorr")
        return

    for x in range(len(nodes)):
        gmap.scatter(nodes[x][0],nodes[x][1],colors[x],size=sizes[x],marker=False)
    gmap.draw(PATH_TO_SAVE+"\\"+filename)


def getApiKey(PATH_TO_SRC):
    '''
    Input: PATH_TO_SRC, String, contains path to SRC directory
    Gets api key from config.txt file
    '''
    os.chdir("..")
    config_file=open("config.txt","r")
    contents=config_file.read()
    lines=contents.split("\n")
    api_key=lines[0].split("=")[-1]
    config_file.close()
    os.chdir(PATH_TO_SRC)
    return api_key

def loadHubs(path):
    '''
    Input: path, String, path to hub data
    Output: hubs, List, list of hubs as nodes
            hubs_coords, List, list of tuples containing just hub lat/longs
    Loads hub locations in lat/long
    '''
    f=open(path+"\\hubs.txt","r")
    content=f.read().split("\n")
    data=[]
    for x in range(len(content)):
        temp_list=content[x].split(", ")
        if len(temp_list[0])>2:
            data.append((float(temp_list[0]),float(temp_list[1])))
    hubs=[]
    hubs_coords=[]
    for hub in data:
        hubs.append(Node(hub[0],hub[1],"hub",0))
        hubs_coords.append((hub[0],hub[1]))
    return hubs, hubs_coords



hubs,hubs_coords=loadHubs(PATH_TO_HUBS)
hub_nodes=hubs[:]

api_key=getApiKey(PATH_TO_SRC)

MAX_FRP=160.8
MAX_SEV=62
MAX_POP_DENSITY=0
archiveName="emergencies.json"
archive_dict = loadEvents(PATH_TO_ARCHIVES,archiveName)

os.chdir(PATH_TO_SRC)

incidentList=[]
incident_nodes=[]
for event in archive_dict: #each e is another event
    incident_nodes.append(FireNode(event["latitude"],event["longitude"],"event",0,event["acq_date"],event["confidence"],event["frp"]))
    incident_nodes[-1].calculateWeight(MAX_SEV,MAX_FRP,MAX_POP_DENSITY)
    incidentList.append((event["latitude"],event["longitude"]))

SIZE_OF_CLUSTER=5
mean_cluster_nodes=[]
cluster_means=[]
incident_nodes=removeDuplicates(incident_nodes)
copy_incident_nodes=incident_nodes[:] # for testing
next_one=incident_nodes[-1]
sizes=[]
mean_nodes=[]
while len(incident_nodes)>=SIZE_OF_CLUSTER:
    genesis_cluster=Cluster()
    next_one,incident_nodes=genesis_cluster.form_cluster(incident_nodes[-1],SIZE_OF_CLUSTER,incident_nodes)
    cluster_nodes=[]
    for node in genesis_cluster.nodes_in_cluster:
        cluster_nodes.append((node.lat,node.long))
        try:
            incident_nodes.remove(node)
            #print("Removing")
        except Exception as e:
            print(str(e))
            pass
    mean_nodes.append(genesis_cluster.cluster_mean)
    mean_cluster_nodes.append(((genesis_cluster.cluster_mean).lat,(genesis_cluster.cluster_mean).long))
    sizes.append(int(30*(genesis_cluster.cluster_mean).weight))
#print(mean_cluster_nodes)
mean_cluster_lats,mean_cluster_lons=zip(*mean_cluster_nodes)
these_nodes=(mean_cluster_lats,mean_cluster_lons)

'''
mean_lat,mean_lons=zip(*mean_nodes)
means=(mean_lat,mean_lons)
'''
for node in mean_nodes:
    node.determineNearestHub(hub_nodes)

gmap = gmplot.GoogleMapPlotter(incidentList[0][0],incidentList[0][1], 9, apikey=api_key) #map for fires and fire stations
gmap2 = gmplot.GoogleMapPlotter(incidentList[0][0],incidentList[0][1], 9, apikey=api_key) #map for cluster means
gmap3 = gmplot.GoogleMapPlotter(incidentList[0][0],incidentList[0][1], 9, apikey=api_key) #map for new hub
gmap4 = gmplot.GoogleMapPlotter(incidentList[0][0],incidentList[0][1], 9, apikey=api_key)

incident_lats, incident_lons=zip(*incidentList) #events


rect_file=open(PATH_TO_SHP+"\\rectangle.txt","r")
contents=(rect_file.read().split("\n")[0]).split(",")
min_lat,max_lat,min_lon,max_lon=float(contents[0]),float(contents[1]),float(contents[2]),float(contents[3])

best_hubs=place_random_hubs(NUMBER_OF_NEW,min_lat,max_lat,min_lon,max_lon,TRIALS,mean_nodes,hub_nodes,api_key)
new_coords=[]
for hub in best_hubs:
    new_coords.append(((hub).lat,(hub).long))
new_lats,new_lons=zip(*new_coords) #new hub to be made
new=(new_lats,new_lons)

hubs_lats, hubs_lons=zip(*hubs_coords) #hubs currently active
incidents=(incident_lats,incident_lons)
hubs=(hubs_lats,hubs_lons)

plotAndSave([incidents,hubs],["#FF0000","#0000FF"],gmap,filename="fires_and_stations.html")
plotAndSave([these_nodes,hubs],["#000000","#0000FF"],gmap2,filename="cluster_means_stations.html")
plotAndSave([these_nodes,new],["#000000","#0000FF"],gmap3,filename="new_hub.html")
plotAndSave([these_nodes,hubs,new],["#000000","#0000FF","#228B22"],gmap4,filename="final.html",sizes=[600,1800,1800])
