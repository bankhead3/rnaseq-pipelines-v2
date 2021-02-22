#!/usr/bin/python
# read in run files from the core and map unique names to samples and replicates

import sys
sys.path.append('src')
import myUtils as mu

import re

inFile1 = 'intermediate/02.txt'
inFile2 = 'input/experimentalDesign.txt'
outFile1 = 'intermediate/03.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['file'])
(records2,header2,keys2) = mu.readRecords(inFile2,['filePrefix'])

# write yo file
with open(outFile1,'w') as out1:

    # write yo header
    header = header1 + ['sampleReplicate','sample','tx','rep']
    out1.write('\t'.join(header) + '\n')

    for myKey in keys1:
        record = records1[myKey]

        # connect with sampleInfo file using sampleID and read
        keys2a = [key for key in keys2 if key in myKey]
        assert len(keys2a) == 1
        record2 = records2[keys2a[0]]
        sampleReplicate,sample,tx,rep = record2['sampleReplicate'],record2['sample'],record2['tx'],record2['replicate']
        parse1 = sampleReplicate.split('_')
        assert len(parse1) == 3 
        tx = parse1[1]

        record['sample'],record['tx'],record['rep'] = sample,tx,rep
        record['sampleReplicate'] = '_'.join([sample,tx,rep])

        # assemble and write line out
        lineOut = []
        for field in header:
            lineOut.append(record[field])
        out1.write('\t'.join(lineOut) + '\n')

        




