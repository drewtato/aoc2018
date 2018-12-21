import sys
from contextlib import contextmanager
from collections import defaultdict as dd
# import os
# import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import deque as dq
# from copy import deepcopy as dc

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
with open(infile, 'r') as inp:
    inp = inp.read()
while inp[-1].isspace():
    inp = inp[:-1]
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
opcodes = {
    'addr':addr,
    'addi':addi,
    'mulr':mulr,
    'muli':muli,
    'banr':banr,
    'bani':bani,
    'borr':borr,
    'bori':bori,
    'setr':setr,
    'seti':seti,
    'gtir':gtir,
    'gtri':gtri,
    'gtrr':gtrr,
    'eqir':eqir,
    'eqri':eqri,
    'eqrr':eqrr,
}
data = []
for line in inp.split('\n'):
    if line[0] == '#':
        ip = int(line.split()[1])
    else:
        ins = list(line.split())
        op = [opcodes[ins[0]]]
        op.extend([int(c) for c in ins[1:]])
        data.append(op)

def pState(data, regs, ip, out):
    if DEBUG:
        out.write(f'{regs[ip]: 3} {data[regs[ip]][0].__name__} {regs}')
        out.write('\n')
        if DEBUG:
            input()

def run(data, regs, ip, out):
    counter = 0
    possibles = {}
    last = 0
    first = True
    while regs[ip] >= 0 and regs[ip] < len(data):
        pState(data,regs,ip,out)
        args = data[regs[ip]][1:]
        data[regs[ip]][0](args,regs)
        regs[ip] += 1
        counter += 1
        if regs[ip] == 28:
            val = regs[3]
            if first:
                print(val)
                first = False
            if val in possibles:
                # print(f'{counter}, {val}, {val - last}')
                print(last)
                break
            possibles.update({val:counter})
            last = val

try:
    with fileOrStdout(outfile) as out:
        regs = [0] * 6
        run(data,regs, ip, out)

except KeyboardInterrupt:
    print('Interrupted')
