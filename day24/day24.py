import sys
from contextlib import contextmanager
from collections import defaultdict as dd
# import os
# import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import deque as dq
from copy import deepcopy as dc

DEBUG,PRINT,OUT,outfile,infile = False,False,False,None,'input.txt'
for arg in sys.argv[1:]:
    if OUT:
        outfile = arg if arg[0] != '-' else 'output.txt'
        OUT = False
    elif arg == '-d':
        DEBUG = True
    elif arg == '-p':
        PRINT = True
    elif arg == '-o':
        OUT = True
    elif arg[0] != '-':
        infile = arg
    else:
        print(f'No "{arg}" arg."')
        sys.exit(1)
@contextmanager
def fileOrStdout(filename=None):
    if filename:
        fh = open(filename, 'w')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()
def replacer(inp, remove=[], replace=[]):
    pairs = []
    for reading,default in [(remove,''),(replace,' ')]:
        if len(reading) == 1:
            reading = [c for c in reading[0]]
        for items in reading:
            first = items[0]
            second = items[1] if len(items) == 2 else default
            pairs.append((first, second))
    for k,v in pairs:
        inp = inp.replace(k,v)
    return inp
with open(infile, 'r') as inp:
    inp = inp.read()
while inp[-1].isspace():
    inp = inp[:-1]

removals = [',',';'
]
replacements = [
    ['hit points with', 'hit points () with'],
    [' units each with ','#'],
    [' hit points ','#'],
    [' with an attack that does ','#'],
    [' damage at initiative ','#'],
    [' to ']
    # '<',
    # '>',
    # '(',
    # ')',
    # '[',
    # ']',
    # ':',
    # ',',
    # ';',
    # '=',
    # '\n',
]
inp = replacer(inp, removals, replacements)
# print(inp)
data = []

elemCount = 0
def elemCounter():
    global elemCount
    elemCount += 1
    return elemCount

elements = dd(elemCounter)
INFECT = 0
IMMUNE = 1
systems = {
    'Infect':INFECT,
    'Immune':IMMUNE
}
for line in inp.split('\n'):
    if not line:
        continue
    try:
        system = systems[line[:6]]
        continue
    except KeyError:
        pass
    items = line.split('#')
    units = int(items[0])
    hp = int(items[1])
    dmgtype = items[3].split()
    ap = int(dmgtype[0])
    elem = elements[dmgtype[1]]
    initiative = int(items[4])
    vulnerabilities = items[2][1:-1].split()
    imms = []
    weaks = []
    onWeak = None
    for word in vulnerabilities:
        if word == 'weak':
            onWeak = True
        elif word == 'immune':
            onWeak = False
        else:
            e = elements[word]
            if onWeak:
                weaks.append(e)
            else:
                imms.append(e)
    effPow = units * ap
    data.append([initiative,effPow,system,units,hp,ap,elem,imms,weaks])
# print(data)
revElems = {v:k for k,v in elements.items()}
elements = dict(elements)

def fight(info,boost=0):
    data,_ = info
    for d in data:
        if d[2] == IMMUNE:
            d[5] += boost
            d[1] = d[5] * d[3]
    data = sorted(data, reverse=True)
    r = 0
    while True:
        r += 1
        targetData = sorted(enumerate(data), key=lambda d: (d[1][1],d[1][0]),reverse=True)
        if DEBUG:
            print(r)
            for item in targetData:
                print(item)
            print()
        
        targets = [None] * len(data)
        
        added = set()
        for i,attacker in targetData:
            maxAttack = 0
            for j,defender in targetData:
                if defender[2] == attacker[2] or attacker[6] in defender[7] or j in added:
                    continue
                multiplier = 2 if attacker[6] in defender[8] else 1
                if multiplier > maxAttack:
                    maxAttack = multiplier
                    targets[i] = j
                    if maxAttack == 2:
                        break
            if targets[i] != None:
                added.add(targets[i])
            
        dead = set()
        totalAttack = 0
        for i,group in enumerate(data):
            if i in dead:
                continue
            if targets[i] == None:
                continue
            effPow = group[3] * group[5]
            defender = data[targets[i]]
            multiplier = 2 if group[6] in defender[8] else 1
            attack = (effPow * multiplier) // defender[4]
            totalAttack += attack
            if DEBUG:
                print(i,attack,defender[0],(effPow,multiplier,defender[4]))
            defender[3] -= attack
            if defender[3] <= 0:
                dead.add(targets[i])
        if not totalAttack:
            raise LoopError
        for i in sorted(dead, reverse=True):
            del data[i]

        for i,group in enumerate(data):
            effPow = group[3] * group[5]
            group[1] = effPow

        immLeft = 0
        infLeft = 0
        unitsLeft = 0
        for group in data:
            if group[3] <= 0:
                print('oh no')
            unitsLeft += group[3]
            if group[2] == IMMUNE:
                immLeft += 1
            else:
                infLeft += 1
        if (not immLeft) or (not infLeft):
            break
    if DEBUG:
        for item in data:
            print(item)
        print()
    return unitsLeft,immLeft,infLeft

class LoopError(Exception):
    pass

def boosting(info):
    data,out = info
    boost = 1
    while True:
        boost += 1
        try:
            units,imm,inf = fight((dc(data),out),boost=boost)
        except LoopError:
            if DEBUG:
                print('looped')
            continue
        if DEBUG:
            print(boost,units,imm,inf)
        if imm:
            break
    return units

try:
    with fileOrStdout(outfile) as out:
        info = dc(data),out
        if DEBUG:
            for item in data:
                print(item)
            for e,v in elements.items():
                print(e,v)
        
        units,_,_ = fight(info)
        print(units)
        
        info = dc(data),out
        neededBoost = boosting(info)
        print(neededBoost)

except KeyboardInterrupt:
    print('Interrupted')