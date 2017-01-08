import unittest
#
# Design and implement an algorithm that can preprocess a
# graph and then answer the question "is x connected to y in the
# graph" for any x and y in constant time Theta(1).
#

#
# `process_graph` will be called only once on each graph.  If you want,
# you can store whatever information you need for `is_connected` in
# global variables
#
def mark_component(G, node):
    marked = {}
    open_list = [node]
    while len(open_list) > 0:
        current_node = open_list.pop()
        marked[current_node] = True
        for neighbor in G[current_node]:
            if neighbor not in marked:
                open_list.append(neighbor)

    return marked

marked_dict = {}
def process_graph(G):
    for node in G.keys():
        marked = mark_component(G, node)
        marked_dict[node] = marked
    pass

#
# When being graded, `is_connected` will be called
# many times so this routine needs to be quick
#
def is_connected(i, j):
    return j in marked_dict[i]

#######
# Testing
#
class test_preprocess(unittest.TestCase):
    def test(self):
        G = {'a':{'b':1},
             'b':{'a':1},
             'c':{'d':1},
             'd':{'c':1},
             'e':{}}
        process_graph(G)
        self.assertTrue(is_connected('a', 'b'))
        self.assertFalse(is_connected('a', 'c'))

        G = {'a':{'b':1, 'c':1},
             'b':{'a':1},
             'c':{'d':1, 'a':1},
             'd':{'c':1},
             'e':{}}
        process_graph(G)
        self.assertTrue(is_connected('a', 'b'))
        self.assertTrue(is_connected('a', 'c'))
        self.assertFalse(is_connected('a', 'e'))


