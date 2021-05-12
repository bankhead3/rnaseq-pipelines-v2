#!/usr/bin/python
# gather gene set enrichment tables from multiple pipeline directories
# updated to contain gene and disease specific results

import sys
sys.path.append('../utils')
import myUtils as mu

import os
import re
import numpy as np

inDir = 'intermediate/'
outFile1 = 'intermediate/05.txt'
significance = 0.05

sources = {'pipeline1a':'kegg', 'pipeline1b':'go', 'pipeline1c':'hallmark', 'pipeline1d':'tft', 'pipeline1e':'cgp'}
#sources = {'pipeline1a':'kegg'} #, 'pipeline1b':'go', 'pipeline1c':'hallmark', 'pipeline1d':'tft', 'pipeline1e':'cgp'}
#subdirs = sorted(sources.keys())

files = os.listdir(inDir)
subdirs = [inDir + file for file in files if '10000.' in file and '.zip' not in file]   # testing
#subdirs = [inDir + file for file in files if '100.' in file]   # testing

# write yo file
with open(outFile1,'w') as out1:

    # write yo header
    header = ['isSignificant?','direction','sample','source','geneset','size','ES','NES','pValue','fwer','fdr','perms']
    out1.write('\t'.join(header) + '\n')
    
    # iterate through pipelines
    for subdir in subdirs:
        parse1 = re.findall(inDir + '([0-9]+)[.](.*)[.](.*)[.]GseaPreranked.([0-9]+).*', subdir)
        assert len(parse1) == 1 and len(parse1[0]) == 4
        perms,sample,source,myID = parse1[0]

        # enrichments for positive fold changes
        inFile1 = '/'.join([subdir,'gsea_report_for_na_pos_' + myID + '.xls'])
        with open(inFile1,'r') as in1:
            inHeader = in1.readline()

            for line in in1:
                parse1 = line.strip().split('\t')
                geneset,size,ES,NES = parse1[0],parse1[3],parse1[4],parse1[5]
                pValue,fdr,fwer = parse1[6],parse1[7],parse1[8]

                significant = 'Y' if float(fdr) < significance else 'N'

                # assemble and write line out
                lineOut = [significant,'pos',sample,source,geneset,size,ES,NES,pValue,fwer,fdr,perms]
                out1.write('\t'.join(lineOut) + '\n')

        # enrichments for negative fold changes
        inFile1 = '/'.join([subdir,'gsea_report_for_na_neg_' + myID + '.xls'])
        with open(inFile1,'r') as in1:
            inHeader = in1.readline()

            for line in in1:
                parse1 = line.strip().split('\t')
                geneset,size,ES,NES = parse1[0],parse1[3],parse1[4],parse1[5]
                pValue,fdr,fwer = parse1[6],parse1[7],parse1[8]

                significant = 'Y' if float(fdr) < significance else 'N'

                # assemble and write line out
                lineOut = [significant,'neg',sample,source,geneset,size,ES,NES,pValue,fwer,fdr,perms]
                out1.write('\t'.join(lineOut) + '\n')
                    
