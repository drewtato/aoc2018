import sys
from contextlib import contextmanager
from collections import defaultdict as dd
# import os
# import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import deque as dq
# from copy import deepcopy as dc

DEBUG,PRINT,OUT,outfile,infile = False,False,False,None,'input.txt'
for arg in sys.argv[1:]:
    if OUT:
        outfile = arg if arg[0] != '-' else 'output.txt'
        OUT = False
    elif arg == '-d':
        DEBUG = True
    elif arg == '-p':
        PRINT = True
    elif arg == '-o':
        OUT = True
    elif arg[0] != '-':
        infile = arg
    else:
        print(f'No "{arg}" arg."')
        sys.exit(1)
@contextmanager
def fileOrStdout(filename=None):
    if filename:
        fh = open(filename, 'w')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()
def replacer(inp, remove=[], replace=[]):
    pairs = []
    for reading,default in [(remove,''),(replace,' ')]:
        if len(reading) == 1:
            reading = [c for c in reading[0]]
        for line in reading:
            items = line.split(' ')
            first = items[0] if items[0] else ' '
            second = items[1] if len(items) > 1 else default
            pairs.append((first, second))
    for k,v in pairs:
        inp = inp.replace(k,v)
    return inp
with open(infile, 'r') as inp:
    inp = inp.read()
while inp[-1].isspace():
    inp = inp[:-1]
def pData(data, out, revMap):
    if PRINT:
        for row in data:
            for c in row:
                out.write(revMap[c])
            out.write('\n')
        out.write('\n')

removals = []
replacements = [
    # '<',
    # '>',
    # '(',
    # ')',
    # '[',
    # ']',
    # ':',
    # ',',
    # ';',
    # '=',
    # '\n',
]
inp = replacer(inp, removals, replacements)
data = []
dataMap = dd(lambda: 0)
dataMap.update({
    '.':0,
})
revMap = {v:k for k,v in dataMap.items()}
for line in inp.split('\n'):
    row = []
    for c in line:
        row.append(dataMap[c])
    data.append(row)
# print(data)

def part1(info):
    # data = info[0]
    pData(*info)

try:
    with fileOrStdout(outfile) as out:
        info = data,out,revMap
        if DEBUG:
            print(inp)
        
        part1(info)

except KeyboardInterrupt:
    print('Interrupted')
except NotImplementedError:
    print('Not implemented')
