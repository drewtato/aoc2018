import sys
from contextlib import contextmanager
from collections import defaultdict as dd
import heapq as hq
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
def pCave(cave, data, out, revMap):
    if PRINT:
        for y,row in enumerate(cave):
            for x,[_,_,c] in enumerate(row):
                if (y,x) == (0,0):
                    out.write(revMap[MOUTH])
                elif [x,y] == data[1:]:
                    out.write(revMap[TARGET])
                else:
                    out.write(revMap[c])
            out.write('\n')
        out.write('\n')

removals = ['depth:targ ']
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
TARGET = -2
MOUTH = -1
ROCKY = 0
WET = 1
NARROW = 2
dataMap = dd(lambda: 0)
dataMap.update({
    '.':ROCKY,
    '=':WET,
    '|':NARROW,
    'M':MOUTH,
    'T':TARGET,
})
revMap = {v:k for k,v in dataMap.items()}
data = [int(n) for n in inp.split()]
# print(data)

def makeCave(info):
    _,tx,ty = info[0]
    cave = []
    region(cave,ty,tx,*info[0])
    return cave

def region(cave,y,x,depth,tx,ty):
    if y < 0 or x < 0:
        raise IndexError
    info = depth,tx,ty
    try:
        return cave[y][x]
    except IndexError:
        geo = 0
        if (y,x) != (0,0):
            try:
                _,erosionLeft,_ = region(cave,y,x-1,*info)
            except IndexError:
                geo = y * 48271
            try: 
                _,erosionAbove,_ = region(cave,y-1,x,*info)
                if not geo:
                    geo = erosionAbove * erosionLeft
            except IndexError:
                geo = x * 16807
            geo = 0 if (y,x) == (ty,tx) else geo
        
        erosion = (geo + depth) % 20183
        terrain = erosion % 3
        regionStats = [geo,erosion,terrain]
        try:
            cave[y].append(regionStats)
        except IndexError:
            cave.append([regionStats])
        return regionStats
        

TORCH = 0
CLIMB = 1
NEITHER = 2
directions = [
    (0,1),
    (1,0),
    (0,-1),
    (-1,0)
]
# equipTerr = {
#     TORCH:[ROCKY,NARROW],
#     CLIMB:[ROCKY,WET],
#     NEITHER:[NARROW,WET]
# }
# terrEquip = dd(list)
# for key,vals in equipTerr.items():
#     for v in vals:
#         terrEquip[v].append(key)

# ROCKY = 0
# WET = 1
# NARROW = 2
terrEquip = [
    [CLIMB,TORCH],
    [CLIMB,NEITHER],
    [TORCH,NEITHER]
]
FACTOR = 1

def route(cave,info):
    _,tx,ty = info[0]
    # candidates: 0 is (weighted time, time), 1 is y, 2 is x, 3 is equip
    candidates = []
    explored = {}
    hq.heappush(candidates, (0,0,0,0,TORCH,None))
    lastwei = 0
    try:
        while True:
            wei,dur,y,x,equip,last = hq.heappop(candidates)
            if DEBUG and wei > lastwei:
                print(dur,wei,y,x,equip,len(candidates),len(explored))
                lastwei = wei
            if (y,x) == (ty,tx):
                if equip != TORCH:
                    dur += 7
                    hq.heappush(candidates, (dur, dur,y,x,TORCH,last))
                    continue
                return dur,y,x,equip,last,explored
            try:
                equipSoFar = explored[y,x][1]
                try:
                    pastDur = equipSoFar[equip]
                    if dur > pastDur:
                        continue
                    explored[y,x][1][equip] = dur
                except IndexError:
                    less = True
                    for v in explored[y,x][1]:
                        if dur > v + 7:
                            less = False
                    if less:
                        explored[y,x][1][equip] = dur
                    else:
                        continue
                
            except KeyError:
                equipVals = [1023] * 3
                equipVals[equip] = dur
                explored.update({(y,x):(last,equipVals)})
            dur += 1
            for dy,dx in directions:
                ny,nx = dy+y,dx+x
                try:
                    _,_,terrain = region(cave,ny,nx,*info[0])
                except IndexError:
                    continue
                weighted = (abs(ny-ty) + abs(nx-tx)) * FACTOR + dur
                if equip in terrEquip[terrain]:
                    if equip != TORCH:
                        weighted += 7
                    hq.heappush(candidates, (weighted, dur,ny,nx,equip,(y,x)))
                else:
                    for newEquip in terrEquip[terrain]:
                        extra = 7 if newEquip != TORCH else 0
                        hq.heappush(candidates, (weighted + extra + 7, dur+7,ny,nx,newEquip,(y,x)))
    except MemoryError:
        print(f'Ran out of memory. candidates: {len(candidates)} explored: {len(explored)}')

with fileOrStdout(outfile) as out:
    info = data,out,revMap
    try:
        cave = makeCave(info)
        if DEBUG:
            print(data)
            # pCave(cave,*info)
        
        risk = sum([sum([terrain for _,_,terrain in row]) for row in cave])
        print(risk)
        
        dur,_,_,equip,last,explored = route(cave,info)
        duration = dur
        while last:
            print(last,duration)
            last,duration = explored[last]
        pCave(cave,*info)
        print(dur)

    except (KeyboardInterrupt, TypeError) as e:
        pCave(cave,*info)
        print('Interrupted', e)
