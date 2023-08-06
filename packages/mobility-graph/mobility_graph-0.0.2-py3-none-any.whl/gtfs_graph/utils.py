"""
Ayman Mahmoud - August 2020

Resources:
https://rosettacode.org/wiki/Haversine_formula#Python
https://github.com/joshchea/gtfs-route-server/blob/master/scripts/GTFS_RouteServer.py

"""
# from math import *
from math import radians, sin, cos, sqrt, asin, pi, atan2
import networkx as nx

def computeGCD(lat1,lon1,lat2,lon2):
    #computes great circle distance from lat/lon
    '''lat1/lon1 = lat/lon of first pt
       lat2/lon2 = lat/lon of second pt
    '''
    degRad = pi/180
    lat1 = degRad*lat1
    lon1 = degRad*lon1
    lat2 = degRad*lat2
    lon2 = degRad*lon2
    dellambda = lon2-lon1
    Numerator = sqrt((cos(lat2)*sin(dellambda))**2 + (cos(lat1)*sin(lat2)- sin(lat1)*cos(lat2)*cos(dellambda))**2)
    Denominator = sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(dellambda)
    delSigma = atan2(Numerator,Denominator)

    return 3963.19059*delSigma


def compute_HS(lat1, lon1, lat2, lon2):
    # computes haversine distance from lat/lon
    '''lat1/lon1 = lat/lon of first pt
       lat2/lon2 = lat/lon of second pt
    '''
    R = 6372.8  # Earth radius in kilometers

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c

