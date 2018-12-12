# import itertools as it
# from collections import Counter as Co
# from collections import defaultdict as dd
from collections import deque as dq
import copy

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
def generate(pots, rules, gens):
    
    def getsum(pots, zero):
        s = 0
        for i,p in zip(range(-zero, len(pots) - zero), pots):
            if p:
                s += i
            # print(f'{i} {p} {s}')
        return s
                
    zeroPot = 0
    for i in range(gens):
        # if i % 100000 == 0:
        #     print(i, sum(pots), getsum(pots, zeroPot))
        newpots = dq()
        # print(pots)
        pots.extendleft([0,0,0,0])
        zeroPot += 1
        pots.extend([0,0,0,0])
        for i in range(len(pots) - 4):
            state = 0
            for j in range(5):
                state = state << 1
                state += pots[i + j]
            # print(f'{rules[state]}', end='')
            newpots.append(rules[state])
            # print(newpots)
        # print()
        # for p in pots:
        #     print(f'{p: 2}', end='')
        while newpots.popleft() == 0:
            zeroPot -= 1
        while newpots.pop() == 0:
            pass
        newpots.appendleft(1)
        newpots.append(1)
        zeroPot += 1
        
        pots = newpots
        # print(len(pots))

    # print(pots)
    

    return getsum(pots, zeroPot)

print(generate(pots.copy(), rules, 20))
# print(generate(pots, rules, 50000000000)) # Lol yea right, let's get a better answer
large = 1000
aftermany = generate(pots.copy(), rules, large)
aftertwice = generate(pots.copy(), rules, large * 2)
difference = aftertwice - aftermany
answer = aftermany + difference * (int(50000000000 / large) - 1)
print(answer)