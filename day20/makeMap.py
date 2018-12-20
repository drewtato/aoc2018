from PIL import Image
import itertools as it

with open('output.txt', 'r') as out:
    out = out.read()

while out[-1].isspace():
    out = out[:-1]

out = out.replace('(','')\
    .replace(')','')\
    .replace(',','')\
    .replace(':','')

cells = []
maxx,maxy,minx,miny = 0,0,10000,10000
for line in out.split('\n'):
    line = list(line.split())
    y,x = list(map(int, line[0:2]))
    n,e,s,w = [c != '.' for c in line[2]]
    cells.append((y,x,n,e,s,w))
    miny = min(miny,y)
    minx = min(minx,x)
    maxy = max(maxy,y)
    maxx = max(maxx,x)

with open('output3.txt', 'r') as out2:
    out2 = out2.read()
out2 = out2.replace('(','')\
    .replace(')','')\
    .replace(',','')\

path = []
for line in out2.split('\n'):
    # print(line)
    line = map(int, line.split())
    path.append(tuple(line))
# print(path)

BLUE = (15,15,35)
RED = (255,0,0)
GREEN = (0,220,0)
GREY = (100,100,110)

WALL = BLUE
GROUND = GREY
START = GREEN
END = RED
PATH = (60,60,130)
WIN = (-3,29)

dimensions = maxy - miny + 1, maxx - minx + 1
cellSize = 6
dimensions = dimensions[0] * cellSize, dimensions[1] * cellSize
rowSize = dimensions[1]
data = []
for _ in range(dimensions[0]):
    data.append([GROUND for _ in range(rowSize)])
# print(data)
for y,x in path:
    y,x = (y - miny)*cellSize, (x - minx)*cellSize
    for dy,dx in it.product(range(cellSize), repeat=2):
        data[y + dy][x + dx] = PATH
    

for y,x,n,e,s,w in cells:
    oldy,oldx = y,x
    y,x = (y - miny)*cellSize, (x - minx)*cellSize
    if (oldy,oldx) == (0,0):
        for dy,dx in it.product(range(1, cellSize - 1), repeat=2):
            data[y + dy][x + dx] = START
    elif (oldy,oldx) == WIN:
        for dy,dx in it.product(range(1, cellSize - 1), repeat=2):
            data[y + dy][x + dx] = END
    for dy,dx in it.product([0,cellSize - 1], repeat=2):
        data[y+dy][x+dx] = WALL
    for ds in range(1, cellSize - 1):
        if not n: data[y][x+ds] = WALL
        if not e: data[y+ds][x+cellSize-1] = WALL
        if not s: data[y+cellSize-1][x+ds] = WALL
        if not w: data[y+ds][x] = WALL

serial = []
for row in data:
    serial.extend(row)
img = Image.new('RGB',dimensions)
img.putdata(serial)
scale = 4
img = img.resize((dimensions[0] * scale, dimensions[1] * scale))
img.save('map.png')
img.show()