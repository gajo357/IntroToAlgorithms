import unittest
from HeapWithClassModule import heap_node, add_to_heap, down_heapify, up_heapify, remove_min
from DijkstraHeapModule import dijkstra_extended

#
# write a function, `top_two` that takes in a graph and a starting
# node and returns two paths, the first and second shortest paths,
# for all the other nodes in the graph.  You can assume that the 
# graph is connected.
#

def top_two(graph, start):
    # your code here
    #
    # the result should be a dictionary, containing a mapping between
    # every node in the graph, except the start node, to a list.  The
    # list should contain two elements.  Each element should contain a
    # cost to get to that node and the path followed.  See the `test`
    # function for an example
    #

    result = {}

    # find shortest path to every node
    (final_dist, paths_dict) = dijkstra_extended(graph, start)
    for node in final_dist:
        # assign this as the shortest path
        result[node] = [(final_dist[node], paths_dict[node])]

    for node1 in graph:
        for node2 in graph[node1]:
            # remove the edge
            weight = graph[node1][node2]
            del graph[node1][node2]
            
            # find shortest path
            (second_dist, second_paths) = dijkstra_extended(graph, start)
            for node in second_dist:
                if second_paths[node] == result[node][0][1]:
                    continue
                # check if we have imporoved #2 
                # if we only have the shortest path, this is the second best
                if len(result[node]) == 1:
                    result[node].append((second_dist[node], second_paths[node]))
                # check if the new route is shorted
                elif result[node][1][0] > second_dist[node]:
                    result[node][1] = (second_dist[node], second_paths[node])

            # reintroduce it to the graph
            graph[node1][node2] = weight
            
    return result

class test_top_two(unittest.TestCase):
    def test(self):
        graph = {'a':{'b':3, 'c':4, 'd':8},
                 'b':{'a':3, 'c':1, 'd':2},
                 'c':{'a':4, 'b':1, 'd':2},
                 'd':{'a':8, 'b':2, 'c':2}}
        result = top_two(graph, 'a') # this is a dictionary
        b = result['b'] # this is a list
        b_first = b[0] # this is a list
        self.assertEqual(b_first[0], 3) # the cost to get to 'b'
        self.assertEqual(b_first[1], ['a', 'b']) # the path to 'b'
        b_second = b[1] # this is a list
        self.assertEqual(b_second[0], 5) # the cost to get to 'b'
        self.assertEqual(b_second[1], ['a', 'c', 'b'])



