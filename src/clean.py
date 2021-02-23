#!/usr/bin/python
# delete files you don't need anymore

import sys
sys.path.append('utils')
import myUtils as mu

# clean
#def clean(step,sampleReplicate,pipeline,out):
def clean(pars):
    mu.logTime(pars['out'],'START CLEAN')

    if pars['flavor'] == '02-reads':
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/02-reads/fastq/*-' + pars['sampleReplicate'] + '*.fastq')
    if pars['flavor'] == 'gdc':
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/00-downloads/' + pars['sampleReplicate'] + '/' + pars['fileName'])
        mu.writeCmd(pars['out'], 'rm -f ' + pars['bamFile'])
        mu.writeCmd(pars['out'], 'rm -f ' + pars['bamFile'] + '.bai')
    if pars['flavor'] == 'standard':
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/02-reads/fastq/*' + pars['sampleReplicate'] + '*.fastq')
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/03-combined/fastq/' + pars['sampleReplicate'] + '*.fastq.gz')
#        mu.writeCmd(pars['out'], 'rm -f ' + pars['bamFile'])
#        mu.writeCmd(pars['out'], 'rm -f ' + pars['bamFile'] + '.bai')
    if pars['flavor'] == 'sequencingCore':
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/02-reads/fastq/*' + pars['sampleReplicate'] + '*.fastq')
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/03-combined/fastq/' + pars['sampleReplicate'] + '*.fastq.gz')
    if pars['flavor'] == 'custom1':        
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/02-reads/fastq/*' + pars['sampleReplicate'] + '*.fastq')
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/03-combined/fastq/' + pars['sampleReplicate'] + '*.fastq.gz')
    if pars['flavor'] == 'rsem':
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/02-reads/fastq/*' + pars['sampleReplicate'] + '*.fastq')
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/03-combined/fastq/' + pars['sampleReplicate'] + '*.fastq.gz')
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '/' + pars['sampleReplicate'] + '.transcript.bam')

    mu.logTime(pars['out'],'FINISH CLEAN')
