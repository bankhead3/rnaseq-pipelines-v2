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
    files = sorted([file for file in files if 'stringtie-gene' in file])

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
        outFile = outDir + sample + '_' + replicate + '-gene.txt'

        # create a lookup table for each file
        lookup = dict()
        with open(inFile) as in1:
            # read yo yeader
            header = in1.readline()
            header = header.strip().split('\t')

            # for each line generate a line out and line in
            for line in in1:
                parse1 = line.strip().split('\t')
                assert len(parse1) == len(header), 'MISSING FIELDS IN FILE!'
                lineDict = dict(zip(header,parse1))
                    
                # assemble and write line out
                gene,value = lineDict['Gene Name'],lineDict['TPM']
                if gene not in lookup:
                    lookup[gene] = [float(value)]
                else:
                    lookup[gene].append(float(value))

        # write it
        genes = sorted(lookup.keys())
        measure = 'tpm'
        with open(outFile,'w') as out1:
            # write yo header
            header = ['gene','measure','value']    
            out1.write('\t'.join(header) + '\n')

            for gene in genes:
                value = str(np.mean(lookup[gene]))
                lineOut = [gene,measure,value]
                out1.write('\t'.join(lineOut) + '\n')
