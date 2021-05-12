#!/bin/bash
# compile a list of cufflinks transcripts for fast look up later
# cufflinks does not always output the same transcripts

inDir=02-txts
tmpFile=intermediate/tmp.txt
outFile1=intermediate/06.txt

# remove if there is an old one
if [ -e $tmpFile ]; then rm $tmpFile; fi

files=$(ls -1 $inDir | grep transcript)
for file in $files
do
  inFile=$inDir/$file
  echo $inFile
  cut -f2 $inFile | tail -n+2 | sort | uniq >> $tmpFile
done

# create final output file
echo 'transcript' > $outFile1
sort $tmpFile | uniq >> $outFile1
