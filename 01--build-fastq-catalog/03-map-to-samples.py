#!/usr/bin/python
# read in run files from the core and map unique names to samples and replicates

import sys
sys.path.append('../utils')
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
    header = header1 + ['sampleReplicate','owner','cellline','tx','rep']
    out1.write('\t'.join(header) + '\n')

    for myKey in keys1:
        record = records1[myKey]

        # connect with sampleInfo file using sampleID and read
        keys2a = [key for key in keys2 if key in myKey]

        assert len(keys2a) == 1
        record2 = records2[keys2a[0]]
        sampleID,owner,cellline,time,rep = record2['sampleID'],record2['owner'],record2['cellline'],record2['time'],record2['replicate']
        parse1 = sampleID.split('_')
        assert len(parse1) == 3 
        tx = parse1[1]

        record['cellline'],record['tx'],record['rep'],record['owner'] = cellline,tx,rep,owner
        record['sampleReplicate'] = '_'.join([owner,cellline,tx,rep])

        # assemble and write line out
        lineOut = []
        for field in header:
            lineOut.append(record[field])
        out1.write('\t'.join(lineOut) + '\n')

        




