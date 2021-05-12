#!/bin/bash
# when pulling from tcga add -n to ln params

inFile1=../../04--diffex/output/diffex20200115.txt
outFile1=input/rnaseq.txt
cmd="ln -sf $inFile1 $outFile1"
echo $cmd; eval $cmd
