import unittest

#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where 
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

def bipartite(G):
    # your code here
    # return a set
    left = []
    right = []
    for node in G.keys():
        isleft = True
        if(node in left):
            isleft = True
        elif (node in right):
            isleft = False
        else:
            left.append(node)
            isleft = True
        
        for neighbor in G[node]:
            if(isleft):
                if(neighbor in left):
                    return None
                if(neighbor not in right):
                    right.append(neighbor)
            else:
                if(neighbor in right):
                    return None
                if(neighbor not in left):
                    left.append(neighbor)
        
    return left

########
#
# Test

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

class test_find_bipartite(unittest.TestCase):
    def test_found(self):
        edges = [(1, 2), (2, 3), (1, 4), (2, 5),
                 (3, 8), (5, 6)]
        G = {}
        for n1, n2 in edges:
            make_link(G, n1, n2)
        g1 = bipartite(G)
        try:
            self.assertEqual(g1, list([1, 3, 5]))
            pass
        except:
            self.assertEqual(g1, list([2, 4, 6, 8]))
            pass

    def test_notfound(self):
        edges = [(1, 2), (1, 3), (2, 3)]
        G = {}
        for n1, n2 in edges:
            make_link(G, n1, n2)
        g1 = bipartite(G)
        self.assertEqual(g1, None)
