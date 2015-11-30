#!/bin/bash

dirpath=$1'/*'
stat_path=$2'/*'

i=0
for file in $stat_path; do
	stat_file[$i]=$file
	(( i += 1 ))
done 

i=0
for dir in $dirpath; do
		echo $dir
#		mkdir $dir'/prob'
		output_path=$dir'/prob'
		IFS=',' 
		j=0
		while read num alpha; do
			echo $num
			file=$dir"/ldac_output_$j/final.beta"
			python '/home/pzwang/workspace/topic-model/src/ldaPy/read_prob.py' -f $file -o "$output_path/prob_$j.pkl"
#			python '/home/pzwang/workspace/topic-model/src/graph/convert_prob.py' -f "$output_path/prob_$j.pkl" -n 15591 -o "$output_path/convert_prob_$j.pkl"
			(( j += 1 ))
		done <  ${stat_file[$i]}
	(( i += 1 ))
done

