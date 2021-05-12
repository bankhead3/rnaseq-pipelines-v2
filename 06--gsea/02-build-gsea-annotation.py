#!/usr/bin/python
# build a generic annotation file from an example disease

import sys
sys.path.append('../utils')
import myUtils as mu

inFile1 = 'input/rnaseq.txt'
outFile1 = 'intermediate/annotation.rnaseq.chip'

(records1,header1,keys1) = mu.readRecords(inFile1,['sample','gene'])

# *** RNA-SEQ *** 
# filter to first sample for each dataset
# assumes that gene universe is identical when multiple samples in the same dataset
samples = sorted(list(set([records1[key]['sample'] for key in keys1])))
keys1a = [key for key in keys1 if records1[key]['sample'] == samples[0]]

# write annotation file 
with open(outFile1,'w') as out1:
    header = ['Probe Set ID','Gene Symbol','Gene Title']
    out1.write('\t'.join(header) + '\n')

    for myKey in keys1a:
        record = records1[myKey]
        entrez,gene = record['entrez'],record['gene']
        lineOut = [entrez,gene,gene]
        out1.write('\t'.join(lineOut) + '\n')
