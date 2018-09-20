from datetime import datetime
import googlemaps
import os


def getDistanceGMAPS(source,destination,api_key):
    return call_api(source,destination,"distance",api_key)

def getDurationGMAPS(source,destination,api_key):
    return call_api(source,destination,"duration",api_key)

def call_api(source,destination,api_type,api_key):
    gmaps=googlemaps.Client(key=api_key)
    now=datetime.now()
    directions_result=gmaps.directions(source,destination,mode="driving",departure_time=now)
    for map1 in directions_result:
            overall_stats=map1['legs']
            for dimensions in overall_stats:
                    distanceOrTime=dimensions[api_type]
                    return distanceOrTime['value'] #distance returned in meters, time returned in seconds
