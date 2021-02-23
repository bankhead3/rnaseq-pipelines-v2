#!/usr/bin/python
# download bam files from external source

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess
import os

# Download
def download(pars):
    mu.logTime(pars['out'],'START DOWNLOAD')

    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/00-downloads',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/00-downloads/' + pars['sampleReplicate'],shell=True)
    outDir = pars['pipeline'] + '/00-downloads/' + pars['sampleReplicate']

    if pars['flavor'] == 'gdc':

        # download bam file
        mu.writeCmd(pars['out'], 'echo ' + pars['sampleReplicate'])
        mu.writeCmd(pars['out'], 'cd ' + outDir)
#        mu.writeCmd(pars['out'], 'time curl -O -J -H "X-Auth-Token: ' + pars['token'] + '" https://api.gdc.cancer.gov/data/' + pars['fileID'])
        mu.writeCmd(pars['out'], 'time curl --remote-name --remote-header-name  --header "X-Auth-Token: ' + pars['token'] + '" https://api.gdc.cancer.gov/data/' + pars['fileID'])
        pars['bamFile'] = outDir + '/' + pars['fileName']
        mu.writeCmd(pars['out'], 'cd ../../.. \n')

        # get size and md5sum
        mu.writeCmd(pars['out'], "du -chs " + pars['bamFile'] + " | grep -v total | awk '{ print $1 }' > " + outDir + "/bam-size.txt")
        mu.writeCmd(pars['out'], "md5sum " + pars['bamFile'] + " | grep -v total | awk '{ print $1 }' > " + outDir + "/bam-md5sum.txt")

    if pars['flavor'] == 'skip' or pars['flavor'] == 'passthru':

        pars['bamFile'] = outDir + '/' + pars['fileName']

    mu.logTime(pars['out'],'FINISH DOWNLOAD')
