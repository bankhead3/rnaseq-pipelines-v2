#!/usr/bin/python
# add is de using 3 different criteria

import sys
sys.path.append('../utils')
import myUtils as mu

inFile1 = 'intermediate/12.txt'
outFile1 = 'intermediate/13.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['sample','gene','criteria'])

keys1a = [key for key in keys1 if records1[key]['criteria'] == 'FC2_q']

# write yo file
with open(outFile1,'w') as out1:

    # write yo header
    out1.write('\t'.join(header1) + '\n')

    for key in keys1a:

        # assemble and write line out
        lineOut = []
        for field in header1:
            lineOut.append(records1[key][field]) 
        out1.write('\t'.join(lineOut) + '\n')

