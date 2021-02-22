#!/bin/bash
# builds sampleFiles file

fileDir=input/run
globalDir=$(realpath input/run | sed 's/\//|/g' | sed 's/|/\\\//g')

files=$(find -L $fileDir -name '*fastq.gz' | sort | grep -v insp1 | grep -v Undetermined)

fileDir=input\\/run

outFile=intermediate/02.txt

echo -e "file\trun\tlane\tread" > $outFile
for file in $files
do
  echo $file

  global=$(echo $file | sed "s/$fileDir/$globalDir/")
  run=1
#  sampleID=$(echo $file | sed 's/.*\///' | sed 's/.fq.gz//' | sed 's/_.$//')
  lane=1

  # get read
  grep _R1_ <(echo $file) > /dev/null
  if [ $? == 0 ]; then 
    read=1
  else
    read=2
  fi

#  read=$(echo $file | sed 's/.fq.gz//' | sed 's/.*_//')

  echo -e "$global\t$run\t$lane\t$read" >> $outFile
done
