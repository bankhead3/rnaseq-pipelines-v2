#!/usr/bin/python
# reformats fastq catalog 

import sys
sys.path.append('src')
import myUtils as mu

import re

inFile1 = 'input/fastqCatalog.txt'
outFile1 = 'intermediate/fastq-catalog.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['run','sampleReplicate','read'])

# write yo out
with open(outFile1,'w') as out1:

    # write yo header
    header = ['file','uniqueName','sampleReplicate','read']
    out1.write('\t'.join(header) + '\n')

    # for each barcode write 2 lines
    for myKey in keys1:
        record = records1[myKey]

        uniqueName = myKey[:-2]

        # extract sampe replicate from sampleReplicate
        parse1 = myKey.split('!')
        assert len(parse1) == 3, 'CANT PARSE UNIQUENAME!'
        run,sampleReplicate,read = parse1
        
        file1 = record['file']

        # assemble and write line out
        lineOut1 = [file1,uniqueName,sampleReplicate,read]
        out1.write('\t'.join(lineOut1) + '\n')
