import itertools
from collections import Counter as Co
from collections import defaultdict as dd
import networkx as nx

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

steps = [(line[5], line[36]) for line in inp.split('\n')]

graph = nx.DiGraph()

graph.add_edges_from(steps)
originalGraph = graph.copy()

part1 = True
if part1:
    # guessNode = 'A'
    # firstNode = None
    # while not firstNode:
    #     # print(list(graph.predecessors(guessNode)))
    #     newNode = list(graph.predecessors(guessNode))
    #     if not newNode:
    #         firstNode = guessNode
    #     else:
    #         guessNode = newNode[0]
            
    # print(firstNode)
    # print(list(graph.predecessors('D')))
    # print(list(graph.successors('D')))
    s = ''
    while graph.nodes:
        possibles = ''
        # print(graph.nodes)
        for node in graph.nodes:
            # print(node)
            if not list(graph.predecessors(node)):
                possibles += node
        # print(possibles)
        remove = sorted(possibles)[0]
        graph.remove_node(remove)
        s += remove
            
    print(s)

graph = originalGraph
timeLeft = dict([
    (chr(ord('A') + num), num + 61) for num in range(26)
])
timeLeft.update([(None, 10000)])
# print(timeLeft)
workers = [None] * 5
# print(graph.nodes)

time = 0
while graph.nodes:
    # print(f'{time}: {sorted(graph.nodes)}')
    # print(sorted(list(timeLeft.items())[:-1]))
    possibles = ''
    for node in graph.nodes:
        # print(f'check node {node} for successors')
        if (node not in workers) and (not list(graph.predecessors(node))):
            possibles += node
    possibles = list(reversed(sorted(possibles)))
    for index in range(len(workers)):
        # print(f'assign worker {index} to {possibles[-1]}')
        if workers[index] == None:
            if possibles:
                # print(possibles)
                workers[index] = possibles[-1]
                possibles = possibles[:-1]
            else:
                workers[index] = None
        
    m = min(map(lambda workNode: timeLeft[workNode], workers))
    # print(m)
    # print(workers)
    for i,node in enumerate(workers):
        if node:
            timeLeft[node] -= m
            if not timeLeft[node]:
                graph.remove_node(node)
                del timeLeft[node]
                workers[i] = None
    time += m
    
print(time)