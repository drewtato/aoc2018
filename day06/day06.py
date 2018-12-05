import itertools

with open('input.txt', 'r') as input:
    input = input.read()
    while input[-1].isspace():
        input = input[:-1]
    