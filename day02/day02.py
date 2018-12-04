from collections import Counter

with open('input.txt', 'r') as input:
    input = input.read()
    threes = 0
    twos = 0
    for line in input.split():
        count = Counter(line)
        isTwo = False
        isThree = False
        for _,item in count.items():
            if item == 2:
                isTwo = True
            elif item == 3:
                isThree = True
        if isTwo: twos +=1
        if isThree: threes += 1
    
    print(threes * twos)
    
    # Part 2
    done = False
    string = ''
    for item in input.split():
        for otherItem in input.split():
            differences = 0
            string = ''
            for letter,otherLetter in zip(item, otherItem):
                if letter != otherLetter:
                    differences += 1
                    if differences > 1:
                        break
                else:
                    string += letter
            if differences == 1:
                # print(item, '\n', otherItem)
                done = True
                break
        if done == True:
            break
    
    print(string)