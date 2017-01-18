import unittest
from HeapWithClassModule import *

def dijkstra(G,v, weight_func = lambda x: x):
    # distances so far
    dist_so_far = []
    # dictionary of nodes for quick access
    dist_dict = {}
    # final list of distances
    final_dist = {}

    # create the initial node with distance 0
    node = heap_node(v, 0)
    # add it to the heap and to the dictionary
    dist_dict[node.name] = node
    add_to_heap(dist_so_far, node)
    
    while len(dist_so_far) > 0:

        # find the closes node
        wNode = remove_min(dist_so_far)
        w = wNode.name
        # remove it from the dictionary for good measure
        dist_dict.pop(w, None)
        # lock it down!
        final_dist[w] = wNode.value
        for x in G[w]:
            # only need the nodes that are not over and done
            if x not in final_dist:
                # calculate the new distance
                new_value = final_dist[w] + weight_func(G[w][x])

                if x not in dist_dict:
                    # if the node is not in the heap, add it to both heap and dictionary
                    node = heap_node(x, new_value)
                    add_to_heap(dist_so_far, node)
                    dist_dict[x] = node
                elif new_value < dist_dict[x].value:
                    # if it is in the heap and the new value is smaller
                    # change it\s value and balance the heap
                    dist_dict[x].value = new_value
                    up_heapify(dist_so_far, dist_dict[x].index)
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

# extended Dijkstra, keeps the path to each node
def dijkstra_extended(G, v, weight_func = lambda x: x):
    # distances so far
    dist_so_far = []
    # dictionary of nodes for quick access
    dist_dict = {}
    # final list of distances
    final_dist = {}

    # structures for keeping the path sa well
    paths_dict = {}

    # create the initial node with distance 0
    node = heap_node(v, 0)
    # add it to the heap and to the dictionary
    dist_dict[node.name] = node
    add_to_heap(dist_so_far, node)
    
    while len(dist_so_far) > 0:

        # find the closes node
        wNode = remove_min(dist_so_far)
        w = wNode.name
        # remove it from the dictionary for good measure
        dist_dict.pop(w, None)
        # lock it down!
        final_dist[w] = wNode.value
        if w not in paths_dict:
            paths_dict[w] = [w]
        for x in G[w]:
            # only need the nodes that are not over and done
            if x not in final_dist:
                # calculate the new distance
                new_value = final_dist[w] + weight_func(G[w][x])

                if x not in dist_dict:
                    # if the node is not in the heap, add it to both heap and dictionary
                    node = heap_node(x, new_value)
                    add_to_heap(dist_so_far, node)
                    dist_dict[x] = node
                    paths_dict[x] = list(paths_dict[w])
                    paths_dict[x].append(x)
                elif new_value < dist_dict[x].value:
                    # if it is in the heap and the new value is smaller
                    # change it\s value and balance the heap
                    dist_dict[x].value = new_value
                    up_heapify(dist_so_far, dist_dict[x].index)
                    paths_dict[x] = list(paths_dict[w])
                    paths_dict[x].append(x)
    return (final_dist, paths_dict)

# extended Dijkstra, keeps the path to each node
def dijkstra_shortest_path(G, start_node, end_node, weight_func = lambda x, y: max(x, y)):
    # distances so far
    dist_so_far = []
    # dictionary of nodes for quick access
    dist_dict = {}
    # final list of distances
    final_dist = {}

    # structures for keeping the path sa well
    paths_dict = {}

    # create the initial node with distance 0
    node = heap_node(start_node, 0)

    # add it to the heap and to the dictionary
    dist_dict[node.name] = node
    add_to_heap(dist_so_far, node)
    
    while len(dist_so_far) > 0:

        # find the closes node
        wNode = remove_min(dist_so_far)
        w = wNode.name
        # remove it from the dictionary for good measure
        dist_dict.pop(w, None)
        # lock it down!
        final_dist[w] = wNode.value
        if w not in paths_dict:
            paths_dict[w] = [w]

        # we have found the shortest path
        if(w == end_node):
            return (final_dist[w], paths_dict[w])

        for x in G[w]:
            # only need the nodes that are not over and done
            if x not in final_dist:
                # calculate the new distance
                new_value = weight_func(final_dist[w], G[w][x])

                if x not in dist_dict:
                    # if the node is not in the heap, add it to both heap and dictionary
                    node = heap_node(x, new_value)
                    add_to_heap(dist_so_far, node)
                    dist_dict[x] = node
                    paths_dict[x] = list(paths_dict[w])
                    paths_dict[x].append(x)
                elif new_value < dist_dict[x].value:
                    # if it is in the heap and the new value is smaller
                    # change it\s value and balance the heap
                    dist_dict[x].value = new_value
                    up_heapify(dist_so_far, dist_dict[x].index)
                    paths_dict[x] = list(paths_dict[w])
                    paths_dict[x].append(x)

    if(end_node not in final_dist or end_node not in paths_dict):
        return (None, None)
    return (final_dist[end_node], paths_dict[end_node])


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

    




