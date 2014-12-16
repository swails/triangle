#!/usr/bin/env python

"""
This program will generate a triangle text data file, used to test the various
solution methods.
"""

import random
from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option('-s', '--size', type='int', default=10, metavar='INT',
                  help='The number of rows of the test triangle to generate. '
                  'Default %default')
parser.add_option('-o', '--output', default='testtriangle.txt', metavar='FILE',
                  help='The output file to write the triangle to. Default '
                  '%default')
opt, arg = parser.parse_args()

# So we only have to change the range in one place
genrand = lambda: random.randint(1, 10000)

if arg:
    sys.exit('Unexpected arguments [%s]' % ', '.join(arg))

if opt.size <= 0:
    sys.exit('Triangle size must be >= 0')

if opt.output == 'triangle.txt':
    sys.exit('I will not overwrite the master triangle file!')

with open(opt.output, 'w') as f:
    for i in range(opt.size):
        f.write('%d' % genrand())
        for j in range(i):
            f.write(' %d' % genrand())
        f.write('\n')

print('Done!')
