#!/bin/bash
# when pulling from tcga add -n to ln params

inFile1=../../02--process/output/fragmentCounts20200415.txt
outFile1=input/fragmentCounts.txt
cmd="ln -sf $inFile1 $outFile1"
echo $cmd; eval $cmd

inFile1=../../03--post-process/output/geneExpression20200415.txt
outFile1=input/geneExpression.txt
cmd="ln -sf $inFile1 $outFile1"
echo $cmd; eval $cmd

inFile1=../../04--diffex/output/diffex20200415.txt
outFile1=input/diffex.txt
cmd="ln -sf $inFile1 $outFile1"
echo $cmd; eval $cmd


