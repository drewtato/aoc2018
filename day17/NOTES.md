# Notes on running `day17.py`

## Correctness

The current algorithm is *very slightly* wrong (about 1% for the first part only). It sometimes stacks flowing water on top of other flowing water. This is insignificant enough that it won't cause problems for visualizing, but let it be known that it exists. Part 2 is perfect, though.

## Optimization

Only turn on options when necessary, and if you can, run with pypy3.

## Options

These are simply space-delimited. Example usage (with slow and debug on):  
`python3 day17.py s d`

* `s`: Slow mode. This creates waterfalls one block per iteration instead of all in one iteration. Good for visualization.
* `d`: Debug mode. Prints out round numbers and how much water is left (according to my input) to fill.
* `p`: Print mode. Saves every iteration to `output.txt`.
