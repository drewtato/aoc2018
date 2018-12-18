from PIL import Image
import os
import shutil

GOLD = (255,255,102)
BLUE = (15,15,35)
RED = (255,0,0)
GREEN = (0,153,0)
GREY = (204,204,204)

OPEN = BLUE
TREES = GREEN
LUMBER = GOLD
areaMap = {
    '.':OPEN,
    '|':TREES,
    '#':LUMBER
}

shutil.rmtree('img', ignore_errors=True)
while True:
    try: os.mkdir('img')
    except PermissionError: continue
    break

imgSize = 200
scale = 1
with open('output.txt', 'r') as inp:
    data = []
    currentImage = 0
    for line in inp:
        if len(line) > 1:
            for c in line[:-1]:
                data.append(areaMap[c])

        else:
            img = Image.new('RGB', (imgSize,imgSize))
            img.putdata(data)
            data = []
            img = img.resize((imgSize * scale, imgSize * scale))
            img.save(f'img/{currentImage:03}.png')
            currentImage += 1