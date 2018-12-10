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
def getChangeY(points):
    minposY = min(map(lambda point: point[0][1], points))
    maxposY = max(map(lambda point: point[0][1], points))
    return maxposY - minposY

maxNegative = max(filter(lambda p: p[0][1] < 0, points), key=lambda p: abs(p[0][1] / p[1][1]))
# print(maxNegative[0][1] / maxNegative[1][1])
pre = abs(int(maxNegative[0][1] / maxNegative[1][1]))
# print(pre)

for p in points:
    dx = p[1][0] * pre
    dy = p[1][1] * pre
    p[0] = [p[0][0] + dx, p[0][1] + dy]

# print(points)
thisY = getChangeY(points)
# print(getMinMax(points))
seconds = 0

while True:
    seconds += 1
    lastPoints = copy.deepcopy(points)
    lastY = thisY
    for p in points:
        ax = p[1][0]
        ay = p[1][1]
        p[0][0] += ax
        p[0][1] += ay
    thisY = getChangeY(points)
    # print(thisY)
    if thisY > lastY:
        points = lastPoints
        seconds -= 1
        break

# img = [[' '] * 200 for _ in range(200)]
# for p in points:
#     try:
#         img[p[0][1]][p[0][0]] = '*'
#     except IndexError as e:
#         print(f'Indexes: {p[0]}')
#         raise e
    
# string = ''
# for line in img:
#     for c in line:
#         string += c
#     string += '\n'

# with open('stars.txt', 'w') as stars:
#     stars.write(string)




minposX = min(map(lambda p: p[0][0], points))
minposY = min(map(lambda p: p[0][1], points))
# print(minposX, minposY)
maxposX = max(map(lambda p: p[0][0], points))
maxposY = max(map(lambda p: p[0][1], points))

img = Image.new('L', (maxposX - minposX + 3, maxposY - minposY + 3))
for p in points:
    x = p[0][0] - minposX + 1
    y = p[0][1] - minposY + 1
    img.putpixel((x,y), 255)

# img.putpixel((0,0), 128)
img.save('stars.png')
print(seconds)