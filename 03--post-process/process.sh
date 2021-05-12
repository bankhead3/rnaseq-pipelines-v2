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

# gather stringtie gene measurements
cmd="./02-parse-cufflinks.py"
cmd="./02-parse-stringtie-genes.py"
echo $cmd; eval $cmd
inFile=02-txts/$(ls -1 02-txts | grep gene | head -n1)
src/qc.sh $inFile 1

# gather stringtie transcript measures
cmd="./02-parse-stringtie-transcripts.py"
echo $cmd; eval $cmd
inFile=02-txts/$(ls -1 02-txts | grep transcript | head -n1)
src/qc.sh $inFile 2

# construct list of cufflinks transcripts
cmd="./06-get-transcripts.sh"
echo $cmd; eval $cmd
src/qc.sh intermediate/06.txt 1

# build annotation for all transcripts
cmd="./07-build-annotation.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/07.txt 2

# calculate uq for normalization
cmd="R CMD BATCH 09-get-uq.R intermediate/09.ROut"
echo $cmd; eval $cmd
src/qc.sh intermediate/09.txt 1-4

# apply normalization
cmd="R CMD BATCH 10-normalize.R intermediate/10.ROut"
echo $cmd; eval $cmd

cmd="./11-merge-expression-gene.py"
echo $cmd; eval $cmd
inDir=11-txts
inFile=$inDir/$(ls -1 $inDir | grep gene | head -n1)
src/qc.sh $inFile 1

cmd="./11-merge-expression-transcript.py"
echo $cmd; eval $cmd
inDir=11-txts
inFile=$inDir/$(ls -1 $inDir | grep transcript | head -n1)
src/qc.sh $inFile 3

# remove non-annotated or redundant genes
# add protein coding
cmd="./12-compile-gene.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/12.txt 1-6

cmd="./13-compile-transcript.py"
echo $cmd; eval $cmd
src/qc.sh intermediate/13.txt 1-8
fi
cmd="cp intermediate/12.txt output/geneExpression$myDate.txt; src/txt2excel.py output/geneExpression$myDate.txt"
echo $cmd; eval $cmd
cmd="cp intermediate/13.txt output/transcriptExpression$myDate.txt;"
echo $cmd; eval $cmd
cmd="cp intermediate/07.txt output/geneAnnotation$myDate.txt;"
echo $cmd; eval $cmd



