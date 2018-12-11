from PIL import Image
from math import sqrt

with open('colors.txt', 'r') as colorFile:
    colors = list(colorFile.read().strip().split(', '))
print(len(colors))

with open('grid.txt', 'r') as gridFile:
    grid = []
    for num in gridFile.read().split():
        if num == '.':
            grid.append(-1)
        else:
            grid.append(int(num))
        
# print(max(grid))
colors.append('#222222')
rgbColors = []
for color in colors:
    r = int('0x' + color[1:3], 16)
    g = int('0x' + color[3:5], 16)
    b = int('0x' + color[5:], 16)
    rgbColors.append((r,g,b))

# print(rgbColors)
data = list(map(lambda num: rgbColors[num], grid))

size = int(sqrt(len(grid)))

img = Image.new('RGB', (size, size))
img.putdata(data)
img = img.resize((size*4, size*4))
img.save('grid.png')