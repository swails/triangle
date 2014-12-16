#!/usr/bin/env python
"""
The way this solution works is to divide up the problem of solving a "large"
triangle into subsets of smaller triangles. The optimum sum of each triangle is
the largest value between the "tip" value of the current triangle and the sum of
the value of the subtriangle whose tip is lower-left and the subtriangle whose
tip is lower-right.  For example:

                1
              3   2
            4   6   5
         10   9   8   7

In the above example, the solution can be broken down into:

    1 +    3         |  1 +     2
         4   6       |        6   5
       10  9   8     |      9   8   7

Each of those 3-by-3 subtriangles can be further broken down into:

    3 +   4    |  3 +  6     ||  2 +   6      |  2 +   5
        10 9   |      9 8    ||       9 8     |       8 7

And then the solution adds up:
    17             -- 18 --  ||  -- 17 --           15

So the 3-row subtriangle above left has a optimum solution of 18 and the
subtriangle to the right has an optimum solution of 17.  Meaning that the
optimum solution is from the subtriangle to the left, with a final answer of 19.
This is similar to the recursive search solution, and scales similarly (i.e.,
O(2^N); which is to say, it is infeasible for triangles above a certain size).

It still contains useful functionality that will be imported to the solution
that is actually scalable, though. This module is also a reasonable reflection
of my Python programming skill and style.
"""
from __future__ import division

import sys
from collections import OrderedDict

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
        beginkey = (1 - len(values)) / 2
        for i, val in enumerate(values):
            self[beginkey+i] = val

    def sub_data(self, begin_key, num_vals):
        """
        Returns a list starting form begin_key and having num_vals
        """
        return [self[begin_key+x] for x in range(num_vals)]

class Triangle(object):
    """
    A triangle of numbers like the following

                1
              2   3
            4   5   6
          7   8   9   10
       11  12   13  14  15
     16  17  18   19   20  21
                ...

    Parameters
    ----------
    data : list, 2-D int
        List of lists of numbers where each list is the row of integers
    """

    def __init__(self, data):
        self.data = []
        for row in data:
            r = Row()
            r.data = row
            self.data.append(r)
        self.rank = len(data)

    def __str__(self):
        """
        Print a formatted triangle
        """
        retstr = ''
        for row in self.data:
            retstr += (' '.join([str(x) for x in row.data])) + '\n'
        return retstr.strip()

    def subtriangle(self, row, index):
        """
        Create a subtriangle starting from the current triangle at a given row
        and starting index. For instance, a subtriangle of the example given in
        the Triangle docstring would be:

                2
              4   5
            7   8   9
          11 12   13  14
        16  17  18  29  20

        Parameters
        ----------
        row : int
            The row number from which to start the new triangle
        index : float
            The index that forms the "tip" of the new triangle

        Returns
        -------
        subtriangle : Triangle
            The Triangle instance that forms the sub-triangle
        """
        data = []
        for i, j in enumerate(range(row, self.rank)):
            data.append(self.data[j].sub_data(index, i+1))
            index -= 0.5
        return Triangle(data)

    def solve(self):
        """
        Solves the triangle using the technique of subtriangles, as described in
        the module docstring
        """
        if self.rank <= 4:
            d = self.data
            if self.rank == 4:
                # Only 8 different possibilities:
                # 0,  0.5,  1,  1.5
                # 0,  0.5,  1,  0.5
                # 0,  0.5,  0,  0.5
                # 0,  0.5,  0, -0.5
                # 0, -0.5,  0,  0.5
                # 0, -0.5,  0, -0.5
                # 0, -0.5, -1, -0.5
                # 0, -0.5, -1, -1.5
                return max([d[0][0] + d[1][0.5] + d[2][1.0] + d[3][1.5],
                            d[0][0] + d[1][0.5] + d[2][1.0] + d[3][0.5],
                            d[0][0] + d[1][0.5] + d[2][0.0] + d[3][0.5],
                            d[0][0] + d[1][0.5] + d[2][0.0] + d[3][-0.5],
                            d[0][0] + d[1][-0.5] + d[2][0.0] + d[3][0.5],
                            d[0][0] + d[1][-0.5] + d[2][0.0] + d[3][-0.5],
                            d[0][0] + d[1][-0.5] + d[2][-1.0] + d[3][-0.5],
                            d[0][0] + d[1][-0.5] + d[2][-1.0] + d[3][-1.5]])
            elif self.rank == 3:
                # Only 4 different possibilities
                # 0,  0.5,  1
                # 0,  0.5,  0
                # 0, -0.5,  0
                # 0, -0.5, -1
                return max([d[0][0] + d[1][0.5] + d[2][1],
                            d[0][0] + d[1][0.5] + d[2][0],
                            d[0][0] + d[1][-0.5] + d[2][0],
                            d[0][0] + d[1][-0.5] + d[2][-1]])
            elif self.rank == 2:
                # Only 2 different possibilities
                # 0,  0.5
                # 0, -0.5
                return max([d[0][0] + d[1][0.5],
                            d[0][0] + d[1][-0.5]])
            elif self.rank == 1:
                return d[0][0]
        
        # Return the maximum of the tip of this triangle + the tip of the
        # previous triangle
        return max(self.data[0][0] + self.subtriangle(1, -0.5).solve(),
                   self.data[0][0] + self.subtriangle(1, 0.5).solve())

    def truncate(self, nrows):
        """
        This truncates the current triangle by throwing away the last `nrows`
        rows of the triangle. (This is used for the "reductions" solution)

        Parameters
        ----------
        nrows : int
            The number of rows from the end of the triangle to discard

        Notes
        -----
        If `nrows` is greater than or equal to the current rank or if it is
        negative, a ValueError is raised.
        """
        if nrows < 0 or nrows >= self.rank:
            raise ValueError('You must discard between 0 and %d rows; not %d' %
                             (self.rank, nrows))
        row = 0
        while row < nrows:
            self.data.pop() # efficient for lists
            self.rank -= 1
            row += 1

def read_triangle_file(fname):
    """ Reads the file name and instantiates (and returns) a Triangle """
    with open(fname, 'r') as f:
        data = []
        for line in f:
            data.append([int(x) for x in line.split()])
        return Triangle(data)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        fname = sys.argv[1] # Allow us to input a file name
    else:
        fname = 'testtriangle.txt'

    print('The optimal solution is %d' % read_triangle_file(fname).solve())
