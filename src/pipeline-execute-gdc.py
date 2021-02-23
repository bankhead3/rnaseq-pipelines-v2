#!/usr/bin/python
# this script generates sh file for each sample replicate
# slurm sh files are generated and submitted

import sys
sys.path.append('../utils')
sys.path.append('../rnaseq-pipelines')

import myUtils as mu
import preprocess as pp
import combine as c
import clean as cl
import align as a
import quantify as q
import count as co
import discover as d
import qc as qc
import check as check
import download as d
import bam2fastq as bf

import subprocess
import os
import re

inFile1 = 'intermediate/sample-sheet.txt'
pipeline = 'pipeline2'
fastqPipeline = 'pipeline1' # link to fastq in another pipeline directory

numThreads=str(8)
tokenFile=os.path.abspath('input/gdc_token.txt')
pwd = os.path.abspath('.') + '/'

sh = '/'.join([pipeline,'prefix.sh']) 
alignerIndexDir1='/nfs/turbo/bankheadTurbo/annotation/aligner-indexes/star/GRCh38' # star
alignerIndexDir1='/home/bankhead/palmbos/projects/bakeOff20200326/00--aligner-indexes/salmon/0.9.1/GRCh38/refgene-01/transcripts.idx'
gtf = '/nfs/turbo/bankheadTurbo/annotation/refgene/20200130/refGene-sorted-canonical.gtf'
stranded = False
end = 'paired'
#alignerIndexDir2='/nfs/turbo/bankheadTurbo/annotation/aligner-indexes/salmon/0.11.3/GRCh38/20200212/transcripts.idx'
#alignerIndexDir='/nfs/turbo/topBfx/bankhead/projects/palmbos/tp63Isoforms20170602/00--aligner-indexes/salmon/GRCh38/gtf17/transcripts.idx'  # both TRIM29's, all TP63 isoforms minus isoform13


# read in token
with open(tokenFile) as in1:
    token = in1.readline()
    token = token.strip()

pars = {'pipeline':pipeline,'fastqPipeline':fastqPipeline,'token':token,'threads':numThreads,'alignerIndexDir':alignerIndexDir1,'gtf':gtf,'stranded':stranded,'end':end,'pwd':pwd}

(records1,header1,keys1) = mu.readRecords(inFile1,['fileID'])
keys1a = [key for key in keys1 if records1[key]['disease'] in ['BLCA']]
#keys1a = keys1a[:30]
#keys1a = keys1a[:5]
keys1a = keys1a[:1]

for fileID in keys1a:
    sampleReplicate = records1[fileID]['sample']
    fileName = records1[fileID]['fileName']

    # create a script to be executed from job array
    script = '/'.join([pipeline,'scripts',sampleReplicate + '.sh']) 
    print script
    with open(script,'w') as out1:
        # update pars dictionary
        pars['sampleReplicate'],pars['fileID'],pars['fileName'] = sampleReplicate,fileID,fileName
        pars['out'] = out1

        # write yo header
        pars['out'].write('#!/bin/bash\n')
        
        # check to make sure sample has not already been successfully run
#        pars['flavor'] = 'salmon-bias'
#        check.isCompleted(pars)

        # 00 download from gdc portal
        pars['flavor'] = 'gdc'
        pars['flavor'] = 'passthru'  # don't download, but set up variables as though you did
        d.download(pars)

        # 01 extract to fastq files
        pars['flavor'] = 'bam2fastq'
        pars['flavor'] = 'link'      # link to fastq files in another pipeline directory to save time
#        pars['flavor'] = 'passthru'  # for testing
        bf.bam2fastq(pars)

        # 04 align with star
        pars['flavor'] = 'salmon-bias'
#        pars['flavor'] = 'star'
#        pars['flavor'] = 'passthru'  # for testing
        a.align(pars) 

        # 05 quantify
        pars['flavor'] = 'salmon-bias'
#        pars['flavor'] = 'cufflinks'
        q.quantify(pars)

        # *** count ***
        pars['flavor'] = 'featureCounts'
#        co.count(pars)

        # *** 10 qc ***
        pars['flavor'] = 'qorts'
#        qc.qc(pars)

        # clean up fastq files to save scratch space
        pars['flavor'] = 'gdc'
        cl.clean(pars)  #'02-reads',sampleReplicate,pipeline,out1)

    # update permissions
    cmd = 'chmod 755 ' + script
    subprocess.check_call(cmd,shell=True) 

# execute script
cmd = 'sbatch ' + sh
#print cmd
#subprocess.check_call(cmd,shell=True)
