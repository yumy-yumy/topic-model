#!/bin/bash
# compute topic distances for dtm

dirpath=$1'/*'
output_path=$2


i=0
for dir in $dirpath; do	
	echo $dir
	year[$i]=${dir##*/}
	file_path=$dir"/prob/*"
	for file in $file_path; do
		ext=${file##*.}
		file_name=$(basename $file .$ext)
		fun=${file_name%%_*}
		if [ "$fun" = "convert" ]; then
			files[$i]=$file
#			cp $file "$output_path/prob_${year[$i]}.pkl"
		fi
	done
	(( i += 1 ))
done
(( i -= 1 ))

j=0
while [ $j -lt $i ]; do
	(( k = j + 1 ))
	while [ $k -le $i ]; do
		echo ${year[$j]}, ${year[$k]}
		python '/home/pzwang/workspace/topic-model/src/graph/compute_distance.py' -f ${files[$j]} -g ${files[$k]} -o $output_path'/distance_'${year[$j]}'_'${year[$k]}'.pkl'
		(( k += 1 ))
	done
	(( j += 1 ))
done
