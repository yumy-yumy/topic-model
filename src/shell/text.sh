#!/bin/bash
# remove duplicate texts and write number of documents to stat.csv

file_path=$1'/*'
outpath=$2

for file in $file_path; do
	echo $file
	python '/home/pzwang/workspace/topic-model/src/preTxt.py' -f $file -o $outpath
done
