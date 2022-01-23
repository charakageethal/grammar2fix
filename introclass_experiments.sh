#!/bin/bash

if [ $# -ne 1 ]; then
	echo "$0 IntroClass directory" 1>&2
	exit
fi


if ! [ -d $1 ]; then
	echo "Not a directory: $1" 1>&2
	exit
fi

gen_steps=("GI" "BG" "HSC" "CCF" "GE")
buggy_subs=("syllables"  "checksum")

for gen in "${gen_steps[@]}"; do
	for sub in "${buggy_subs[@]}"; do
		bug_dir="$1${sub}/"

		source_prog="\"$(echo $bug_dir | rev | cut -d/ -f2 | rev)\""

		for s in $(ls -1d $bug_dir/*/); do

		    if [[ "$s" == *"tests/" ]]; then
			golden_dir=$(echo $s | rev | cut -d/ --complement -f3 | rev)
			gcc -Wall -fno-stack-protector $golden_dir$sub.c -o $golden_dir$sub
		    fi

		done

		for s in $(ls -1d $bug_dir/*/); do
		    for v in $(ls -1d $s/*/); do

				if [[ "$v" == *"blackbox/" ]]  || [[ "$v" == *"whitebox/" ]]; then
				    continue
				fi


				v=$(echo $v | rev | cut -d/ --complement -f3,5 | rev)
				gcc -Wall -fno-stack-protector $v$sub.c -o $v$sub

				for i in $(seq 1 32); do
				(

				    autotest=$(timeout 15m python Introclass_$gen.py -s $v -g $golden_dir -i $i)

				    if [ $? -eq 0 ]; then
				        echo $autotest
				    fi
				) >> results/$gen/results_i_${gen}_$i.csv &

		       done
		      wait
		    done

		done
	done
	cat results/$gen/results_i_${gen}_*.csv > results/$gen/results_introclass.csv
done