#!/usr/bin/python

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# discover
def discover(flavor,out,records,sampleLabel,pipeline,numThreads,gtf):
    mu.logTime(out,'START DISCOVER')

    sample,replicate = sampleLabel.split('#')

    subprocess.check_call('mkdir -p ' + pipeline + '/06-discover',shell=True)
    subprocess.check_call('mkdir -p ' + pipeline + '/06-discover/' + sampleLabel,shell=True)
    out.write('echo discover \n')

    if flavor == 'cufflinks':
        bam = pipeline + '/04-aligned/' + sampleLabel + '.bam'
        out.write('cufflinks -p ' + numThreads + ' --max-bundle-frags 10000000 --library-type fr-unstranded -o ' + pipeline + '/06-discover/' + sampleLabel + ' ' + bam + '\n')
#        out.write('cp ' + pipeline + '/05-quantified/' + sampleLabel + '/genes.fpkm_tracking ' + pipeline + '/05-quantified/' + sampleLabel + '-genes.fpkm' + '\n')
#        out.write('cp ' + pipeline + '/05-quantified/' + sampleLabel + '/isoforms.fpkm_tracking ' + pipeline + '/05-quantified/' + sampleLabel + '-isoforms.fpkm' + '\n')
        out.write('\n')
    else:
        print flavor
        raise 'DONT RECOGNIZE DISCOVER FLAVOR'

    mu.logTime(out,'FINISH DISCOVER')

