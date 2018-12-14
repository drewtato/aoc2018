from collections import deque as dq
import itertools as it

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

pots = inp.split('\n')[0][15:]
pots = dq(map(lambda p: 1 if p == '#' else 0, pots))
# print(pots)

rules = [0] * 2**5

for line in reversed(sorted(inp.split('\n')[2:])):
    # print(line)
    if line[-1] == '#':
        state = 0
        for i in range(5):
            state = state << 1
            state += 1 if line[i] == '#' else 0
        rules[state] = 1

# print(rules)
# print(len(pots))
def generate(pots, rules, gens, f):
    
    def getsum(pots, zero):
        s = 0
        for i,p in zip(range(-zero, len(pots) - zero), pots):
            if p:
                s += i
        return s
                
    zeroPot = 0
    pots.extendleft(it.repeat(0, 2))
    
    for i in range(gens):
        # print(i)
        
        for p in pots:
            c = '#' if p else ' '
            f.write(c)
        f.write('\n')
        
        newpots = dq([0,0])
        pots.extendleft([0,0])
        pots.extend([0,0,0,0])
        for i in range(len(pots) - 4):
            state = 0
            for j in range(5):
                state = state << 1
                state += pots[i + j]
            newpots.append(rules[state])
        while newpots.pop() == 0:
            pass
        newpots.append(1)
        
        pots = dq(list(newpots)[2:])
    return getsum(pots, zeroPot)
    
with open('pots.txt', 'w') as f:
    generate(pots, rules, 200, f)