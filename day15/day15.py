import itertools as it
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq

with open('input2.txt', 'r') as inp:
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

cavern = [[0 for _ in range(width)] for _ in range(height)]
units = []
taken = {}

for y,line in enumerate(inp.split('\n')):
    for x,c in enumerate(line):
        cavern[y][x] = cavernParser[c]
        if not cavernParser[c]:
            taken[(y,x)] = -1
        possibleUnit = unitParser[c]
        if possibleUnit:
            u = (y, x, possibleUnit, HP, AP)
            units.append(u)
            taken[(y,x)] = len(units) - 1

def printCavern(cavern, units):
    printableCavern = []
    for line in cavern:
        row = []
        for c in line:
            row.append({0:'#', 1:'.'}[c])
        printableCavern.append(row)
    for u in sorted(units):
        y = u[0]
        x = u[1]
        force = 'E' if u[2] == 1 else 'G'
        health = u[3]
        if health:
            printableCavern[y][x] = force
            printableCavern[y].append(f' {force}({health})')
    for line in printableCavern:
        for c in line:
            print(c, end='')
        print()

def checkRange(u, taken):
    targets = []
    for dx,dy in NEIGHBORS:
        y = u[0] + dy
        x = u[1] + dx
        if (y,x) in taken:
            possible = taken[(y,x)]
            if possible >= 0:
                targets.append(possible)
    minHP = HP
    for t in targets:
        if 
    return targets

def search(location, units, taken):
    
    
def move(u, units, taken):
    targets = search(u[:2], units, taken)
    try:
        chosen = min(targets)
    except ValueError:
        raise Exception
    
    
        
    return 
        
        

def fight(cavern, units, print=False, step=False):
    moves = 0
    
    while True:
        if print:
            printCavern(cavern, units)
            if step:
                input()
        
        units = sorted(units)
        for i,u in enumerate(units):
            if not u[3]:
                continue
            force = u[2]
            attacking = checkRange(u, taken)
            if not attacking:
                try:
                    dx,dy = move(u, units, taken)
                except Exception:
                    return moves
                newY = u[0] + dy
                newX = u[1] + dx
                units[i][0] = newY
                units[i][1] = newX
                del taken[(u[0],u[1])]
                taken[(newY,newX)] = i
            else:
                units[attacking][3] -= u[4]
                if units[attacking][3] <= 0:
                    units[attacking][3] = 0
                    del taken[units[attacking][:2]]
        moves += 1
        
print(fight(cavern, units, print=True, step=True))