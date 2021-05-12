#!/usr/bin/python
# combine gene expression and counts into a single file

import sys
sys.path.append('../utils') 
import myUtils as mu

inFile1 = 'intermediate/02.txt'
inFile2 = 'input/geneExpression.txt'
outFile1 = 'intermediate/03.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['sampleReplicate','gene'])
(records2,header2,keys2) = mu.readRecords(inFile2,['sampleReplicate','gene'])

genes1 = sorted(list(set([records1[key]['gene'] for key in keys1])))
genes2 = sorted(list(set([records2[key]['gene'] for key in keys2])))

common = sorted(list(set(genes1).intersection(genes2)))

# write yo file
with open(outFile1,'w') as out1:
    # write yo header
    out1.write('gene\n')

    # write yo gene
    for gene in common:
        out1.write(gene + '\n')
