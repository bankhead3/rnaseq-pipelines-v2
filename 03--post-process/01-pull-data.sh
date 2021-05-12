#!/bin/bash
# when pulling from tcga add -n to ln params

# link to rnaseq pipeline output files
inFile1=../../02--process/pipeline1/
outFile1=input/stringtie
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd

inFile1=~/annotation/refgene/20200130/refseq2entrez20200130.txt
outFile1=input/refseq2entrez.txt
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd
