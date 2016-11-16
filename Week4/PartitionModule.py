import unittest
import random

#
# Write partition to return a new array with 
# all values less then `v` to the left 
# and all values greater then `v` to the right
#

def find_ith_smallest(L, index):
    # for a small case, just sort the array and return the i-th element
    if len(L) < 6:
        sort = sorted(L)
        return sort[index]

    # split L into smaller lists of lenght 5
    n = 5
    chunks = [L[i:i + n] for i in range(0, len(L), n)]
    # find median for each chunk
    medians = [find_median(l) for l in chunks]
    # find median of all medians
    median = find_median(medians)

    # partition around median
    (smaller, middle, bigger) = partition(L, median)
    if index < len(smaller):
        return find_ith_smallest(smaller, index)
    if index > len(smaller) + len(middle):
        return find_ith_smallest(bigger, index - (len(smaller) + len(middle)))
    return middle[0]

def find_median(L):
    return find_ith_smallest(L, int((len(L) - 1)/2))

#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the absolute value of the difference
# between each element in L and x: SUM_{i=0}^{n-1} |L[i] - x|
# 
# Your code should run in Theta(n) time
#
def minimize_absolute(L):
    # to minimaze this sum, we find the derivative
    # the derivative over x is -1*SUM_{i=0}^{n-1} ((L[i] - x)/(|L[i] - x|))
    # next we need the value when this derivative is equal to 0
    # there are 2 cases:
    #   x < L[i] which yealds the element is 1
    #   x > L[i] which yealds the element is -1
    # if there is an even number of elements, the sum of them is 0, if x is median
    return find_median(L)

def find_mean(L):
    return sum(L)*1.0/len(L)



#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the square of the difference
# between each element in L and x: SUM_{i=0}^{n-1} (L[i] - x)^2
# 
# Your code should run in Theta(n) time
# 
def minimize_square(L):
    # to minimaze the sum of squares, we find the derivative
    # the derivative over x is 2*SUM_{i=0}^{n-1} (x - L[i])
    # next we need the value when this derivative is equal to 0
    # which yealds x = SUM_{i=0}^{n-1}(L[i])/n, which is the mean value
    return find_mean(L)

def partition(L, v):
    smaller = []
    bigger = []
    middle = []
    for val in L:
        if val < v:
            smaller.append(val)
        elif val > v:
            bigger.append(val)
        else:
            middle.append(val)

    return (smaller, middle, bigger)

def rank(L, v):
    pos = 0
    for val in L:
        if val < v:
            pos += 1
    return pos

def top_k(L, k):
    v = L[random.randrange(len(L))]
    (left, middle, right) = partition(L, v)
    if len(left) == k: 
        return left
    if len(left) + 1 == k:
        return left + [v]
    if len(left) > k:
        return top_k(left, k)
    return left + [v] + top_k(right, k - len(left) - 1)

class test_partition(unittest.TestCase):
    def test_partition(self):
        L = [31, 45, 91, 51, 66, 82, 28, 33, 11, 89, 84, 27, 36]
        v = 84
        (left, middle, right) = partition(L, v)
        self.assertEqual(left, [31, 45, 51, 66, 82, 28, 33, 11, 27, 36])
        self.assertEqual(right, [91, 89])
    def test_topk(self):
        L = [31, 45, 91, 51, 66, 82, 28, 33, 11, 89, 84, 27, 36]
        top10 = top_k(L, 10)
        result = [31, 45, 51, 66, 82, 28, 33, 11, 27, 36]
        self.assertEqual(len(top10), len(result))
        for v in result:
            self.assertTrue(v in top10)
    def test_median(self):
        L = [31, 45, 91, 51, 66, 82, 28, 33, 11, 89, 84, 27, 36]
        median = find_median(L)
        self.assertEqual(median, 36)