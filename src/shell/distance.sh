#!/bin/bash
# compute topic distances for htm

dirpath=$1'/*'

k=0
for dir in $dirpath; do	
		echo $dir
		mkdir $dir'/distance'
		output_path=$dir'/distance'
		file_path=$dir"/prob/*"
		i=0
		for file in $file_path; do
#			ext=${file##*.}
#			file_name=$(basename $file .$ext)
#			fun=${file_name%%_*}
#			if [ "$fun" = "convert" ]; then
				files[$i]=$file
				(( i += 1 ))
#			fi
		done
		(( i -=1 ))
		j=0
		while [ $j -lt $i ]; do
			ext=${files[$j]##*.}
			file_name=$(basename ${files[$j]} .$ext)
			level_i=${file_name##*_}
			file_name=$(basename ${files[$j+1]} .$ext)
			level_j=${file_name##*_}	
			echo $level_i, $level_j
			python '/home/pzwang/workspace/topic-model/src/graph/compute_distance.py' -f ${files[$j]} -g ${files[$j+1]} -o $output_path'/distance_'$level_i'_'$level_j'.pkl'
			(( j += 1 ))
		done
done
