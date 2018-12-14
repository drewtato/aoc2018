from PIL import Image, ImageDraw, ImageFont
import itertools as it

GOLD = (255,255,102)
BLUE = (15,15,35)
RED = (255,0,0)
GREEN = (0,153,0)
GREY = (204,204,204)

pots = []
with open('pots.txt', 'r') as potsFile:
    for line in potsFile:
        pots.append([0 if c == ' ' else 1 for c in line])
        
# print(pots[1:4])

maxLen = max([len(x) for x in pots])
# print(maxLen)
for line in pots:
    line.extend(it.repeat(0, maxLen - len(line)))
    
data = []
for i,line in enumerate(pots):
    for j,p in enumerate(line):
        if i == 20:
            if j % 100 == 0:
                data.append(RED if p else GREY)
            else:
                data.append(RED if p else BLUE)
        else:
            if j % 100 == 0:
                data.append(GOLD if p else GREY)
            else:
                data.append(GOLD if p else BLUE)
        
sizeX = maxLen
sizeY = len(pots)
img = Image.new('RGB', (sizeX, sizeY))

img.putdata(data)
# img.show()
img = img.resize((sizeX * 2, sizeY * 4))

dr = ImageDraw.Draw(img)
font = ImageFont.truetype('../assets/SourceCodePro-Light.ttf', 38)
botleft = (230, 56)
# dr.rectangle([(312, 55), (500,105)], fill=BLUE)
dr.text(botleft, '<- 3061', RED, font)

img.save('pots.png')