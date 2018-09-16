import os
import json
from gmplot import gmplot
from pathlib import Path
from FireNode import FireNode
from cluster import Cluster
from utils import removeDuplicates
from Node import Node
from algorithms import calculate_score
def loadEvents(PATH_TO_DATA,archiveName):
    os.chdir(PATH_TO_DATA)
    with open(archiveName, 'r') as f:
        event_dict = json.load(f)
    f.close()
    return event_dict

def plotAndSave(incidents,hubs,c1,c2,gmap,filename="saved.html",sizes=[400]):
    '''
    Incidents is a tuple of incident lats and incident longs
    Hubs is a tuple of hub lats and hub longs
    '''
    if sizes==[400]:
        sizes=sizes*len(incidents[0])

    for x in range(len(incidents[0])):
        gmap.scatter([incidents[0][x]],[incidents[1][x]],c1,size=sizes[x],marker=False)
    gmap.scatter(hubs[0],hubs[1],c2,size=1600,marker=False)
    gmap.draw(PATH_TO_SAVE+"\\"+filename)

def loadHubs(data):
    hubs=[]
    hubs_coords=[]
    for hub in data:
        hubs.append(Node(hub[0],hub[1],"hub",0))
        hubs_coords.append((hub[0],hub[1]))
    return hubs, hubs_coords


locations = [(34.8302, 33.3933),
            (35.1283, 33.3145),
            (34.6815, 33.0281),
            (34.6903, 33.0692),
            (34.6684, 32.9928),
            (34.9207, 33.6163),
            (34.9608, 33.6574),
            (34.8739, 33.6177),
            (34.7694, 32.4355),
            (35.0297, 32.4306),
            (34.7152, 32.4782),
            (35.0575, 33.9704),
            (35.1728, 33.3573),
            (35.1883, 33.394)]

hubs,hubs_coords=loadHubs(locations)
hub_nodes=hubs[:]
#print(hubs)
FILENAME="saved.html"
PATH_TO_CODE=os.path.dirname(os.path.abspath(__file__))
PATH_TO_SAVE=(Path(PATH_TO_CODE).parent).__str__()+"\\saves"
PATH_TO_DATA=(Path(PATH_TO_CODE).parent).__str__()+"\\data"
MAX_FRP=160.8
MAX_SEV=62
MAX_POP_DENSITY=0
archiveName="archive.json"
archive_dict = loadEvents(PATH_TO_DATA,archiveName)

os.chdir(PATH_TO_CODE)

incidentList=[]
incident_nodes=[]
for e in archive_dict: #each e is another event
    incident_nodes.append(FireNode(e["latitude"],e["longitude"],"event",0,e["acq_date"],e["confidence"],e["frp"]))
    incident_nodes[-1].calculateWeight(MAX_SEV,MAX_FRP,MAX_POP_DENSITY)
    incidentList.append((e["latitude"],e["longitude"]))

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

gmap = gmplot.GoogleMapPlotter(incidentList[0][0],incidentList[0][1], 9) #map for fires and fire stations
gmap2 = gmplot.GoogleMapPlotter(incidentList[0][0],incidentList[0][1], 9) #map for cluster means
incident_lats, incident_lons=zip(*incidentList) #events
hubs_lats, hubs_lons=zip(*hubs_coords) #hubs currently active
incidents=(incident_lats,incident_lons)
hubs=(hubs_lats,hubs_lons)
#print(these_nodes)
plotAndSave(incidents,hubs,"#FF0000","#0000FF",gmap,filename="fires_and_stations.html")
plotAndSave(these_nodes,hubs,"#000000","#0000FF",gmap2,filename="cluster_means_stations.html",sizes=sizes)
b=calculate_score(mean_nodes,hub_nodes)
