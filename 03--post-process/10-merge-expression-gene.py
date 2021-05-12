#!/usr/bin/python
# map refgene universe to hgnc gene universe
# get rid of NA
# take the mean of redundancies

import sys
sys.path.append('../utils')
import myUtils as mu

import os,re
import numpy as np

inDir = '02-txts'
inFile1 = 'intermediate/07.txt' # annotation
outDir = '10-txts'

(records1,header1,keys1) = mu.readRecords(inFile1,['transcript'])

# refgene2gene
refgene2gene = list(set([(records1[key]['refgeneGene'],records1[key]['gene']) for key in keys1]))
refgene2gene = dict(refgene2gene)
# gene2entrez
gene2entrez = list(set([(records1[key]['gene'],records1[key]['entrez']) for key in keys1]))
gene2entrez = dict(gene2entrez)
# transcript2Gene
transcript2Gene = list(set([(records1[key]['transcript'],records1[key]['gene']) for key in keys1]))
transcript2Gene = dict(transcript2Gene)
# pcGene
pcGenes = list(set([(records1[key]['gene'],None) for key in keys1 if records1[key]['isProteinCoding?'] == 'Y']))
pcGenes = dict(pcGenes)
# pcTranscript
pcTranscripts = list(set([(records1[key]['transcript'],None) for key in keys1 if records1[key]['isProteinCoding?'] == 'Y']))
pcTranscripts = dict(pcTranscripts)

measure = 'tpm'

# make out dirs if not present 
if not os.path.exists(outDir):
    os.makedirs(outDir)

files = os.listdir(inDir)
files = [file for file in files if 'gene' in file]
files = sorted(files)
for file in files:

    # parse sample from file name
    parse1 = re.findall('(.*)-(gene|transcript).txt$',file)

    assert len(parse1) == 1 and len(parse1[0]) == 2, 'CANT PARSE SAMPLE NAME!!'
    sample = parse1[0][0]

    inFile = inDir + '/' + file
    outFile = inFile.replace(inDir,outDir)

    print outFile

    # read through expression data and sum together redundant annotation expression
    geneLookup = dict()
    with open(inFile) as in1:
        inHeader = in1.readline()
        inHeader = inHeader.strip().split('\t')

        for line in in1:
            # assemble lineDict
            parse1 = line.strip().split('\t')
            assert len(parse1) == len(inHeader), 'MISSING FIELDS!'
            lineDict = dict(zip(inHeader,parse1))

            refgene,value = lineDict['gene'],lineDict['value']
            gene = refgene2gene[refgene]

            # add to gene lookup for summation later
            if gene not in geneLookup:
                geneLookup[gene] = [float(value)]
            else:
                geneLookup[gene].append(float(value))

        # write to file
        genes = geneLookup.keys()
        genes = [gene for gene in genes if gene != 'NA']
        with open(outFile,'w') as out1:
            # assemble and write output header
            outHeader = ['gene','entrez','isProteinCoding?','measure','value','log2value']
            out1.write('\t'.join(outHeader) + '\n')

            # walk through yo genes
            for gene in genes:
                values = geneLookup[gene]
                value = np.mean(values)  # why is this mean?
                log2value = np.log2(value + 1)

                # look up annotation yo
                entrez = gene2entrez[gene]
                isPC = 'Y' if gene in pcGenes else 'N'

                # assemble and write yo line
                lineOut = [gene,entrez,isPC,measure,value,log2value]
                lineOut = [str(field) for field in lineOut]
                out1.write('\t'.join(lineOut) + '\n')
