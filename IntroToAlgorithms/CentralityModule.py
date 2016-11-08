#
# Write centrality_max to return the maximum distance
# from a node to all the other nodes it can reach
#
import unittest
from DictGraphModule import make_link

def centrality_max(G, v):
    marked = {}
    open_list = [v]
    distance = {}
    distance[v] = 0
    max_distance = 0
    while len(open_list) > 0:
        current_node = open_list.pop(0)
        marked[current_node] = True
        for neighbor in G[current_node]:
            if neighbor not in marked:
                open_list.append(neighbor)
                distance[neighbor] = distance[current_node] + 1
                if(distance[neighbor] > max_distance):
                    max_distance = distance[neighbor]

    return max_distance

class test_centrality(unittest.TestCase):
    def text_centrality_max(self):
        chain = ((1,2), (2,3), (3,4), (4,5), (5,6))
        G = {}
        for n1, n2 in chain:
            make_link(G, n1, n2)
        self.assertEqual(centrality_max(G, 1), 5)
        self.assertEqual(centrality_max(G, 3), 3)
        tree = ((1, 2), (1, 3),
                (2, 4), (2, 5),
                (3, 6), (3, 7),
                (4, 8), (4, 9),
                (6, 10), (6, 11))
        G = {}
        for n1, n2 in tree:
            make_link(G, n1, n2)
        self.assertEqual(centrality_max(G, 1), 3)
        self.assertEqual(centrality_max(G, 11), 6)
