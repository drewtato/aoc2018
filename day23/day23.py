import sys
from contextlib import contextmanager
from collections import defaultdict as dd
# import os
import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import deque as dq
# from copy import deepcopy as dc
import math

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
    m,bpos = max([(r,(x,y,z)) for x,y,z,r in data])
    inrad = 0
    for nano in data:
        distance = 0
        for pos,b in zip(nano[:3],bpos):
            distance += abs(pos - b)
        if distance <= m:
            inrad += 1
    return inrad

def part2(info):
    nanobots,_,_ = info
    
    # Find a bounding square that contains all nanobots
    maxCube = nanobots[0][0]
    minCube = nanobots[0][0]
    for nano in nanobots:
        for dimension in range(3):
            maxCube = max(nano[dimension], maxCube)
            minCube = min(nano[dimension], minCube)
    maxDimension = max(maxCube, -minCube)
    # Round up to nearest power of 2 for ease of division
    maxDimension = 2 ** math.ceil(math.log2(maxDimension))
    
    # Set initial values
    topleft = [-maxDimension,-maxDimension,-maxDimension]
    # Recurse
    closest,count = split(maxDimension * 2, topleft, nanobots, 0)
    if DEBUG:
        print(f'{closest} is in range of {count} bots.')
    return sum(map(abs,closest))

# Now that I got the answer, I realize that this method is best for sparsely
# populated spaces, where the number of bots in range of the ideal point is 
# is much less than the total number of bots. What I should have done is 
# check all spaces that contain all bots, then all - 1 bots, etc.
def split(size, topleft, nanobots, bestSoFar):
    # If this is only one square
    if size == 1:
        if DEBUG:
            print(f'Point at {topleft} has {len(nanobots)}.')
            # input()
        return topleft,len(nanobots)
    
    # Get the next 8 quadrants
    quads = quadrants(size, topleft)
    # List of next argument lists
    nextArgs = []
    for quad in quads:
        nextList = list(pruneBots(*quad,nanobots))
        if len(nextList) <= bestSoFar:
            continue
        nextArgs.append((*quad,nextList))
    
    newClosest,newCount = [0,0,0],0
    
    nextArgs = sortedByDistance(nextArgs)
    for argList in nextArgs:
        closest,count = split(*argList,bestSoFar)
        if count > bestSoFar:
            newClosest = closest
            newCount = count
            bestSoFar = count
    
    return newClosest,newCount
            

def sortedByDistance(argList):
    sortedArgs = sorted(argList, key=sortFn)
    return sortedArgs

def sortFn(args):
    size,topleft,botList = args
    center = [(d + size // 2) - 1 for d in topleft]
    distance = sum(map(abs,center))
    return distance,len(botList),topleft

def quadrants(size, topleft):
    x,y,z = topleft
    if size % 2 != 0:
        print(f'{size} is not divisible by 2 :P')
        raise Exception
    newSize = size // 2
    for dx,dy,dz in it.product([0,newSize], repeat=3):
        yield newSize,[x+dx,y+dy,z+dz]

def pruneBots(size, topleft, nanobots):
    for bot in nanobots:
        if intersects(size, topleft, bot):
            # print(f'{bot} is in range')
            yield bot
        # else:
        #     print(f'{bot} is not in range')

def intersects(size, topleft, bot):
    botright = [d + size - 1 for d in topleft]
    penalty = 0
    for mincube,maxcube,pos in zip(topleft,botright,bot):
        if pos > maxcube:
            penalty += pos - maxcube
        elif pos < mincube:
            penalty += mincube - pos
    return penalty <= bot[-1]

try:
    with fileOrStdout(outfile) as out:
        info = data,out,revMap
        # if DEBUG:
        #     print(data)
        
        inrad = part1(info)
        print(inrad)
        best = part2(info)
        print(best)

except KeyboardInterrupt:
    print('Interrupted')
except NotImplementedError:
    print('Not implemented')