# import itertools as it
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

stop = int(inp) # This kills zero padding, so beware
# print(stop)

def taste(elves, scoreboard):
    combined = 0
    for elf in elves:
        combined += scoreboard[elf]
    scoreboard.extend([int(c) for c in str(combined)])
    numrecipes = len(scoreboard)
    newelves = []
    for elf in elves:
        newelves.append((elf + 1 + int(scoreboard[elf])) % numrecipes)
    
    return newelves, scoreboard

elves = [0,1]
scoreboard = [3,7]
seen = 0

while len(scoreboard) < stop + 10:
    elves, scoreboard = taste(elves, scoreboard)

for c in scoreboard[stop : stop + 10]:
    print(c, end='')
print()

stopstr = [int(c) for c in inp]
stoplen = len(stopstr)
nextmilestone = 1000000
while not seen:
    combined = 0
    for elf in elves:
        combined += scoreboard[elf]
    for c in str(combined):
        scoreboard.append(int(c))
        if stopstr == scoreboard[-stoplen:]:
            # print(scoreboard)
            seen = len(scoreboard) - stoplen
    numrecipes = len(scoreboard)
    # if numrecipes >= nextmilestone:
    #     nextmilestone = numrecipes + 1000000
    #     print(numrecipes)
    newelves = []
    for elf in elves:
        newelves.append((elf + 1 + int(scoreboard[elf])) % numrecipes)
        
    elves = newelves

print(seen)