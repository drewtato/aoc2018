import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq
# from copy import deepcopy
import sys

if sys.argv[1:]:
    PRINT = True
else:
    PRINT = False

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

def printGround(ground):
    for line in ground:
        for n in line:
            c = {
                0:'.',
                1:'#',
                2:'|',
                3:'~'
            }[n]
            print(c, end='')
        print()
    print()
    input()

def fill(ground, start, minx):
    start -= minx
    while True:
        try:
            drop(ground, 0, start)
        except FillEx:
            break
        if PRINT:
            printGround(ground)

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
        while ground[y][x] == 0:
            ground[y][x] = 2
            y += 1
        
        else:
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

try:
    fill(ground, 500, minx)
    if PRINT:
        printGround(ground)
    water = sum([
        sum(
            1 if c >= 2 else 0 for c in line
        ) for line in ground
    ])
    print(water)
    retained = sum([
        sum(
            1 if c == 3 else 0 for c in line
        ) for line in ground
    ])
    print(retained)

except KeyboardInterrupt:
    print('Interrputed')
except RecursionError:
    printGround(ground)
    print('Too much recursion')