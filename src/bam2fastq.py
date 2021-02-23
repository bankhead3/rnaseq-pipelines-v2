#!/usr/bin/python
# sort and extract fastq from bam files
# i should probably do this with pysam but am too old and crotchety

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess
import os

# Download
def bam2fastq(pars):
    mu.logTime(pars['out'],'START BAM2FASTQ')

    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/01-fastqs/',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/01-fastqs/' + pars['sampleReplicate'],shell=True)
    outDir = pars['pipeline'] + '/01-fastqs/' + pars['sampleReplicate']
    pars['sortedBam'] = outDir + '/sorted.bam'
    pars['fastq1'],pars['fastq2'] = outDir + '/R1.fastq',outDir + '/R2.fastq'
    pars['fqgz1'],pars['fqgz2'] = outDir + '/R1.fastq.gz',outDir + '/R2.fastq.gz'
    pars['fagzFiles'] = [pars['fqgz1'],pars['fqgz2']]

    if pars['flavor'] == 'bam2fastq':
        # sort bam
        mu.writeCmd(pars['out'], 'samtools sort -@ ' + pars['threads'] + ' -n ' + pars['bamFile'] + ' -o ' + pars['sortedBam'])

        # bam2fastq
        mu.writeCmd(pars['out'], 'samtools fastq -@ ' + pars['threads'] + ' ' + pars['sortedBam'] + ' -1 ' + pars['fastq1'] + ' -2 ' + pars['fastq2'])

        # zcat
        mu.writeCmd(pars['out'], 'gzip -c ' + pars['fastq1'] + ' > ' + pars['fqgz1'])  
        mu.writeCmd(pars['out'], 'gzip -c ' + pars['fastq2'] + ' > ' + pars['fqgz2'])  

        # count reads
        mu.writeCmd(pars['out'], "wc -l " + pars['fastq1'] + " | awk '{print $1/4}' > " + outDir + "/readCount1.txt")  
        mu.writeCmd(pars['out'], "wc -l " + pars['fastq2'] + " | awk '{print $1/4}' > " + outDir + "/readCount2.txt")  

        # clean up
        mu.writeCmd(pars['out'], 'rm -f ' + pars['bamFile'])  
        mu.writeCmd(pars['out'], 'rm -f ' + pars['sortedBam'])  
        mu.writeCmd(pars['out'], 'rm -f ' + pars['fastq1'])  
        mu.writeCmd(pars['out'], 'rm -f ' + pars['fastq2'])  

    if pars['flavor'] == 'link':
        assert 'fastqPipeline' in pars

        fqgz1_source = pars['pwd'] + pars['fqgz1'].replace(pars['pipeline'],pars['fastqPipeline'])
        fqgz2_source = pars['pwd'] + pars['fqgz2'].replace(pars['pipeline'],pars['fastqPipeline'])
        
        # link with old files
        mu.writeCmd(pars['out'], 'ln -s ' + fqgz1_source + ' ' + pars['fqgz1'])
        mu.writeCmd(pars['out'], 'ln -s ' + fqgz2_source + ' ' + pars['fqgz2'])

        # read counts not attained here - get this from fastqPipeline...

    if pars['flavor'] == 'skip' or pars['flavor'] == 'passthru':
        # nothing to here pars has already been updated above
        next

    mu.logTime(pars['out'],'FINISH BAM2FASTQ')
