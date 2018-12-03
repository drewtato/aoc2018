# Creates an image of the fabric with claims marked
from PIL import Image, ImageDraw
import numpy as np

GOLD = (255,255,102)
BLUE = (15,15,35)
RED = (200,15,15)

img = Image.new('RGB', (1000,1000))

with open('fab.txt', 'r') as fab:
    fab = fab.read().replace('  ', ' 0')
    imglist = []
    for pix in fab.split():
        val = int(pix)
        if val == 0:
            val = BLUE
        else:
            val = val / 8 + 0.3
            val = (int(GOLD[0] * val), int(GOLD[1] * val), int(GOLD[2] * val))
        imglist.append(val)
    
    img.putdata(list(imglist))
    
    # Values of success claim
    #650 @ 830,151: 25x21
    draw = ImageDraw.Draw(img)
    draw.rectangle([830, 151, 830+25, 151+21], fill=RED)
    
    img.save('fabric.png')