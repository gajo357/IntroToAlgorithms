import unittest
import HeapWithClassModule
from HeapWithClassModule import heap_node

#
# The code below uses a linear
# scan to find the unfinished node
# with the smallest distance from
# the source.
#
# Modify it to use a heap instead
# 

def shortest_dist_node(dist):
    best_node = 'undefined'
    best_value = 1000000
    for v in dist:
        if dist[v] < best_value:
            (best_node, best_value) = (v, dist[v])
    return best_node

def dijkstra(G,v):
    dist_so_far = []
    HeapWithClassModule.add_to_heap(dist_so_far, heap_node(v, 0))
    final_dist = {}
    while len(dist_so_far) > 0: #len(final_dist) < len(G):
        wNode = HeapWithClassModule.remove_min(dist_so_far)
        w = wNode.name
        #w = shortest_dist_node(dist_so_far)
        # lock it down!
        final_dist[w] = wNode.value
        #del dist_so_far[w]
        for x in G[w]:
            if x not in final_dist:
                node = None
                for i in range(len(dist_so_far)):
                    if dist_so_far[i].name == x:
                        node = dist_so_far[i]
                        break
                newValue = final_dist[w] + G[w][x]
                if node is None:
                    HeapWithClassModule.add_to_heap(dist_so_far, heap_node(x, newValue))
                elif newValue < node.value:
                    node.value = newValue
                    HeapWithClassModule.up_heapify(dist_so_far, i)
                #if x not in dist_so_far:
                #    dist_so_far[x] = final_dist[w] + G[w][x]
                #elif final_dist[w] + G[w][x] < dist_so_far[x]:
                #    dist_so_far[x] = final_dist[w] + G[w][x]
    return final_dist

############
# 
# Test

def make_link(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G


class test_dijkstra(unittest.TestCase):
    def test(self):
        # shortcuts
        (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
        triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
                   (e,g,1),(e,f,5),(f,g,2),(b,f,1))
        G = {}
        for (i,j,k) in triples:
            make_link(G, i, j, k)

        dist = dijkstra(G, a)
        self.assertEquals(dist[g], 8) #(a -> d -> e -> g)
        self.assertEquals(dist[b], 11) #(a -> d -> e -> g -> f -> b)

    




