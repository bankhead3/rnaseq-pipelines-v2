#!/usr/bin/python
# this script cleans up fold change table by getting rid of the following:
# 1) non-protein coding  <--- no longer
# 2) genes not mapped to entrez
# 3) multiple genes mapping to the same entrez

import sys
sys.path.append('../utils')
import myUtils as mu

inFile1 = 'intermediate/09.txt'
outFile1 = 'intermediate/10.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['sample','gene','entrez'])

#keys1a = list(set([key for key in keys1 if records1[key]['isProteinCoding'] == 'Y' and records1[key]['entrez'] != 'NA']))
keys1a = list(set([key for key in keys1 if records1[key]['entrez'] != 'NA']))

# construct dictionary with acceptable gene symbols
# forcc
entrez2gene = dict()
for key in keys1a:
    record = records1[key]
    entrez,gene = record['entrez'],record['gene']
    
    # identify select gene per entrez id by arbitrarily choosing gene
    if entrez not in entrez2gene:
        entrez2gene[entrez] = gene
    elif gene < entrez2gene[entrez]:
        entrez2gene[entrez] = gene

# write yo file
with open(outFile1,'w') as out1:
    
    # write yo header
    out1.write('\t'.join(header1) + '\n')

    for myKey in keys1a:
        record = records1[myKey]
        entrez,gene = record['entrez'],record['gene']
        
        # ignore read out if not the chose gene
        # these don't happen often
        assert entrez in entrez2gene
        if gene != entrez2gene[entrez]:
            continue

        # assemble and write line out
        lineOut = []
        for field in header1:
            lineOut.append(records1[myKey][field])
        out1.write('\t'.join(lineOut) + '\n')        
                        
