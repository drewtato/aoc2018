"""
This runs in constant space, but still takes O(n^2) time.
(as opposed to O(n*iterations) time for the original answer)
There's surely a way to get it to run in constant time,
but I struggle.
"""

with open('input.txt', 'r') as input:
    newinput = input.read()
    freq = 0
    visited = [0]
    for line in newinput.split():
        freq += int(line)
        visited.append(freq)
    
    done = False
    for v in visited:
        for u in visited:
            # print(f'{v} {u} {(v - u) % freq}')
            if (not (u - v) % freq) and v != u and v != freq and u != freq:
                print(u) # u is what the frequency *will* be.
                done = True
                break
        if done:
            break