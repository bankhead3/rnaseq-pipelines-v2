#!/usr/bin/python
# unknown flavors will be ignored

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# align
#def align(flavor,out,records,sampleLabel,pipeline,fastqFiles,numThreads,alignerIndexDir):
def align(pars):
    mu.logTime(pars['out'],'START ALIGN')

    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/04-aligned',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'],shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/04-aligned/totalFragments',shell=True)
    pars['out'].write('echo align \n')

    pars['outDir'] = pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '/'
    pars['bamFile'] = pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '.bam'

    # *** salmon-bias ***
    if pars['flavor'] == 'salmon-bias':
        pars['fqgz1'] = pars['fagzFiles'][0]
        pars['fqgz2'] = pars['fagzFiles'][1]

        mu.writeCmd(pars['out'], 'salmon quant --libType A -p ' + pars['threads'] + ' -i ' + pars['alignerIndexDir'] + ' -o ' + pars['outDir'] + ' --posBias --seqBias --gcBias -1 ' + pars['fqgz1'] + ' -2 ' + pars['fqgz2'])
        mu.writeCmd(pars['out'], ' ')

    # *** salmon ***
    elif pars['flavor'] == 'salmon':
        pars['fqgz1'] = pars['fagzFiles'][0]
        pars['fqgz2'] = pars['fagzFiles'][1]

        mu.writeCmd(pars['out'], 'salmon quant --libType A -p ' + pars['threads'] + ' -i ' + pars['alignerIndexDir'] + ' -o ' + pars['outDir'] + ' -1 ' + pars['fqgz1'] + ' -2 ' + pars['fqgz2'])
        mu.writeCmd(pars['out'], ' ')

    # *** star ***
    elif pars['flavor'] == 'star':
        pars['out'].write('STAR  --runThreadN ' + pars['threads'] + ' --genomeDir ' + pars['alignerIndexDir'] + ' --readFilesIn ' + ' '.join(pars['fagzFiles']) + ' --outFileNamePrefix ' + pars['outDir'] + ' --outSAMtype BAM Unsorted  --outFilterType BySJout  --outFilterMultimapNmax 20  --outFilterMismatchNmax 999  --outFilterMismatchNoverLmax 0.04  --alignIntronMin 20  --alignIntronMax 1000000 --alignMatesGapMax 1000000  --alignSJoverhangMin 8  --alignSJDBoverhangMin 1 --outSAMstrandField intronMotif --readFilesCommand zcat --outSAMunmapped Within ' + '\n')

        pars['out'].write('samtools sort -@ ' + pars['threads'] + ' ' + pars['outDir'] + 'Aligned.out.bam -o ' + pars['bamFile'] + ' \n')
        pars['out'].write('samtools index ' + pars['bamFile'] + ' \n')
        pars['out'].write('rm -f ' + pars['outDir'] + 'Aligned.out.bam' + ' \n')
        pars['out'].write('\n')

    # *** hisat2 ***
    elif 'hisat2' in pars['flavor']:
        pars['fqgz1'] = pars['fagzFiles'][0]
        pars['fqgz2'] = pars['fagzFiles'][1]
        sam = pars['outDir'] + 'tmp.sam'
        bam1 = pars['outDir'] + 'tmp.bam'
        summary = pars['outDir'] + 'summary.log'
        dta = '--dta-cufflinks' if 'cufflinks' in pars['flavor'] else '--dta'
        strandCommand = '' if pars['stranded'] == False else '--rna-strandness RF'

        # run hisat2
        pars['out'].write('hisat2 -p ' + pars['threads'] + ' ' + dta + ' ' + strandCommand + ' --summary-file ' + summary + ' -x ' + pars['alignerIndexDir'] + ' -1 ' + pars['fqgz1'] + ' -2 ' + pars['fqgz2'] + ' -S ' + sam + '\n')

        # polish up the bam
        pars['out'].write('samtools sort -O BAM -@ ' + pars['threads'] + ' ' + sam + ' -o ' + pars['bamFile'] + ' \n')
        pars['out'].write('samtools index ' + pars['bamFile'] + ' \n')

        # delete the unnecessary artifacts (the crap)
        pars['out'].write('rm -f ' + sam + ' ' + ' \n')
        pars['out'].write('\n')

    elif pars['flavor'] == 'rsem':
        # for when we are workign with files directly from fastq 
        pars['fqgz1'] = pars['fagzFiles'][0]
        pars['fqgz2'] = pars['fagzFiles'][1]

        # rsem call here...
#        pars['out'].write('rsem-calculate-expression -p ' + pars['threads'] + ' --paired-end --bowtie2 --bowtie2-path /sw/med/centos7/bowtie2/2.3.4.3/ --estimate-rspd --append-names ' + pars['fqgz1'] + ' ' + pars['fqgz2'] + ' ' + pars['alignerIndexDir'] + ' ' + pars['outDir'] + pars['sampleReplicate'] + ' \n')
#        pars['out'].write('rsem-calculate-expression -p ' + pars['threads'] + ' --paired-end --star --estimate-rspd --append-names ' + pars['fqgz1'] + ' ' + pars['fqgz2'] + ' ' + pars['alignerIndexDir'] + ' ' + pars['outDir'] + pars['sampleReplicate'] + ' \n')
#        pars['out'].write('rsem-calculate-expression -p ' + pars['threads'] + ' --paired-end --star --star-gzipped-read-file --estimate-rspd --append-names ' + pars['fqgz1'] + ' ' + pars['fqgz2'] + ' ' + pars['alignerIndexDir'] + ' ' + pars['outDir'] + pars['sampleReplicate'] + ' \n')
        pars['out'].write('rsem-calculate-expression -p ' + pars['threads'] + ' --paired-end --bowtie2 --estimate-rspd --append-names ' + pars['fqgz1'] + ' ' + pars['fqgz2'] + ' ' + pars['alignerIndexDir'] + ' ' + pars['outDir'] + pars['sampleReplicate'] + ' \n')
        pars['out'].write('\n')

    elif pars['flavor'] == 'kallisto':
        # for when we are workign with files directly from fastq 
        pars['fqgz1'] = pars['fagzFiles'][0]
        pars['fqgz2'] = pars['fagzFiles'][1]

        # to reduce processing time and save space bams will not be generated
        pars['out'].write('kallisto quant -t ' + pars['threads'] + ' -i ' + pars['alignerIndexDir'] + ' -o ' + pars['outDir'] + ' ' + pars['fqgz1'] + ' ' + pars['fqgz2'] + '\n')
        pars['out'].write('\n')

    elif pars['flavor'] == 'skip':
        mu.logTime(pars['out'],'FINISH ALIGN')
        return

    """
    # need to be tested - refactoring
    elif pars['flavor'] == 'tophat':
        # coverage search is only recommended for <45bp reads or <10m reads per sample
        pars['out'].write('# tophat -p ' + pars['threads'] + ' --output-dir ' + pars['outDir'] + ' --no-coverage-search ' + pars['alignerIndexDir'] + ' ' + ' '.join(pars['fagzFiles']) + '\n')
        pars['out'].write('tophat -p ' + pars['threads'] + ' --output-dir ' + pars['outDir'] + ' --no-coverage-search ' + pars['alignerIndexDir'] + ' ' + ' '.join(pars['fagzFiles']) + '\n')
        pars['out'].write('cp ' + pars['outDir'] + 'accepted_hits.bam ' + pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '.bam' + '\n')
        pars['out'].write('samtools index ' + pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '.bam' + '\n')
        pars['out'].write('\n')
    elif pars['flavor'] == 'kallisto-pseudo':
        # run kallisto specifically to generate pseudo bams
        pars['out'].write('kallisto quant --pseudobam -i ' + pars['alignerIndexDir'] + ' -o ' + pars['outDir'] + ' ' + ' '.join(pars['fagzFiles']) + ' > ' + pars['outDir'] + 'pseudo.sam' + '\n')

        # use sam tools to compress, sort, and index
        pars['out'].write('samtools view -@ ' + pars['threads'] + ' -bS ' + pars['outDir'] + 'pseudo.sam > ' + pars['outDir'] + 'pseudo.bam \n')
        pars['out'].write('samtools sort -@ ' + pars['threads'] + ' ' + pars['outDir'] + 'pseudo.bam ' + pars['outDir'] + 'pseudo-sorted \n')
        pars['out'].write('samtools index ' + pars['outDir'] + 'pseudo-sorted.bam \n')
        
        # clean up un necessary artifacts
        pars['out'].write('rm ' + pars['outDir'] + 'pseudo.sam \n') 
        pars['out'].write('rm ' + pars['outDir'] + 'pseudo.bam \n') 
        pars['out'].write('mv ' + pars['outDir'] + 'pseudo-sorted.bam ' + pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '.bam \n')
        pars['out'].write('mv ' + pars['outDir'] + 'pseudo-sorted.bam.bai ' + pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '.bam.bai \n')

        pars['out'].write('\n')
    """
    # count total aligned fragments
    if pars['flavor'] == 'star' or pars['flavor'] == 'tophat' or 'hisat2' in pars['flavor']:
        countFile = pars['pipeline'] + '/04-aligned/totalFragments/' + pars['sampleReplicate'] + '.txt'
        bam = pars['pipeline'] + '/04-aligned/' + pars['sampleReplicate'] + '.bam'
        tmp1 = pars['pipeline'] + '/04-aligned/totalFragments/' + pars['sampleReplicate'] + '.tmp1.txt'
        tmp2 = pars['pipeline'] + '/04-aligned/totalFragments/' + pars['sampleReplicate'] + '.tmp2.txt'
        pars['out'].write('samtools view -F 4 ' + bam + ' | cut -f1 > ' + tmp1 + '\n')
        pars['out'].write('sort ' + tmp1 + ' | uniq > ' + tmp2 + '\n')
        pars['out'].write('wc -l ' + tmp2 + ' | sed "s/ .*//" > ' + countFile + '\n')
        pars['out'].write('rm -f ' + tmp1 + ' ' + tmp2 + '\n')

    mu.logTime(pars['out'],'FINISH ALIGN')
