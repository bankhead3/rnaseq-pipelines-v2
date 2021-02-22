#!/bin/bash
# get location of fastq files
# this may need to be updated *!!*

fileDir=input/run
globalDir=$(realpath input/run | sed 's/\//|/g' | sed 's/|/\\\//g')

# *!!* update to search for patterns of interest *!!*
files=$(find -L $fileDir -name '*fastq.gz' | sort | grep -v insp1 | grep -v Undetermined)
files=$(find -L $fileDir -name '*fastq.gz' | sort)
# *!!*

fileDir=input\\/run

outFile=intermediate/02.txt

echo -e "file\trun\tlane\tread" > $outFile
for file in $files
do
  echo $file

  global=$(echo $file | sed "s/$fileDir/$globalDir/")

  # *!!* assume samples are in same run and lane *!!*
  run=1
  lane=1
  # *!!*

  # *!!* update to recognize read ro 2 if paired end data *!!* or 1 if single end
  grep _R1_ <(echo $file) > /dev/null
  if [ $? == 0 ]; then 
    read=1
  else
    read=2
  fi
  # *!!*
#  read=$(echo $file | sed 's/.fq.gz//' | sed 's/.*_//')

  echo -e "$global\t$run\t$lane\t$read" >> $outFile
done
