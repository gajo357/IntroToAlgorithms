from HeapModule import parent
from HeapModule import one_child
from HeapModule import right_child
from HeapModule import left_child
from HeapModule import is_leaf

class heap_node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.index = -1

def swap(heap, i, j):
    heap[i].index = j
    heap[j].index = i
    (heap[i], heap[j]) = (heap[j], heap[i])  
    
# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its immediate children
def down_heapify(heap, i):
    # If i is a leaf, heap property holds
    if is_leaf(heap, i): 
        return

    left_index = left_child(i)
    right_index = right_child(i)
    
    # If i has one child...
    if one_child(heap, i):
        # check heap property
        if heap[i].value > heap[left_index].value:
            # If it fails, swap, fixing i and its child (a leaf)
            swap(heap, i, left_index)
        return
    # If i has two children...
    # check heap property
    if min(heap[left_index].value, heap[right_index].value) >= heap[i].value: 
        return
    # If it fails, see which child is the smaller
    # and swap i's value into that child
    # Afterwards, recurse into that child, which might violate
    if heap[left_index].value < heap[right_index].value:
        # Swap into left child
        swap(heap, i, left_index)
        down_heapify(heap, left_index)
        return
    else:
        swap(heap, i, right_index)
        down_heapify(heap, right_index)
        return
    
def up_heapify(heap, i):
    # this is the root node, we're done
    if i == 0:
        return
    p = parent(i)
    # nothing to do, we are satisfied
    if heap[i].value >= heap[p].value:
        return
    
    # swap parrent and the child
    swap(heap, i, p)
    # up heapify starting from the parent
    up_heapify(heap, p)
    return

def remove_min(heap):
    minimum = heap[0]
    temp = heap.pop()
    if len(heap) > 0:
        heap[0] = temp
        temp.index = 0
        down_heapify(heap, 0)
    return minimum

def add_to_heap(heap, v):
    index = len(heap)
    heap.append(v)
    v.index = index
    up_heapify(heap, index)