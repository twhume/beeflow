from beeflow import process_image, get_average, speeds
import cv2 as cv
import os
import gym
import gym_donkeycar
import numpy as np

# SET UP ENVIRONMENT
# You can also launch the simulator separately
# in that case, you don't need to pass a `conf` object


WINDOW_SIZE = 50
SPEED = 0.1
left_w = []
right_w = []

env = gym.make("donkey-generated-track-v0")

# PLAY

min_v = 0
max_v = 0

obs = env.reset()
action = np.array([0.0, SPEED]) # drive straight with small speed

fourcc = cv.VideoWriter_fourcc(*'MP4V')
out = cv.VideoWriter("donkey.mp4", fourcc, 25, (160,120))


for t in range(1000):
	# execute the action
	obs, reward, done, info = env.step(action)
	rgb = cv.cvtColor(obs,cv.COLOR_BGR2RGB)
	out.write(rgb)
	filtered = process_image(obs)
	(left, right, _top, _bottom) = get_average(filtered, edge_size=20)

  # Record the readings, while maintaing the window size

	left_w.append(left)
	left_w = left_w[-WINDOW_SIZE:]
	right_w.append(right)
	right_w = right_w[-WINDOW_SIZE:]

  # Calculate speeds from the two windows

	if (len(left_w)==WINDOW_SIZE):
		left_s = speeds(left_w)
		right_s = speeds(right_w)

		r_av = np.average(right_s)
		l_av = np.average(left_s)
		diff = l_av-r_av

		steering = 0.0
		speed = SPEED

		if (diff<0): # Right side is faster

			if (diff < -4):
				steering = 1.0
				speed = speed / 2
			elif (diff < -2): 
				steering = 0.7
				speed = speed / 2
			elif (diff < -1): 
				steering = 0.5
			elif (diff < -0.5): 
				steering = 0.3
			else:
				steering = 0.1

		else: # Left size is faster

			if (diff > 4):
				steering = -1.0
				speed = speed / 2
			elif (diff > 2): 
				steering = -0.7
				speed = speed / 2
			elif (diff > 1): 
				steering = -0.5
			elif (diff > 0.5): 
				steering = -0.3
			else:
				steering = -0.1



		print(f"{t}: l={l_av:0.3}, r={r_av:0.3}, diff={diff:0.3}, steering={steering:0.3}, speed={speed:0.3}")

		action = np.array([steering, speed])

	else:
		action = np.array([0.0, SPEED]) # drive straight with small speed


# Exit the scene
out.release()
env.close()