from PIL import Image

with open('output.txt', 'r') as out:
    out = out.read()

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
    cells.append(((y,x),(n,e,s,w)))
    miny = min(miny,y)
    minx = min(minx,x)
    maxy = max(maxy,y)
    maxx = max(maxx,x)

# print(cells)
dimensions = maxy - miny, maxx - minx
cellSize = 3
data = [0] * dimensions[0] * dimensions[1] * cellSize**2

