import itertools
import sys

LENGTH = 1000

with open('input.txt', 'r') as input:
    ans = 0
    fabric = [0]*LENGTH*LENGTH
    # print(fabric)
    
    rectangles = []
    for line in input:
        part = line\
            .replace('#','')\
            .replace(' @ ', ' ')\
            .replace(',', ' ')\
            .replace(': ', ' ')\
            .replace('x', ' ')\
            .split()
        rectangles.append(list(map(int,part)))
    # print(rectangles)
    
    for rect in rectangles:
        x = rect[1]
        y = rect[2]
        for sx in range(rect[3]):
            for sy in range(rect[4]):
                index = x + sx + (y + sy)*LENGTH
                fabric[index] += 1
                
                
    for square in fabric:
        if square > 1:
            ans += 1
    
    try :
        if sys.argv[1]:
            with open('fab.txt', 'w') as fab:
                for i,square in enumerate(fabric):
                    fab.write(f'{square: 2}')
                    if not (i + 1)%LENGTH:
                        fab.write('\n')
    except IndexError:
        pass
    print(ans)
    
    # Part 2
    for rect in rectangles:
        works = True
        x = rect[1]
        y = rect[2]
        for sx in range(rect[3]):
            for sy in range(rect[4]):
                index = x + sx + (y + sy)*LENGTH
                if fabric[index] - 1:
                    works = False
        if works:
            print(rect[0])
            # print(rect)
            break