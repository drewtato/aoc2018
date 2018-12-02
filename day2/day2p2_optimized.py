with open('input.txt', 'r') as input:
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