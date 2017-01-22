import unittest
import copy
from DijkstraHeapModule import dijkstra_shortest_path

#
# Take a weighted graph representing a social network where the weight
# between two nodes is the "love" between them.  In this "feel the
# love of a path" problem, we want to find the best path from node `i`
# and node `j` where the score for a path is the maximum love of an
# edge on this path. If there is no path from `i` to `j` return
# `None`.  The returned path doesn't need to be simple, ie it can
# contain cycles or repeated vertices.
#
# Devise and implement an algorithm for this problem.
#
def break_link(G, node1, node2):
    if node1 not in G:
        print("error: breaking link in a non-existent node")
        return
    if node2 not in G:
        print("error: breaking link in a non-existent node")
        return
    if node2 not in G[node1]:
        print("error: breaking non-existent link")
        return
    if node1 not in G[node2]:
        print("error: breaking non-existent link")
        return
    del G[node1][node2]
    del G[node2][node1]
    return G

def FindAllEdges(G):
    all_edges = []
    for nodeA, edges in G.items():
        for nodeB, weight in edges.items():
            if((nodeA, nodeB) not in all_edges and (nodeB, nodeA) not in all_edges):
                all_edges.append((nodeA, nodeB))
    return all_edges

def feel_the_love(G, i, j):
    # return a path (a list of nodes) between `i` and `j`,
    # with `i` as the first node and `j` as the last node,
    # or None if no path exists
    (score, path) = dijkstra_shortest_path(G, i, j)
    # there is no path, no need to look any further
    if path is None:
        return None
    
    # visit all possible edges, so we're sure we got the maximum
    # remove the destination from the graph, as we do not want to end there
    Gcopy = copy.deepcopy(G)
    dest_edges = G[j]
    entering_node = None
    max_weight = None
    for node, weight in dest_edges.items():
        break_link(Gcopy, j, node)
        # find the final edge that gives us the maximum
        if entering_node is None or weight > max_weight:
            entering_node = node
            max_weight = weight

    #start from the start node
    temp_start = i
    final_path = []
    # for each edge in the graph
    for nodeA, nodeB in FindAllEdges(Gcopy):
        # find any path to it's begining nodeA
        (score, path) = dijkstra_shortest_path(G, temp_start, nodeA)
        # if it can't be reached, skip it
        if(path is None):
            continue
        # travel to node A
        final_path.extend(path)
        # travel to node B (we are looking at the A-B edge, so there is a direct path)
        # set node B as our new origin
        temp_start = nodeB

    
    # find the shortest path from where we are to 
    (score, path) = dijkstra_shortest_path(Gcopy, temp_start, entering_node)
    final_path.extend(path)
    final_path.append(j)
    return final_path

#########
#
# Test

def score_of_path(G, path):
    max_love = -float('inf')
    for n1, n2 in zip(path[:-1], path[1:]):
        love = G[n1][n2]
        if love > max_love:
            max_love = love
    return max_love

class test_feelthelove(unittest.TestCase):
    def test(self):
        G = {'a':{'c':1},
             'b':{'c':1},
             'c':{'a':1, 'b':1, 'e':1, 'd':1},
             'e':{'c':1, 'd':2},
             'd':{'e':2, 'c':1},
             'f':{}}

        path = feel_the_love(G, 'a', 'b')
        self.assertEqual(score_of_path(G, path), 2)

        path = feel_the_love(G, 'a', 'f')
        self.assertEqual(path, None)

    
