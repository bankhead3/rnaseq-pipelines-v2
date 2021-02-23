#!/usr/bin/python

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# quantify
def quantify(pars):
    mu.logTime(pars['out'],'START QUANTIFY')

    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/05-quantified',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'],shell=True)
    pars['out'].write('echo quantify \n')

    # *** salmon ***
    if pars['flavor'] == 'salmon' or pars['flavor'] == 'salmon-bias' or pars['flavor'] == 'salmon-bias-stranded':
        mu.writeCmd(pars['out'], 'cp ' + pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '/quant.sf ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-abundance.txt')
        mu.writeCmd(pars['out'], ' ')

    # *** stringtie ***
    elif pars['flavor'] == 'stringtie':

        # program call
        prefix = pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-stringtie-'
        outGTF = prefix + 'transcript-exon.gtf'
        outGene = prefix + 'gene.txt'
        outCov = prefix + 'cov.gtf'

        pars['out'].write('stringtie ' + pars['bamFile'] + ' -e -p ' + pars['threads'] + ' -G ' + pars['gtf'] + ' -e -o ' + outGTF + ' -A ' + outGene + ' -C ' + outCov + '\n')
        pars['out'].write('\n')

    # *** cufflinks ***
    elif pars['flavor'] == 'cufflinks':

        # call cufflinks
        if pars['stranded']:
            pars['out'].write('cufflinks --quiet --no-update-check -p ' + pars['threads'] + ' -G ' + pars['gtf'] + ' --max-bundle-frags 10000000 --library-type fr-firststrand -o ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + ' ' + pars['bamFile'] + '\n')
        else:
            pars['out'].write('cufflinks --quiet --no-update-check -p ' + pars['threads'] + ' -G ' + pars['gtf'] + ' --max-bundle-frags 10000000 --library-type fr-unstranded -o ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + ' ' + pars['bamFile'] + '\n')

        # copy and rename quantification files
        pars['out'].write('cp ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '/genes.fpkm_tracking ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-genes.fpkm' + '\n')
        pars['out'].write('cp ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '/isoforms.fpkm_tracking ' + pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-isoforms.fpkm' + '\n')

        pars['out'].write('\n')

    # *** rsem *** 
    elif pars['flavor'] == 'rsem':
        inFile1 = pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '/' + pars['sampleReplicate'] + '.genes.results'
        outFile1 = pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-rsem-gene.txt'
        inFile2 = pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '/' + pars['sampleReplicate'] + '.isoforms.results'
        outFile2 = pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-rsem-transcript.txt'

        pars['out'].write('cp ' + inFile1 + ' ' + outFile1 + '\n')
        pars['out'].write('cp ' + inFile2 + ' ' + outFile2 + '\n')
        pars['out'].write('\n')

    # *** kallisto *** 
    elif pars['flavor'] == 'kallisto':
        inFile = pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '/abundance.tsv'
        outFile = pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-kallisto-transcript.txt'
        pars['out'].write('cp ' + inFile + ' ' + outFile + '\n')
        pars['out'].write('\n')

    mu.logTime(pars['out'],'FINISH QUANTIFY')
