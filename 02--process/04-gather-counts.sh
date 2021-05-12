#!/bin/bash
# gathers fragment counts from pipeline

pipeline=pipeline1
inDir1=$pipeline/03-combined/totalFragments
inDir1=$pipeline/02-reads/totalFragments
inDir2=$pipeline/04-aligned/totalFragments

outFile1=intermediate/04.txt

files1=$(ls -1 $inDir1/* | grep -v raw) 
files2=$(ls -1 $inDir2/*) 

echo -e "sampleReplicate\tcountType\tfragmentCount" > $outFile1
for file in $files1
do
  countType='total'    
  sampleReplicate=$(echo $file | sed 's/.*\///' | sed 's/.txt//' | sed 's/1!//')
  count=$(cat $file)

  echo -e "$sampleReplicate\t$countType\t$count" >> $outFile1
done

for file in $files2
do
  countType='aligned'    
  sampleReplicate=$(echo $file | sed 's/.*\///' | sed 's/.txt//')
  count=$(cat $file)

  echo -e "$sampleReplicate\t$countType\t$count" >> $outFile1
done

