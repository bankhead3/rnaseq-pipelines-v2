#!/usr/bin/python
# pivot counts up

import sys
sys.path.append('../utils')
import myUtils as mu

inFile1 = 'intermediate/04.txt'
outFile1 = 'intermediate/05.txt' 

(records1,header1,keys1) = mu.readRecords(inFile1,['sampleReplicate','countType'])

sampleReplicates = sorted(list(set([records1[key]['sampleReplicate'] for key in keys1])))

# write yo file
with open(outFile1,'w') as out1:

    # write yo header
    header = ['sampleReplicate','sample','totalFragments','alignedFragments', 'percentAligned']
    out1.write('\t'.join(header) + '\n')

    for sampleReplicate in sampleReplicates:
        myKey1 = '!'.join([sampleReplicate,'total'])
        myKey2 = '!'.join([sampleReplicate,'aligned'])

        # get values
        total = float(records1[myKey1]['fragmentCount'])
        aligned = float(records1[myKey2]['fragmentCount'])
        percent = aligned/total*100


        owner,cellline,treatment,replicate = sampleReplicate.split('_')
        sample = '_'.join([cellline,treatment])
        
        # assemble and write line out
        lineOut = [sampleReplicate,sample,total,aligned,percent]
        lineOut = [str(field) for field in lineOut]
        out1.write('\t'.join(lineOut) + '\n')

        
