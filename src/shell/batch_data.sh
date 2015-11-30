#!/bin/bash

file_path=$1'/*'
outpath=$2
term_file=$3



for file in $file_path; do
	echo $file
	ext=${file##*.}
	file_name=$(basename $file .$ext)
	year=${file_name#*_}
	python ~/hiit/py/dtm_mult.py -f $file -t $term_file -o "$outpath/foo-mult-$year.dat"
done
