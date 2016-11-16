import unittest
import csv
import HeapModule

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its immediate children
def down_heapify(L, i):
    # If i is a leaf, heap property holds
    if HeapModule.is_leaf(L, i): 
        return
    # If i has one child...
    if HeapModule.one_child(L, i):
        # check heap property
        if L[i].value > L[HeapModule.left_child(i)].value:
            # If it fails, swap, fixing i and its child (a leaf)
            (L[i], L[HeapModule.left_child(i)]) = (L[HeapModule.left_child(i)], L[i])
        return
    # If i has two children...
    # check heap property
    if min(L[HeapModule.left_child(i)].value, L[HeapModule.right_child(i)].value) >= L[i].value: 
        return
    # If it fails, see which child is the smaller
    # and swap i's value into that child
    # Afterwards, recurse into that child, which might violate
    if L[HeapModule.left_child(i)].value < L[HeapModule.right_child(i)].value:
        # Swap into left child
        (L[i], L[HeapModule.left_child(i)]) = (L[HeapModule.left_child(i)], L[i])
        down_heapify(L, HeapModule.left_child(i))
        return
    else:
        (L[i], L[HeapModule.right_child(i)]) = (L[HeapModule.right_child(i)], L[i])
        down_heapify(L, HeapModule.right_child(i))
        return
    
def up_heapify(L, i):
    # this is the root node, we're done
    if i == 0:
        return
    p = HeapModule.parent(i)
    # nothing to do, we are satisfied
    if L[i].value >= L[p].value:
        return
    
    # swap parrent and the child
    (L[i], L[p]) = (L[p], L[i])
    # up heapify starting from the parent
    up_heapify(L, p)
    return

def read_file(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    G = {}
    actors = []
    with open(filename) as f:
        tsv = csv.reader(f, delimiter='\t')
        for (actor, title, year) in tsv:
            make_link(G, actor, title + ' ' + year)
            if actor not in actors:
                actors.append(actor)
    return (actors, G)

class actor_node:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def add_to_heap(heap, v):
    heap.append(v)
    up_heapify(heap, len(heap) - 1)

def centrality(G, v):
    distance_from_start = {}
    open_list = [v]
    distance_from_start[v] = 0
    while len(open_list) > 0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current] + 1
                open_list.append(neighbor)
    return float(sum(distance_from_start.values()))/len(distance_from_start)

def remove_min(L):
    minimum = L[0]
    L[0] = L.pop()
    down_heapify(L, 0)
    return minimum

class test_actor_centrallity(unittest.TestCase):
    def test(self):
        (actors, G) = read_file('imdb-1.tsv')
        v = 'Tatasciore, Fred'
        heap = []
        for actor in actors:
            add_to_heap(heap, actor_node(actor, centrality(G, actor)))
        top = []
        for i in range(20):
            actor = remove_min(heap)
            top.append(actor)
            #print(actor.name + " " + str(actor.value))
        self.assertEqual(top[0].name == v)
        self.assertEqual(top[19].name == 'Hoffman, Dustin')