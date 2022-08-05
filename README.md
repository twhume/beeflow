# Beeflow

Implementation of the non-directional speed detector described in "How Bees Exploit Optic Flow: Behavioural Experiments and Neural Models [and Discussion]" (MSrinivasan and Gregory, 1992)

# Process

1. Convert to a binary image (high sensitivity to contrast, saturate at low contrast)
2. Spatially low-pass filter, to give an image in which abrupt edges have been converted into ramps of constant slope
3. Measure speed of image by measuring rate of change of response at the ramps. One image generates a train of pulses, one at each edge. Amplitude of each pulse is proportional to the rate of change of intensity at the corresponding ramp, and thus to the speed of the image at that location.
4. Use rectification to ensure the response is positive regardless of direction of movement.


