"""
Ayman Mahmoud - September 2020

An example to run the mobility_graph package
Example 2: Create a GTFS Graph

"""

from utils.common import *
import gtfs_graph as gg


g2 = gg.GTFS()
directory = f'{os.getcwd()}\\..\\..\\data\\'
data = 'cairo_metro-GTFS-master.zip'
path = f'{directory}{data}'

path_uz, temp_dir_object = gg.unzip(path)
TRIPS_FILE = f'{path_uz}trips.txt'
ROUTES_FILE = f'{path_uz}routes.txt'
STOPS_FILE = f'{path_uz}stops.txt'
AGENCY_FILE = f'{path_uz}agency.txt'
STOP_TIME_FILE = f'{path_uz}stop_times.txt'

INCLUDE_AGENCIES = gg.load_agencies(AGENCY_FILE)
ROUTES = gg.load_routes(filename=ROUTES_FILE, agencies=INCLUDE_AGENCIES)
TRIPS = gg.load_trips(filename=TRIPS_FILE, routes_dict=ROUTES)
STOPS = gg.load_stops(filename=STOPS_FILE)
stop_times_csv = gg.load_stop_times(filename=STOP_TIME_FILE)

stops, edges = gg.get_stops(stop_times_csv, TRIPS)

for stop_id in STOPS:
    if stop_id in stops:
        g2 = gg.add_stop_to_graph(g2, stop_id, STOPS)

# edges = gg.get_stops(stop_times_csv, TRIPS)[1]
for (start_stop_id, end_stop_id), route_short_name in edges.items():
    # g2.add_edge(from_id=start_stop_id, to_id=end_stop_id)
    g2 = gg.add_edge_to_graph(g2,
                              from_id=start_stop_id,
                              to_id=end_stop_id,
                              route_short_name=route_short_name,
                              STOPS=STOPS
                              )

# when done delete files
# gg.delete_files(temp_dir_object)