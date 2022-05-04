#!/bin/bash

if [ $# -ne 1 ]; then
	echo "$0 Codeflaws directory" 1>&2
	exit
fi


if ! [ -d $1 ]; then
	echo "Not a directory: $1" 1>&2
	exit
fi

codeflaws_dir=$1
gen_steps=("GI" "BG" "HSC" "CCF" "GE")

for gen in "${gen_steps[@]}"; do

	for s in $(ls -1d $codeflaws_dir/*/); do

		found=false

		subject=$(echo $s | rev | cut -d/ -f2 | rev)

		if [ 0 -eq $(grep "$subject" $codeflaws_dir/codeflaws-defect-detail-info.txt | grep "WRONG_ANSWER" | wc -l ) ]; then
			echo "Skipping non-semantic and numeric inputs:$s" 1>&2
			continue
		fi

		for f in $(ls -1 $s/*input*); do if [ $(wc -l $f | cut -d" " -f1) -gt 1 ]; then found=true; continue; fi; done;

		if [ "$found" = false ]; then


			isAlpha=false
	  		#for f in $(ls -1 $s/*input*); do if [ $(cat $f | grep -x -E "[[:blank:]]*([[:digit:]]+[[:blank:]]*)*" | wc -l ) -gt 0 ]; then isAlpha=true; continue; fi; done;
	  		for f in $(ls -1 $s/*input*); do if [ $(cat $f | grep -x -E "^[a-zA-Z]*$" | wc -l ) -gt 0 ]; then isAlpha=true; continue; fi; done;

			if [ "$isAlpha" = true ]; then

				buggy=$(echo $subject | cut -d- -f1,2,4)
				golden=$(echo $subject | cut -d- -f1,2,5)

				if ! [ -f "$s/$buggy" ]; then
					gcc -fno-optimize-sibling-calls -fno-strict-aliasing -fno-asm -std=c99 -c $s/$buggy.c -o $s/$buggy.o &> /dev/null
		        	gcc $s/$buggy.o -o $s/$buggy -lm -s -O2 &> /dev/null
				fi

				if ! [ -f "$s/$golden" ]; then
					gcc -fno-optimize-sibling-calls -fno-strict-aliasing -fno-asm -std=c99 -c $s/$golden.c -o $s/$golden.o &> /dev/null
		        	gcc $s/$golden.o -o $s/$golden -lm -s -O2 &> /dev/null
				fi

				
				echo "[INFO] Running subject:$subject in $gen"

		         for i in $(seq 1  $(nproc --all)); do
		         (
		                autotest=$(timeout 15m python Codeflaws_$gen.py -s $subject -p $codeflaws_dir -i $i)
		    
		                 if [ $? -eq 0 ]; then
		                        echo $autotest 
	            			
		                 fi
		    
		         ) >> results/$gen/results_c_${gen}_$i.csv &
		         done
		          wait
		       
		        echo "[INFO] $subject in $gen completed...."

			else
				echo "Skipping numeric inputs:$s" 1>&2	
			fi 


		else

			echo "Skipping multiline output:$s" 1>&2

		fi

	done
	cat results/$gen/results_c_${gen}_*.csv > results/$gen/results_codeflaws.csv
done
