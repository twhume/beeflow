#!/bin/sh

WINDOWS=(10 )
SPEEDS=(0.8)
EDGES=(24)
ITERATIONS=10
TIMEOUT=120

TRACKS=("donkey-warehouse-v0" "donkey-generated-roads-v0" "donkey-minimonaco-track-v0")
TRACKS=("donkey-generated-roads-v0")
POWERS=(0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
# Dropped "donkey-avc-sparkfun-v0" 

for w in "${WINDOWS[@]}"
do
	for s in "${SPEEDS[@]}"
	do
		for e in "${EDGES[@]}"
		do
			for p in "${POWERS[@]}"
			do

				for t in "${TRACKS[@]}"
				do
					echo Track $t
					bee_pid_array=()
					for i in `seq 1 $ITERATIONS`
					do
						NOW=$(date "+%Y%m%d-%H%M%S")
						FN=results/donkey-$NOW,w=$w,s=$s,e=$e,i=$i.mp4
						PORT=$((9000 + $i)) 
						timeout -s 9 $TIMEOUT python beeflow-donkey.py $FN --pause=1 --power=$p --port=$PORT --track_name=$t --window_size=$w --edge_size=$e --run_max=1000 --base_speed=$s 2>>/tmp/donkey.log | grep RESULT >> results.log &
						sav_pid=$!
						bee_pid_array+=($sav_pid)
					done
					echo Waiting for round to end: ${bee_pid_array[@]}
					while kill -0 ${bee_pid_array[@]} 2> /dev/null; do sleep 1; done;
				done
			done
		done
	done
done