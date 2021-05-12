#!/bin/bash

inDir1=intermediate
inDirs=$(ls -d $inDir1/* | grep 10000.)

for inDir in $inDirs
do
  inDir2=$(echo $inDir | sed 's/intermediate\///')
  outFile="$inDir2.zip"

  cmd="cd $inDir1; zip -r $outFile $inDir2; cd .."
  echo $cmd; eval $cmd

done
mv $inDir1/*zip output
