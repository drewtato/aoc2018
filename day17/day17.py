import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq
# from copy import deepcopy
import sys
PRINT = False
FAST = True
for arg in sys.argv[1:]:
    if arg == 'p':
        PRINT = True
    elif arg == 'f':
        FAST = False

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

inp = inp.replace('=', ' ')
inp = inp.replace(',', ' ')
minx = 100000
miny = 100000
maxx = 0
maxy = 0
for line in inp.split('\n'):
    first,firstNum,second,secondRange = line.split()
    start,end = secondRange.split('..')
    firstNum = int(firstNum)
    start = int(start)
    end = int(end)
    xfirst = (first == 'x')
    if xfirst:
        minx = firstNum if firstNum < minx else minx
        maxx = firstNum if firstNum > maxx else maxx
        for y in (start,end):
            miny = y if y < miny else miny
            maxy = y if y > maxy else maxy
    else:
        miny = firstNum if firstNum < miny else miny
        maxy = firstNum if firstNum > maxy else maxy
        for x in (start,end):
            minx = x if x < minx else minx
            maxx = x if x > maxx else maxx

minx -=1
# print(minx, maxx, miny, maxy)

# ground
# 0 is sand
# 1 is clay
# 2 is flowing
# 3 is stationary
ground = [
    [0 for _ in range(minx, maxx + 2)]\
    for _ in range(miny, maxy + 1)
]

for line in inp.split('\n'):
    first,firstNum,second,secondRange = line.split()
    firstNum = int(firstNum)
    xfirst = (first == 'x')
    
    start,end = secondRange.split('..')
    start = int(start)
    end = int(end)
    span = range(start,end + 1)
    if xfirst:
        for y in span:
            ground[y - miny][firstNum - minx] = 1
    else:
        for x in span:
            ground[firstNum - miny][x - minx] = 1

def printGround(ground, fp):
    for line in ground:
        for n in line:
            c = {
                0:'.',
                1:'#',
                2:'|',
                3:'~'
            }[n]
            fp.write(c)
        fp.write('\n')
    fp.write('\n')
    # input()

def fill(ground, start, minx, fp):
    start -= minx
    oldWater = 0
    for i in it.count():
        try:
            drop(ground, 0, start)
        except FillEx:
            break
        if PRINT:
            printGround(ground, fp)
        water = sum([
            sum(
                1 if c >= 2 else 0 for c in line
            ) for line in ground
        ])
        print(f'Round: {i}, Water: {water - oldWater}')
        oldWater = water

class FillEx(Exception):
    pass
class OutOfBoundsEx(FillEx):
    pass
class NoSpaceEx(FillEx):
    pass

# drop
def drop(ground, y, x):
    # print('drop', y, x)
    g = ground[y][x]
    if g == 3 or g == 1:
        raise NoSpaceEx
    try:
        while ground[y][x] == 2:
            y += 1
        if FAST:
            while ground[y][x] == 0:
                ground[y][x] = 2
                y += 1
        else:
            if ground[y][x] == 0:
                ground[y][x] = 2
                return

        try:
            dropside(ground, y-1, x)
        except NoSpaceEx:
            convertRow(ground, y-1, x)
    except IndexError:
        raise OutOfBoundsEx
                
def dropside(ground, y, x):
    lx = x - 1
    fall = False
    bounds = False
    while ground[y][lx] != 1:
        ground[y][lx] = 2
        try:
            drop(ground, y+1, lx)
            fall = True
            break
        except NoSpaceEx:
            lx -= 1
        except OutOfBoundsEx:
            bounds = True
            break
    rx = x + 1
    while ground[y][rx] != 1:
        ground[y][rx] = 2
        try: 
            drop(ground, y+1, rx)
            fall = True
            break
        except NoSpaceEx:
            rx += 1
        except OutOfBoundsEx:
            bounds = True
            break
    if not fall:
        if bounds:
            raise OutOfBoundsEx
        else:
            raise NoSpaceEx

def convertRow(ground, y, x):
    lx = x - 1
    while ground[y][lx] == 2:
        ground[y][lx] = 3
        lx -= 1
    while ground [y][x] == 2:
        ground[y][x] = 3
        x += 1
with open('output.txt', 'w') as out:
    try:
        if PRINT:
            printGround(ground, out)
        fill(ground, 500, minx, out)
        if PRINT:
            printGround(ground, out)
        water = sum([
            sum(
                1 if c >= 2 else 0 for c in line
            ) for line in ground
        ])
        retained = sum([
            sum(
                1 if c == 3 else 0 for c in line
            ) for line in ground
        ])
        if not PRINT:
            print(water)
            print(retained)

    except KeyboardInterrupt:
        if PRINT:
            printGround(ground, out)
        print('Interrputed')
    except RecursionError:
        if PRINT:
            printGround(ground, out)
        print('Too much recursion')