What is it
==========

The triangle problem!! The task is to create an algorithm that will find the
maximum sum of a path _through_ a triangle of numbers in which only adjacent
entries from the rows below may be taken as part of the path.

For example, consider the following triangle:

```
        1
      2   3
   10   8   4
  7   1   20  5
```

The optimum path is fairly clear... 1 + 3 + 8 + 20 = 32.  Triangles with 2 rows
have 2 possible sums.  Add a third row and the number of possible sums jumps to
4.  Add the 4th row and the number of possible sums jumps to 8.  A 5th row will
result in 16 possible sums... and so on.  The number of paths through the
triangle scales as O(2^N), so for large triangles (of, say, 100 rows), a
brute-force search through all of the paths quickly becomes infeasible.

Creating test cases
===================

The `generate_triangle.py` file included here creates a triangle text file that
can be read by these scripts and fills the triangle with random numbers between
1 and 10000.  It takes as an input parameter the number of rows you want in your
triangle, allowing you to quickly generate test cases of any size.

The solutions
=============

There are 3 solutions posted here in different files, described below. The first
algorithm was a naive algorithm that I devised almost as soon as I read the
problem.  Since it scaled so poorly, and takes too long for a 100-row triangle,
I tried another algorithm.

The second algorithm was a little bit more thought out, but I was afraid it
would suffer from the same poor scaling issues... and indeed it did (it, too,
scales as O(2^N)). I still think it's an elegant solution, but that does not
count for much when it is too inefficient to be of use.  It _does_, however,
contain functionality that I found useful in my last approach.

This forced me to consider an algorithm that reduced the size of the problem to
avoid the O(2^N) scaling problem that resulted from the rapidly growing number
of possible pathways. This final approach is very efficient -- it scales as
O(N).  Whereas the first two solutions are unable to process a 100-row triangle
in over 8 hours using pypy, this approach can solve it in less than 1 second.

See the subsections below for more details.

recursive_search.py
-------------------

In this algorithm, we recursively search down a path, with the final row ending
the recursion and returning the running sum back up that path. The sum to the
right and the sum to the left are both evaluated, and the greater one is
returned up the recursion chain.

This method, however, traverses all of the possible paths, and so it scales as
O(2^N), making it infeasible for use with the `testtriangle.txt` file included
here.

But feel free to use `generate_triangle.py` to create smaller triangles to check
how the cost of this solution grows.

One slight modification made to this solution is a minor optimization.  For each
row, we can compute an absolute maximum possible sum starting from a certain
row.  This is done by simply adding up the largest value for each row starting
from the row of interest.  Therefore, at each depth we can check our current
path and see if it is even possible to exceed the largest sum we have already
found, and simply return early if it's not.  This cuts down on the number of
branches the algorithm needs to traverse (possibly very significantly), but
except in contrived examples will not appreciably affect the O(N^2) scaling of
the solution.

Clearly a better algorithm is needed to solve large triangles.

subtriangles.py
---------------

This module actually contains a set of useful classes -- `Triangle` and `Row`.
The way this solution works is to evaluate the optimum triangle sum as the sum
of the "tip" of the triangle with the sums of the two triangles on the row
immediately below it.  These triangles, themselves, can be broken down in the
same way, and you can continue to do this until the resulting triangles are
small enough to figure out quickly.  It is in the same vein as the recursive
search, although in my opinion the solution is a bit more elegant.  For a more
detailed schematic of how this algorithm works, see the docstring in
`subtriangles.py`.

However, the overhead involved with creating sub-`Triangle` objects is far
greater than the overhead involved with the original recursion (and there is no
early-branch termination here), so this approach is actually substantially
slower than the `recursive_search.py` approach above.

Clearly a better algorithm is needed to solve large triangles.

reductions.py
-------------

This approach is quite radically different from the previous two approaches.
Whereas the previous two approaches started from the top and traced out paths
down, this approach started from the _bottom_ and tried to "condense" the
triangle.  The basic premise is this:

At each point in a specific row, the maximum sum of all pathways from that point
to the final row is invariant (i.e., it doesn't matter _how_ you get there; once
you get to that point, the maximum possible additional value you can add to the
sum is always the same from that point on).  So we can pre-compute this.  We can
start from the 4th-to-last row and compute the optimum sum of the subtriangles
emanating from each point in that row.  Those sums then replace those points in
the 4th-to-last row, and the final 3 rows are lopped off.  You then move up and
do this again until you are left with a triangle that is small enough to solve
using one of the methods described above.  Since I use the code from
`subtriangles.py` to extract the subtriangles that I solve in the 4th-to-last
row, I simply use the algorithm in `subtriangles.py` (i.e., `Triangle.solve`) to
solve each of these subtriangles and the resulting, reduced triangle.

Note that there is nothing inherently "special" about choosing triangles with 4
rows to reduce the dimensionality of the problem.  It is, however, the most rows
in which I consider the number of possible solutions reasonably enumberable
(there are 8).  So evaluating the sub-triangles for the 4th-to-last rows is
_very_ cheap, and it results in a much larger dimensionality reduction
(percentage-wise) than picking triangles of size 2 or 3.  Above 4, the growth in
the size of the possible solutions rapidly outpaces the decrease in the number
of "steps" required to reduce the triangle to something reasonably solvable.

Again, see the docstring in `reductions.py` for a more thorough description.

The Answer
==========

While I would love for the answer to be 42, it is not.  The solution to
`testtriangle.txt` posted here is 724269 (but there's a 42 _in_ it :)).
