# Options

These are simply space-delimited. Example usage (with slow and debug on):  
`python3 day17.py s d`

* `s`: Slow mode. This creates waterfalls one block per iteration instead of all in one iteration. Good for visualization.
* `d`: Debug mode. Prints out round numbers and how much water was added on that round.
* `p`: Print mode. Saves every iteration to `output.txt`.

## Optimization

Only turn on options when necessary, and if you can, run with pypy3.