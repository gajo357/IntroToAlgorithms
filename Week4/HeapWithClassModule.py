import HeapModule

class heap_node:
    def __init__(self, name, value):
        self.name = name
        self.value = value

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

def remove_min(L):
    minimum = L[0]
    temp = L.pop()
    if len(L) > 0:
        L[0] = temp
        down_heapify(L, 0)
    return minimum

def add_to_heap(heap, v):
    heap.append(v)
    up_heapify(heap, len(heap) - 1)