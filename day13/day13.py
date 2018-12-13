# import itertools as it
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq
from copy import deepcopy

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

tracks = []
carts = []
for y,line in enumerate(inp.split('\n')):
    trackline = []
    for x,c in enumerate(line):
        if c in 'v^<>':
            carts.append(((x,y),c))
            if c in 'v^':
                trackline.append('|')
            elif c in '<>':
                trackline.append('-')
        else:
            trackline.append(c)
    tracks.append(trackline)

# for line in tracks:
#     print(line)
for i,cart in enumerate(carts):
    direction = {
        '^':0,
        '>':1,
        'v':2,
        '<':3
    }[cart[1]]
    carts[i] = [cart[0], direction, 0]
# print(carts)
def simulate(tracks, carts, collisions):
    carts = sorted(carts, key=lambda c: (c[0][1], c[0][0]))
    newPositions = dict([(c[0], i) for i,c in enumerate(carts)])
    toDel = []
    for i,cart in enumerate(carts):
        # print(' ' + str(cart), end='')
        # input()
        try:
            del newPositions[cart[0]]
        except KeyError:
            continue
        position = cart[0]
        movement = [(0,-1), (1,0), (0,1), (-1,0)][cart[1]]
        moved = (position[0] + movement[0], position[1] + movement[1])
        # print(position, movement)
        upcoming = tracks[moved[1]][moved[0]]
        if upcoming == '+':
            if cart[2] == 0:
                carts[i][1] = (cart[1] - 1) % 4
            elif cart[2] == 2:
                carts[i][1] = (cart[1] + 1) % 4
            carts[i][2] = (cart[2] + 1) % 3
        elif upcoming == '/':
            if cart[1] % 2 == 1:
                carts[i][1] -= 1
            else:
                carts[i][1] += 1
        elif upcoming == '\\':
            if cart[1] % 2 == 1:
                carts[i][1] = (cart[1] + 1) % 4
            else:
                carts[i][1] = (cart[1] - 1) % 4
        elif upcoming == ' ':
            raise Exception
        carts[i][0] = (moved[0], moved[1])
        # print(newPositions)
        if moved in newPositions:
            # print(f'Appending {i} and {newPositions[moved]}')
            toDel.append(i)
            toDel.append(newPositions[moved])
            del newPositions[moved]
        else:
            newPositions[moved] = i
            
    for i in reversed(sorted(toDel)):
        del carts[i]
    return (carts, collisions)

def display(tracks, carts, collisions):
    printable = deepcopy(tracks)
    for ((x,y),direction,_) in carts:
        printable[y][x] = {
            0:'^',
            1:'>',
            2:'v',
            3:'<'
        }[direction]
    for (x,y) in collisions:
        printable[y][x] = 'X'
    s = ''
    for line in printable:
        for c in line:
            s += c
        s += '\n'
    return s
# print(carts)
# print(tracks)
collisions = []
# while not collisions:
#     # print(display(tracks,carts,collisions))
#     # print(carts)
#     # input()
#     carts, collisions = simulate(tracks, carts, collisions)
# print(f'{collisions[0][0]},{collisions[0][1]}')

while len(carts) > 1:
    # print(display(tracks,carts,[]))
    # print(carts)
    # input()
    carts, collisions = simulate(tracks, carts, collisions)
print(f'{carts[0][0][0]},{carts[0][0][1]}')