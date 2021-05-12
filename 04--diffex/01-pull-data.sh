#!/bin/bash
# when pulling from tcga add -n to ln params

# link to rnaseq pipeline output files
inFile1=../../02--process/pipeline1/05-quantified
outFile1=input/quantified
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd

# cufflinks quantifications
inFile1=../../03--post-process/output/geneExpression20200505.txt
outFile1=input/geneExpression.txt
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd

# cufflinks quantifications
inFile1=../../03--post-process/output/geneAnnotation20200505.txt
outFile1=input/geneAnnotation.txt
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd
