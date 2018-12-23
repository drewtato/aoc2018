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

removals = ['posr=<>']
replacements = [
    # '<',
    # '>',
    # '(',
    # ')',
    # '[',
    # ']',
    # ':',
     ',',
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
    for c in line.split():
        row.append(int(c))
    data.append(row)
# print(data)

def part1(info):
    # data = info[0]
    # pData(*info)
    m,best,bpos = max([(r,i,(x,y,z))\
    for i,(x,y,z,r) in enumerate(data)])
    inrad = 0
    for nano in data:
        distance = 0
        for pos,b in zip(nano[:3],bpos):
            distance += abs(pos - b)
        if distance <= m:
            inrad += 1
    return inrad

def part2(data):
    maxes = [-1000000000] * 3
    mins = [1000000000] * 3
    for item in data:
        for i,dim in enumerate(item[:-1]):
            maxes[i] = max(maxes[i],dim)
            mins[i] = min(mins[i],dim)
    best = (0,0)
    
    return best

try:
    with fileOrStdout(outfile) as out:
        info = data,out,revMap
#        if DEBUG:
#            print(inp)
        
        inrad = part1(info)
        print(inrad)
        best = part2(data)
        print(best[1])

except KeyboardInterrupt:
    print('Interrupted')
