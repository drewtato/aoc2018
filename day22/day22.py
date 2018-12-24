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
def pCave(cave, data, out, revMap, exp=[]):
    y,x,eq = *data[1:],TORCH
    pathPieces = {}
    while (y,x) != (0,0):
        pass
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

# ROCKY = 0 torch,climb
# WET = 1 climb,neither
# NARROW = 2 torch,neither
terrEquip = [
    [1,1,0],
    [0,1,1],
    [1,0,1]
]
terrSwitch = [
    {0:1,1:0},
    {1:2,2:1},
    {0:2,2:0}
]
FACTOR = 1

def route(cave,info):
    _,tx,ty = info[0]
    # candidates: 0 is (weighted time, time), 1 is y, 2 is x, 3 is equip, 4 is last
    candidates = []
    explored = {}
    hq.heappush(candidates, ((0,0),0,0,TORCH,None))
    lastwei = 0
    try:
        while True:
            (wei,dur),y,x,equip,last = hq.heappop(candidates)
            # print(wei,dur,y,x,equip)
            # input()
            # if DEBUG and wei > lastwei
            if DEBUG:
                print(wei,dur,ty-y,tx-x)
                lastwei = wei
            if (y,x) == (ty,tx):
                if equip != TORCH:
                    dur += 7
                    cand = (dur,dur),y,x,TORCH,last
                    explored[y,x,TORCH] = dur,(y,x),equip
                    hq.heappush(candidates,cand)
                return dur,explored
            curterr = region(cave,y,x,*info[0])[2]
            try:
                if dur >= explored[y,x,equip][0]:
                    print('why')
                    continue
            except KeyError:
                pass
            othereq = terrSwitch[curterr][equip]
            try:
                if dur >= explored[y,x,othereq][0] + 7:
                    print('other tool better')
                    continue
            except KeyError:
                pass
            dur += 1
            for dy,dx in directions:
                ny,nx = y+dy,x+dx
                try:
                    nextterr = region(cave,ny,nx,*info[0])[2]
                except IndexError:
                    continue
                if terrEquip[nextterr][equip]:
                    nexteq = equip
                else:
                    dur += 7
                    nexteq = terrSwitch[curterr][equip]
                try:
                    if dur >= explored[ny,nx,nexteq][0]:
                        continue
                except KeyError:
                    pass
                othereq = terrSwitch[nextterr][nexteq]
                try:
                    if dur >= explored[ny,nx,othereq][0] + 7:
                        continue
                except KeyError:
                    pass
                explored[ny,nx,nexteq] = dur,(y,x),equip
                weight = abs(ny-ty) + abs(nx-tx) + dur
                weight += 7 if nexteq != TORCH else 0
                cand = (weight,dur),ny,nx,nexteq,(y,x)
                hq.heappush(candidates,cand)

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

        dur,explored = route(cave,info)
        pCave(cave,*info,exp=explored)
        print(dur)

    except KeyboardInterrupt as e:
        print('Interrupted', e)

    pCave(cave,*info)
