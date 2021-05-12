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

cmd="./02-build-fastq-catalog.py"
echo $cmd; eval $cmd

cmd="./03-build-sample-replicate-catalog.sh"
echo $cmd; eval $cmd
fi

exit
cmd="./04-gather-counts.sh"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/04.txt 1,2

cmd="./05-pivot-counts.py"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/05.txt 1

cmd="cp intermediate/05.txt output/fragmentCounts$myDate.txt"
echo $cmd; eval $cmd
