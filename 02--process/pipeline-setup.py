#!/usr/bin/python
# this script sets up the directory structure, prefix.sh, and execute.sh files

import sys
sys.path.append('../utils')

import myUtils as mu

import subprocess
import os
import re

inFile1 = 'intermediate/sample-replicate-catalog.txt'
pipeline = 'pipeline1'
account = 'neamati1'
jobName = pipeline.replace('ipeline','l')

# combos 62 X 8 
# combos 124 X 4
nodes=25
numThreads=str(8)
shHeader = 'input/slurm-header-' + numThreads + '-array.sh'

(na,na,keys1) = mu.readRecords(inFile1,['sampleReplicate'])
# keys1 = keys1[:2]  # testing purposes

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
            altLine = '#SBATCH --array=1-' + str(len(keys1)) + '%' + str(nodes) + '\n'
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
    out1.write('sampleReplicate=$(head -n$((1+$1)) ' + inFile1 + '| tail -n1 | cut -f1)' + '\n')

    # print sampleReplicate
    out1.write('echo -e "sampleReplicate\t$sampleReplicate"' + '\n')
    out1.write('echo' + '\n')

    mu.logTime(out1,'ALL START')

    # set up custom script 
    out1.write('cmd="./' + pipeline + '/scripts/$sampleReplicate.sh"' + '\n')
    out1.write('echo $cmd; eval $cmd' + '\n')

    mu.logTime(out1,'ALL FINISHED!')
    out1.write('echo' + '\n')

# update script permissions
cmd = 'chmod 755 ' + execute
subprocess.check_call(cmd,shell=True) 
