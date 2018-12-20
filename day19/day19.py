import sys
from contextlib import contextmanager
from collections import defaultdict as dd
# import os
# import itertools as it
# import functools as ft
# from collections import Counter as Co
# from collections import deque as dq
# from copy import deepcopy as dc
import math
import time

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
        for line in reading:
            items = line.split(' ')
            first = items[0] if items[0] else ' '
            second = items[1] if len(items) > 1 else default
            pairs.append((first, second))
    for k,v in pairs:
        inp = inp.replace(k,v)
    return inp
with open(infile, 'r') as inp:
    inp = inp.read()
while inp[-1].isspace():
    inp = inp[:-1]
def pData(data, out, revMap):
    if PRINT:
        for row in data:
            for c in row:
                out.write(str(c) + ' ')
            out.write('\n')
        out.write('\n')
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
# removals = []
# replacements = [
#     # '<',
#     # '>',
#     # ':',
#     # ',',
#     # ';',
#     # '=',
#     # '\n',
# ]
# inp = replacer(inp, removals, replacements)
program = []
for line in inp.split('\n'):
    args = line.split()
    if args[0] == '#ip':
        ipReg = int(args[1])
    else:
        row = [opcodes[args[0]]]
        row.extend(map(int, args[1:]))
        program.append(row)
# print(data)

# ipReg: index of instruction pointer register (first line of input)
# regs: list of 6 numbers representing registers
# opcodes: mapping of opcodes to their respective functions
# instructions: input parsed as list of [function pointer, arg1, arg2, arg3]
def runProgram(ipReg,regs,instructions):
    if DEBUG:
        counter = 0
        t = time.perf_counter()
        try:
            while counter < 100000000:
                ins = instructions[regs[ipReg]]
                ins[0](ins[1:],regs)
                regs[ipReg] += 1
                counter += 1
        except IndexError:
            pass
        t = time.perf_counter() - t
        perG = t * 10**9 / counter
        print(f'Time: {t}\nPer 1G instructions: {perG:.8}')
        number = max(regs)
        print(f'Time to run all (days): {perG * 8 * number**2/10**9/60/60/24:.8}')
    else:
        # Instruction 1 starts the main loop. When it reaches
        # 1, we know that the large number is in the registers.
        while regs[ipReg] != 1:
                ins = instructions[regs[ipReg]]
                ins[0](ins[1:],regs)
                regs[ipReg] += 1
        # Not sure if the large number is in a different position, so
        # find it by taking the max.
        number = max(regs)
    # Find the sum all factors of the large number (the
    # algorithm from the input), stored in divisors.
    root = math.sqrt(number)
    end = int(root)
    # If it is a perfect square, count its square root.
    # Otherwise, initialize to zero.
    divisors = end if root == end else 0
    # Check all numbers from 1 to the root - 1
    for i in range(1, end):
        if number % i == 0:
            divisors += i
            divisors += number // i
    return divisors

try:
    with fileOrStdout(outfile) as out:
        regs = [0] * 6
        ans = runProgram(ipReg,regs,program)
        if DEBUG:
            print(regs)
        out.write(str(ans))
        out.write('\n')
        regs = [0] * 6
        regs[0] = 1
        ans = runProgram(ipReg,regs,program)
        if DEBUG:
            print(regs)
        out.write(str(ans))

except KeyboardInterrupt:
    print('Interrupted')
