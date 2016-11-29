import unittest

def remove_min(L):
    L[0] = L.pop()
    down_heapify(L, 0)
    return L

def parent(i): 
    return int((i-1)/2)
def left_child(i): 
    return 2*i+1
def right_child(i): 
    return 2*i+2
def is_leaf(L,i): 
    return (left_child(i) >= len(L)) and (right_child(i) >= len(L))
def one_child(L,i): 
    return (left_child(i) < len(L)) and (right_child(i) >= len(L))

#
# write up_heapify, an algorithm that checks if
# node i and its parent satisfy the heap
# property, swapping and recursing if they don't
#
# L should be a heap when up_heapify is done
#
def up_heapify(L, i):
    # this is the root node, we're done
    if i == 0:
        return
    p = parent(i)
    # nothing to do, we are satisfied
    if L[i] >= L[p]:
        return
    
    # swap parrent and the child
    (L[i], L[p]) = (L[p], L[i])
    # up heapify starting from the parent
    up_heapify(L, p)
    return


# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its immediate children
def down_heapify(L, i):
    # If i is a leaf, heap property holds
    if is_leaf(L, i): 
        return
    # If i has one child...
    if one_child(L, i):
        # check heap property
        if L[i] > L[left_child(i)]:
            # If it fails, swap, fixing i and its child (a leaf)
            (L[i], L[left_child(i)]) = (L[left_child(i)], L[i])
        return
    # If i has two children...
    # check heap property
    if min(L[left_child(i)], L[right_child(i)]) >= L[i]: 
        return
    # If it fails, see which child is the smaller
    # and swap i's value into that child
    # Afterwards, recurse into that child, which might violate
    if L[left_child(i)] < L[right_child(i)]:
        # Swap into left child
        (L[i], L[left_child(i)]) = (L[left_child(i)], L[i])
        down_heapify(L, left_child(i))
        return
    else:
        (L[i], L[right_child(i)]) = (L[right_child(i)], L[i])
        down_heapify(L, right_child(i))
        return

def add_to_heap(heap, v):
    heap.append(v)
    up_heapify(heap, len(heap) - 1)

# build_heap
def build_heap(L):
    for i in range(len(L)-1, -1, -1):
        down_heapify(L, i)
    return L

class test_heap(unittest.TestCase):
    def test_remove_min(self):
        L = [i for i in range(10)]
        build_heap(L)
        remove_min(L)
        # now, the new minimum should be 1
        self.assertEqual(L[0], 1)
    def test_up_heapify(self):
        L = [2, 4, 3, 5, 9, 7, 7]
        L.append(1)
        up_heapify(L, 7)
        self.assertEqual(1, L[0])
        self.assertEqual(2, L[1])