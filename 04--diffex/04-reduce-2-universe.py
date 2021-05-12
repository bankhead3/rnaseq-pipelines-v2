#!/usr/bin/python
# combine counts with gene expression quantification

import sys
sys.path.append('../utils')
import myUtils as mu

inFile1 = 'intermediate/03.txt'
inFile2 = 'intermediate/02.txt'
inFile3 = 'input/geneExpression.txt'
outFile1 = 'intermediate/04.txt'

(na,na,genes) = mu.readRecords(inFile1,['gene'])
(records2,header2,keys2) = mu.readRecords(inFile2,['sampleReplicate','gene'])

universe = dict([(gene,gene) for gene in genes])

# write yo file
with open(inFile3,'r') as in3,open(outFile1,'w') as out1:

    # write yo header
    header = in3.readline()
    header = header.strip().split('\t')
    header += ['count']
    out1.write('\t'.join(header) + '\n')

    for line in in3:
        parse1 = line.strip().split('\t')
        assert len(parse1) == len(header)-1, 'HEADER DOES NOT MATCH'
        
        lineDict = dict(zip(header,parse1))

        # only read data for Andrea's experiment
        gene = lineDict['gene']
        if gene in universe:
            sampleReplicate = lineDict['sampleReplicate']
            count = records2['!'.join([sampleReplicate,gene])]['count']
            lineDict['count'] = count

            # assemble lineOut
            lineOut = []
            for field in header:
                lineOut.append(lineDict[field])
            out1.write('\t'.join(lineOut) + '\n')
