"""
Ayman Mahmoud - August 2020
A script to convert GTFS data to a directed graph

This work is inspired from: https://github.com/Data-Monkey/GTFS-NetworkX/blob/master/GTFStoGraph.py
"""

import networkx as nx
from csv import DictReader
from itertools import groupby
from utils.common import compute_HS


###########################
# Time Analytics
###########################
import time, os
# start = time.time()

current_directory = os.getcwd() # not needed for now

# ==============================================
"Ignore route is a variable for routes we want to ignore"
IGNORE_ROUTE = [] # unnecessary for now
# =============================================

def get_stop_id(stop_id, STOPS):
     """ translate stop_id to parent_stop_id
         if available
     """
     if STOPS[stop_id]['parent_station'] == '':
          return stop_id
     else:
          return STOPS[stop_id]['parent_station']

def add_stop_to_graph(G, stop_id, STOPS):
     """
    add stop as new node to graph

    lookup details of the stop (parent stop if available)
     """
     stop_id = get_stop_id(stop_id, STOPS)
     node = STOPS

     if G.get_node(node[stop_id]['stop_id']) is None:
          G.add_node(stop_id=node[stop_id]['stop_id'],
                     stop_name=node[stop_id]['stop_name'],
                     stop_lon=node[stop_id]['stop_lon'],
                     stop_lat=node[stop_id]['stop_lat'])
     return G

#######################################
## Adding weight to the edge
#######################################
# TODO: fix location problem
def add_weight_to_edge(from_loc, to_loc):
    weight = compute_HS(float(from_loc[1]),float(from_loc[0]),float(to_loc[1]),float(to_loc[0]))
    return weight

def add_edge_to_graph(G, from_id, to_id, route_short_name=None,STOPS=None): # needs work here...
     """ add edge to graph
         adding the route short name as a key
         if the edge and key exist, increment the count
     """
     if STOPS is None:
         STOPS = []

     if G.isEdge(from_id, to_id) is None:
          G.add_edge(from_id=from_id, to_id=to_id,
                     key=route_short_name, mode='METRO',
                     STOPS=STOPS)
         # add_edge(self, from_id, to_id, cost=0, mode='GTFS', STOPS=None):
     # TODO: add_edge() got an unexpected keyword argument 'key'
     """
     else:
          G.add_edge(get_stop_id(from_id), get_stop_id(to_id),
                     key=route_short_name,
                     count=edge['count'] + 1, weight = add_weight_to_edge(from_id, to_id))
     """
     return G

def load_routes(filename, agencies):
     """ include only routes from agencies we are interested in
     """
     routes_csv = DictReader(open(filename, 'r'))
     routes_dict = dict()
     for route in routes_csv:
          if (route['agency_id'] in agencies and
                  route['route_id'] not in IGNORE_ROUTE):
               routes_dict[route['route_id']] = route
     print('routes', len(routes_dict))
     return routes_dict


def load_trips(filename, routes_dict):
     """ load trips from file
         only include trips on routes we are interested in
     """
     trips_csv = DictReader(open(filename, 'r'))
     trips_dict = dict()
     for trip in trips_csv:
          if trip['route_id'] in routes_dict:
               trip['color'] = routes_dict[trip['route_id']]['route_color']
               trip['route_short_name'] = routes_dict[trip['route_id']]['route_short_name']
               trips_dict[trip['trip_id']] = trip
     print('trips', len(trips_dict))
     return trips_dict


def load_stops(filename):
     stops_csv = DictReader(open(filename, 'r'))
     stops_dict = dict()
     for stop in stops_csv:
          stops_dict[stop['stop_id']] = stop
     print('stops', len(stops_dict))
     return stops_dict


def load_agencies(filename):
     agency_csv = DictReader(open(filename, 'r'))
     agency_dict = dict()
     for agency in agency_csv:
          agency_dict[agency['agency_id']] = agency
     print('Agencies', len(agency_dict))
     return agency_dict

def load_stop_times(filename):
    try:
        stop_times_csv = DictReader(open(filename, 'r'))
    except PermissionError:
        print("An exception occurred, permission denied. trying a workaround")
        from shutil import copyfile
        src = filename
        dst = f'{os.getcwd()}/copy_stop_times.txt'
        copyfile(src, dst)
        stop_times_csv = DictReader(open(dst, 'r'))

    return stop_times_csv

def get_stops(stop_times_csv, TRIPS):
    # TODO: fix the problem here, normally there should be edges and stops
    stops = set()
    edges = dict()
    for trip_id, stop_time_iter in groupby(stop_times_csv, lambda stop_t: stop_t['trip_id']):
        if trip_id in TRIPS:
            trip = TRIPS[trip_id]
            prev_stop = next(stop_time_iter)['stop_id']
            stops.add(prev_stop)
            for stop_time in stop_time_iter:
                stop = stop_time['stop_id']
                edge = (prev_stop, stop)
                edges[edge] = trip['route_short_name']
                stops.add(stop)
                prev_stop = stop
    print('stops', len(stops))
    print('edges', len(edges))
    return stops, edges

def unzip(path):
    """
    Input: path to the zip file
    Output: path to the unzipped file.
    """
    import zipfile
    import tempfile as tf

    foi = tf.TemporaryDirectory()
    print('created temporary directory', foi)

    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(foi.name)
        folder = zip_ref.namelist()[0]

    # TODO: return the path if there is no subdirectory, I need to verify the value of folder first
    return os.path.join(foi.name, folder), foi


def delete_files(path):
    """
    the path is to the unzipped location that is going to be deleted when the graph is created
    input: temporary directory object
    """
    try:
        import tempfile as tf
        path.cleanup()
    except PermissionError:
        print("Warning [Windows Error] An exception occurred, permission denied.")
        os.unlink(path.name)
    print('graph of GTFS is built. deleting temporary directory...', path.name)


def save_graph(G):
    # Save graph to memory if nx is used
    #nx.write_gpickle(G, "./output_graph.gpickle")
    pass
    # TODO: Still need to find a way to save the graph class, maybe look into saving objects in a file
# ==============================================

if __name__ == '__main__':
    print("Hello There, test me")


# not needed for now.
#deg = nx.degree(Graph)
#labels = {stop_id: Graph.nodes[stop_id]['stop_name'] if deg[stop_id] >= 0 else '' for stop_id in Graph.nodes}
#pos = {stop_id: (Graph.nodes[stop_id]['stop_lon'], Graph.nodes[stop_id]['stop_lat']) for stop_id in Graph.nodes}




