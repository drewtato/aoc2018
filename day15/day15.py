import itertools as it
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq
from copy import deepcopy

with open('input3.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

HP = 200
AP = 3
NEIGHBORS = [
    (0,-1),
    (-1,0),
    (1,0),
    (0,1)
]
cavernParser = {
    '#':0,
    '.':1,
    'E':1,
    'G':1
}
unitParser = {
    '#':0,
    '.':0,
    'E':1,
    'G':2
}

height = len(inp.split('\n'))
width = len(inp.split('\n')[0])

# cavern: 
# 1 for empty spaces (which may include units) 
# 0 for walls
cavern = [[0 for _ in range(width)] for _ in range(height)]
# taken:
# -2 for wall
# -1 for empty space
# otherwise index of unit in units
taken = deepcopy(cavern)
# units: (y, x, force, hp, ap)
# force is 1 for elf and 2 for goblin
units = []

for y,line in enumerate(inp.split('\n')):
    for x,c in enumerate(line):
        cavern[y][x] = cavernParser[c]
        possibleUnit = unitParser[c]
        if possibleUnit:
            u = [y, x, possibleUnit, HP, AP]
            units.append(u)
            taken[y][x] = len(units) - 1
        else:
            taken[y][x] = cavernParser[c] - 2

def printCavern(taken, units):
    printableCavern = []
    for line in taken:
        printableLine = []
        for c in line:
            if c < 0:
                printableLine.append({
                    -2:'#',
                    -1:'.'
                }[c])
            elif units[c][3] > 0:
                force = 'E' if units[c][2] == 1 else 'G'
                printableLine.append(force)
            else:
                printableLine.append('.')
        printableCavern.append(printableLine)
    
    for u in units:
        if u[3] > 0:
            force = 'E' if u[2] == 1 else 'G'
            printableCavern[u[0]].append(f' {force}({u[3]})')
            # printableCavern[u[0]].append(u)
    
    for line in printableCavern:
        for c in line:
            print(c, end='')
        print()
    print()

def checkRange(u, units, taken):
    targets = []
    for dx,dy in NEIGHBORS:
        y = u[0] + dy
        x = u[1] + dx
        if taken[y][x] >= 0:
            possible = taken[y][x]
            if possible >= 0:
                if units[possible][3] == 0:
                    raise Exception
                    # This should never happen as dead units
                    # are not in taken
                if u[2] != units[possible][2]:
                    targets.append(possible)
    minHP = 1000000
    selected = None
    for t in targets:
        if units[t][3] < minHP:
            selected = t
            minHP = units[t][3]
    return selected

def search(u, units, taken):
    taken = deepcopy(taken)
    y,x,force = u[:3]
    targets = []
    edge = set([(y,x)])
    while edge and not targets:
        for ey,ex in edge:
            taken[ey][ex] = -2
        for ey,ex in edge.copy():
            for dx,dy in NEIGHBORS:
                py,px = (ey+dy,ex+dx)
                unitIndex = taken[py][px]
                if unitIndex >= 0:
                    if units[unitIndex][2] != force:
                        targets.append((ey,ex))
                elif unitIndex == -1:
                    edge.add((py,px))
            edge.remove((ey,ex))
    return targets
    
def pick(start, end, taken):
    mutTaken = deepcopy(taken)
    targets = []
    edge = set([end])
    while edge and not targets:
        for ey,ex in edge:
            mutTaken[ey][ex] = -2
        for ey,ex in edge.copy():
            for dx,dy in NEIGHBORS:
                py,px = (ey+dy,ex+dx)
                unitIndex = mutTaken[py][px]
                if unitIndex >= 0:
                    if (py,px) == start:
                        targets.append((ey,ex))
                elif unitIndex == -1:
                    edge.add((py,px))
            edge.remove((ey,ex))

    select = min(targets)
    dy = select[0] - start[0]
    dx = select[1] - start[1]
    return (dy,dx)

def move(u, units, taken):
    for dx,dy in NEIGHBORS:
        y = u[0] + dy
        x = u[1] + dx
        possibleUnit = taken[y][x]
        if possibleUnit >= 0:
            if units[possibleUnit][2] != u[2]:
                return (0,0)
    targets = search(u, units, taken)
    try:
        chosen = min(targets)
    except ValueError:
        return (0,0)
    return pick(tuple(u[:2]),chosen, taken)
        
        

def fight(units, taken, p=False, step=False):
    moves = 0
    perfect = True
    elves = len(list(filter(lambda u: u[2] == 1, units)))
    goblins = len(list(filter(lambda u: u[2] == 2, units)))
    
    for moves in it.count():
        # print(moves, elves, goblins)
        units = sorted(units)
        for y,line in enumerate(taken):
            for x,t in enumerate(line):
                if t >= 0:
                    taken[y][x] = -1
        for i,u in enumerate(units):
            if u[3] > 0:
                y = u[0]
                x = u[1]
                taken[y][x] = i
        
        if p:
            print(f'Round {moves}')
            printCavern(taken, units)
            if step:
                input()
        
        for i,u in enumerate(units):
            if not u[3]:
                continue
            if not (elves and goblins):
                health = 0
                for _,_,_,hp,_ in units:
                    health += hp
                return moves, health, elves, goblins, perfect
            dy,dx = move(u, units, taken)
            if (dy or dx):
                newY = u[0] + dy
                newX = u[1] + dx
                # print(u[0],u[1], '->', newY,newX)
                taken[u[0]][u[1]] = -1
                taken[newY][newX] = i
                units[i][0] = newY
                units[i][1] = newX
            attacking = checkRange(u, units, taken)
            if attacking != None:
                units[attacking][3] -= u[4]
                ay,ax,f,hp,_ = units[attacking]
                if hp <= 0:
                    units[attacking][3] = 0
                    taken[ay][ax] = -1
                    if f == 1:
                        perfect = False
                        elves -= 1
                    else: 
                        goblins -= 1

result = fight(deepcopy(units), deepcopy(taken), p=True)
# print(result)
print(result[0] * result[1])
# print(result)

STARTAP = AP
for ap in it.count(STARTAP, 1):
    for i,u in enumerate(units):
        if u[2] == 1:
            units[i][4] = ap
    result = fight(deepcopy(units), deepcopy(taken))
    # print(ap, result)
    if result[4]:
        break
print(result[0] * result[1])