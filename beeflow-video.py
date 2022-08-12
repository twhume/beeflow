# Processes and reports on a video input

import argparse
from beeflow import process_image, get_average
from tqdm import tqdm
import csv
import cv2 as cv
import numpy as np
import time

font = cv.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 2
color = (255, 0, 0)

def process_video(in_fn, out_csv_fn, output_video, edge_size, horizon, max_frames, preview, preserve_fps):
	cap = cv.VideoCapture(in_fn)

	# Determine FPS

	ret, first_frame = cap.read()
	fps = cap.get(cv.CAP_PROP_FPS)
	ms_per_frame = 1000/fps

	length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
	if (max_frames is not None) and (max_frames > length):
		print(f"Not enough frames: max_frames={max_frames}, length={length}")

	if (output_video is not None):
		fourcc = cv.VideoWriter_fourcc(*'MP4V')
		out = cv.VideoWriter(output_video, fourcc, fps, (640,360))

	v_width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
	v_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

	print(f"Input video resolution={v_width}x{v_height}, {length} frames at {fps:.2f} fps")

	cur_time = last_time = time.time()

	num = 0
	with open(out_csv_fn, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile,  quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Frame","Left", "Right", "Top", "Bottom"])

		pbar = tqdm(total=length)
		while(cap.isOpened()):
			# ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
			ret, frame = cap.read()

			if (not ret):
				break;

			if (max_frames is not None) and (num >= max_frames):
				break;

			filtered = process_image(frame)
			filtered = filtered[horizon:,:]
			(left, right, top, bottom) = get_average(filtered, edge_size)


			backtorgb = cv.cvtColor(filtered,cv.COLOR_GRAY2RGB)
			output = backtorgb

			if (preview or (output_video is not None)):
				output = cv.putText(output, f"Left={left:.2f}" , (30,180), font, fontScale, color, thickness, cv.LINE_AA)
				output = cv.putText(output, f"Right={right:.2f}", (420,180), font, fontScale, color, thickness, cv.LINE_AA)
				output = cv.putText(output, f"Top={top:.2f}", (200,30), font, fontScale, color, thickness, cv.LINE_AA)
				output = cv.putText(output, f"Bottom={bottom:.2f}", (200,330), font, fontScale, color, thickness, cv.LINE_AA)
				output = cv.putText(output, f"f={num}", (280,180), font, fontScale, color, thickness, cv.LINE_AA)

			if (preview):
				cv.imshow("beeflow preview", output)
				# Frames are read by intervals of 10 milliseconds. The programs breaks out of the while loop when the user presses the 'q' key
				if cv.waitKey(10) & 0xFF == ord('q'):
					break

			if (output_video is not None):
				out.write(output)

			# Sleep to preserve input FPS in output
			if (preserve_fps):
				cur_time = time.time()
				frame_time = (cur_time - last_time)
				time.sleep((ms_per_frame - frame_time)/1000)
				last_time = cur_time

			num += 1
			writer.writerow([num, left, right, top, bottom])
			pbar.update(1)

		# The following frees up resources and closes all windows
		cap.release()
		if (output_video is not None):
			out.release()
		cv.destroyAllWindows()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input", type=str)
	parser.add_argument("output_csv", type=str)
	parser.add_argument("--output_video", type=str, default=None)
	parser.add_argument("--edge_size", type=int, default=5)
	parser.add_argument("--horizon", type=int, default=0)
	parser.add_argument("--max_frames", type=int, default=None)
	parser.add_argument("--preview", action=argparse.BooleanOptionalAction)
	parser.add_argument("--preserve_fps", action=argparse.BooleanOptionalAction)
	args = parser.parse_args()
	process_video(args.input, args.output_csv, args.output_video, args.edge_size,
		args.horizon, args.max_frames, args.preview, args.preserve_fps)


if __name__ == "__main__":
    main()
