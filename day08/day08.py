# import itertools
# from collections import Counter as Co
# from collections import defaultdict as dd

with open('input.txt', 'r') as inp:
    inp = inp.read()

while inp[-1].isspace():
    inp = inp[:-1]

inpItems = list(map(int, inp.split()))
maxItem = max(inpItems)
# print(maxItem)

def createTree(items, nodes, counter=[1]):
    children = items[0]
    metadata = items[1]
    childNames = []
    restOfItems = items[2:]
    for _ in range(children):
        restOfItems,child = createTree(restOfItems, nodes, counter)
        childNames.append(child)
    metas = restOfItems[:metadata]
    nodes[counter[0]] = (metas, childNames)
    counter[0] += 1
    return restOfItems[metadata:], counter[0] - 1

nodes = {}
_,root = createTree(inpItems, nodes)
# print(root)
# print(nodes)
total = 0
for name,(metas,childNames) in nodes.items():
    total += sum(metas)
    # print(name, childNames, metas)
    
print(total)

def sumNode(nodes, root):
    metas,childNames = nodes[root]
    s = 0
    if childNames:
        for meta in metas:
            if meta != 0 and meta <= len(childNames):
                s += sumNode(nodes, childNames[meta - 1])
                # print(f'Summing child {meta - 1} for {root}: s={s}')
    else:
        s = sum(metas)
        # print(f'Summing metas for {root}: s={s}')
    return s        
        
        
print(sumNode(nodes, root))