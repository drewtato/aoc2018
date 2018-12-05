import itertools
from collections import Counter as Co
from collections import defaultdict as dd

with open('input.txt', 'r') as input:
    input = input.read()

while input[-1].isspace():
    input = input[:-1]

