with open('input.txt', 'r') as input:
    input = input.read().strip()
    
    newinput = ''
    last = ''
    # print(input)
    # print(len(input))
    
    for letter in input:
        if last.islower() == letter.isupper():
            if last.lower() == letter.lower():
                # print(f'remove {last} {letter}')
                newinput = newinput[:-1]
                try:
                    last = newinput[-1]
                except IndexError:
                    last = ''
                # print(newinput)
                continue
        
        last = letter
        newinput += last
        # print(newinput)
    input = newinput

    print(len(input))
    
    # part 2
    letters = 'abcdefghijklmnopqrstuvwxyz'
    lengths = []
    
    for letter in letters:
        testinput = input.replace(letter, '')
        testinput = testinput.replace(letter.upper(), '')
        newinput = ''
        last = ''
        
        for letter in testinput:
            if last.islower() == letter.isupper():
                if last.lower() == letter.lower():
                    # print(f'remove {last} {letter}')
                    newinput = newinput[:-1]
                    try:
                        last = newinput[-1]
                    except IndexError:
                        last = ''
                    # print(newinput)
                    continue
            
            last = letter
            newinput += last
        
        lengths.append(len(newinput))
        # print(newinput)
    
    minimum = 1000000
    badone = ''
    for length,letter in zip(lengths, letters):
        if length < minimum:
            badone = letter
            minimum = length
    
    # print(badone, lengths, input)
    print(minimum)
    # for l,let in zip(lengths, letters):
    #     print(let, len(input) - l)