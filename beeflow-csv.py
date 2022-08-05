# 

import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

right = []
left = []
top = bottom = []
max = 0
with open('beeflow.csv', 'r', newline='') as csvfile:
	reader = csv.reader(csvfile)
	next(reader, None)  # skip the headers
	for row in reader:
		max = row[0]
		left.append(float(row[1]))
		right.append(float(row[2]))
		top.append(float(row[3]))
		bottom.append(float(row[4]))

def calc_speeds(l):

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
	return speeds

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def average_speed(l):
	out = []
	for c in chunker(l, 30):
		out.append(sum(c)/30)
	return out

l_speeds = calc_speeds(left[1700:2200])
l_av = average_speed(l_speeds)
r_speeds = calc_speeds(right[1700:2200])
r_av = average_speed(r_speeds)

print(len(l_av))
print(len(r_av))
plt.title("Speeds")
plt.plot(l_av)
plt.plot(r_av)
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


