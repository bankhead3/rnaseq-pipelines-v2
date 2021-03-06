#!/usr/bin/python
# this script sets up the directory structure, prefix.sh, and execute.sh files
# customized for downloading lots of data from gdc data portal

import sys
sys.path.append('../utils')

import myUtils as mu

import subprocess
import os
import re

inFile1 = 'intermediate/sample-sheet.txt'
pipeline = 'pipeline2'
account = 'cdsc_project1'
jobName = pipeline

# combos 62 X 8 
# combos 124 X 4
nodes=32   # liberal
#nodes=20   # conservative
numThreads=str(8)
shHeader = 'input/slurm-header-' + numThreads + '-array.sh'

(records1,header,keys1) = mu.readRecords(inFile1,['fileID'])
keys1a = [key for key in keys1 if records1[key]['disease'] in ['BLCA']]
#keys1a = keys1a[:30]  # testing 
#keys1a = keys1a[:5]  # testing 
keys1a = keys1a[:1]  # testing 
subprocess.check_call('mkdir -p ' + pipeline,shell=True)
subprocess.check_call('mkdir -p ' + '/'.join([pipeline,'logs']),shell=True)
subprocess.check_call('mkdir -p ' + '/'.join([pipeline,'scripts']),shell=True)

# create sh prefix and execution script
sh = '/'.join([pipeline,'prefix.sh']) 
execute = pipeline + '/execute.sh'

# write sh prefix
with open(sh,'w') as out1, open(shHeader,'r') as in1:
    for line in in1:
        # copy prefix header except for array spec
        if '--array' in line:
            altLine = '#SBATCH --array=1-' + str(len(keys1a)) + '%' + str(nodes) + '\n'
            out1.write(altLine)
        elif '--account' in line:
            altLine = '#SBATCH --account=' + account + '\n'
            out1.write(altLine)
        elif '--job-name' in line:
            altLine = '#SBATCH --job-name=' + jobName + '\n'
            out1.write(altLine)
        elif '--output' in line:
            altLine = '#SBATCH --output="' + pipeline + '/logs/slurm-%A-%a.txt"' + '\n'
            out1.write(altLine)
        else:
            out1.write(line)
    out1.write(execute + ' $SLURM_ARRAY_TASK_ID' + '\n')

# write execute script
with open(execute,'w') as out1:
    out1.write('#!/bin/bash' + '\n')
    out1.write('echo -e "SLURM_ARRAY_TASK_ID\t$1"' + '\n')

    # assign variables based on array id
#    out1.write('sampleReplicate=$(head -n$((1+$1)) ' + inFile1 + '| tail -n1 | cut -f4)' + '\n')
    out1.write('sampleScript=$(ls -1 ' + pipeline + '/scripts/*.sh | head -n$(($1)) | tail -n1) ' + '\n')

    # print sampleReplicate
    out1.write('echo -e "sampleScript\t$sampleScript"' + '\n')
    out1.write('echo' + '\n')

    mu.logTime(out1,'ALL START')

    # set up custom script 
    out1.write('cmd=$sampleScript ' + '\n')
    out1.write('echo $cmd; eval $cmd' + '\n')

    mu.logTime(out1,'ALL FINISHED!')
    out1.write('echo' + '\n')

# update script permissions
cmd = 'chmod 755 ' + execute
subprocess.check_call(cmd,shell=True) 
