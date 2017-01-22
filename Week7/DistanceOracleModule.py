import unittest
from math import log, ceil
from random import randint
from copy import deepcopy
from collections import deque
from HeapWithClassModule import heap_node, add_to_heap, up_heapify, remove_min
from DijkstraHeapModule import dijkstra_extended

# 
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
# 
# Given a graph G that is a balanced binary tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a balanced binary tree and the root element
# and returns a dictionary, mapping each node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#

def add_one_degree(heap_dict, heap, node):
    if node not in heap_dict:
        heap_dict[node] = heap_node(node, 1)
        add_to_heap(heap, heap_dict[node])
    else:
        heap_dict[node].value = 1.0/(1.0/heap_dict[node].value + 1)
        up_heapify(heap, heap_dict[node].index)

def get_top_hubs(graph, nodes, no_hubs = 1):
    # count degree number for each node
    heap_dict = {}
    heap = []
    node_indexes = {}
    for i in range(len(nodes)):
        nodeA = nodes[i]
        node_indexes[nodeA] = i
        for nodeB in graph[nodeA].keys():
            add_one_degree(heap_dict, heap, nodeA) 
            add_one_degree(heap_dict, heap, nodeB) 

    for i in range(no_hubs):
        hub = remove_min(heap)
        yield hub.name
    #return hubs

def max_labels(labels):
    return max(len(labels[u]) for u in labels)

def labels_needed(G):
    return int(ceil(log(len(G) + 1, 2)))

def determine_tree_root(G, max_depth):
    min_dist = None
    root_node_data = None
    root_node_datas = {}
    for node in G.keys():
        (distances, path) = dijkstra_extended(G, node)
        max_distance = max(len(path[n]) for n in G.keys()) 
        # if the distance of this node to every other node in the tree is smaller 
        # then the maximum allowed distance, this is the root node of the tree
        #if max_distance <= max_depth:
        #    return (node, distances, path)
        if min_dist is None or max_distance < min_dist:
            min_dist = max_distance
            root_node_data = (node, distances, path)
            root_node_datas = {}
            root_node_datas[node] = root_node_data
        elif min_dist == max_distance:
            root_node_datas[node] = (node, distances, path)

    # if there is a choice, take the more central one
    if min_dist > max_depth and len(root_node_datas) > 1:
        for hub in get_top_hubs(G, [node for (node, d, p) in root_node_datas.values()]):
            return root_node_datas[hub]

    return root_node_data

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def mark_component(G, node):
    marked = {}
    new_graph = {}
    open_list = [node]    
    while len(open_list) > 0:
        current_node = open_list.pop()
        marked[current_node] = True
        for neighbor in G[current_node]:
            make_link(new_graph, current_node, neighbor, G[current_node][neighbor])
            if neighbor not in marked:
                open_list.append(neighbor)

    return new_graph

def split_graph(graph, root):
    # find connections of root
    nodes = list(graph[root].keys())
    for node in nodes:
        del graph[node][root]
        del graph[root][node]
        yield mark_component(graph, node)

def create_labels(G):
    labels = {}

    # connect everyone with itself
    for node in G.keys():
        labels[node] = {}
        labels[node][node] = 0

    max_labels = labels_needed(G)
    sub_graphs = [(deepcopy(G), max_labels)]
    while(len(sub_graphs) > 0):
        # take the first sub graph from the list
        (graph, max_depth) = sub_graphs.pop()
        
        # the graph has only one node
        if len(graph) < 2:
            continue
        
        # find it's root
        (root, root_distances, root_path) = determine_tree_root(graph, max_depth)
        
        # connect all nodes to the root
        for node in graph.keys():
            if node == root:
                continue
            labels[node][root] = root_distances[node]

        # split the subgraph in the root node
        for sub_graph in split_graph(graph, root):
            if len(sub_graph) > 0:
                sub_graphs.append((sub_graph, max_depth - 1))

    return labels

def create_labels_simple(G, root):
    labels = {}

    open_list = [root]
    labels[root] = {}
    labels[root][root] = 0

    while len(open_list) > 0:
        node = open_list.pop()
        for neighbor, weight in G[node].items():
            if neighbor not in labels:
                open_list.append(neighbor)
                
                labels[neighbor] = {}
                labels[neighbor][neighbor] = 0
                labels[neighbor][node] = weight
                for parent, distance in labels[node].items():
                    labels[neighbor][parent] = distance + weight
                labels[node][neighbor] = weight
    return labels

#######
# Testing
#

def get_distances(G, labels):
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.items():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def distance(tree, w, u):
    if w==u: return 0

    distances = {w: 0}
    frontier = deque([w])
    while frontier:
        n = frontier.popleft()
        for s in tree[n]:
            if s not in distances: 
                distances[s] = distances[n] + tree[n][s]
                frontier.append(s)
            if s==u:
                return distances[u]

    return None

class test_distance_oracle(unittest.TestCase):
    def test_binary_tree(self):
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
                 (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
        tree = {}
        for n1, n2 in edges:
            make_link(tree, n1, n2)
        labels = create_labels(tree)
        self.assertTrue(labels_needed(tree) >= max_labels(labels))

        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][2], 1)
        self.assertEqual(distances[1][4], 2)
        self.assertEqual(distances[1][2], 1)
        self.assertEqual(distances[1][4], 2)   
        self.assertEqual(distances[4][1], 2)
        self.assertEqual(distances[1][4], 2)
        self.assertEqual(distances[2][1], 1)
        self.assertEqual(distances[1][2], 1)  
        self.assertEqual(distances[1][1], 0)
        self.assertEqual(distances[2][2], 0)
        self.assertEqual(distances[9][9], 0)
        self.assertEqual(distances[2][3], 2)
        self.assertEqual(distances[12][13], 2)
        self.assertEqual(distances[13][8], 6)
        self.assertEqual(distances[11][12], 6)
        self.assertEqual(distances[1][12], 3)

    def test_chain_graph(self):
        edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
                (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]

        tree = {}
        for n1, n2 in edges:
            make_link(tree, n1, n2)
        labels = create_labels(tree)
        self.assertTrue(labels_needed(tree) >= max_labels(labels))

        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][2], 1)
        self.assertEqual(distances[1][2], 1)
        self.assertEqual(distances[1][3], 2)
        self.assertEqual(distances[1][13], 12)
        self.assertEqual(distances[6][1], 5)
        self.assertEqual(distances[6][13], 7)
        self.assertEqual(distances[8][3], 5)
        self.assertEqual(distances[10][4], 6)

    def test_star_chain(self):
        edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 7), 
                (7, 8), (8, 9), (1, 10), (10, 11), (11, 12), (12, 13)]

        tree = {}
        for n1, n2 in edges:
            make_link(tree, n1, n2)
        labels = create_labels(tree)
        self.assertTrue(labels_needed(tree) >= max_labels(labels))

        distances = get_distances(tree, labels)
        self.assertEqual(distances[1][1], 0)
        self.assertEqual(distances[5][5], 0)
        self.assertEqual(distances[1][2], 1)
        self.assertEqual(distances[1][3], 2)   
        self.assertEqual(distances[1][4], 3)
        self.assertEqual(distances[1][5], 4)
        self.assertEqual(distances[5][6], 5)
        self.assertEqual(distances[5][7], 6)
        self.assertEqual(distances[5][8], 7)
        self.assertEqual(distances[5][9], 8)

    def test_random_test(self):
        N = 10
        n0 = 20
        n1 = 100

        for _ in range(N):
            tree = {}
            for w in range(1, n0):
                make_link(tree, w, w+1, randint(1, 1))

            for w in range(n0+1, n1+1):
                make_link(tree, randint(1, w-1), w, randint(1, 1))

            labels = create_labels(tree)
            distances = get_distances(tree, labels)

            self.assertTrue(max_labels(labels) <= labels_needed(tree))

            for _ in range(N):
                w = randint(1, n1)
                u = randint(1, n1)
                self.assertEqual(distance(tree, w, u), distances[w][u])
