with open('input.txt', 'r') as input:
    freq = 0
    newinput = input.read()
    visited = set()
    for line in newinput.split():
        freq += int(line)
    print(freq)
    
    going = True
    freq = 0
    while going:
        for line in newinput.split():
            freq += int(line)
            if freq in visited:
                going = False
                print(freq)
                break
            else:
                visited.add(freq)
