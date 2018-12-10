# import itertools
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq
import copy
from PIL import Image, ImageDraw

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

points = []
for line in inp.split('\n'):
    points.append([[int(line[10:16]), int(line[18:24])], [int(line[36:38]), int(line[40:42])]])

# print(points)
def getMinMax(points):
    minposX = min(map(lambda point: point[0][0], points))
    minposY = min(map(lambda point: point[0][1], points))
    maxposX = max(map(lambda point: point[0][0], points))
    maxposY = max(map(lambda point: point[0][1], points))
    return (maxposX - minposX, maxposY - minposY)

thisMinMax = getMinMax(points)
# print(getMinMax(points))
seconds = 0

# It's gonna take a long time so might as well skip a few
# SKIP = 1000


while True:
    seconds += 1
    lastPoints = copy.deepcopy(points)
    lastMinMax = thisMinMax
    for p in points:
        ax = p[1][0]
        ay = p[1][1]
        p[0][0] += ax
        p[0][1] += ay
    thisMinMax = getMinMax(points)
    # print(thisMinMax)
    if thisMinMax > lastMinMax:
        points = lastPoints
        seconds -= 1
        break

thisMinMax = (thisMinMax[0] + 1, thisMinMax[1] + 1)
img = Image.new('L', thisMinMax)

minposX = min(map(lambda p: p[0][0], points))
minposY = min(map(lambda point: point[0][1], points))

for p in points:
    x = p[0][0] - minposX
    y = p[0][1] - minposY
    img.putpixel((x,y), 255)

# img.putpixel((0,0), 128)
img.save('stars.png')
print(seconds)