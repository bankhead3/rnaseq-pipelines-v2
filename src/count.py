#!/usr/bin/python
# implements subread feature counts

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# count
#def count(flavor,out,records,sampleLabel,pipeline,numThreads,gtf):
def count(pars):
    mu.logTime(pars['out'],'START COUNT')

    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/05-quantified',shell=True)

    if pars['flavor'] == 'featureCounts':
        outDir = pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '/'

        # quantify for gene and transcripts
        if pars['stranded'] and pars['end'] == 'paired':
            pars['out'].write('featureCounts -p -s 2 --primary -T ' + pars['threads'] + ' -a ' + pars['gtf'] + ' -o ' + outDir + 'gene-counts.txt ' + pars['bamFile'] + '\n')
            pars['out'].write('featureCounts -O -s 2 -p --primary -g transcript_id -T ' + pars['threads'] + ' -a ' + pars['gtf'] + ' -o ' + outDir + 'isoform-counts.txt ' + pars['bamFile'] + '\n')
        elif pars['stranded'] and pars['end'] == 'single':
            pars['out'].write('featureCounts -s 2 --primary -T ' + pars['threads'] + ' -a ' + pars['gtf'] + ' -o ' + outDir + 'gene-counts.txt ' + pars['bamFile'] + '\n')
            pars['out'].write('featureCounts -O -s 2 --primary -g transcript_id -T ' + pars['threads'] + ' -a ' + pars['gtf'] + ' -o ' + outDir + 'isoform-counts.txt ' + pars['bamFile'] + '\n')
        elif pars['end'] == 'single':
            pars['out'].write('featureCounts --primary -T ' + pars['threads'] + ' -a ' + pars['gtf'] + ' -o ' + outDir + 'gene-counts.txt ' + pars['bamFile'] + '\n')
            pars['out'].write('featureCounts -O --primary -g transcript_id -T ' + pars['threads'] + ' -a ' + pars['gtf'] + ' -o ' + outDir + 'isoform-counts.txt ' + pars['bamFile'] + '\n')
        elif pars['end'] == 'paired':
            pars['out'].write('featureCounts -p --primary -T ' + pars['threads'] + ' -a ' + pars['gtf'] + ' -o ' + outDir + 'gene-counts.txt ' + pars['bamFile'] + '\n')
            pars['out'].write('featureCounts -O -p --primary -g transcript_id -T ' + pars['threads'] + ' -a ' + pars['gtf'] + ' -o ' + outDir + 'isoform-counts.txt ' + pars['bamFile'] + '\n')
        else:
            raise 'DONT UNDERSTAND!!'

        pars['out'].write('\n')

        pars['out'].write('mv ' + outDir + 'gene-counts.txt ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-gene-counts.txt' + '\n')
        pars['out'].write('mv ' + outDir + 'isoform-counts.txt ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-isoform-counts.txt' + '\n')
        pars['out'].write('\n')

    mu.logTime(pars['out'],'FINISH COUNT')

