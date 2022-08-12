# Takes the CSV file from beeflow-video.py and identifies difference in edge
# speed between LHS and RHS, graphing them

import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np
from beeflow import peaks, speeds

def average_speed(l, frames=30):
	out = []
	for i in range(len(l)):
		num_back = min(frames, i+1)
		start=max(0, i-num_back)
		out.append(sum(l[start:i+1])/num_back)
	return out

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def to_seconds(l, fps=30):
	ret = []
	c = chunker(l, fps)
	for c in chunker(l, fps):
		ret.append(sum(c)/len(c))
	return np.array(ret)

def process_csv(input_csv, position_file, speed_file, fps, window_size, frame_start, frame_end):

	# Read in the CSV file made by beeflow-video.py

	right = []
	left = []
	with open(input_csv, 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		next(reader, None)  # skip the headers
		for row in reader:
			left.append(float(row[1]))
			right.append(float(row[2]))

	# cut out 

	if (frame_end is not None):
		left = left[:frame_end]
		right = right[:frame_end]

	if (frame_start is not None):
		left = left[frame_start:]
		right = right[frame_start:]

	l_speeds = speeds(left,pad_to=len(left))
	r_speeds = speeds(right, pad_to=len(l_speeds))
	if len(r_speeds) > len(l_speeds):
		pad_from = len(l_speeds)
		l_speeds.resize(len(r_speeds))
		l_speeds[pad_from:] = l_speeds[pad_from]

	l_av = average_speed(l_speeds, frames=window_size)
	l_av_s = to_seconds(l_av, fps=fps)
	r_av = average_speed(r_speeds, frames=window_size)
	r_av_s = to_seconds(r_av, fps=fps)

	max_av = np.max([np.amax(l_av_s), np.amax(r_av_s)])
	min_av = np.min([np.amin(l_av_s), np.amin(r_av_s)])

	plt.title("L/R position by second")
	plt.plot((r_av_s-l_av_s)/(max_av-min_av))
	plt.ylim((-1,1))
	plt.xlim((0,(len(left)/fps)))
	plt.xlabel("Time (s)")
	plt.ylabel("Position (L=-1, R=1)")

	if (position_file is not None):
		plt.savefig(position_file)
	else:
		plt.show()

#	plt.clf()
#	plt.title("Left speed - Right speed/frame")
#	plt.plot(l_av, label="Left")
#	plt.plot(r_av, label="right")
#	plt.plot(np.array(l_av)-np.array(r_av), label="L-R")
#	plt.legend(loc="upper left")
#	plt.xlabel("Time (frame)")
#	plt.ylabel("Speed")
#	plt.show()

	plt.clf()
	plt.title("Right av speed - Left av speed/second")
	plt.plot(l_av_s, label="Left")
	plt.plot(r_av_s, label="Right")
	plt.plot(r_av_s-l_av_s, label="R-L")
	plt.legend(loc="upper left")

	plt.xlim((0,(len(left)/fps)))
	plt.xlabel("Time (s)")
	plt.ylabel("Speeds")
	if (speed_file is not None):
		plt.savefig(speed_file)
	else:
		plt.show()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input_csv", type=str)
	parser.add_argument("--position_file", type=str)
	parser.add_argument("--speed_file", type=str)
	parser.add_argument("--fps", type=int, default=30)
	parser.add_argument("--window_size", type=int, default=90)
	parser.add_argument("--frame_start", type=int, default=0)
	parser.add_argument("--frame_end", type=int, default=None)

	args = parser.parse_args()

	process_csv(args.input_csv, args.position_file, args.speed_file, args.fps, args.window_size, args.frame_start, args.frame_end)


if __name__ == "__main__":
    main()

