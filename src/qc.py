#!/usr/bin/python
# run qorts for post alignment qc

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

#def qc(flavor,out,records,sampleLabel,pipeline,numThreads,gtf):
def qc(pars):
    mu.logTime(pars['out'],'START QC')

    # use when this function has already been called
    # assumes we have 44GB of memory
    # assumes we have 64GB of memory
    # this can be lowered but by default we need to be robust to TCGA
    if pars['flavor'] == 'qorts':

        qorts = '/nfs/turbo/bankheadTurbo/software/QoRTs/v1.3.6/QoRTs.jar'

        # assemble parameters
        outDir = pars['pipeline'] + '/10-qc/' + pars['sampleReplicate']
        subprocess.check_call('mkdir -p ' + outDir,shell=True)

        sortedBam = outDir + '/' + pars['sampleReplicate'] + '.bam'
        pars['out'].write('samtools sort -n -@ ' + pars['threads'] + ' ' + pars['bamFile'] + ' -o ' + sortedBam + ' \n')

        # specifty endedness and strandedness
        params = '--keepMultiMapped '  # for hisat compatibility
        if pars['end'] == 'single':
            params += '--singleEnded '
        if pars['stranded']:
            params += '--stranded '

        # run qorts here
        pars['out'].write('java -Xmx12G -jar ' + qorts + ' QC ' + params + ' --skipFunctions overlapMatch,NVC,GCDistribution,readLengthDistro,QualityScoreDistribution,writeClippedNVC,CigarOpDistribution,cigarLocusCounts,chromCounts --generatePlots ' + sortedBam + ' ' + pars['gtf'] + ' ' + outDir+ '\n')

        # clean up name sorted bam
        pars['out'].write('echo rm -f ' + sortedBam + '*'+ '\n')
        pars['out'].write('rm -f ' + sortedBam + '*'+ '\n')

    # use when this function has already been called
    elif pars['flavor'] == 'picard':

        outDir = pars['pipeline'] + '/06-qc/' + pars['sampleReplicate'] + '/'
        outFile = outDir + pars['flavor'] + '.txt'
        call = 'time java -Xmx28G -jar /sw/med/centos7/picard/2.4.1/picard.jar CollectRnaSeqMetrics I=' + pars['bam'] + ' O=' + outFile + ' REF_FLAT=' + pars['gtf'] + ' STRAND_SPECIFICITY=NONE'

        # call yo program
        subprocess.check_call('mkdir -p ' + outDir,shell=True)
        pars['out'].write(call + '\n')

    mu.logTime(pars['out'],'FINISH QC')
