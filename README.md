# Beeflow

Implementation of the non-directional speed detector described in "How Bees Exploit Optic Flow: Behavioural Experiments and Neural Models [and Discussion]" (MSrinivasan and Gregory, 1992)

# TODO

- implement arguments
- test on more footage
- better averaging - take a moving average not a chunk at a time
- plot the difference in R/L speed per frame (which should tell a bee its horizontal position)
- paste this into the movie

# Process

1. Convert to a binary image (high sensitivity to contrast, saturate at low contrast)
2. Spatially low-pass filter, to give an image in which abrupt edges have been converted into ramps of constant slope
3. Measure speed of image by measuring rate of change of response at the ramps. One image generates a train of pulses, one at each edge. Amplitude of each pulse is proportional to the rate of change of intensity at the corresponding ramp, and thus to the speed of the image at that location.
4. Use rectification to ensure the response is positive regardless of direction of movement.


# Videos

mumbai-720p.mp4 - original Mumbai street video, downloaded from https://www.youtube.com/watch?v=70OUmiT-Rzc

mumbai-320.mp4 - transformed to be lower resolution and no audio, using command line:

ffmpeg -i mumbai-720p.mp4 -vf scale=-1:360 -c:v libx264 -crf 18 -an -preset veryslow -c:a copy output.mp4

Good subsections to analyze:
00:41 - 01:17 (frames 1700 - 2200) and 01:30 - 02:45 (walkway scenes with walls to left and right)

v1.mp4 - short run through a b/w tunnel, good to calibrate on
v2.mp4 - much longer run through a b/w tunnel
sonoma.mp4 - some footage I shot walking along a tunnel of trees in sonoma

# Usage

Turn a video into a CSV logging the average edge-values at each frame:

python beeflow-video.py input.mp4 output.csv --edgesize=1 --maxframes=10000 --preview=true --preservefps=false

Take one of these CSV files and plot the average speed of pulses at left and right edges:

python beeflow-csv.py input.csv --startframe=1 --endframe=1000
