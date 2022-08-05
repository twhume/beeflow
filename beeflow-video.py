# Processes and reports on a video input

import csv
import cv2 as cv
import numpy as np
import time

font = cv.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 2
color = (255, 0, 0)

cap = cv.VideoCapture("mumbai-320p.mp4")

# Determine FPS

ret, first_frame = cap.read()
fps = cap.get(cv.CAP_PROP_FPS)
ms_per_frame = 1000/fps
print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

fourcc = cv.VideoWriter_fourcc(*'MP4V')
out = cv.VideoWriter('mumbai-320p-processed.mp4', fourcc, fps, (640,360))


cur_time = last_time = time.time()

num = 0
with open('beeflow.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile,  quotechar='|', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(["Frame","Left", "Right", "Top", "Bottom"])

	while(cap.isOpened()):
		# ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
		ret, frame = cap.read()

		# Convert to black and white

		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		(thresh, im_bw) = cv.threshold(gray, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

		# Add a low pass filter

		#prepare the 5x5 shaped filter
		kernel = np.array([[1, 1, 1, 1, 1], 
			[1, 1, 1, 1, 1], 
			[1, 1, 1, 1, 1], 
			[1, 1, 1, 1, 1], 
			[1, 1, 1, 1, 1]])
		kernel = kernel/sum(kernel)

		#filter the source image
		filtered = cv.filter2D(gray,-1,kernel)
		backtorgb = cv.cvtColor(filtered,cv.COLOR_GRAY2RGB)

		left = np.average(filtered[:,0:5])
		right = np.average(filtered[:,635:640])
		top = np.average(filtered[0:5,:])
		bottom = np.average(filtered[355:360,:])

		output = backtorgb
		output = cv.putText(output, f"Left={left:.2f}" , (30,180), font, fontScale, color, thickness, cv.LINE_AA)
		output = cv.putText(output, f"Right={right:.2f}", (420,180), font, fontScale, color, thickness, cv.LINE_AA)
		output = cv.putText(output, f"Top={top:.2f}", (200,30), font, fontScale, color, thickness, cv.LINE_AA)
		output = cv.putText(output, f"Bottom={bottom:.2f}", (200,330), font, fontScale, color, thickness, cv.LINE_AA)
		output = cv.putText(output, f"f={num}", (280,180), font, fontScale, color, thickness, cv.LINE_AA)

		cv.imshow("sparse optical flow", output)
		out.write(output)
		# Frames are read by intervals of 10 milliseconds. The programs breaks out of the while loop when the user presses the 'q' key
		if cv.waitKey(10) & 0xFF == ord('q'):
			break

		# Sleep to preserve input FPS in output
#		cur_time = time.time()
#		frame_time = (cur_time - last_time)
#		time.sleep((ms_per_frame - frame_time)/1000)
#		last_time = cur_time

		num += 1
		writer.writerow([num, left, right, top, bottom])
	# The following frees up resources and closes all windows
	cap.release()
	out.release()
	cv.destroyAllWindows()

