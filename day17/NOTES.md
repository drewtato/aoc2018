# Notes on Day 17

## Running `day17.py`

### Correctness

The current algorithm is *very slightly* wrong (about 1%, sometimes, for the first part only). It sometimes stacks flowing water on top of other flowing water. This is insignificant enough that it won't cause problems for visualizing, but let it be known that it exists. Part 2 is perfect.

### Optimization

Only turn on options when necessary, and if you can, run with pypy3.

### Options

These are simply space-delimited. Example usage (with slow and debug on):  
`python3 day17.py s d`

* `s`: Slow mode. This creates waterfalls one block per iteration instead of all in one iteration. Good for visualization.
* `d`: Debug mode. Prints out round numbers and how much water is left (according to my input) to fill.
* `p`: Print mode. Saves every iteration to `output.txt`.

## Running `gifmaker.py`

This is very straightforward. There's some commented sections but unchanged, it simply takes all the frames from `output.txt` and turns them into PNGs inside the `img` folder.

## Creating video

I used ffmpeg but you can use moviepy or whatever you like.

Creating the original video:

```sh
ffmpeg -r 60 -f image2 -i ./img/%04d.png fill_vertical.mp4
```

Creating the horizontal version:

```sh
ffmpeg.exe -i .\fill_vertical.mp4 -vf 'transpose=2' fill_horizontal.mp4
```