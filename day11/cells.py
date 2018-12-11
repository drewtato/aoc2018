from PIL import Image, ImageDraw


img = Image.new('RGB', (300,300))
flat = []
with open('cells.txt', 'r') as cells:
    for line in cells:
        for c in map(int, line.split()):
            if c < 0:
                flat.append((c * -51, 0, 0))
            else:
                flat.append((0, int(c * 63.75), 0))

print(min(flat))
print(max(flat))
img.putdata(flat)

img = img.resize((600,600))

win = list(map(lambda c: c * 2, [233,228,12]))
winRect = [win[0], win[1], win[0] + win[2] - 1, win[1] + win[2] - 1]
imgdraw = ImageDraw.Draw(img)
imgdraw.rectangle(winRect, outline='white')

img = img.resize((1200,1200))
img.save('cells.png')
img.show()