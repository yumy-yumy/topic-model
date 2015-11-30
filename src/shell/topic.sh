#!/bin/bash
# extract all topics for all years and all levels

dirpath=$1'/*'
all_term=$2

i=0
for dir in $dirpath; do
#	if [ $i -gt 15 ]; then
		echo $dir
		mkdir $dir'/topic'
		output_path="$dir/topic"
		file_path="$dir/prob/*"
		j=0
		for file in $file_path; do
#			ext=${file##*.}
#			file_name=$(basename $file .$ext)
#			fun=${file_name%_*}
#			if [ "$fun" = "prob" ]; then
				echo $file
				python '/home/pzwang/workspace/topic-model/src/graph/top_term.py' -f $file -t $all_term -o "$output_path/topic_$j.pkl"
				(( j += 1 ))
#			fi
		done
#	fi
	(( i += 1 ))
done
