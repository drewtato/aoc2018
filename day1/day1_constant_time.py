with open('input.txt', 'r') as input:
    
    # # This one ran in constant space, but O(n^2)
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
    

    # This one is O(n)
    freq = 0
    visited = []
    # Get all first iteration frequencies
    for line in input:
        freq += int(line)
        visited.append(freq)
        
    mods = {}
    # minIterations = (
    #   iterations, 
    #   frequency that will be reached at that iteration,
    #   index when we hit that iteration
    # )
    minIterations = (100000, 0, 0)
    # Go through and modulo each one with the last frequency, which
    # will be the offset from one iteration to the next
    #
    # We are assuming the offset is > 0
    for index,item in enumerate(visited):
        m = item % freq
        # If that modulo was already found, it means that the lower
        # frequency will eventually meet the higher frequency
        if m in mods:
            iterations = int((visited[mods[m]] - item) / freq)
            negative = False
            # Check which index's value is lower: the lower one will
            # increase (we assumed offset > 0) until it reaches the
            # higher one
            if iterations < 0:
                iterations *= -1
                negative = True
            # If this is the lowest number of iterations we have seen,
            # save the lower frequency's index and higher frequency's,
            # well, frequency
            if iterations < minIterations[0]:
                if negative:
                    minIterations = (iterations, item, mods[m])
                else:
                    minIterations = (iterations, visited[mods[m]], index)
            # If this is equal to the lowest iterations, check if the index
            # of the lower frequency is earlier than what we have saved (the
            # earlier one will be reached first)
            elif iterations == minIterations[0]:
                if negative:
                    if minIterations[2] > mods[m]:
                        minIterations = (iterations, item, mods[m])
                else:
                    if minIterations[2] > index:
                        minIterations = (iterations, visited[mods[m]], index)
        
        else:
            # If we didn't find the modulo yet, add it
            mods.update({m: index})
    
    print(minIterations[1])