import unittest

def star_network(n):
    # return number of edges
    return n-1

class test_star(unittest.TestCase):
    def test_numberOfEdges(self):
        self.assertEqual(star_network(5), 4)