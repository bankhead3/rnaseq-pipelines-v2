#!/usr/bin/python
# generate a table that converts refseq ids to hgnc genes and entrez ids
# also include filter field - we want to summarize global distribution based on protein generating mrnas
# cufflinks seems to be a problem in that the same isoforms are not always quantified on


import sys
sys.path.append('src') 
import myUtils as mu

import os

inFile1 = 'input/refseq2entrez.txt'
inFile2 = 'intermediate/06.txt' # cufflinks transcript list
inDir1 = '02-txts/'  # cufflinks example file
outFile1 = 'intermediate/07.txt'

nonRefgeneTranscripts = ['ENST00000460036.1','TCONS_00009125','TCONS_00014146']

(records1,header1,keys1) = mu.readRecords(inFile1,['refgeneRefseq'])
(records2,header2,keys2) = mu.readRecords(inFile2,['transcript'])

# check that we have sufficient annotation for transcripts
isoformTranscripts1 = set(keys2)
isoformTranscripts = isoformTranscripts1
isoformTranscripts = sorted(list(isoformTranscripts))

with open(outFile1,'w') as out1:

    # assemble and write yo header
    header = ['gene','transcript','hgnc','entrez','refgeneGene','isProteinCoding?']
    out1.write('\t'.join(header) + '\n')

    # look up annotation for each transcript
    for transcript in isoformTranscripts:
        record = records1[transcript]
        gene,hgnc,entrez,refgeneGene = record['symbol'],record['hgnc'],record['entrez'],record['refgeneGene']
        proteinCoding = 'Y' if 'NM_' in transcript else 'N'

        # assemble and write yo line out
        lineOut = [gene,transcript,hgnc,entrez,refgeneGene,proteinCoding]
        out1.write('\t'.join(lineOut) + '\n')


