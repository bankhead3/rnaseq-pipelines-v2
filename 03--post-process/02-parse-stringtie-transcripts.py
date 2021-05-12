#!/usr/bin/python
# parse stringtie gene expression values
# sum together duplicate genes

import sys
sys.path.append('../utils')
import myUtils as mu

import os,re
import numpy as np

inDirs = ['input/stringtie/05-quantified/'] 
outDir = '02-txts/'

# create out directory if there isn't one
if not os.path.exists(outDir):
    os.makedirs(outDir)

for inDir in inDirs:

    files = os.listdir(inDir)
    files = sorted([file for file in files if 'stringtie-transcript' in file])

    for file in files:
        inFile = inDir + file
        print inFile

        # parse sample from file name
        sep_count = file.count('_')
        if sep_count == 3:
            parse1 = re.findall('(.*?)_(.*?)_(.*?)_([0-9])-stringtie.*$',file)
            assert len(parse1) == 1 and len(parse1[0]) == 4, 'CANT PARSE SAMPLE NAME!!'
            owner,cellline,tx,replicate = parse1[0]
        else:
            print 'no understand...'
            raise

        sample = cellline + '_' + tx

        outFile = outDir + sample + '_' + replicate + '-transcript.txt'

        # create a lookup table for each file
        lookup = dict()
        with open(inFile) as in1, open(outFile,'w') as out1:
            # read yo yeader
            in1.readline(); in1.readline()

            # write yo header
            header = ['gene','transcript','measure','value']    
            out1.write('\t'.join(header) + '\n')

            # for each line generate a line out and line in
            for line in in1:
                parse1 = line.strip().split('\t')

                if parse1[2] == 'transcript':
                    assert len(parse1) == 9
                    info = parse1[8]

                    # parse line
                    parse2 = re.findall('gene_id "(.*?)"; transcript_id "(.*?)".* TPM "(.*?)"',info)
                    assert len(parse2) == 1 and len(parse2[0]) == 3
                    gene,transcript,value = parse2[0]

                    # assemble and write line out
                    lineOut = [gene,transcript,'tpm',value]
                    out1.write('\t'.join(lineOut) + '\n')
