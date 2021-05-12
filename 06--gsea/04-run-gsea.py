#!/usr/bin/python
# read in catalog and execute gsea runs linearly 
# wait for gsea to finish before running another

import sys
sys.path.append('../utils')
import myUtils as mu

import subprocess

inFile1 = 'input/catalog.txt'

numThreads=str(4)
perms = 10000  # should be 10000
# perms = 1000  # should be 10000
#perms = 100  # should be 10000

(records1,header1,keys1) = mu.readRecords(inFile1,['label','pipeline'])

pipeline2gmt = {'pipeline1a':'input/c2.cp.kegg.v7.0.symbols.gmt', 'pipeline1b':'input/c5.bp.v7.0.symbols.gmt', 'pipeline1c':'input/h.all.v7.0.symbols.gmt', 'pipeline1d':'input/c3.tft.v7.0.symbols.gmt'}
pipeline2genesets = {'pipeline1a':'kegg','pipeline1b':'bp','pipeline1c':'hallmark','pipeline1d':'tft'}

#keys1 = [keys1[0]]
#keys1 = [keys1[0],keys1[2]]

for myKey in keys1:
    record = records1[myKey]
    label,pipeline,annotation = record['label'],record['pipeline'],record['annotation']

    pbsHeader = 'input/header-' + numThreads + '.pbs'    

    subprocess.check_call('mkdir -p ' + pipeline,shell=True)
    subprocess.check_call('mkdir -p ' + '/'.join([pipeline,'logs']),shell=True)

    # create script
    script = '/'.join([pipeline,label + '.sh']) 

    with open(script,'w') as out1:
        # write body of script
        out1.write('#/bin/bash\n')
        out1.write('\n')

        out1.write('gseaJar=~/software/gsea/gsea2-2.2.3.jar' + '\n')
        out1.write('gseaTool=xtools.gsea.GseaPreranked' + '\n')
        out1.write('gmts=' + pipeline2gmt[pipeline] + '\n')
        out1.write('plotTop=100' + '\n')
        out1.write('perms=' + str(perms) + '\n')
        out1.write('mode=weighted' + '\n')
        out1.write('label=' + '.'.join([str(perms),label,pipeline2genesets[pipeline]]) + '\n')
        out1.write('annotation=' + 'intermediate/' + annotation + '\n')
        out1.write('rnk=' + 'intermediate/' + label + '.rnk' + '\n')
        out1.write('\n')
        out1.write('cmd="java -Xmx8000m -cp $gseaJar $gseaTool -gmx $gmts -nperm $perms -scoring_scheme $mode -collapse false -norm meandiv -mode Max_probe -rnk $rnk -chip $annotation -rpt_label $label -include_only_symbols true -make_sets true -plot_top_x $plotTop -rnd_seed timestamp -set_max 500 -set_min 15 -out intermediate -gui false"' + '\n')
        out1.write('\n')
        out1.write('echo $cmd; eval $cmd')

        out1.write('\n')

    # execute script
    cmd = script
    print cmd
    subprocess.check_call(cmd,shell=True)


        
