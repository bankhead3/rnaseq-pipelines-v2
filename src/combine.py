#!/usr/bin/python

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# 03 combine
def combine(pars):
    mu.logTime(pars['out'],'START COMBINE')

    # add location of fagz files
    fastqFile1 = pars['pipeline'] + '/03-combined/fastq/' + pars['sampleReplicate'] + '-R1.fastq'
    pars['fagzFiles'] = [fastqFile1 + '.gz']
    if pars['end'] == 'paired':
        fastqFile2 = pars['pipeline'] + '/03-combined/fastq/' + pars['sampleReplicate'] + '-R2.fastq'
        pars['fagzFiles'].append(fastqFile2 + '.gz')

    # use when this function has already been called
    if pars['flavor'] == 'skip':
        return

    path = pars['pipeline'] + '/02-reads/fastq/'
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/03-combined',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/03-combined/fastq',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/03-combined/totalFragments',shell=True)
    pars['out'].write('echo combine \n')

    # combine together all R1 reads into a single compressed file
    relevantFiles = sorted([file for file in pars['fastqFiles'] if pars['sampleReplicate'] in file and 'R1.fastq' in file])
#    print relevantFiles

    pars['out'].write('cat ' + ' '.join(relevantFiles) + ' > ' + fastqFile1 + '\n')

    # count total fragments
    countFile = pars['pipeline'] + '/03-combined/totalFragments/' + pars['sampleReplicate'] + '.txt'
    pars['out'].write("wc -l " + fastqFile1 + "| awk '{print $1/4}' > " + countFile + '\n')

    # zip it good
    pars['out'].write('gzip ' + fastqFile1 + '\n')
    pars['out'].write('\n')

    if pars['end'] == 'paired':
        # combine together all R2 reads int a single compressed file
        relevantFiles = sorted([file for file in pars['fastqFiles'] if pars['sampleReplicate'] in file and 'R2.fastq' in file])
#        print relevantFiles

        pars['out'].write('cat ' + ' '.join(relevantFiles) + ' > ' + fastqFile2 + '\n')
        pars['out'].write('gzip ' + fastqFile2 + '\n')
        pars['out'].write('\n')

    mu.logTime(pars['out'],'FINISH COMBINE')
    return
