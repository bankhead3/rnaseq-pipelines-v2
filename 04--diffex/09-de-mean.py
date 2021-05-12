#!/usr/bin/python
# include mean treatment and control fpkm across replicates

import sys
sys.path.append('../utils')
import myUtils as mu

inFile1 = 'intermediate/07.txt'   # de results
inFile2 = 'intermediate/08.txt'   # mean expression
inFile3 = 'input/combos.txt'
outFile1 = 'intermediate/09.txt'

(records1,header1,keys1) = mu.readRecords(inFile1, ['sample','gene'])
(records2,header2,keys2) = mu.readRecords(inFile2, ['sample','gene'])
(records3,header3,keys3) = mu.readRecords(inFile3, ['tx'])

# write yo file
with open(outFile1,'w') as out1:
    
    # write yo header
    header = header1 + ['meanTPM','minMeanTPM','meanTPMTreatment','meanTPMControl']
    out1.write('\t'.join(header) + '\n')
    
    for key in keys1:
        record = records1[key]
        treatment,cellline,gene = record['sample'],record['cellline'],record['gene']
        control = records3[treatment]['ctrl']

        # add mean fpkm values for treatment and controls
        trKey = treatment + '!' + gene
        coKey = control + '!' + gene

        assert trKey in records2 and coKey in records2, 'CANT LOOKUP MEAN EXPRESSION!'
        record['meanTPMTreatment'] = records2[trKey]['meanTPM']
        record['meanTPMControl'] = records2[coKey]['meanTPM']        
        record['minMeanTPM'] = str(min([float(record['meanTPMTreatment']),float(record['meanTPMControl'])]))
        record['meanTPM'] = str( (float(record['meanTPMTreatment']) + float(record['meanTPMControl'])) / 2 )

        # assemble and write yo line out
        lineOut = []
        for field in header:
            lineOut.append(record[field])
        out1.write('\t'.join(lineOut) + '\n')

