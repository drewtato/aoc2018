import itertools as it
from collections import Counter as Co

with open('input.txt', 'r') as inp:
    inp = inp.read()
    while inp[-1].isspace():
        inp = inp[:-1]

coordinates = []
for line in inp.split('\n'):
    coordinates.append(tuple(map(lambda item: int(item), line.split(', '))))
    
# print(coordinates)

SIZE = 1 + max(\
    max(coordinates)[0],\
    max(map(lambda c: list(reversed(c)), coordinates))[0]
)
# print(SIZE)

grid = list(list(-1 for _ in range(SIZE)) for _ in range(SIZE))
newgrid = list(list(-1 for _ in range(SIZE)) for _ in range(SIZE))

def gridstring(grid):
    string = ''
    for line in grid:
        for c in line:
            if c == -1:
                string += '  .'
            else:
                string += f'{c: 3}'
        string += '\n'
    return string[:-1]


# for i,point in enumerate(coordinates):
#     x = point[0]
#     y = point[1]
#     # print(x, y)
#     grid[y][x] = i
    
# print(gridstring(grid))
# print()

# infinites = set()
# count = Co()

# for x,y in it.product(range(SIZE),repeat=2):
#     # print(x,y)
#     i = 0
#     possibles = []
#     if grid[y][x] != -1:
#         possibles.append(grid[y][x])
#     distance = 0
#     while len(possibles) == 0:
#         distance += 1
#         # print(distance)
#         sequence = [
#             list(zip(range(distance),range(distance, 0, -1))),
#             list(zip(range(distance, 0, -1),range(0, -distance, -1))),
#             list(zip(range(0, -distance, -1),range(-distance, 0))),
#             list(zip(range(-distance, 0),range(distance)))
#         ]
#         # print(list(it.chain.from_iterable(sequence)))
#         for d3,d4 in it.chain.from_iterable(sequence):
#             newx = d3 + x
#             newy = d4 + y
#             # print(newx,newy)
#             # input()
#             i += 1
#             try: 
#                 if newx < 0 or newy < 0:
#                     raise IndexError
#                 if grid[newy][newx] != -1:
#                     possibles.append(grid[newy][newx])
#                     # print('Append ' + str(possibles[-1]))
#             except IndexError:
#                 continue
        
#     if len(possibles) == 1:
#         newgrid[y][x] = possibles[0]
#         for coord in [x,y]:
#             if not (coord > 0 and coord < SIZE - 1):
#                 infinites.add(possibles[0])
#         count.update([possibles[0]])
#     # print(gridstring(newgrid))
#     else:
#         print(x, y, possibles, i)
#     # print(input())


# print(gridstring(newgrid))
# print(count)
# for key in infinites:
#     del count[key]

# print(count.most_common(1)[0][1])

# with open('grid.txt', 'w') as pg:
#     pg.write(gridstring(grid))

THRESHHOLD = 10000
area = 0
for x,y in it.product(range(SIZE),repeat=2):
    totaldistance = 0
    for cx,cy in coordinates:
        totaldistance += abs(x - cx)
        totaldistance += abs(y - cy)
    newgrid[y][x] = totaldistance
    if totaldistance < THRESHHOLD:
        area += 1
    
# print(gridstring(newgrid))
print(area)