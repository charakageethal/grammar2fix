#!/bin/bash

if [ $# -ne 1 ]; then
	echo "$0 Quixbugs directory" 1>&2
	exit
fi


if ! [ -d $1 ]; then
	echo "Not a directory: $1" 1>&2
	exit
fi

gen_steps=("GI" "BG" "HSC" "CCF" "GE")
buggy_subs=("lcs_length" "longest_common_subsequence" "levenshtein" "is_valid_parenthesization")

for gen in "${gen_steps[@]}"; do
	for sub in "${buggy_subs[@]}"; do

		echo "[INFO] Running subject:$sub in $gen"

		for i in $(seq 1  $(nproc --all)); do
		(
			autotest=$(timeout 15m python QuixBugs_$gen.py -s $sub -p $1 -i $i)

			if [ $? -eq 0 ]; then
				echo $autotest
			fi


		)>> results/$gen/results_q_${gen}_$i.csv &		 
		done
		wait

		echo "[INFO] $sub in $gen completed...."
	done
	cat results/$gen/results_q_${gen}_*.csv > results/$gen/results_quixbugs.csv
done
