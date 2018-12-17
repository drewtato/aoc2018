# import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import defaultdict as dd
# from collections import deque as dq
# from copy import deepcopy

with open('input2.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

tests = []
program = []
firstPart = True
for line in inp.split('\n'):
    if firstPart:
        line = line.replace(',', ' ')
        line = line.replace('[', ' ')
        line = line.replace(']', ' ')
        line = line.split()
        if line:
            if line[0][0] == 'B':
                preregs = list(map(int, line[1:]))
            elif line[0].isdigit():
                instruction = list(map(int, line))
            elif line[0][0] == 'A':
                postregs = list(map(int, line[1:]))
        else:
            if preregs:
                tests.append([preregs, instruction, postregs])
                preregs = None
            else:
                firstPart = False
    else:
        if line:
            program.append(list(map(int,line.split())))

def addr(args, regs):
    a,b,c = args
    regs[c] = regs[a] + regs[b]
def addi(args, regs):
    a,b,c = args
    regs[c] = regs[a] + b
def mulr(args, regs):
    a,b,c = args
    regs[c] = regs[a] * regs[b]
def muli(args, regs):
    a,b,c = args
    regs[c] = regs[a] * b
def banr(args, regs):
    a,b,c = args
    regs[c] = regs[a] & regs[b]
def bani(args, regs):
    a,b,c = args
    regs[c] = regs[a] & b
def borr(args, regs):
    a,b,c = args
    regs[c] = regs[a] | regs[b]
def bori(args, regs):
    a,b,c = args
    regs[c] = regs[a] | b
def setr(args, regs):
    a,_,c = args
    regs[c] = regs[a]
def seti(args, regs):
    a,_,c = args
    regs[c] = a
def gtir(args, regs):
    a,b,c = args
    regs[c] = int(a > regs[b])
def gtri(args, regs):
    a,b,c = args
    regs[c] = int(regs[a] > b)
def gtrr(args, regs):
    a,b,c = args
    regs[c] = int(regs[a] > regs[b])
def eqir(args, regs):
    a,b,c = args
    regs[c] = int(a == regs[b])
def eqri(args, regs):
    a,b,c = args
    regs[c] = int(regs[a] == b)
def eqrr(args, regs):
    a,b,c = args
    regs[c] = int(regs[a] == regs[b])

allIns = [
    addr,addi,
    mulr,muli,
    banr,bani,
    borr,bori,
    setr,seti,
    gtir,gtri,gtrr,
    eqir,eqri,eqrr
]

badTests = 0
possibles = []
for i in range(len(allIns)):
    possibles.append(allIns.copy())
    
for test in tests:
    before = test[0]
    after = test[2]
    args = test[1][1:]
    correctIns = 0
    for ins in allIns:
        bcopy = before.copy()
        ins(args, bcopy)
        if after == bcopy:
            correctIns += 1
        else:
            try:
                possibles[test[1][0]].remove(ins)
            except ValueError:
                pass
    if correctIns >= 3:
        badTests += 1

print(badTests)
    
while max(map(len, possibles)) > 1:
    for i,fs in enumerate(possibles):
        if len(fs) == 1:
            for j in range(len(possibles)):
                if j != i:
                    try:
                        possibles[j].remove(fs[0])
                    except ValueError:
                        pass

# for i,fs in enumerate(possibles):
#     print(i, end=' ')
#     for f in fs:
#         print(f.__name__, end=' ')
#     print()

opcodes = [f[0] for f in possibles]

# for op in opcodes:
#     print(op.__name__)

regs = [0,0,0,0]
for ins in program:
    opcodes[ins[0]](ins[1:], regs)

print(regs[0])
