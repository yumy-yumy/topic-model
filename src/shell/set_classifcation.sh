#!/bin/bash
# create dictonary between text and classification
# set classification to each document

file_path=$1'/*'
file_path_r=$2
outpath=$3
dict_file=$4

for file in $file_path; do
	ext=${file##*.}
	file_name=$(basename $file .$ext)
	year=${file_name##*_}
	echo $year
	echo "$file_path_a/all_$year.txt"
	#echo "$outpath/acm-class_$year.txt"
	#python '/home/pzwang/workspace/topic-model/src/classification/set_classification.py' -f $file -r "$file_path_r/data_$year.txt" -c acm-class -d $dict_file -o "$outpath/acm-class_$year.txt"
	python '/home/pzwang/workspace/topic-model/src/classification/set_classification.py' -f $file -r "$file_path_r/data_$year.txt" -c arxiv-category -o "$outpath/category_$year.txt"
done
