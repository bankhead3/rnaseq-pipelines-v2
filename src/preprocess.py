#!/usr/bin/python

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# 02 preprocess
def preprocess(pars):
    mu.logTime(pars['out'],'START PREPROCESS')

    records = pars['records']
    files = sorted([records[key]['file'] for key in records.keys() if records[key]['sampleReplicate'] == pars['sampleReplicate']])
    pars['fastqFiles'] = []

    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads/fastq',shell=True)
    if pars['fastqc']:
        subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads/fastqc',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads/totalFragments',shell=True)

    pars['out'].write('echo preprocess \n')

    # no trimming no fastqc just set up symbolic link for next step
    if pars['flavor'] == 'passthru':
        uniqueNames = sorted(set(list([records[key]['uniqueName'] for key in records.keys() if records[key]['sampleReplicate'] == pars['sampleReplicate']])))

        # need to get pairs of files that are associated with a given coreSampleLabel
        for uniqueName in uniqueNames:

            myFiles = sorted([records[key]['file'] for key in records.keys() if records[key]['uniqueName'] == uniqueName])
            assert len(myFiles) <= 2, 'SHOULD ONLY BE NO MORE THAN 2 MYFILES ASSOCIATED...'

            # process first fastq file
            in1 = myFiles[0]
            fastqFile1 = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-R1.fastq.gz'
            pars['out'].write('ln -s ' + in1 + ' ' + fastqFile1 + '\n')

            # for paired end data we have two sets of fasteq reads per uniqueName
            if pars['end'] == 'paired':
                in2 = myFiles[1] if pars['end'] == 'paired' else none
                fastqFile2 = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-R2.fastq.gz'
                pars['out'].write('ln -s ' + in2 + ' ' + fastqFile2 + '\n')
            pars['out'].write('\n')

            # assign 
            pars['fagzFiles'] = [fastqFile1]
            if pars['end'] == 'paired':
                pars['fagzFiles'].append(fastqFile2)

            # count reads
            readCountFile = pars['pipeline'] + '/02-reads/totalFragments/' + uniqueName + '.txt'
            pars['out'].write("zcat " + myFiles[0] + " | wc -l | awk '{print $1/4}' > " + readCountFile + '\n')

    # no preprocessing or trimming - just convert to fastq files
    elif pars['flavor'] == 'none':
        uniqueNames = sorted(set(list([records[key]['uniqueName'] for key in records.keys() if records[key]['sampleReplicate'] == pars['sampleReplicate']])))

        # need to get pairs of files that are associated with a given coreSampleLabel
        for uniqueName in uniqueNames:

            myFiles = sorted([records[key]['file'] for key in records.keys() if records[key]['uniqueName'] == uniqueName])
            assert len(myFiles) <= 2, 'SHOULD ONLY BE NO MORE THAN 2 MYFILES ASSOCIATED...'

            # process first fastq file
            in1 = myFiles[0]
            fastqFile1 = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-R1.fastq'
            pars['out'].write('zcat ' + in1 + ' > ' + fastqFile1 + '\n')
            if pars['fastqc']:
                pars['out'].write('fastqc ' + fastqFile1 + ' --outdir=' + pars['pipeline'] + '/02-reads/fastqc/' + '\n')

            # for paired end data we have two sets of fasteq reads per uniqueName
            if pars['end'] == 'paired':
                in2 = myFiles[1] if pars['end'] == 'paired' else none
                fastqFile2 = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-R2.fastq'
                pars['out'].write('zcat ' + in2 + ' > ' + fastqFile2 + '\n')
                if pars['fastqc']:
                    pars['out'].write('fastqc ' + fastqFile2 + ' --outdir=' + pars['pipeline'] + '/02-reads/fastqc/' + '\n')

            pars['out'].write('\n')

            # count reads
            rawReadCountFile = pars['pipeline'] + '/02-reads/totalFragments/raw-' + uniqueName + '.txt'
            readCountFile = pars['pipeline'] + '/02-reads/totalFragments/' + uniqueName + '.txt'
            pars['out'].write("zcat " + myFiles[0] + " | wc -l | awk '{print $1/4}' > " + rawReadCountFile + '\n')
            pars['out'].write("wc -l " + fastqFile1 + "| awk '{print $1/4}' > " + readCountFile + '\n')

    elif pars['flavor'] == 'rrna-removal':

        uniqueNames = sorted(set(list([records[key]['uniqueName'] for key in records.keys() if records[key]['sampleReplicate'] == pars['sampleReplicate']])))

        # need to get pairs of files that are associated with a given coreSampleLabel
        for uniqueName in uniqueNames:

            myFiles = sorted([records[key]['file'] for key in records.keys() if records[key]['uniqueName'] == uniqueName])
            assert len(myFiles) <= 2, 'SHOULD ONLY BE NO MORE THAN 2 MYFILES ASSOCIATED...'

            # process first fastq file
            in1 = myFiles[0]
            fastqFile1_raw = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-raw-R1.fastq'

            pars['out'].write('zcat ' + in1 + ' > ' + fastqFile1_raw + '\n')

            # for paired end data we have two sets of fasteq reads per uniqueName
            if pars['end'] == 'paired':
                in2 = myFiles[1] if pars['end'] == 'paired' else none
                fastqFile2_raw = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-raw-R2.fastq'
                pars['out'].write('zcat ' + in2 + ' > ' + fastqFile2_raw + '\n')

            pars['out'].write('\n')

            # remove reads mapping to ribosomal rna
            # use start to align to align to rrna reference
            # what ever does not align goes to fastqFile
            fastqFile1 = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-R1.fastq'            
            fastqFile2 = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-R2.fastq'
            pars['out'].write('bbduk.sh in1=' + fastqFile1_raw + ' in2=' + fastqFile2_raw + ' out1=' + fastqFile1 + ' out2=' + fastqFile2 + ' ref=' + pars['rrnaReference'] + '\n')

            # fastqc
            if pars['fastqc']:
                pars['out'].write('fastqc ' + fastqFile1 + ' --outdir=' + pars['pipeline'] + '/02-reads/fastqc/' + '\n')
                if pars['end'] == 'paired':
                    pars['out'].write('fastqc ' + fastqFile2 + ' --outdir=' + pars['pipeline'] + '/02-reads/fastqc/' + '\n')

            # count reads
            rawReadCountFile = pars['pipeline'] + '/02-reads/totalFragments/raw-' + uniqueName + '.txt'
            readCountFile = pars['pipeline'] + '/02-reads/totalFragments/' + uniqueName + '.txt'
            pars['out'].write("wc -l " + fastqFile1_raw + "| awk '{print $1/4}' > " + rawReadCountFile + '\n')
            pars['out'].write("wc -l " + fastqFile1 + "| awk '{print $1/4}' > " + readCountFile + '\n')

        pass


    elif pars['flavor'] == 'skip':
        pass

    # dont understand
    else:
        print pars['flavor']
        raise 'DONT UNDERSTAND PREPROCESS FLAVOR!!'

    # get fastq file entries
    myKeys = sorted([key for key in records.keys() if records[key]['sampleReplicate'] == pars['sampleReplicate']])
    for myKey in myKeys:
        record = records[myKey]
        label = record['uniqueName'] + '-R' + record['read']
        fastqFile = pars['pipeline'] + '/02-reads/fastq/' + label + '.fastq'
        pars['fastqFiles'].append(fastqFile)


    """
    NEEDS TO BE REFACTORED USING DICTIONARY PARAMS AND SINGLE END SUPPORT

    elif pars['flavor'] == 'trimmomatic':
        uniqueNames = sorted(set(list([records[key]['uniqueName'] for key in records.keys() if records[key]['sample'] == sample and records[key]['replicate'] == replicate])))

        # need to get pairs of files that are associated with a given coreSampleLabel
        for uniqueName in uniqueNames:
            myFiles = sorted([records[key]['file'] for key in records.keys() if records[key]['uniqueName'] == uniqueName])
            assert len(myFiles) == 2, 'SHOULD ONLY BE 2 MYFILES ASSOCIATED...'
            in1 = myFiles[0]
            in2 = myFiles[1]
            label = uniqueName + '-' + sample + '-' + replicate

            out1=pars['pipeline'] + '/02-reads/fastq/' + label + '-R1.fastq'
            out2=pars['pipeline'] + '/02-reads/fastq/' + label + '-R1-U.fastq'
            out3=pars['pipeline'] + '/02-reads/fastq/' + label + '-R2.fastq'
            out4=pars['pipeline'] + '/02-reads/fastq/' + label + '-R2-U.fastq'
            fastqFiles += [out1,out3]
            
            # write to pbs file
            pars['out'].write('java -jar /sw/lsa/centos7/trimmomatic/0.36/bin/trimmomatic-0.36.jar PE -threads ' + numThreads + ' ' + ' '.join([in1,in2,out1,out2,out3,out4]) + ' ILLUMINACLIP:/sw/lsa/centos7/trimmomatic/0.36/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 \n')
            pars['out'].write('fastqc ' + out1 + ' --outdir=' + pars['pipeline'] + '/02-reads/fastqc/' + '\n')
            pars['out'].write('fastqc ' + out3 + ' --outdir=' + pars['pipeline'] + '/02-reads/fastqc/' + '\n')
            pars['out'].write('\n')

            # get total read count
            rawReadCountFile = pars['pipeline'] + '/02-reads/totalFragments/raw-' + label + '.txt'
            readCountFile = pars['pipeline'] + '/02-reads/totalFragments/' + label + '.txt'
            pars['out'].write("zcat " + in1 + " | wc -l | awk '{print $1/4}' > " + rawReadCountFile + '\n')            
            pars['out'].write("wc -l " + out1 + "| awk '{print $1/4}' > " + readCountFile + '\n')
    """

    mu.logTime(pars['out'],'FINISH PREPROCESS')
