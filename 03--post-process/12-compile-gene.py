#!/usr/bin/python

import sys
sys.path.append('src')
import myUtils as mu

import os,re

inDir = '11-txts/'
outFile1 = 'intermediate/12.txt'

files = os.listdir(inDir)
files = [file for file in files if 'gene' in file]
files = sorted(files)

# write yo file
with open(outFile1,'w') as out1:

    # get example header and build on it
    (records1,header1,keys1) = mu.readRecords(inDir + files[0],['gene'])
    header = ['sample','sampleReplicate','cellline','tx','replicate'] + header1
    out1.write('\t'.join(header) + '\n')

    for file in files:
        inFile = inDir + file
        (records1,header1,keys1) = mu.readRecords(inFile,['gene'])

        sampleReplicate = file.replace('-gene.txt','')
        print sampleReplicate
        cellline,tx,rep = sampleReplicate.split('_')
        sample = '_'.join([cellline,tx])

        # iterate through records
        for myKey in keys1:
            
            # assemble and write line out
            lineOut = [sample,sampleReplicate,cellline,tx,rep]
            for field in header1:
                lineOut.append(records1[myKey][field])
            out1.write('\t'.join(lineOut) + '\n')
