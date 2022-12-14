from beeflow import process_image, get_average, speeds
from math import copysign
from time import sleep
import argparse 
import cv2 as cv
import os
import gym
import gym_donkeycar
import numpy as np

# SET UP ENVIRONMENT
# You can also launch the simulator separately
# in that case, you don't need to pass a `conf` object


font = cv.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
thickness = 1
color = (255, 255, 255)

speed_choices = dict()
steering_choices = dict()

class Smoother:

	def __init__(self, window_size):
		self.window_size = window_size
		self.history = []

	def smooth(self, input):
		self.history.append(input)
		self.history = self.history[-self.window_size:]
		return sum(self.history)/len(self.history)

def get_controls(diff, base_speed):
	global speed_choices, steering_choices	
	steering = 0.0
	speed = base_speed


	if (diff<0): # Right side is faster

		if (diff < -4):
			steering = 1.0 # Better than 0.7
			speed = speed /2 # Was / 2
		elif (diff < -2): 
			steering = 0.7 
			speed = speed /2
		elif (diff < -1): 
			steering = 0.5
			speed = speed /2
		elif (diff < -0.5): 
			steering = 0.2
			speed = speed /2
		else:
			steering = 0.1

	else: # Left size is faster

		if (diff > 4):
			steering = -1.0
			speed = speed /2
		elif (diff > 2): 
			steering = -0.7
			speed = speed /2
		elif (diff > 1): 
			steering = -0.5
			speed = speed /2
		elif (diff > 0.5): 
			steering = -0.2
			speed = speed /2
		else:
			steering = -0.1

	if (str(speed) in speed_choices):
		speed_choices[str(speed)] = speed_choices[str(speed)] + 1
	else:
		speed_choices[str(speed)] = 1

	if (str(steering) in steering_choices):
		steering_choices[str(steering)] = steering_choices[str(steering)] + 1
	else:
		steering_choices[str(steering)] = 1

	return(steering,speed)

def run_simulation(output_file, debug, base_speed, window_size, edge_size, run_max, track_name, port):

	left_w = []
	right_w = []

	conf = {
        "exe_path": "/Applications/donkey_sim.app/Contents/MacOS/donkey_sim",
        "host": "127.0.0.1",
        "port": port
    }

	env = gym.make(track_name, conf=conf)
	obs = env.reset()
	action = np.array([0.0, base_speed]) # start by driving straight with small speed

	fourcc = cv.VideoWriter_fourcc(*'MP4V')
	out = cv.VideoWriter(output_file, fourcc, 25, (160,120))

	def cleanup():
		out.release()
		env.viewer.exit_scene()
		env.close()

		global speed_choices, steering_choices	
		speed_choices = dict(sorted(speed_choices.items(), key=lambda item: item[1]))
		steering_choices = dict(sorted(steering_choices.items(), key=lambda item: item[1]))
		print("Speeds=", speed_choices)
		print("Steering=", steering_choices)

	speed_smoother = Smoother(3)
	steering_smoother = Smoother(3)

	for t in range(run_max):
		# execute the action
		obs, reward, done, info = env.step(action)

		# If we hit a wall, call it a day

		if (info["speed"]<0.01) and (t>10):
			cleanup()
			return (t, "CRASH")
			break;

		# If we get too far off track, finish

		if (abs(info["cte"])>7.75):
			cleanup()
			return (t, "OFFTRACK")
			break;

		rgb = cv.cvtColor(obs,cv.COLOR_BGR2RGB)
		rgb = cv.putText(rgb, f"{t}" , (10,20), font, fontScale, color, thickness, cv.LINE_AA)

		out.write(rgb)
		filtered = process_image(obs)

		# restrict to a central 80x80 square
		filtered = filtered[20:120,30:130]
		(left, right, _top, _bottom) = get_average(filtered, edge_size=edge_size)

	  # Record the readings, while maintaing the window size

		left_w.append(left)
		left_w = left_w[-window_size:]
		right_w.append(right)
		right_w = right_w[-window_size:]

	  # Calculate speeds from the two windows

		if (len(left_w)==window_size):
			left_s = speeds(left_w)
			right_s = speeds(right_w)

			r_av = np.average(right_s)
			l_av = np.average(left_s)

			diff = l_av-r_av

			(steering, speed) = get_controls(diff, base_speed)
#			steering = steering_smoother.smooth(steering)
#			speed = speed_smoother.smooth(speed)

			if (debug):
				print(f"{t}: l={l_av:0.3}, r={r_av:0.3}, diff={diff:0.3}, steering={steering:0.3}, speed={speed:0.3}")

			action = np.array([steering, speed])

		else:
			action = np.array([0.0, base_speed]) # drive straight with small speed

	# Exit the scene
	cleanup()

	return (t,"COMPLETE")


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("output_file", type=str)
	parser.add_argument("--base_speed", type=float, default=0.4)
	parser.add_argument("--window_size", type=int, default=10)
	parser.add_argument("--edge_size", type=int, default=20)
	parser.add_argument("--run_max", type=int, default=1000)
	parser.add_argument("--port", type=int, default=9091)
	parser.add_argument("--pause", type=int, default=0)
	parser.add_argument("--debug", type=bool, default=False)
	parser.add_argument("--track_name", type=str, default="donkey-generated-roads-v0")

	args = parser.parse_args()
	sleep(args.pause)
	(run_length, result) = run_simulation(args.output_file, args.debug, args.base_speed, args.window_size, args.edge_size,
		args.run_max, args.track_name, args.port)
	results = [args.output_file, args.track_name, run_length, args.base_speed, args.window_size, args.edge_size, result]
	results = [str(x) for x in results] 
	print("RESULT,",",".join(results))


if __name__ == "__main__":
	main()
