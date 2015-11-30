#!/bin/bash
# train LDA for all levels(htm) and all years(dtm)
# excuate in lda-c foler

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
	file=$dir'/foo-mult.dat'
	echo $file
	IFS=',' 
	j=1
	while read num alpha; do
		if [ "$j" -gt 2 ]; then
			echo $num
			echo $dir"/ldac_output_$j/"
			#./lda est $alpha  $num 'settings.txt' $file 'random' $dir"/ldac_output_$j/"
		fi
		(( j += 1 ))
	done <  ${stat_file[$i]}	
	(( i += 1 ))
done
