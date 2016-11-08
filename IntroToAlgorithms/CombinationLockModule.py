import unittest
from DictGraphModule import make_link

# Generate a combination lock graph given a list of nodes
def create_combo_lock(nodes):
    G = {}
    i = 1
    while i < len(nodes):
        make_link(G, nodes[0], nodes[i])
        make_link(G, nodes[i], nodes[i-1])
        i += 1
    return G

##############
# Code for testing
#
def is_chain(graph, nodes):
    # find the first node with degree one
    #start = (n for n, e in graph.items()
    #         if len(e) == 1).next()
    for n,e in graph.items():
        if len(e) == 1:
            start = n
            break

    count = 1
    # keep track of what we've seen to make
    # sure there are no cycles
    seen = set([start])
    # follow the edges
    prev = None
    current = start
    while True:
        nexts = graph[current].keys()
        # get rid of the edge back to prev
        nexts = [n for n in nexts if not n == prev]
        if len(nexts) > 1:
            # bad.  too many edges to be a chain
            return False
        elif len(nexts) == 0:
            # We're done following the chain
            # Did we get enough edges:
            return count == len(nodes)
        prev = current
        current = nexts[0]
        if current in seen:
            # bad.  this isn't a chain
            # it has a loop
            return False
        seen.add(current)
        count += 1

def is_combo_lock(graph, nodes):
    # first see if we have a star
    center = None
    degree = 0
    for node, edges in graph.items():
        if len(edges) > degree:
            center = node
            degree = len(edges)
    if not degree == len(nodes) - 1:
        return False
    # make a graph out of all the edges
    # not connected to the center
    chain = {}
    for node, edges in graph.items():
        if node == center:
            continue
        for e in edges:
            if e == center:
                continue
            make_link(chain, node, e)
    return is_chain(chain, [n for n in nodes if n != center])

class test(unittest.TestCase):
    def test_create(self):
        for n in [5, 10, 20]:
            combo = create_combo_lock(range(n))
            self.assertTrue(is_combo_lock(combo, range(n)))