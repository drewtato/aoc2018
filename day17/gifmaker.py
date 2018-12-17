import os
import shutil
from PIL import Image

GOLD = (255,255,102)
BLUE = (15,15,35)
RED = (255,0,0)
GREEN = (0,153,0)
GREY = (204,204,204)

pixelMap = {
    '.':BLUE,
    '#':GREEN,
    '|':(77, 160, 177),
    '~':(28, 90, 152)
}
# GIFPalette = []
# for pix in [GOLD,BLUE,RED,GREEN,GREY,(77, 160, 177),(28, 90, 152)]:
#     GIFPalette.extend(pix)
# GIFPalette = bytearray(GIFPalette)

frames = []
scale = 2
# print('Running solver')
with open('output.txt') as inp:
    rows = []
    iterations = 0
    for i,line in enumerate(inp):
        if len(line) == 1:
            iterations += 1
            print(f'Saving frame {iterations} on line {i}')
            height = len(rows)
            width = len(rows[0])
            buffer = []
            for row in rows:
                buffer.extend(row)
            img = Image.new('RGB', (width, height))
            img.putdata(buffer)
            img = img.resize((width * scale, height * scale))
            frames.append(img)
            # img.show()
            # input()
            rows = []
        else:
            rows.append([pixelMap[c] for c in filter(lambda c: c != '\n', line)])

print('Removing old img dir')
shutil.rmtree('img', ignore_errors=True)
os.mkdir('img')

print('Creating new img dir')
filenames = []
for i,img in enumerate(frames):
    if not i % 100:
        print(f'Saving img {i}')
    filenames.append(f'img/{i:04}.png')
    img.save(filenames[-1])

# print('Making durations')
# durations = []
# for _ in frames:
#     durations.append(200)
# durations[-1] = 2000
# print('Saving gif')
# frames[0].save(
#     'fill.gif',
#     save_all=True,
#     append_images=frames[1:],
#     duration=durations,
#     loop=0
# )