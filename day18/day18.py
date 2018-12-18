import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq
from copy import deepcopy as dc

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

OPEN = 0
TREES = 1
LUMBER = 2
areaMap = {
    '.':OPEN,
    '|':TREES,
    '#':LUMBER
}
invAreaMap = {v:k for k,v in areaMap.items()}

area = []
for line in inp.split('\n'):
    row = []
    for item in line:
        row.append(areaMap[item])
    area.append(tuple(row))
area = tuple(area)

def pArea(area):
    for line in area:
        for c in line:
            print(invAreaMap[c], end='')
        print()
    print()

NEIGHBORS = [(y,x) for y,x in it.product([-1,0,1], repeat=2)]
NEIGHBORS.remove((0,0))
def countAdjacent(area, y, x):
    o = 0
    t = 0
    l = 0
    for dy,dx in NEIGHBORS:
        ny = y + dy
        nx = x + dx
        if ny < 0 or nx < 0:
            continue
        try:
            near = area[ny][nx]
        except IndexError:
            continue
        if near == OPEN:
            o += 1
        elif near == TREES:
            t += 1
        elif near == LUMBER:
            l += 1
        else:
            raise Exception
    # print((y,x), (o,t,l))
    # input()
    return o,t,l

def iterate(area):
    newArea = []
    for y,row in enumerate(area):
        newRow = []
        for x,cell in enumerate(row):
            newCell = cell
            _,t,l = countAdjacent(area, y, x)
            if cell == OPEN:
                if t >= 3:
                    newCell = TREES
            elif cell == TREES:
                if l >= 3:
                    newCell = LUMBER
            elif cell == LUMBER:
                if not (l >= 1 and t >= 1):
                    newCell = OPEN
                
            newRow.append(newCell)
        newArea.append(tuple(newRow))
    return tuple(newArea)

def resourceValue(area):
    t = 0
    l = 0
    for row in area:
        for cell in row:
            if cell == TREES:
                t += 1
            elif cell == LUMBER:
                l += 1
    return t,l

# pArea(area)
originalArea = dc(area)
for _ in range(10):
    area = iterate(area)
    # pArea(area)
# pArea(area)
rv = resourceValue(area)
print(rv[0] * rv[1])

area = dc(originalArea)
seen = {}
CYCLES = 1000000000
for i in range(CYCLES):
    # if not i % 10000:
    #     print(i, resourceValue(area))
    area = iterate(area)
    if area in seen:
        break
    seen.update({area: i})

# print(i, seen[area])
j = seen[area]
extras = CYCLES - i - 1
partial = extras % (i - j)
for _ in range(partial):
    area = iterate(area)
rv = resourceValue(area)
print(rv[0] * rv[1])
