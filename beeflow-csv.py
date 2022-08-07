# 

import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

right = []
left = []
top = bottom = []
max = 0
with open('sonoma.csv', 'r', newline='') as csvfile:
	reader = csv.reader(csvfile)
	next(reader, None)  # skip the headers
	for row in reader:
		max = row[0]
		left.append(float(row[1]))
		right.append(float(row[2]))
		top.append(float(row[3]))
		bottom.append(float(row[4]))

def calc_speeds(l, pad_to):

	l = np.array(l)
	neg_l = 255 - l

	l_peaks, _ = find_peaks(l, prominence=(10, ))
	l_troughs, _ = find_peaks(neg_l, prominence=(10, )) 

	points = np.concatenate((l_peaks, l_troughs))
	points.sort()

	speeds = [0] * points[0]

	for point_num in range(len(points)-1):
		start_frame = points[point_num]
		end_frame = points[point_num+1]

		start_val = l[start_frame]
		end_val = l[end_frame]

		speed = abs((end_val - start_val) / (end_frame - start_frame))
		print("From frame", start_frame, "to frame", end_frame, "speed=", speed)
		speeds.extend([speed] * (end_frame-start_frame))

	if (len(speeds)<pad_to):
		speeds.extend([speeds[-1]] * (pad_to - len(speeds)))

	return np.array(speeds)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def average_speed(l, frames=30):
	out = []
	for i in range(len(l)):
		num_back = min(frames, i+1)
		out.append(sum(l[i-num_back:i]) / num_back)
	return out

def to_seconds(l, fps=30):
	ret = []
	for c in chunker(l, fps):
		ret.append(sum(c)/fps)
	return np.array(ret)

#left = left[:3000]
#right = right[:3000]
print("l=",len(left))
print("r=",len(right))

l_speeds = calc_speeds(left, 0)
r_speeds = calc_speeds(right, len(l_speeds))

print("l_speeds=",len(l_speeds))
print("r_speeds=",len(r_speeds))


l_av = to_seconds(average_speed(l_speeds, frames=30))
r_av = to_seconds(average_speed(r_speeds, frames=30))

print("l_av=",len(l_av))
print("r_av=",len(r_av))

max_av = np.max([np.amax(l_av), np.amax(r_av)])
min_av = np.min([np.amin(l_av), np.amin(r_av)])



print(len(l_av))
print(len(r_av))
plt.title("L/R position by second")
#plt.xlim(left=1)
#plt.plot(l_av)
#plt.plot(r_av)
plt.plot((r_av-l_av)/(max_av-min_av))
plt.ylim((-1,1))
plt.show()

#plt.plot(left)
#plt.title("Intensity of left and right frame edges")
#plt.plot(left, label="Left")
#plt.plot(right, label="right")
#plt.xlabel("Frame")
#plt.ylabel("Intensity")
#plt.legend()
#plt.show()




#plt.plot(l_peaks, left[l_peaks], "x")
#plt.plot(r_peaks, right[r_peaks], "o")
#plt.plot(l_troughs, left[l_troughs], "o")
#plt.plot(r_peaks, right[r_peaks], "o")
#plt.plot(r_peaks)
#plt.show()


