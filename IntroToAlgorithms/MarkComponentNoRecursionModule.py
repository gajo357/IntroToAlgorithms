# Rewrite `mark_component` to not use recursion 
# and instead use the `open_list` data structure 
# discussed in lecture
#
import unittest
from DictGraphModule import make_link

def mark_component(G, node, marked):
    total_marked = 0
    open_list = [node]
    while len(open_list) > 0:
        current_node = open_list.pop()
        marked[current_node] = True
        total_marked += 1
        for neighbor in G[current_node]:
            if neighbor not in marked:
                open_list.append(neighbor)

    return total_marked

class test_mark_component(unittest.TestCase):
    def test_markComponentNoRecursion(self):
        test_edges = [(1, 2), (2, 3), (4, 5), (5, 6)]
        G = {}
        for n1, n2 in test_edges:
            make_link(G, n1, n2)
        marked = {}
        self.assertEqual(mark_component(G, 1, marked), 3)
        self.assertTrue(1 in marked)
        self.assertTrue(2 in marked)
        self.assertTrue(3 in marked)
        self.assertTrue(4 not in marked)
        self.assertTrue(5 not in marked)
        self.assertTrue(6 not in marked)
