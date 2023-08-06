"""
Ayman Mahmoud - August 2020

"""

class Graph(object):
    """
    This class outlines the structure of a graph, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    Class inspiration: https://gist.github.com/eovares/4035265, https://github.com/bmander/graphserver/blob/master/core/graph.h

    Abstraction graph example: https://www.geeksforgeeks.org/abstract-classes-in-python/
    Graph theory in python: https://www.python-course.eu/graphs_python.php

    Class implementation: https://www.bogotobogo.com/python/python_graph_data_structures.php

    """
    def __init__(self):
        # Initialize a graph of n vertices
        # self.nodes = 0
        self.node_dict = {}
        self.num_nodes = 0

    def __iter__(self):
        return iter(self.node_dict.values())

    def add_node(self, stop_id, stop_name=None, stop_lon='0', stop_lat='0'):
        self.num_nodes = self.num_nodes + 1
        new_node = Node(stop_id, stop_name, stop_lon, stop_lat)
        self.node_dict[stop_id] = new_node
        return new_node

    def get_node(self, n):
        if n in self.node_dict:
            return self.node_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0, mode='NA', color=None):
        # create edge between two vertices/nodes
        add_edge = True
        if frm not in self.node_dict:
            self.add_node(frm, 'NA', 'NA')
            print('The node', frm, 'does not exist, please add missing information in order to add the node to the database.')
            add_edge = False
        if to not in self.node_dict:
            self.add_node(to, 'NA', 'NA')
            print('The node', to,'does not exist, please add missing information in order to add the node to the database.')
            add_edge = False
        if color == None:
            color = ''
            r, g, b = (0, 0, 0)
        else:
            r = int(color[:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:], 16)

        if add_edge:
            self.node_dict[frm].add_neighbor(self.node_dict[to], cost, mode, 'r')
            self.node_dict[to].add_neighbor(self.node_dict[frm], cost, mode, 'r')

    def del_Edge(self, n1, n2):
        # deletes edge between two vertices/nodes
        pass

    def get_nodes(self):
        return self.node_dict.keys()

    def isEdge(self, n1, n2):
        # Determine if an edge is in the graph
        pass

    def visualize(self):
        # visualize Graph based lon and lat
        pass

class Node:
    def __init__(self, id, name, lon, lat):
        self.id = id
        self.name = name
        self.lon = lon
        self.lat = lat
        self.tags = {}
        self.adjacent = {}
        self.mode = {}
        self.color = {}
        self.key = {}
    # TODO: unify weight and cost
    def add_neighbor(self, neighbor, weight=0, mode='NA', color=None, key=None):
        self.adjacent[neighbor] = weight
        self.mode[neighbor] = mode
        self.color[neighbor] = color
        self.key[neighbor] = key


    def del_neighbor(self, neighbor):
        self.__delattr__(neighbor)

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def get_mode(self, neighbor):
        return self.mode[neighbor]

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class GTFS(Graph):
    """
        This class adapts GTFS features with Graph
        use package gtfs-graph
    """
    def __init__(self, type='GTFS'):
        # Initialize a graph of n vertices
        # self.nodes = 0
        Graph.__init__(self)
        self.node_dict = {}
        self.num_nodes = 0

    def __iter__(self):
        return iter(self.node_dict.values())

    def add_node(self, stop_id, stop_name=None, stop_lon='0', stop_lat='0'):
        self.num_nodes = self.num_nodes + 1
        new_node = Node(stop_id, stop_name, stop_lon, stop_lat)
        self.node_dict[stop_id] = new_node
        return new_node

    def get_node(self, n):
        if n in self.node_dict:
            return self.node_dict[n]
        else:
            return None


    def add_edge(self, from_id, to_id, cost=0, mode='GTFS', STOPS=None, key=None):
        # create edge between two vertices/nodes
        #
        add_edge = True
        if STOPS is None:
            STOPS = []
        if key is None:
            key=''
        """
        if frm not in self.node_dict:
            self.add_node(frm, 'NA', 'NA')
            print('The node', frm, 'does not exist, please add missing information in order to add the node to the database.')
            add_edge = False
        if to not in self.node_dict:
            self.add_node(to, 'NA', 'NA')
            print('The node', to,'does not exist, please add missing information in order to add the node to the database.')
            add_edge = False
        """

        frm = gg.get_stop_id(from_id, STOPS)
        to = gg.get_stop_id(to_id, STOPS)
        node_frm = STOPS[frm]
        node_to = STOPS[to]
        from_loc = (node_frm['stop_lon'], node_frm['stop_lat'])
        to_loc = (node_to['stop_lon'], node_to['stop_lat'])
        cost = gg.add_weight_to_edge(from_loc, to_loc)

        if add_edge:
            self.node_dict[frm].add_neighbor(self.node_dict[to], weight=cost, mode=mode,key=key)
            self.node_dict[to].add_neighbor(self.node_dict[frm], weight=cost, mode=mode, key=key)

    def del_Edge(self, n1, n2):
        # deletes edge between two vertices/nodes
        pass

    def get_nodes(self):
        return self.node_dict.keys()

    def isEdge(self, n1, n2):
        # Determine if an edge is in the graph
        return None

    def build_graph(self):
        pass


    def visualize(self, mode='plain'):
        """
        Inspired from: https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
        """
        if mode == 'plain':
            print("Printing nodes in plain mode")
            # get_map(a, 1)
        elif mode == 'sat':
            print("Getting satellite data")
            # get_map(a, 2)
        elif mode == 'map':
            print("Getting map data")
            # get_map(a, 3)
        else:
            print("An error occured. please check mode")

class Walk(Graph):
    """
        This class adapts OSM or OSRM walk routing

        It should inherit all the nodes available, then apply OSM - OSRM routing API and finally filter accordingly with
        the TP config for the maximum walking distance or time.
    """

class Nearby(Graph):
    """
        This class adapts OSM or OSRM walk routing

        And is going to be used for locations that are not in the vertices.
        Inspiration and source for some pieces of code:
        https://github.com/SAUSy-Lab/nearby-transit-trip-frequency/blob/0c38df7ef149291e8dbd3fad06db26b0de50dd17/nearby_stops.py
    """
    def __init__(self):
        """
        Initialize graph objects
        """
        Graph.__init__(self)

    def findNearby(self, gtfs,origin_x,origin_y,distance):
        """
        To find nearby stations
        Distance is an input that we can use to define a distance Threshold
        But we can also define a distance limit from the beginning
        or check the routing walking time and limit by walking time limit

        """

        walk_speed = 1.3

        stops = gtfs + "/stops.txt"

        # grab locations of all stops
        stop_locations = []
        with open(stops, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                xs = float(row["stop_lon"])
                ys = float(row["stop_lat"])

                if compute_HS(origin_x, origin_y, xs, ys) < distance * 3:
                    # some if for distance threshold

                    stop_id = row["stop_id"]
                    stop_locations.append([stop_id, xs, ys])

        # grab string of all the coordinates - for plugging into OSRM url
        coord_str = str(origin_x) + ',' + str(origin_y) + ';'
        for row in stop_locations:
            coord_str = coord_str + str(row[1]) + ',' + str(row[2]) + ';'
        coord_str = coord_str[:-1]

        # grab list of destinations IDs for URL string
        distr = ''
        di = 1
        while di <= len(stop_locations):
            distr = distr + str(di) + ';'
            di += 1
        distr = distr[:-1]

        # url for OSRM request
        url = 'http://localhost:5000/table/v1/walking/' + coord_str + '?sources=0&destinations=' + distr

        # getting the data via request and loading json into a python dict
        page = requests.get(url)
        data = json.loads(page.content)

        if len(stop_locations) != len(data['durations'][0]):
            return "at least one stop failed"

        c = 0

        out_stop_ids = []
        while c < len(stop_locations):
            duration = data['durations'][0][c]
            distance_to_stop = float(duration) * walk_speed
            stop_id = stop_locations[c][0]
            if distance_to_stop <= distance:
                out_stop_ids.append(stop_id)
            c += 1

        return out_stop_ids



    def walk(self):
        """
        Walk to nearby station using OSRM Api
        """

class MOD(Graph):
    """
        This class adapts MOD features with Graph
    """


if __name__ == '__main__':
    print("Hello There")
