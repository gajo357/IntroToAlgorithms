import unittest
from DictGraphModule import make_link

##################################################################
# Traversal...
# Call this routine on nodes being visited for the first time
def mark_component(G, node, marked):
    marked[node] = True
    total_marked = 1
    for neighbor in G[node]:
        if neighbor not in marked:
            total_marked += mark_component(G, neighbor, marked)
    return total_marked

def check_connection(G, v1, v2):
    # Return True if v1 is connected to v2 in G
    # or False if otherwise
    marked = {}
    mark_component(G, v1, marked)
    if(v2 in marked):
        return True
    return False

class test_connectivity(unittest.TestCase):
    def testConnectivity(self):
        edges = [('a', 'g'), ('a', 'd'), ('g', 'c'), ('g', 'd'), 
                 ('b', 'f'), ('f', 'e'), ('e', 'h')]
        G = {}
        for v1, v2 in edges:
            make_link(G, v1, v2)
        self.assertTrue(check_connection(G, "a", "c"))
        self.assertFalse(check_connection(G, 'a', 'b'))
    


