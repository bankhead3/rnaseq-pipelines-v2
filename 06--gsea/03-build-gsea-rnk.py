#!/usr/bin/python
# build gsea expression txt file
# requires at least mean fpkm of 0.5

import sys
sys.path.append('../utils')
import myUtils as mu

inFile1 = 'input/rnaseq.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['sample','gene'])

samples1 = sorted(list(set([records1[key]['sample'] for key in keys1])))

# *** build RNA-Seq ranks ***
for sample in samples1:

    keys1a = [key for key in keys1 if records1[key]['sample'] == sample and records1[key]['log2FC'] != 'NA' and float(records1[key]['meanFPKM']) > 0.5]
    # write yo file
    platform = 'rnaseq'
    outFile = 'intermediate/' + sample.replace('-','_') + '_' + platform + '.rnk'
    print outFile
    with open(outFile,'w') as out1:
        # write yo header
        header = ['# gene','log2fc']
        out1.write('\t'.join(header) + '\n')
        
        # for each key we write a line
        for key in keys1a:
            gene,log2fc = records1[key]['gene'],records1[key]['log2FC']
            out1.write('\t'.join([gene,log2fc]) + '\n')
