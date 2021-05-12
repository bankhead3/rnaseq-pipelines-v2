#!/usr/bin/python
# map refgene universe to hgnc gene universe
# get rid of NA
# sum together redundancies

import sys
sys.path.append('src')
import myUtils as mu

import os,re
import numpy as np

inDir = '10-txts'
inFile1 = 'intermediate/07.txt' # annotation
outDir = '11-txts'

(records1,header1,keys1) = mu.readRecords(inFile1,['transcript'])

measure = 'tpm'

# make out dirs if not present 
if not os.path.exists(outDir):
    os.makedirs(outDir)

files = os.listdir(inDir)
files = [file for file in files if 'transcript' in file]
files = sorted(files)
for file in files:

    # parse sample from file name
    parse1 = re.findall('(.*)-(gene|transcript).txt$',file)

    assert len(parse1) == 1 and len(parse1[0]) == 2, 'CANT PARSE SAMPLE NAME!!'
    sample = parse1[0][0]

    inFile = inDir + '/' + file
    outFile = inFile.replace(inDir,outDir)

    (records,header,keys) = mu.readRecords(inFile,['transcript'])
    keys = [key for key in keys if records1[key]['gene'] != 'NA'] 
    
    print outFile
    with open(outFile,'w') as out1:
        # assemble and write output header
        outHeader = ['gene','entrez','transcript','isProteinCoding?','measure','value','log2value','rawValue']
        out1.write('\t'.join(outHeader) + '\n')

        # walk through yo genes
        for transcript in keys:
            record = records[transcript]
            value = float(record['valueNorm'])
            log2value = np.log2(value + 1)
            rawValue = float(record['value'])

            # look up annotation yo
            entrez,gene,isPC = records1[transcript]['entrez'],records1[transcript]['gene'],records1[transcript]['isProteinCoding?']
            
            # assemble and write yo line
            lineOut = [gene,entrez,transcript,isPC,measure,value,log2value,rawValue]
            lineOut = [str(field) for field in lineOut]
            out1.write('\t'.join(lineOut) + '\n')
