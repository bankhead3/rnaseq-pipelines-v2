#!/bin/bash

myDate=$(date +%Y%m%d)
ln -sf ../rnaseq-pipelines-v2/src
mkdir -p intermediate
mkdir -p output
mkdir -p input

if [ 1 == 0 ]; then

# create two files one sample metadata and the other with chip expression
cmd="./01-pull-data.sh"
echo $cmd; eval $cmd

cmd="Rscript 02-david-rnaseq.R > intermediate/02.rout"
echo $cmd; eval $cmd
src/qc.sh intermediate/02.txt 1-4
fi

cmd="./03-polish-david.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/03.txt 1-4

cmd="Rscript 04-summary.R > intermediate/04.rout"
echo $cmd; eval $cmd; 
src/qc.sh intermediate/04.txt 1,2

cmd="cp intermediate/04.txt output/davidSummary$myDate.txt; src/txt2excel.py output/davidSummary$myDate.txt"
echo $cmd; eval $cmd
cmd="cp intermediate/03.txt output/david$myDate.txt; src/txt2excel.py output/david$myDate.txt"
echo $cmd; eval $cmd


