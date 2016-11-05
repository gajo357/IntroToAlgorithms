def clique_numberOfEdges(n):
    # Return the number of edges
    # Try to use a mathematical formula...
    return n*(n-1)/2

import unittest

class clique_test(unittest.TestCase):
    def test_numberOfEdges(self):
        self.assertEqual(clique_numberOfEdges(9), 36)
    