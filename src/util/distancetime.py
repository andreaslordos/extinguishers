from datetime import datetime
import googlemaps
import os

os.chdir("..")
config_file=open("config.txt","r")
contents=config_file.read()
lines=contents.split("\n")
api_key=lines[0].split("=")[-1]
config_file.close()
os.chdir("src")


def getDistanceGMAPS(source,destination):
    return call_api(source,destination,"distance")

def getDurationGMAPS(source,destination):
    return call_api(source,destination,"duration")

def call_api(source,destination,api_type):
    gmaps=googlemaps.Client(key=api_key)
    now=datetime.now()
    directions_result=gmaps.directions(source,destination,mode="driving",departure_time=now)
    for map1 in directions_result:
            overall_stats=map1['legs']
            for dimensions in overall_stats:
                    distanceOrTime=dimensions[api_type]
                    return distanceOrTime['value'] #distance returned in meters, time returned in seconds
