import unittest

############
#
# Verify a coloring of a graph
#
############

# if cert a k-coloring of G?
#   colors in {0, ..., k-1}
def verify(G, cert, k):
    # check number of colors used
    colors = []
    for (node, color) in cert.items():
        if(color not in colors):
            colors.append(color)
    if len(colors) != k:
        return False

    for (node, link) in G.items():
        for (neighbour) in G[node]:
            # no two neighbours can share the same color
            if cert[node] == cert[neighbour]:
                return False

    return True

#######
#
# Testing

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

class test_colorability(unittest.TestCase):
    def test_verify(self):
        (a,b,c,d,e,f,g,h) = ('a','b','c','d','e','f','g','h')
        cxns = [(a,c),(a,b),(c,d),(b,d),(d,e),(d,f),(e,g),(f,g),(f,h),(g,h)]

        G = {}
        for (x,y) in cxns: 
            make_link(G,x,y)

        cert = {}
        for (node, color) in [(a,0),(b,1),(c,2),(d,0),(e,1),(f,2),(g,0),(h,1)]:
            cert[node] = color
        self.assertTrue(verify(G,cert,3))

        cert = {}
        for (node, color) in [(a,0),(b,1),(c,2),(d,0),(e,0),(f,1),(g,2),(h,0)]:
            cert[node] = color
        self.assertFalse(verify(G,cert,4))

