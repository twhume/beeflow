# Beeflow

<img src="assets/beedonkey.png" width="200" align="right" alt="Snarling half-bee, half-donkey" hspace="20" vspace="20"/>

Implementation of the non-directional speed detector described in ["How Bees Exploit Optic Flow: Behavioural Experiments and Neural Models [and Discussion]"](https://www.jstor.org/stable/57057) (Srinivasan and Gregory, 1992)

Goal is to use this mechanism to drive a [Donkey Car](https://docs.donkeycar.com).

tl;dr beeflow-video.py takes a video and analyzes it, creating a CSV output. beeflow-csv.py turns this output into a graph showing whether the camera position is towards left or right of the environment, based on relative speed of movement at the left and right edges. beeflow-donkey.py uses this approach to drive a donkey car.

# Algorithm

1. Convert to a binary image (high sensitivity to contrast, saturate at low contrast)
2. Spatially low-pass filter, to give an image in which abrupt edges have been converted into ramps of constant slope
3. Measure speed of image by measuring rate of change of response at the ramps. One image generates a train of pulses, one at each edge. Amplitude of each pulse is proportional to the rate of change of intensity at the corresponding ramp, and thus to the speed of the image at that location.
4. Use rectification to ensure the response is positive regardless of direction of movement.

# Videos

[sonoma.mp4](https://drive.google.com/file/d/1pS__zMrgDUPZOpNc8RTeaN6jJbX48iaD/view?usp=sharing) : some footage I shot walking along a tunnel of trees in Sonoma, good for demo'ing

# Usage

Turn a video into a CSV logging the average edge-values at each frame to a CSV file

```
python beeflow-video.py input.mp4 output.csv --edge_size=1 --max_frames=10000 --preview|no-preview --preserve_fps|no-preserve_fps --output_video=debug.mp4
```

Parameters:
- (required) input.mp4 : input video to read from. Size, FPS should be inferred automatically.
- (required output.csv : output CSV file to write. Existing files will be overwritten
- edge_size : how many pixels in from the edge should be averaged together to infer "what's at the egde"?
- max_frames : maximum number of video frames to read
- preview/no-preview : controls whether a visible preview is shown
- preserve_fps/no-preserve_fps : should the FPS of the input be preserved when showing the preview?
- output_video : if set, preview is written to this file


Take one of these CSV files and plot the average speed of pulses at left and right edges:

```
python beeflow-csv.py input.csv --frame_start=1 --frame_end=1000 --fps=30 --prominence=10 --window_size=90
```

Parameters:
- (required) input.csv : CSV file created by beeflow-video.csv
- frame_start : what frame should processing start at?
- frame_end : what frame should processing end at?
- fps : fps of the original video (used to create a grap with an x axis in seconds)
- prominence : how "prominent" should peaks be when looking for them?
- window_size : over what window size (in frames) should we average inferred speed when creating a graph
- output_file : if present, write the output graph to a file, otherwise preview


Use the same method to drive a simulated donkey car:

```
python beeflow-donkey.py output.mp4 --base_speed=0.8 --window_size=28 --edge_size=24 --run_max=1000 --port=9091 --pause=1 --debug=True --track_name=donkey-generated-roads-v0
```

- (required) output_file : where to put a video of the cars-eye view of the drive
- base_speed: basic speed to run the car (may be altered by steering algorithm)
- window_size: window of previous speed readings over which to average speed calculation
- edge_size: how many pixels in from the left and right to look for speed changes
- run_max: how many steps to run for
- port: which port to connect to the donkey simulator using
- pause: how many seconds to pause after startup
- debug : whether to output extra debugging
- track_name : which track name to launch in the simulator

