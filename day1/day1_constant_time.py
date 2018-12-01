"""
This runs in constant space, but still takes O(n^2) time.
(as opposed to O(n*iterations) time for the original answer)
There's surely a way to get it to run in constant time,
but I struggle.
"""

with open('input.txt', 'r') as input:
    # freq = 0
    # visited = [0]
    # for line in input:
    #     freq += int(line)
    #     visited.append(freq)
    
    # done = False
    # for v in visited:
    #     for u in visited:
    #         # print(f'{v} {u} {(v - u) % freq}')
    #         if (not (u - v) % freq) and v != u and v != freq and u != freq:
    #             print(u) # u is what the frequency *will* be.
    #             done = True
    #             break
    #     if done:
    #         break
    

# This one will be O(n) I promise
    freq = 0
    visited = []
    for line in input:
        freq += int(line)
        visited.append(freq)
        
    mods = {}
    minIterations = (100000, 0)
    for index,item in enumerate(visited):
        m = item % freq
        if m in mods:
            iterations = (item - visited[mods[m]]) / freq
            if iterations <= minIterations[0]:
                minIterations = (iterations, max(
                    visited[index],
                    visited[mods[m]],
                    minIterations[1]
                ))
        else:
            mods.update({m: index})
    
    print(minIterations[1])