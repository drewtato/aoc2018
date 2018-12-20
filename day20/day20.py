import sys
from contextlib import contextmanager
from collections import defaultdict as dd
# import os
import itertools as it
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
        for c in data:
            out.write(revMap[c])
        out.write('\n')

removals = ['^$']
CPAREN = -2
OPAREN = -1
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
PIPE = 4
inp = replacer(inp, removals)
regex = []
dataMap = dd(lambda: 0)
dataMap.update({
    'N':NORTH,
    'E':EAST,
    'S':SOUTH,
    'W':WEST,
    '(':OPAREN,
    ')':CPAREN,
    '|':PIPE,
})
coord = {
    NORTH:(-1,0),
    EAST:(0,1),
    SOUTH:(1,0),
    WEST:(0,-1),
}
opposite = {
    NORTH:SOUTH,
    EAST:WEST,
}
opposite.update({v:k for k,v in opposite.items()})
revMap = {v:k for k,v in dataMap.items()}
for c in inp:
    regex.append(dataMap[c])
# print(data)

def pRooms(rooms,regex,out,revMap):
    if PRINT:
        for room,(doors,_) in sorted(rooms.items()):
            out.write(str(room) + ': ')
            for direction in sorted(coord):
                out.write(revMap[direction] if direction in doors else '.')
            out.write('\n')

def createMap(regex):
    rooms = dd(lambda: [set(),set()])
    addToMap(rooms,regex)
    return rooms

def addToMap(rooms,regex,y=0,x=0,index=0):
    if index in rooms[y,x][1]:
        return
    while index < len(regex):
        c = regex[index]
        try:
            dy,dx = coord[c]
            rooms[y,x][1].add(index)
            rooms[y,x][0].add(c)
            ny,nx = y+dy,x+dx
            rooms[ny,nx][0].add(opposite[c])
            y,x = ny,nx
        except KeyError:
            if c == PIPE:
                depth = 1
                while depth:
                    index += 1
                    c = regex[index]
                    if c < 0:
                        depth += {OPAREN:1,CPAREN:-1}[c]
                if index in rooms[y,x][1]:
                    return
                
            elif c == OPAREN:
                depth = 1
                index += 1
                addToMap(rooms,regex,y,x,index)
                while depth:
                    c = regex[index]
                    index += 1
                    if c == PIPE and depth == 1:
                        addToMap(rooms,regex,y,x,index)
                    elif c < 0:
                        depth += {OPAREN:1,CPAREN:-1}[c]
                    
                return
        
        index += 1
                
def findShortest(rooms, coord, info):
    depth = 0
    farRooms = 0
    thisRooms = set()
    thisRooms.add((0,0))
    searchedRooms = {(0,0):[depth,None]}
    while thisRooms:
        depth += 1
        nextRooms = set()
        for y,x in thisRooms:
            for dy,dx in map(lambda c: coord[c], rooms[(y,x)][0]):
                ny,nx = y+dy,x+dx
                if (ny,nx) not in searchedRooms:
                    searchedRooms.update({(ny,nx):[depth,(y,x)]})
                    nextRooms.add((ny,nx))
                    if depth >= 1000:
                        farRooms += 1

        thisRooms = nextRooms
    answer = [depth - 1, farRooms]
    if DEBUG:
        answer.append((y,x))
        last = searchedRooms[y,x]
        while last[1]:
            answer.append(last[1])
            last = searchedRooms[last[1]]
    return answer

try:
    with fileOrStdout(outfile) as out:
        info = regex,out,revMap
        rooms = createMap(regex)
        if DEBUG: print('created map')
        pRooms(rooms,*info)
        for n in findShortest(rooms, coord, info):
            print(n)

except KeyboardInterrupt:
    print('Interrupted')
