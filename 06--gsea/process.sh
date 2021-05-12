#!/bin/bash

myDate=$(date +%Y%m%d)

if [ 1 == 0 ]; then
ln -sf ../rnaseq-pipelines-v2/src
mkdir -p intermediate
mkdir -p output
mkdir -p input

# create two files one sample metadata and the other with chip expression
cmd="./01-pull-data.sh"
echo $cmd; eval $cmd
fi

cmd="./05-gather.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/05.txt 1-5

cmd="cp intermediate/05.txt output/gsea$myDate.txt; src/txt2excel.py output/gsea$myDate.txt"
echo $cmd; eval $cmd;

