#!/bin/bash
# when pulling from tcga add -n to ln params

# link to directory containing gdc bam directories
inFile1=/home/bankhead/alumkal/bfx/rawData/RNA150410JA_16-cell-line_JQ1
outFile1=input/run
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd

# link to directory containing gdc bam directories
inFile1=experimentalDesign.txt
#dos2unix input/$inFile1
inFile1=run/$inFile1
outFile1=input/experimentalDesign.txt
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd
