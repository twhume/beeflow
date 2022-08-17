#!/bin/sh

WINDOWS=(30)
SPEEDS=(0.4 0.6 0.8 0.3)
EDGES=(2 8 16 24 32 64 128)
ITERATIONS=10
TIMEOUT=300

for w in "${WINDOWS[@]}"
do
	for s in "${SPEEDS[@]}"
	do
		for e in "${EDGES[@]}"
		do
			for i in `seq 1 $ITERATIONS`
			do
				NOW=$(date "+%Y%m%d-%H%M%S")
				fn=results/donkey-$NOW,w=$w,s=$s,e=$e,i=$i.mp4

				echo python beeflow-donkey.py $fn --window_size=$w --edge_size=$e --run_max=1000 --base_speed=$s  
				killall -9 donkey_sim
				sleep 2
				open -g /Applications/donkey_sim.app
				sleep 5
				timeout $TIMEOUT python beeflow-donkey.py $fn --window_size=$w --edge_size=$e --run_max=1000 --base_speed=$s 2>>/tmp/donkey.log | grep RESULT >> results.log

			done
		done
	done
done

exit

# | grep RESULT >> results.log

