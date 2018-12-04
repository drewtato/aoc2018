with open('input.txt', 'r') as input:
    # Working example that uses a ton of space for the set
    seenWords = set()
    try:
        for word in input:
            for takenOutIndex in range(len(word) - 1):
                scrunched = (word[0:takenOutIndex] + word[(takenOutIndex + 1)::], takenOutIndex)
                if scrunched in seenWords:
                    print(scrunched[0][:-1])
                    raise Exception
                else:
                    seenWords.add(scrunched)
    except Exception:
        pass
        
    # # Me trying to get an answer using sorted lists: unsuccessful
    # input = list(input)
    # sortedFront = sorted(input)
    # sortedBack = sorted([list(reversed(x)) for x in input])
    
    # for item,other in zip(sortedFront,sortedBack):
    #     diffs = 0
    #     for letter,otherLetter in zip(item,other):
    #         if letter != otherLetter:
    #             diffs += 1
    #         elif diffs > 1:
    #             break
    #     if diffs == 1:
    #         print(item, other)