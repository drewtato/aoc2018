# import itertools
from collections import deque as dq
# from collections import Counter as Co
from collections import defaultdict as dd
# import time

with open('input.txt', 'r') as inp:
    inp = inp.read()

# while inp[-1].isspace():
#     inp = inp[:-1]

inp = inp.split()
numPlayers = int(inp[0])
last = int(inp[6])

def play(numPlayers, last):
    players = dd(int)
    currentPlayer = 0
    circle = dq([0])

    for marble in range(1,last + 1):
        currentPlayer = currentPlayer % numPlayers + 1
        if marble % 23:
            circle.append(circle.popleft())
            circle.append(marble)
        else:
            players[currentPlayer] += marble
            for _ in range(7):
                circle.appendleft(circle.pop())
            players[currentPlayer] += circle.pop()
            circle.append(circle.popleft())
            
        # print(marble, currentPlayer, end='')
        # for member in circle:
        #     print(f' | {member}', end='')
        # print()

    return max(players.values())

# t = time.perf_counter()

print(play(numPlayers, last))
print(play(numPlayers, last * 100))

# print(f'{time.perf_counter() - t}')