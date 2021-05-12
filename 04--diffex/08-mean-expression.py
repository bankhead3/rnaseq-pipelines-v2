#!/usr/bin/python
# calculate mean normalized log2 value per sample

import sys
sys.path.append('../utils')
import myUtils as mu

import numpy as np

inFile1 = 'input/geneExpression.txt'
outFile1 = 'intermediate/08.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['sampleReplicate','gene'])

sampleGenes = dict()
for key in keys1:
    sample,gene = records1[key]['sample'],records1[key]['gene']
    sampleGene = '!'.join([sample,gene])
    if sampleGene in sampleGenes:
        sampleGenes[sampleGene].append(key)
    else:
        sampleGenes[sampleGene] = [key]
    
# write yo file
sampleGenesOrdered = sorted(sampleGenes.keys())
with open(outFile1,'w') as out1:

    # write yo header
    header = ['sample','gene', 'meanTPM']
    out1.write('\t'.join(header) + '\n')
    
    for sampleGene in sampleGenesOrdered:
        myKeys = sampleGenes[sampleGene]
        
        values = [float(records1[key]['value']) for key in myKeys]
        meanValue = str(np.mean(values))
        sample,gene = sampleGene.split('!')
        
        # assemble and write line out
        lineOut = [sample,gene,meanValue]
        out1.write('\t'.join(lineOut) + '\n')
