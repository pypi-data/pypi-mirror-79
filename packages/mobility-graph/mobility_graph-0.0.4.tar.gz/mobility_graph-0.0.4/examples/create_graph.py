"""
Ayman Mahmoud - September 2020

An example to run the mobility_graph package
Example 1: Create a generic Graph

"""
from utils.common import *
import gtfs_graph as gg


g = gg.Graph()

gg.g.add_node('a', '1', '2')
gg.g.add_node('b', '2', '1')

gg.g.add_edge('a', 'b', 7, 'walk')

for v in g:
    for w in v.get_connections():
        vid = v.get_id()
        wid = w.get_id()
        print ('( %s , %s, %s, %s)' % (vid, wid, v.get_weight(w), v.get_mode(w)))

for v in g:
    print ('g.node_dict[%s]=%s' % (v.get_id(), g.node_dict[v.get_id()]))

a = (-1.554934, 53.804198)
get_map(a)
