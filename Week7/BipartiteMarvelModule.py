import unittest
from marvel import marvel, characters
#
# In lecture, we took the bipartite Marvel graph,
# where edges went between characters and the comics
# books they appeared in, and created a weighted graph
# with edges between characters where the weight was the
# number of comic books in which they both appeared.
#
# In this assignment, determine the weights between
# comic book characters by giving the probability
# that a randomly chosen comic book containing one of
# the characters will also contain the other
#

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    G[node1][node2] = w

    if node2 not in G:
        G[node2] = {}
    G[node2][node1] = w

    return G

def create_weighted_graph(bipartiteG, characters):
    G = {}
    all_comics = []
    for char in characters:
        comics = bipartiteG[char]
        for comic in comics.keys():
            if comic not in all_comics:
                all_comics.append(comic)

    for charA in characters:
        for charB in characters:
            if charA == charB:
                continue
            if charA in G and charB in G[charA]:
                continue

            together_count = 0.0
            all_count = 0
            for comic in all_comics:
                if charA in bipartiteG[comic]:
                    if charB in bipartiteG[comic]:
                        together_count += 1
                    all_count += 1
                elif charB in bipartiteG[comic]:
                    all_count += 1

            if all_count > 0 and together_count > 0:
                make_link(G, charA, charB, together_count/all_count)
    return G

######
#
# Test
class test_bipartitemarvel(unittest.TestCase):
    def test(self):
        bipartiteG = {'charA':{'comicB':1, 'comicC':1},
                      'charB':{'comicB':1, 'comicD':1},
                      'charC':{'comicD':1},
                      'comicB':{'charA':1, 'charB':1},
                      'comicC':{'charA':1},
                      'comicD': {'charC':1, 'charB':1}}
        G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
        # three comics contain charA or charB
        # charA and charB are together in one of them
        self.assertEqual(G['charA']['charB'], 1.0 / 3)
        self.assertEqual(G['charA'].get('charA'), None)
        self.assertEqual(G['charA'].get('charC'), None)

    #def test2(self):
        #G = create_weighted_graph(marvel, characters)
        #self.assertEqual(G['HULK/DR. ROBERT BRUC']['DEMOLITION MAN/DENNI'], 0.0345)
