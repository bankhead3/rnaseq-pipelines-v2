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

cmd="./02-parse-counts.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/02.txt 1,2

# get yo universe
cmd="./03-get-universe.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/03.txt 1

# join expression with counts
cmd="./04-reduce-2-universe.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/04.txt 1-7

cmd="R CMD BATCH --vanilla 05-pivot-counts.R intermediate/05.ROut"
echo $cmd; eval $cmd;
src/qc.sh intermediate/05.txt 1

cmd="Rscript 06-deseq2.R > intermediate/06.rout"
echo $cmd; eval $cmd
src/qc.sh intermediate/06.txt 1-3

# clean up columns and add fc
cmd="./07-polish-de.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/07.txt 1,4

# calcualte mean fpkm expression
cmd="./08-mean-expression.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/08.txt 1,2

# add in minMeanDE
cmd="./09-de-mean.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/09.txt 1,4

# remove measurements that don't have a unique entrez id associated with them
# also filter to protein coding genes
cmd="./10-polish-gene-universe.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/10.txt 1,5

# order 
cmd="Rscript 11-order.R > intermediate/09.ROut"
echo $cmd; eval $cmd
src/qc.sh intermediate/11.txt 1,4
fi
# perform thresholding for differential expression
cmd="./12-threshold-de.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/12.txt 1-6

cmd="./13-filter.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/13.txt 1-6

# copy to output
cmd="cp intermediate/12.txt output/diffexMultipleCriteria$myDate.txt;" # src/txt2excel.py output/diffexMultipleCriteria$myDate.txt;"
echo $cmd; eval $cmd
cmd="cp intermediate/04.txt output/geneExpression$myDate.txt;" #  src/txt2excel.py output/geneExpression$myDate.txt"
echo $cmd; eval $cmd
cmd="cp intermediate/11.txt output/foldChanges$myDate.txt;" # src/txt2excel.py output/foldChanges$myDate.txt"
echo $cmd; eval $cmd
cmd="cp intermediate/13.txt output/diffex$myDate.txt; src/txt2excel.py output/diffex$myDate.txt"
echo $cmd; eval $cmd



