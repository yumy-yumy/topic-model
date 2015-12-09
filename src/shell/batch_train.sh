#!/bin/bash
# train LDA
# excuate in lda-c foler

file_path=$1'/*'
stat_path=$2'/*'
outpath=$3

i=0
for file in $stat_path; do
	stat_file[$i]=$file
	(( i += 1 ))
done 

i=0
for file in $file_path; do		
	echo $file
	ext=${file##*.}
	file_name=$(basename $file .$ext)
	year=${file_name##*-}
	model_path="$outpath/$year"
	mkdir $model_path
	IFS=',' 
	j=0
	while read num alpha; do
		echo $num
		echo "$model_path/ldac_output_$j/"
		#./lda est $alpha  $num 'settings.txt' $file 'random' "$model_path/ldac_output_$j/"
		(( j += 1 ))
	done <  ${stat_file[$i]}
	(( i += 1 ))
done
