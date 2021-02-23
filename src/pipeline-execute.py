#!/usr/bin/python
# this script generates slurm sh file for each sample replicate
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

inFile1 = 'intermediate/fastq-catalog.txt'
inFile2 = 'intermediate/sample-replicate-catalog.txt'
pipeline = 'pipeline1'
end = 'paired'
stranded = True

numThreads=str(8)

sh = '/'.join([pipeline,'prefix.sh']) 
gtf = '/nfs/turbo/bankheadTurbo/annotation/refgene/20200130/refGene-sorted-canonical.gtf'
alignerIndexDir1='/nfs/turbo/bankheadTurbo/annotation/aligner-indexes/star/GRCh38' # star
alignerIndexDir2='/nfs/turbo/bankheadTurbo/annotation/aligner-indexes/salmon/0.11.3/GRCh38/20200212/transcripts.idx'

(records1,header1,keys1) = mu.readRecords(inFile1,['uniqueName','read'])
(records2,header2,keys2) = mu.readRecords(inFile2,['sampleReplicate'])
# keys2 = keys2[:2]  # testing purposes
fastqc = True
#fastqc = False # testing
pars = {'pipeline':pipeline,'threads':numThreads, 'alignerIndexDir':alignerIndexDir1, 'end':end, 'records':records1, 'stranded':stranded, 'gtf':gtf, 'fastqc':fastqc}

for sampleReplicate in keys2:

    # create a script to be executed from job array
    script = '/'.join([pipeline,'scripts',sampleReplicate + '.sh']) 
    with open(script,'w') as out1:
        # update pars dictionary
        pars['sampleReplicate'] = sampleReplicate
        pars['out'] = out1

        # write yo header
        pars['out'].write('#!/bin/bash\n')

        # *** 02 preprocess ***
        # none - generate fastqc reports
        pars['flavor'] = 'none'
        pp.preprocess(pars)
        # passthru - set up symbolic links to fq.gz files
        pars['flavor'] = 'passthru'  # symbolic link, no fastqc
        pp.preprocess(pars)

        # *** 03 combine ***
        # no need to run if we don't have fastq files to combine
        pars['flavor'] = 'combine'
#        pars['flavor'] = 'skip'
#        c.combine(pars)

        # *** 04 align *** 
        # star - generate bams

        pars['alignerIndexDir'] = alignerIndexDir1
        pars['flavor'] = 'star'
#        pars['flavor'] = 'skip'
        a.align(pars) 
        
#        pars['alignerIndexDir'] = alignerIndexDir2
#        pars['flavor'] = 'salmon'
#        a.align(pars) 

        # *** 05 quantify ***
        # cufflinks - generate quantifications from bams
#        pars['flavor'] = 'cufflinks'
        pars['flavor'] = 'stringtie'
        q.quantify(pars)

        # *** count ***
        # featureCounts
        pars['flavor'] = 'featureCounts'
        co.count(pars)

        # *** 10 qc ***
        # qorts - generate in case qc problems later
        pars['flavor'] = 'qorts'
        qc.qc(pars)

        # *** 20 clean *** 
        # get rid of fastq files 
        pars['flavor'] = 'standard'
        cl.clean(pars) 

        # *** check to make sure sample has not already been successfully run ***
#        pars['flavor'] = 'salmon-bias'
#        check.isCompleted(pars)

        # *** 00 download from gdc portal
#        pars['flavor'] = 'gdc'
#        pars['flavor'] = 'skip'  # for testing
#        d.download(pars)

        # *** 01 extract to fastq files ***
#        pars['flavor'] = 'bam2fastq'
#        pars['flavor'] = 'skip'  # for testing
#        bf.bam2fastq(pars)

    # update permissions
    cmd = 'chmod 755 ' + script
    subprocess.check_call(cmd,shell=True) 

# execute script
cmd = 'sbatch ' + sh
print cmd
subprocess.check_call(cmd,shell=True)
