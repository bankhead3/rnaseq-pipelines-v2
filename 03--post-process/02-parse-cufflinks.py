#!/usr/bin/python
# parse a set of gene and isoform files from cufflinks

import sys
sys.path.append('../utils')
import myUtils as mu

import os
import re

inDirs = ['input/cufflinks1/05-quantified/'] 
outDir = '02-txts/'

# create out directory if there isn't one
if not os.path.exists(outDir):
    os.makedirs(outDir)

for inDir in inDirs:

    files = os.listdir(inDir)
    files = [file for file in files if '.fpkm' in file]

    for file in files:

        # parse sample from file name
        parse1 = re.findall('(.*)-([0-9])-(genes|isoforms).fpkm$',file)
        assert len(parse1) == 1 and len(parse1[0]) == 3, 'CANT PARSE SAMPLE NAME!!'
        sample,replicate,myType = parse1[0][0],parse1[0][1],parse1[0][2]

        # write a single file per sample
        outFile = outDir + sample + '-' + replicate + '-' + myType[:-1] + '.txt'
        print outFile
        with open(outFile,'w') as out1:

            # write yo header
            if myType == 'genes':
                header = ['gene','locus','measure','value','status']    
                out1.write('\t'.join(header) + '\n')
            else:
                header = ['gene','transcript','locus','measure','value','status']
                out1.write('\t'.join(header) + '\n')

            # read sample file
            inFile = inDir + file
            with open(inFile,'r') as in1:
                # read yo yeader
                header = in1.readline()
                header = header.strip().split('\t')

                # for each line generate a line out and line in
                for line in in1:
                    parse1 = line.strip().split('\t')
                    assert len(parse1) == len(header), 'MISSING FIELDS IN FILE!'
                    lineDict = dict(zip(header,parse1))
                    #                print lineDict

                    if myType == 'genes':
                        lineOut = [lineDict['gene_id'],lineDict['locus'],'fpkm',lineDict['FPKM'],lineDict['FPKM_status']]
                    else:
                        lineOut = [lineDict['gene_id'],lineDict['tracking_id'],lineDict['locus'],'fpkm',lineDict['FPKM'],lineDict['FPKM_status']] 
                    out1.write('\t'.join(lineOut) + '\n')
