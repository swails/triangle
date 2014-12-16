#!/usr/bin/env python
"""
This method works similarly to the subtriangles method (and uses a lot of the
same functionality), but it avoids the atrocious exponential scaling in the
other two solutions.

The way this solution works is to reduce the original triangle into smaller and
smaller triangles by starting from the bottom and replacing each row by the sum
of the subtriangle beginning from that point. This is quite feasible, because
for the Nth row of the triangle, there are only N subtriangles originating from
that row (each number in the row can be the "point" of the subtriangle). Each
value in that row is replaced by the maximum sum of that subtriangle. Then we
move up several rows and do it again, repeating this process until the triangle
is of a feasible size (e.g., a 4-row triangle has only 8 possible values). This
is shown diagrammatically below using the example from subtriangles.py

                1
              3   2
            4   6   5      <------
         10   9   8   7

Using subtriangles with 2 rows, we start from the row indicated above. So we
have to solve the triangles:

    4       6       5
  10 9     9 8     8 7

These answers are, respectively, 14, 15, and 13.  So the original triangle above
is reduced to:

                1
              3   2        <------
           14  15   13

Starting again from the indicated line, we solve the triangles:

    3       2
  14 15   15 13

These answers are, respectively, 18 and 17.  So the second iteration of the
original triangle (whose rows were reduced to 3) is:

                1
             18   17

And this is small enough to solve very easily: 19.
"""
from __future__ import division

from subtriangles import read_triangle_file

if __name__ == '__main__':
    # I would use argparse, but that would require an external dependency OR
    # Python 2.7 or greater. Since I want this to be compatible with Python
    # 2.4+, and I don't need any argparse-specific options, I will just use
    # optparse
    from optparse import OptionParser
    import sys

    parser = OptionParser()
    parser.add_option('-i', '--input-file', default='testtriangle.txt',
                      help='Input triangle data file. Default is %default',
                      metavar='FILE')
    parser.add_option('-s', '--size', default=4, type='int', metavar='INT',
                      help='The number of rows after which the triangle is '
                      'solved directly rather than continuing to reduce its '
                      'dimensionality. This is also the size subtriangle we '
                      'will reduce the original triangle by each step. '
                      'Default is %default')

    opt, arg = parser.parse_args()

    if arg:
        sys.exit('Unexpected arguments: [%s]' % ', '.join(arg))

    # Read the original triangle
    triangle = read_triangle_file(opt.input_file)

    size = opt.size # slight optimization

    # Reduce the triangle
    while triangle.rank > size:
        # Take the rank-size'th row, compute the subtriangle solutions for every
        # point on that row, and replace that row's entry with the subtriangle
        # solutions, then drop those rows from the triangle
        row = triangle.rank - size
        rowdata = triangle.data[row]
        for key in rowdata:
            rowdata[key] = triangle.subtriangle(row, key).solve()
        triangle.truncate(size-1)

    print('The optimal solution is %d' % triangle.solve())
