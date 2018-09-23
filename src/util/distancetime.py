from datetime import datetime
import googlemaps
import os


def getDistanceGMAPS(source,destination,api_key):
    '''
    Input: source, String, comma-separated lat/long values of source node
           destination, String, comma-separated lat/long values of destination node
           api_key, String, API key for Google Maps Directions API
    Output: distanceOrTime['value'], Integer, driving time in seconds from source
            to destination
    '''
    return call_api(source,destination,"distance",api_key)

def getDurationGMAPS(source,destination,api_key):
    '''
    Input: source, String, comma-separated lat/long values of source node
           destination, String, comma-separated lat/long values of destination node
           api_key, String, API key for Google Maps Directions API
    Output: distanceOrTime['value'], Integer, driving distance in meters from
            source to destination
    '''
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
