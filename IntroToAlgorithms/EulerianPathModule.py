# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]
import operator
import unittest

def get_degrees(graph):
    # count degree number for each node
    nodes = {}
    for edge in graph:
        for node in edge:
            nodes[node] = nodes.get(node, 0) + 1
    return nodes

def find_eulerian_tour(graph):
    # we don't wat to modify the original graph
    local_graph = list(graph)

    if(len(local_graph) == 0):
        return []

    nodes = get_degrees(local_graph)
            
    # find two odd degree nodes to set as start - stop
    start_node = local_graph[0][0]
    for node, degree in nodes.items():
        if degree % 2 == 1:
            start_node = node
            break
        if degree > nodes[start_node]:
            start_node = node
            
    #print nodes
    #print start_node
    
    tour = []
    tour.append(start_node)
    node = start_node
    edge = None
    while len(local_graph) > 0:
        prev_edge = edge
        edge = find_edge(local_graph, node, start_node)
        
        #print edge
        local_graph.remove(edge)
        for n in edge:
            if n != node:
                tour.append(n)
        node = tour[-1]
    return tour
    
def find_edge(graph, node, start_node):
    if node == None or len(graph) == 1:
        return graph[0]
    
    # find all edges containg this node
    edges = []
    for edge in graph:
        if node in edge:
            edges.append(edge)
    
    if len(edges) == 1:
        return edges[0]
    
    # find the first edge that does not bring us the the beginning
    for edge in edges:
        if start_node not in edge:
            return edge
    
    return edges[0]

def is_eulerian_tour(self, graph, tour):    
    nodes = get_degrees(graph)
    for i in range(len(tour)):
        node = tour[i]
        diff = 2
        if(i == 0 or i == len(tour) - 1):
            diff = 1                         
        nodes[node] = nodes[node] - diff

    for node, degree in nodes.items():
        self.assertEqual(degree, 0)

    #self.assertEqual(tour[0], tour[-1])


class test_euler(unittest.TestCase):
    def tests(self):
        graph = [(1, 2), (2, 3), (3, 1)]  
        is_eulerian_tour(self, graph, find_eulerian_tour(graph))
        
        graph = [(0, 1), (1, 5), (1, 7), (4, 5),
                (4, 8), (1, 6), (3, 7), (5, 9),
                (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]
        is_eulerian_tour(self, graph, find_eulerian_tour(graph))
        
        graph = [(1, 13), (1, 6), (6, 11), (3, 13),
                (8, 13), (0, 6), (8, 9),(5, 9), (2, 6), (6, 10), (7, 9),
                (1, 12), (4, 12), (5, 14), (0, 1),  (2, 3), (4, 11), (6, 9),
                (7, 14),  (10, 13)]  
        is_eulerian_tour(self, graph, find_eulerian_tour(graph))
        
        graph = [(8, 16), (8, 18), (16, 17), (18, 19),
                (3, 17), (13, 17), (5, 13),(3, 4), (0, 18), (3, 14), (11, 14),
                (1, 8), (1, 9), (4, 12), (2, 19),(1, 10), (7, 9), (13, 15),
                (6, 12), (0, 1), (2, 11), (3, 18), (5, 6), (7, 15), (8, 13), (10, 17)]
        is_eulerian_tour(self, graph, find_eulerian_tour(graph))
        