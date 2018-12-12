import itertools as it
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

serial = int(inp)

SIZE = 300
# SIZE = 10
# serial = 3999

SIZE += 1
cells = [[0]*SIZE for _ in range(SIZE)]
# for line in cells:
#     print(line)
for x,y in it.product(range(1,SIZE), repeat=2):
    # print(x, y)
    rackID = x + 10
    power = rackID * y
    power += serial
    power *= rackID
    power %= 1000
    power = int(power / 100)
    power -= 5
    # print(x, y, power)
    cells[y][x] = power

print(sum([sum(cell) for cell in cells]))
    
squares = []
for x,y in it.product(range(1, SIZE - 3), repeat=2):
    square = 0
    for dx,dy in it.product(range(3), repeat=2):
        square += cells[y + dy][x + dx]
    squares.append((square, x, y))
    # print(square)

m = max(squares)

print(f'{m[1]},{m[2]}')

# with open('cells.txt', 'w') as cellsFile:
#     for line in cells:
#         for c in line:
#             cellsFile.write(f'{c: 4}')
#         cellsFile.write('\n')

maxSoFar = (0, 0, 0)
for s in range(1,301):
    print(s)
    possible = False
    for x,y in it.product(range(1, SIZE - s), repeat=2):
        square = 0
        for dx,dy in it.product(range(s), repeat=2):
            square += cells[y + dy][x + dx]
        # squares.append((square, x, y))
        if square > maxSoFar[0]:
            maxSoFar = (square, x, y, s)
            print(maxSoFar)
            possible = True
        elif square == maxSoFar[0]:
            if possible:
                print('nope')
                possible = False