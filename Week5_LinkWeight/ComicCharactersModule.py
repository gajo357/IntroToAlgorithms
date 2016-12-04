import unittest
import csv
from DijkstraHeapModule import dijkstra_extended

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = (G[node1]).get(node2, 0) + 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = (G[node2]).get(node1, 0) + 1
    return G

def read_file(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    G = {}
    characters = []
    with open(filename) as f:
        tsv = csv.reader(f, delimiter='\t')    
        for (character, title) in tsv:
            make_link(G, character, title)
            if character not in characters:
                characters.append(character)
    return (characters, G)

def create_characters_graph(full_graph, characters):
    char_graph = {}
    for character in characters:
        for comic in full_graph[character]:
            for co_char in full_graph[comic]:
                if co_char < character:
                    make_link(char_graph, character, co_char)
    return char_graph

def find_strongest_link(char_graph):
    max_weight = None
    strongest_link = None
    for (char1, links) in char_graph.items():
        for (char2, weight) in links.items():
            if max_weight is None or max_weight < weight:
                max_weight = weight
                strongest_link = (char1, char2)

    return strongest_link

def find_path_diffs(char_graph, node):
    (number_hops, path_hops) = dijkstra_extended(char_graph, node, lambda x : 1.0)
    (number_weight, path_weight) = dijkstra_extended(char_graph, node, lambda x : 1.0/x)
    diff_count = 0
    diffs = []
    for (co_char, path) in path_hops.items():
        if len(path) != len(path_weight[co_char]):
            diff_count += 1
            diffs.append((path, path_weight[co_char]))
    return diffs

class test_comic_characters(unittest.TestCase):
    #def test_strongest_link(self):
    #    (characters, full_graph) = read_file('marvel_chars.tsv')
    #    char_graph = create_characters_graph(full_graph, characters)
    #    strongest_link = find_strongest_link(char_graph)

    #    try:
    #        self.assertEqual(strongest_link, ('HUMAN TORCH/JOHNNY S', 'THING/BENJAMIN J. GR'))
    #        pass
    #    except:
    #        self.assertEqual(strongest_link, ('THING/BENJAMIN J. GR', 'HUMAN TORCH/JOHNNY S'))
    #        pass

    #def test_weighted_cases(self):
    #    (characters, full_graph) = read_file('marvel_chars.tsv')
    #    char_graph = create_characters_graph(full_graph, characters)
    #    node = 'SPIDER-MAN/PETER PAR'
    #    co_char = 'YAP'
    #    (number_hops, path_hops) = dijkstra_extended(char_graph, node, lambda x : 1.0)
    #    (number_weight, path_weight) = dijkstra_extended(char_graph, node, lambda x : 1.0/x)

    #    self.assertNotEqual(len(path_hops[co_char]), len(path_weight[co_char]))

    def test_weighted_graph(self):
        (characters, full_graph) = read_file('marvel_chars.tsv')
        char_graph = create_characters_graph(full_graph, characters)
        char_to_check = ['SPIDER-MAN/PETER PAR', 'GREEN GOBLIN/NORMAN ', 'WOLVERINE/LOGAN ', 'PROFESSOR X/CHARLES ', 'CAPTAIN AMERICA']
        diff_count = 0
        for c in char_to_check:
            diff_count += len(find_path_diffs(char_graph, c))
        print diff_count