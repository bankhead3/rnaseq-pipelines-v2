#!/bin/bash

myDate=$(date +%Y%m%d)
ln -sf ../rnaseq-pipelines-v2/src
mkdir -p intermediate
mkdir -p output
mkdir -p input

# create two files one sample metadata and the other with chip expression
cmd="./01-pull-data.sh"
echo $cmd; eval $cmd

# gather fq files and sample names
cmd="./02-build-fq2sample.sh"
echo $cmd; eval $cmd
src/qc.sh intermediate/02.txt 1

# map unique names to samples and replicates
cmd="./03-map-to-samples.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/03.txt 1

cmd="cp intermediate/03.txt output/fastqCatalog$myDate.txt"
echo $cmd; eval $cmd
