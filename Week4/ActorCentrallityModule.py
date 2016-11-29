import unittest
import csv
import HeapModule
import HeapWithClassModule

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

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

class test_actor_centrallity(unittest.TestCase):
    def test(self):
        (actors, G) = read_file('imdb-1.tsv')
        v = 'Tatasciore, Fred'
        heap = []
        for actor in actors:
            HeapWithClassModule.add_to_heap(heap, HeapWithClassModule.heap_node(actor, centrality(G, actor)))
        top = []
        for i in range(20):
            actor = HeapWithClassModule.remove_min(heap)
            top.append(actor)
            #print(actor.name + " " + str(actor.value))
        self.assertEqual(top[0].name == v)
        self.assertEqual(top[19].name == 'Hoffman, Dustin')