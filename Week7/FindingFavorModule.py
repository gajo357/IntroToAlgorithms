import unittest

# Finding a Favor v2 
#
# Each edge (u,v) in a social network has a weight p(u,v) that
# represents the probability that u would do a favor for v if asked.
# Note that p(v,u) != p(u,v), in general.
#
# Write a function that finds the right sequence of friends to maximize
# the probability that v1 will do a favor for v2.
# 

#
# Provided are two standard versions of dijkstra's algorithm that were
# discussed in class. One uses a list and another uses a heap.
#
# You should manipulate the input graph, G, so that it works using
# the given implementations.  Based on G, you should decide which
# version (heap or list) you should use.
#

# code for heap can be found in the instructors comments below
from math import log
from heap import *
from operator import itemgetter

def make_link(G, node, neighbor, weight):
    G[node][neighbor] = weight

def get_log_weight(max_weight, weight):
    w = max_weight/weight
    w = log(w)
    if w < 0:
        return 0
    return w

def mark_component(G, node, end_node):
    reached = False
    marked = {}
    open_list = [node]
    max_weight = None
    while len(open_list) > 0:
        current_node = open_list.pop()
        marked[current_node] = {}
        for neighbor in G[current_node]:
            weight = G[current_node][neighbor]
            make_link(marked, current_node, neighbor, weight)
            if max_weight is None or weight > max_weight:
                max_weight = weight
            if neighbor not in marked:
                open_list.append(neighbor)
            if neighbor == end_node:
                reached = True

    for n1, edge in marked.items():
        for n2, weight in edge.items():
            marked[n1][n2] = get_log_weight(max_weight, weight)
    return (marked, reached)

def count_nodes_and_edges(G):
    nodes = 0.
    edges = 0.
    for node1 in G:
        nodes += 1
        for node2 in G[node1]:
            edges += 1
    return float(nodes), float(edges)

def maximize_probability_of_favor(G, v1, v2):
    # your code here
    # call either the heap or list version of dijkstra
    # and return the path from `v1` to `v2` 
    # along with the probability that v1 will do a favor 
    # for v2
    G_prim, reached = mark_component(G, v1, v2)
    if not reached:
        return None

    n, m = count_nodes_and_edges(G)
    final_dist = None
    if n*n >= m * log(n):
        final_dist = dijkstra_heap(G_prim, v1)
    else:
        final_dist = dijkstra_list(G_prim, v1)

    path = []
    node = v2
    d, parent = final_dist[node]
    distance = 1
    while parent is not None:
        path.append(node)
        distance *= G[parent][node]
        node = parent
        d, parent = final_dist[node]
    path.append(v1)
    path.reverse()
    return path, distance

#
# version of dijkstra implemented using a heap
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_heap(G, a):
    # Distance to the input node is zero, and it has
    # no parent
    first_entry = (0, a, None)
    heap = [first_entry]
    # location keeps track of items in the heap
    # so that we can update their value later
    location = {first_entry:0}
    dist_so_far = {a:first_entry} 
    final_dist = {}
    while len(dist_so_far) > 0:
        dist, node, parent = heappopmin(heap, location)
        # lock it down!
        final_dist[node] = (dist, parent)
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, x, node)
            if x not in dist_so_far:
                # add to the heap
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                # update heap
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry
    return final_dist

#
# version of dijkstra implemented using a list
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_list(G, a):
    dist_so_far = {a:(0, None)} #keep track of the parent node
    final_dist = {}
    while len(final_dist) < len(G):
        node, entry = min(dist_so_far.items(), key=itemgetter(1))
        # lock it down!
        final_dist[node] = entry
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, node)
            if x not in dist_so_far:
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                dist_so_far[x] = new_entry
    return final_dist

##########
#
# Test

class test_finding_favor(unittest.TestCase):
    def test(self):
        G = {'a':{'b':.9, 'e':.5},
             'b':{'c':.9},
             'c':{'d':.01},
             'd':{},
             'e':{'f':.5},
             'f':{'d':.5}}
        path, prob = maximize_probability_of_favor(G, 'a', 'd')
        self.assertEqual(path, ['a', 'e', 'f', 'd'])
        self.assertTrue(abs(prob - .5 * .5 * .5) < 0.001)

    
