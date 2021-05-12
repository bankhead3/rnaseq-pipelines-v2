#!/usr/bin/python
# convert entrez 2 gene

import sys
sys.path.append('../utils')
import myUtils as mu

inFile1 = 'intermediate/02.txt'
inFile2 = 'input/hgnc.txt'
outFile1 = 'intermediate/03.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['label','geneset'])
(records2,header2,keys2) = mu.readRecords(inFile2,['hgnc_id'])  # hgnc

# map uniquely and deterministicaly to hgnc
entrez2hgnc = dict()
for myKey in keys2:
    entrez,hgnc = records2[myKey]['entrez_id'],records2[myKey]['hgnc_id']
    if entrez not in entrez2hgnc:
        entrez2hgnc[entrez] = hgnc
    elif len(hgnc) <= len(entrez2hgnc[entrez]) and hgnc < entrez2hgnc[entrez]:
        entrez2hgnc[entrez] = hgnc
entrez2gene = dict()

# then use hgnc symbols
for entrez in entrez2hgnc.keys():
    entrez2gene[entrez] = records2[entrez2hgnc[entrez]]['symbol']
    
# write yo file
with open(outFile1,'w') as out1:

    # write yo header
    header = header1
    header[-1] = 'genes'
    header += ['entrezes']
    out1.write('\t'.join(header) + '\n')

    for myKey in keys1:
        record = records1[myKey]

        # replace entrez with genes
        entrezes = record['entrezes']
        entrezes = entrezes.split(',')
        genes = ['NA' if entrez not in entrez2gene else entrez2gene[entrez] for entrez in entrezes]
        genes = ','.join(genes)
        record['genes'] = genes

        # assemble andw write line out
        lineOut = []
        for field in header1:
            lineOut.append(record[field])
        out1.write('\t'.join(lineOut) + '\n')
