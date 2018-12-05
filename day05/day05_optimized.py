from collections import defaultdict as dd
from collections import Counter as Co
import itertools as it

with open('input.txt', 'r') as input:
    input = input.read().strip()

# Part 1: trim the input down as this helps part 2 anyway
newinput = ''
last = ''

for letter in input:
    if last.lower() == letter.lower() and last.islower() == letter.isupper():
        newinput = newinput[:-1]
        try:
            last = newinput[-1]
        except IndexError:
            last = ''
        continue
    
    last = letter
    newinput += last

input = newinput

# Answer to part 1
print(len(input))

# Part 2
# reductions is a dict that maps letters to a counter and a set 
# of already counted indicies. I used a set because there are
# usually not too many indicies that need to be counted, aka
# count(indicies) << len(input)
reductions = dd(lambda: [0, set()])

# addif takes a letter and index and only increments reductions[letter]
# if the index hasn't been counted yet. The indicies are stored in the
# set from above.
def addif(reductions, index, letter):
    # Check if index is already in the set
    if not index in reductions[letter][1]:
        # Add the index to the set (if there is a way to do this
        # and the last line in one go, please create an issue, ty)
        reductions[letter][1].add(index)
        # Increment the count
        reductions[letter][0] += 1

# Similar to the Part 1 loop, except we are going to need the 
# index a lot
for index,letter in enumerate(input):
    # make the current letter lowercase (the upper and lower
    # are counted together). This letter is what we are dealing 
    # with this loop, so all references to reductions will
    # be reductions[letter].
    letter = letter.lower()
    # The current letter, obviously, would get removed if we
    # chose this letter as the best one.
    addif(reductions, index, letter)
    
    backx = index
    forwx = index
    # Now we iterate forward and backward from the current letter 
    # to find how many pairings would collapse if we removed
    # this letter
    while True:
        # The try block is in case of index errors at the beginning
        # or end of the input.
        try:
            # Start 1 behind and 1 in front of the current letter
            backx -= 1
            forwx += 1
            # Sometimes we hit a letter that is the same as our 'letter'.
            # Note that we do not check reductions[letter][1] for this. I
            # think this has to do with the 'cCc' example from the prompt,
            # but am not entirely sure. In any case, letters already counted
            # must not be skipped.
            while input[backx].lower() == letter:
                backx -= 1
            # In front, all we have are letters like our 'letter'. Skip these.
            while input[forwx].lower() == letter:
                forwx += 1
            
            # Get the character at that position
            backchar = input[backx]
            forwchar = input[forwx]
            
            # Check for collapses as in Part 1. I particularly like
            # a.islower() == b.isupper().
            if forwchar.lower() == backchar.lower() and forwchar.islower() == backchar.isupper():
                # Add both back index and forward index to reductions.
                for x in [backx, forwx]:
                    addif(reductions, x, letter)
            # If we did not find a match, then we are done collapsing.
            else:
                break
        # If we have hit an end of the input, there are definitely no 
        # more characters to remove. We break.
        except IndexError:
            break

# Simply find which character had the most removals.
best = max(reductions.values())
# The answer is the length of the remaining string, so subtract.
print(len(input) - best[0])