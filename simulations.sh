#!/bin/sh

WINDOWS=(5 10 15)
SPEEDS=(0.6 0.7 0.8 0.9 1.0)
EDGES=(16 20 24 28)
ITERATIONS=10
TIMEOUT=120

for w in "${WINDOWS[@]}"
do
	for s in "${SPEEDS[@]}"
	do
		for e in "${EDGES[@]}"
		do
			bee_pid_array=()
			for i in `seq 1 $ITERATIONS`
			do
				NOW=$(date "+%Y%m%d-%H%M%S")
				FN=results/donkey-$NOW,w=$w,s=$s,e=$e,i=$i.mp4
				PORT=$((9000 + $i)) 
				timeout $TIMEOUT python beeflow-donkey.py $FN --port=$PORT --window_size=$w --edge_size=$e --run_max=1000 --base_speed=$s 2>>/tmp/donkey.log | grep RESULT >> results.log &
				sav_pid=$!
				bee_pid_array+=($sav_pid)
			done
			echo Waiting for round to end ( ${bee_pid_array[@]} )
			while kill -0 ${bee_pid_array[@]} 2> /dev/null; do sleep 1; done;

		done
	done
done