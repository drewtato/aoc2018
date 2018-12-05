from collections import defaultdict as dd
import itertools as it

CORRECT = True

with open('input.txt', 'r') as input:
    input = input.read().strip()

# Part 1: trim the input down as this helps part 2 anyway
newinput = ''
last = ''

for letter in input:
    if last.lower() == letter.lower() and last != letter:
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
# of already counted indicies. It keeps track of which indicies
# of input would be removed if the corresponding key (a lowercase
# letter) was chosen as the best. This is to avoid double-counting,
# which happens since we do not store a separate input for each letter.
# I used a set because there are usually not too many indicies 
# that need to be counted, aka count(indicies) << len(input)
reductions = dd(lambda: [0, set()])

# addif takes an index and only increments reduct if
# the index hasn't been counted yet. reduct is an item from the
# dict reductions. The indicies are remembered in the set from above.
def addif(reduct, index):
    # Check if index is already in the set
    if not index in reduct[1]:
        # Add the index to the set (if there is a way to do this
        # and the last line in one go, please create an issue, ty)
        reduct[1].add(index)
        # Increment the count
        reduct[0] += 1

# Similar to the Part 1 loop, except we are going to need the
# index a lot
for index,letter in enumerate(input):
    # make the current letter lowercase (the upper and lower
    # are counted together). This letter is what we are dealing
    # with this loop, so all references to reductions will
    # be reductions[letter].
    letter = letter.lower()
    reduct = reductions[letter]
    # The current letter, obviously, would get removed if we
    # chose this letter as the best one.
    addif(reduct, index)

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
            if CORRECT:
                while backx in reduct[1]:
                    backx -= 1
            else:
                while input[backx].lower() == letter:
                    backx -= 1
            # In front, skip all letters like our 'letter'.
            while input[forwx].lower() == letter:
                forwx += 1

            # Get the character at that position
            backchar = input[backx]
            forwchar = input[forwx]

            # Check for collapses as in Part 1.
            if forwchar.lower() == backchar.lower() and forwchar != backchar:
                # Add both back index and forward index to reductions.
                for x in [backx, forwx]:
                    addif(reduct, x)
            # If we did not find a match, then we are done collapsing.
            else:
                break
        # If we have hit an end of the input, there are definitely no
        # more characters to remove. We break.
        except IndexError:
            break

# Simply find which character had the most removals.
# Remember that a value is [counter, set], so the counter
# is maxed (and set is used for ties, which don't happen).
best = max(reductions.values())
# The answer is the length of the remaining string, so subtract.
print(len(input) - best[0])