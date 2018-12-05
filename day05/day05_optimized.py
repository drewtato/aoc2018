with open('input.txt', 'r') as input:
    input = input.read().strip()
    
    newinput = ''
    last = ''
    
    for letter in input:
        if last.islower() == letter.isupper():
            if last.lower() == letter.lower():
                newinput = newinput[:-1]
                try:
                    last = newinput[-1]
                except IndexError:
                    last = ''
                continue
        
        last = letter
        newinput += last
    input = newinput

    print(len(input))
    
    # part 2
    letters = 'qwertyuiopasdfghjklzxcvbnm'
    lengths = []
    
    for letter in letters:
        testinput = input.replace(letter, '')
        testinput = testinput.replace(letter.upper(), '')
        newinput = ''
        last = ''
        
        for letter in testinput:
            if last.islower() == letter.isupper():
                if last.lower() == letter.lower():
                    newinput = newinput[:-1]
                    try:
                        last = newinput[-1]
                    except IndexError:
                        last = ''
                    continue
            
            last = letter
            newinput += last
        
        lengths.append(len(newinput))
    
    minimum = min(zip(lengths, letters))[0]
    
    print(minimum)