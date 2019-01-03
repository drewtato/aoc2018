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
def pCave(cave, data, out, revMap, exp={}):
    if PRINT:
        for y,row in enumerate(cave):
            for x,[_,_,c] in enumerate(row):
                if (y,x) == (0,0):
                    out.write(revMap[MOUTH])
                elif [x,y] == data[1:]:
                    out.write(revMap[TARGET])
                elif (y,x) in exp:
                    out.write(pathMap[exp[y,x]])
                else:
                    out.write(revMap[c])
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
PATH = 3

TORCH = 1
CLIMB = 2
NEITHER = 3

pathMap = {
    TORCH:'F',
    CLIMB:'C',
    NEITHER:'N'
}
dataMap = dd(lambda: 0)
dataMap.update({
    '.':ROCKY,
    '=':WET,
    '|':NARROW,
    'M':MOUTH,
    'T':TARGET,
    '+':PATH,
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

directions = [
    (0,1),
    (1,0),
    (0,-1),
    (-1,0),
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

# ROCKY = 0 torch,climb
# WET = 1 climb,neither
# NARROW = 2 torch,neither

# newEquip = terrSwitch[terrain][equipment]
terrSwitch = [
    [None,CLIMB,TORCH,0],
    [None,0,NEITHER,CLIMB],
    [None,NEITHER,0,TORCH]
]

def bestSoFar(explored,duration,y,x,equipment,last,lastEquip):
    best = True
    for eq,(dur,_,_) in explored[y,x].items():
        if eq == equipment:
            if dur <= duration:
                best = False
                break
        else:
            if dur + 7 <= duration:
                best = False
                break
    
    if best:
        explored[y,x][equipment] = duration,last,lastEquip
    return best

def route(cave,info):
    data,_,_ = info
    depth,tx,ty = data
    candidates = []
    hq.heappush(candidates, (0,0,0,0,TORCH,region(cave,0,0,depth,tx,ty),None))
    explored = dd(dict)
    while True:
        weight,duration,y,x,equipment,terrain,last = hq.heappop(candidates)
        # Reached the target, check if using torch
        if (y,x) == (ty,tx):
            if equipment != TORCH:
                hq.heappush(candidates, (weight+7,duration+7,y,x,TORCH,terrain,last))
                continue
            # If using torch, return
            return duration, explored
        duration += 1
        for dy,dx in directions:
            ny,nx = y + dy, x + dx
            try:
                _,_,newTerr = region(cave,y,x,depth,tx,ty)
            except IndexError:
                continue
            if terrSwitch[newTerr][equipment]:
                offset = 0
                newEquip = equipment
            else:
                offset = 7
                newEquip = terrSwitch[terrain][equipment]
            if not bestSoFar(explored, duration + offset, ny, nx, newEquip, (y,x), equipment):
                continue
            weight = duration + offset
            weight += abs(ny - ty)
            weight += abs(nx - tx)
            weight += 0 if newEquip == TORCH else 7
            newCandidate = weight,duration + offset,ny,nx,newEquip,newTerr,(y,x)
            hq.heappush(candidates, newCandidate)

with fileOrStdout(outfile) as out:
    info = data,out,revMap
    try:
        cave = makeCave(info)
        if DEBUG:
            print(data)
            # pCave(cave,*info)

        risk = sum([sum([terrain for _,_,terrain in row]) for row in cave])
        print(risk)

        dur,explored = route(cave,info)
        print(dur)
        # Can't get this to print the right thing.
        if PRINT:
            path = {}
            last = tuple(reversed(data[1:]))
            if TORCH in explored[last]:
                equip = TORCH
            else:
                _,_,equip = min(explored[last].values())
            while last != (0,0):
                dur,last,nextequip = explored[last][equip]
                path[last] = equip
                equip = nextequip
            pCave(cave,*info,exp=path)

    except KeyboardInterrupt as e:
        print('Interrupted', e)