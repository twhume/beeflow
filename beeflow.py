import cv2 as cv
import numpy as np
from scipy.signal import find_peaks

'''
Convert input image to grayscale, threshold it to make it B/W and gaussian blur it
'''

def process_image(frame):
	# Convert to black and white

	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	(thresh, im_bw) = cv.threshold(gray, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

	# Add a low pass filter to blur the image

	kernel = np.array([[1, 1, 1, 1, 1], 
		[1, 1, 1, 1, 1], 
		[1, 1, 1, 1, 1], 
		[1, 1, 1, 1, 1], 
		[1, 1, 1, 1, 1]])
	kernel = kernel/sum(kernel)
	filtered = cv.filter2D(im_bw,-1,kernel)
	return filtered

'''
Given a width of edge to look at, return the average values at each edge
'''

def get_average(frame, edge_size):
	width=frame.shape[1]
	height=frame.shape[0]

	# pull out average values at each edge

	left = np.average(frame[:,0:edge_size])
	right = np.average(frame[:,(width-edge_size):width])
	top = np.average(frame[0:edge_size,:])
	bottom = np.average(frame[(height-edge_size):height,:])
	return (left, right, top, bottom)

'''
Given an input series of values, return a sequence of the peaks in these values
e.g. input of 0,1,2,1,0,3,0 would return 2,5
'''

def peaks(l, prominence=0):
	peaks = []
	last_up = None

	if (len(l)==0):
		return []

	if (l[0] > (l[1] + prominence)):
		peaks.append(0)

	for i in range(1,len(l)):
		if (l[i] > (l[i-1] + prominence)):
			last_up = i
		elif (l[i] < l[i-1]) and (last_up is not None):
			peaks.append(last_up)
			last_up = None

	if (last_up is not None):
		peaks.append(last_up)
	return peaks

'''
Given an input array which is a sequence of frames, each containing a pulse value,
return the speed at each frame, being defined as the average change in value between
peaks and troughs in the signal
'''

def speeds(l, pad_to=0):

	l = np.array(l)
	l_peaks = peaks(l)
	l_troughs = peaks(255 - l)

	points = np.concatenate((l_peaks, l_troughs))
	points.sort()
	ret = []

	if (len(points)>0):
		ret = [0] * int(points[0])

	for point_num in range(len(points)-1):
		start_frame = points[point_num]
		end_frame = points[point_num+1]

		speed = abs((l[end_frame] - l[start_frame]) / (end_frame - start_frame))
		ret.extend([speed] * (end_frame-start_frame))

	if (len(ret)<pad_to):
		if (len(ret)>0):
			padch = ret[-1]
		else:
			padch = 0
		ret.extend([padch] * (pad_to - len(ret)))

	return np.array(ret)