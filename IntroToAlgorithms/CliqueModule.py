def clique_numberOfEdges(n):
    # Return the number of edges
    # Try to use a mathematical formula...
    edges = 0
    i = n - 1
    while i > 0:
        edges += i
        i -= 1
    return edges