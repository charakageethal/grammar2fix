#!/bin/bash
if [ $# -ne 1 ]; then
  echo "$0 <codeflaws directory>" 1>&2
  exit
fi
if ! [ -d "$1" ]; then
  echo "Not a directory: $1" 1>&2
  exit
fi


if [ -z "$(which cilly)" ]; then
  echo "cilly compiler not found!" 1>&2
  exit
fi


gr_modules="/root/grammar2fix"

if ! [ -e "$gr_modules" ]; then
  echo $gr_modules does not exist.
  exit
fi


codeflaws_dir=$1
repair_dir=$codeflaws_dir/../
rm $codeflaws_dir/*/autogen* &> /dev/null
rm $codeflaws_dir/*/dfa_grammar* &> /dev/null


if [ -e $repair_dir/genprog-run ]; then
  echo "[INFO] Saving $repair_dir/genprog-run.." 1>&2
  rm -rf $repair_dir/genprog-run.old 2> /dev/null
  mv $repair_dir/genprog-run $repair_dir/genprog-run.old
fi


cp $gr_modules/repairs/genprog/* $repair_dir/
mkdir $repair_dir/genprog-run

#TODO Where is genprog_allfixes created?
if [ -e $repair_dir/genprog-allfixes ]; then
  echo "[INFO] Saving $repair_dir/genprog-allfixes.." 1>&2
  rm -rf $repair_dir/genprog-allfixes.old 2> /dev/null
  mv $repair_dir/genprog-allfixes $repair_dir/genprog-allfixes.old
fi
mkdir $repair_dir/genprog-allfixes



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

	
		cp $gr_modules/repairs/genprog/test_genprog_grammar.py $s/

	  for i in $(seq 1 $(nproc --all)); do
	   (
	          autotest=$(timeout 10m python Codeflaws_GE_repair.py -s $subject -p $codeflaws_dir -i $i)


	          if [ $? -eq 0 ]; then
	           		manual=$($repair_dir/run-version-genprog.sh $subject $i manual 10m)
	    					autogen=$($repair_dir/run-version-genprog.sh $subject $i autogen 10m)
	
	              echo $autotest | tr -d '\n'
	    					echo ,$manual | tr -d '\n'
	    					echo ,$autogen
	           fi

	   ) >> results/codeflaws_repair/results_cit_$i.csv & 
	   done
	    wait
	  
		rm -rf $repair_dir/genprog-run/tempworkdir-*
	    

		else
			echo "Skipping numeric inputs:$s" 1>&2	
		fi 

	else
		echo "Skipping multiline output:$s" 1>&2
	fi

done

cat results/codeflaws_repair/results_cit_*.csv > results/codeflaws_repair/results_codeflaws.csv
