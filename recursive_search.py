#!/usr/bin/env python
"""
This is a naive solution, and somewhat stupid as well.  Except in lucky
circumstances, this will scale very poorly for large triangles. It is also
rather poorly, and quickly written.  However, it reflects what is in my opinion
a neat recursive algorithm, which is why I have included it. This algo reaches a
maximum recursion depth equal to the number of rows in the triangle.

One neat aspect used for optimizing the search is to construct a list of the
"maximum theoretically possible" value for the final answer starting from each
row which is calculated by adding up the maximum values in each row down to the
bottom together. We test at each depth -- if the current running sum plus the
maximum possible remaining values is less than or equal to the value of a sum
*already found*, then we can stop searching down from that point and eliminate a
lot of branches (potentially).

However neat, this recursive algorithm is wildly inefficient for large
triangles, even with the branch prediction built in (in pathological cases, that
prediction actually makes things worse). This scales formally O(2^N), which is
rather atrocious exponential scaling.
"""

from __future__ import division
from collections import OrderedDict

import sys

if len(sys.argv) == 2:
    fname = sys.argv[1] # Allow us to input a file name
else:
    fname = 'testtriangle.txt'

class Row(OrderedDict):
    """
    A row in the triangle indexed relative to the row above. The absolute
    indexing is set by assuming that the single value at the top of the triangle
    is 0. The indexing scheme is:

    (N-1)/2  (N-1)/2+1  (N-1)/2+2  ... (N-1)/2+(N-1)  (N-1)/2+N

    According to this numbering scheme, even rows have half-integral indexes
    while odd rows have integral indexes. Therefore, each path can only have the
    index increase or decrease by 0.5 in each row.
    """
    @property
    def data(self):
        return [self[x] for x in self]

    @data.setter
    def data(self, values):
        # Clear out the existing data
        self.clear()
        # Add the data in
        beginkey = (1 - len(words)) / 2
        for i, val in enumerate(values):
            self[beginkey+i] = val

with open(fname, 'r') as f:
    rows = []
    maxvals = [] # Maximum value in each row
    for line in f:
        words = [int(x) for x in line.split()]
        maxvals.append(max(words))
        maxkey = (len(words) - 1) / 2
        row = Row()
        row.data = words
        rows.append(row)

# Keep track of the absolute maximum possible value left, regardless of whether
# or not the numbers are adjacent. It should be a good way of efficiently
# terminating some of the searches when it gets low enough in the branching
# search
maxpossible = [sum(maxvals[i:]) for i in range(len(rows))]

# Keep track of the largest value we've currently found
maxfound = 0

lastrow = len(rows) - 1 # pre-compute

# Define the recursive search
def search_down(row, index, running_sum):
    """
    A recursive search function that takes the current row and index and looks
    to the right, then to the left when looking for the sum of that path.

    Parameters
    ----------
    row : int
        The current row we are on, starting from 0
    index : float
        The current index that the pointer is on in this row
    running_sum : int
        The current value of all numbers in the path so far

    Returns
    -------
    value : int
        The value of the sum along the completed search route. This value is not
        guaranteed to be correct if it has no chance of being the largest value,
        since the iteration may be truncated early. Since we are only interested
        in the maximum possible value, this is not a problem
    """
    global maxfound, lastrow
    # First thing we do is add our current value to the running_value
    currow = rows[row]
    running_sum += currow[index]
    if row == lastrow:
        return running_sum
    # If we can't possibly beat our best, stop recursing now
    if running_sum + maxpossible[row] < maxfound:
        return running_sum
    # Now look to the right
    rightsum = search_down(row+1, index+0.5, running_sum)
    maxfound = max(maxfound, rightsum)
    leftsum = search_down(row+1, index-0.5, running_sum)
    maxfound = max(maxfound, leftsum)

# Make sure we set our recursion limit to at least the total number of rows
sys.setrecursionlimit(max(sys.getrecursionlimit(), len(rows)))

search_down(0, 0, 0)

print('The optimal solution is %d' % maxfound)
