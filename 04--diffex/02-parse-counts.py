#!/usr/bin/python
# parse a set of gene and isoform files from cufflinks

import sys
sys.path.append('../utils')
import myUtils as mu

import os
import re

inDir = 'input/quantified/'
outFile1 = 'intermediate/02.txt'

files = os.listdir(inDir)
files = sorted([file for file in files if 'gene-counts.txt' in file])

# write yo file
with open(outFile1,'w') as out1:
    header = ['sampleReplicate','gene','count']    
    out1.write('\t'.join(header) + '\n')

    for file in files:

        # parse sample from file name
        sampleReplicate = file.replace('-gene-counts.txt','')
        if sampleReplicate.count('_') == 3:
            sampleReplicate = re.sub('^.*?_','',sampleReplicate)
        print sampleReplicate

        # read sample file
        inFile = inDir + file
        with open(inFile,'r') as in1:
            in1.readline()

            # read yo yeader
            header = in1.readline()
            header = header.strip().split('\t')
            header[-1] = 'count'
            
            # for each line generate a line out and line in
            for line in in1:
                parse1 = line.strip().split('\t')
                assert len(parse1) == len(header), 'MISSING FIELDS IN FILE!'
                lineDict = dict(zip(header,parse1))

                # assemble and write line out
                lineOut = [sampleReplicate,lineDict['Geneid'],lineDict['count']]
                out1.write('\t'.join(lineOut) + '\n')

