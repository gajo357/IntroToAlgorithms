import unittest
from math import log, ceil
from random import randint
from collections import deque
from HeapWithClassModule import *
from DijkstraHeapModule import *

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

def get_top_hubs(graph, root, no_hubs):
    # count degree number for each node
    heap_dict = {}
    heap = []
    for nodeA, edges in graph.items():
        for nodeB in edges.keys():
            add_one_degree(heap_dict, heap, nodeA) 
            add_one_degree(heap_dict, heap, nodeB) 

    hubs = [root]
    for i in range(2, no_hubs):
        hubs.append(remove_min(heap).name)
    return hubs

def max_labels(labels):
    return max(len(labels[u]) for u in labels)

def labels_needed(G):
    return int(ceil(log(len(G) + 1, 2)))

def determine_tree_root(G):
    depth = labels_needed(G)
    min_dist = None
    root_node_data = None
    for node in G.keys():
        (distances, path) = dijkstra_extended(G, node)
        max_distance = max(len(path[n]) for n in G.keys()) 
        # if the distance of this node to every other node in the tree is smaller 
        # then the maximum allowed distance, this is the root node of the tree
        if max_distance <= depth:
            return (node, distances, path)
        if min_dist is None or max_distance < min_dist:
            min_dist = max_distance
            root_node_data = (node, distances, path)

    return root_node_data

def add_label(labels, node1, node2, distance, node2_not_root = True):
    if node2 in labels and node1 in labels[node2]:
        if node2_not_root:
            # there is a connection already
            return
        del labels[node2][node1]
    if node2_not_root:        
        if node1 in labels:
            # if node2 has less labels, we add labels to it rather then to node1
            if node2 not in labels or len(labels[node1]) > len(labels[node2]):
                add_label(labels, node2, node1, distance)
                return

    if node1 not in labels:
        labels[node1] = {}
    
    labels[node1][node2] = distance

def connect_the_chain(G, path, max_labels, labels):
    if len(path) == 1:
        return

    if max_labels == 0:
        return

    if max_labels >= len(path) - 1:
        # there is enough labels for all connections
        for i in range(len(path) - 1):
            distance = 0
            for j in range(i, len(path) - 1):
                distance += G[path[j]][path[j + 1]]
                add_label(labels, path[i], path[j + 1], distance)
                add_label(labels, path[j + 1], path[i], distance)
        return

    if len(path) == 3:
        add_label(labels, path[0], path[1], G[path[0]][path[1]])
        add_label(labels, path[2], path[1], G[path[2]][path[1]])
        return

    # new root is the center of the chain
    root_index = len(path)/2 
    root = path[root_index]
    # connect every node to the root
    distance = 0
    for i in range(root_index - 1, -1, -1):
        distance += G[path[i]][path[i + 1]]
        add_label(labels, path[i], root, distance, False)

    distance = 0
    for i in range(root_index + 1, len(path)):
        distance += G[path[i]][path[i - 1]]
        add_label(labels, path[i], root, distance, False)

    connect_the_chain(G, path[:root_index - 1], max_labels - 1, labels)
    connect_the_chain(G, path[root_index + 1:], max_labels - 1, labels)
    pass

def create_labels(G):
    # find root and shortest paths to the root
    (root, root_distances, root_path) = determine_tree_root(G)
    max_labels = labels_needed(G)

    labels = {}
    labels[root] = {}
    labels[root][root] = 0
    chaines_checked = []
    for node in G.keys():
        if node == root:
            continue
        # add a node, add the root
        distance = root_distances[node]
        prev_node = root

        add_label(labels, node, node, 0, False)
        add_label(labels, node, root, distance, False)
        
        if len(root_path[node]) > max_labels:
            # connect the nodes on this route
            # we already used the root and node, so there are 2 labels less to use
            skip_node = False
            for chain in chaines_checked:
                if node in chain:
                    skip_node = True
                    break
            if skip_node:
                continue
            connect_the_chain(G, root_path[node][1:], max_labels - 2, labels)
            chaines_checked.append(root_path[node])
        else:
            # otherwise just connect all nodes on the path
            for hub in root_path[node]:
                if hub == node or hub == root:
                    continue
                distance -= G[prev_node][hub]
                add_label(labels, node, hub, distance)
                prev_node = hub

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
            for intermediate_node, dist in label_node.iteritems():
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

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

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
        N = 100
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
