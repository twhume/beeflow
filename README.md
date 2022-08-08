# Beeflow

Implementation of the non-directional speed detector described in ["How Bees Exploit Optic Flow: Behavioural Experiments and Neural Models [and Discussion]"](https://www.jstor.org/stable/57057) (Srinivasan and Gregory, 1992)

# TODO

- make a single script which analyzes a movie and pastes results into it (bonus points: gradually displaying graph). paste this into the movie

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

Turn a video into a CSV logging the average edge-values at each frame to a CSV file

python beeflow-video.py input.mp4 output.csv --edge_size=1 --max_frames=10000 --preview|no-preview --preserve_fps|no-preserve_fps --output_video=debug.mp4

Parameters:
(required) input.mp4 : input video to read from. Size, FPS should be inferred automatically.
(required output.csv : output CSV file to write. Existing files will be overwritten
edge_size : how many pixels in from the edge should be averaged together to infer "what's at the egde"?
max_frames : maximum number of video frames to read
preview/no-preview : controls whether a visible preview is shown
preserve_fps/no-preserve_fps : should the FPS of the input be preserved when showing the preview?
output_video : if set, preview is written to this file


Take one of these CSV files and plot the average speed of pulses at left and right edges:

python beeflow-csv.py input.csv --frame_start=1 --frame_end=1000 --fps=30 --prominence=10 --window_size=90

(required) input.csv : CSV file created by beeflow-video.csv
frame_start : what frame should processing start at?
frame_end : what frame should processing end at?
fps : fps of the original video (used to create a grap with an x axis in seconds)
prominence : how "prominent" should peaks be when looking for them?
window_size : over what window size (in frames) should we average inferred speed when creating a graph
output_file : if present, write the output graph to a file, otherwise preview

