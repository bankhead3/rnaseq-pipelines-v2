#!/bin/bash
# when pulling from tcga add -n to ln params

# link to global path of directory containing fastqc files
inFile1=/home/bankhead/alumkal/bfx/rawData/RNA150410JA_16-cell-line_JQ1
inFile1=/scratch/cdsc_project_root/cdsc_project1/shared_data/raw_data/dsilva/rnaseq20210219/
outFile1=input/run
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd

# link to directory containing gdc bam directories
inFile1=experimentalDesignTableV3.txt
#dos2unix input/$inFile1
inFile1=run/$inFile1
outFile1=input/experimentalDesign.txt
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd
