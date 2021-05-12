#!/usr/bin/python
# update de file

import sys
sys.path.append('src')
import myUtils as mu

inFile1 = 'intermediate/06.txt'
inFile2 = 'input/geneAnnotation.txt'
outFile1 = 'intermediate/07.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['cellline','tx','id'])
(records2,header2,keys2) = mu.readRecords(inFile2,['gene','transcript'])

gene2entrez = dict(list(set([(records2[key]['gene'],records2[key]['entrez']) for key in keys2])))

# create lookup dictionary
gene2keys = dict()
for key in keys2:
    gene = records2[key]['gene']

    # create entry or add to it
    if gene not in gene2keys:
        gene2keys[gene] = [key]
    else:
        gene2keys[gene].append(key)

genes = gene2keys.keys()
gene2pc = dict()
for gene in genes:
    keys2a = [key for key in gene2keys[gene]]
    pcs = list(set([records2[key]['isProteinCoding?'] for key in keys2a]))

    # case where we have both and need to ignore the 'N's
    if len(pcs) == 2:
        gene2pc[gene] = 'Y'
    elif len(pcs) == 1:
        gene2pc[gene] = pcs[0]        
    else:
        raise 'DO NOT UNDERSTAND!'

# write yo file
with open(outFile1,'w') as out1:

    # write yo header
    header = ['sample','cellline','tx','gene','entrez','isProteinCoding','FC','log2FC','shrunkLFC','pValue','qValue','dir']
    out1.write('\t'.join(header) + '\n')
    
    for key in keys1:
        record = records1[key]

        # add missing fields
        cellline,tx = record['cellline'],record['tx']
        sample = cellline + '_' + tx
        record['sample'] = sample
        record['cellline'] = cellline
        gene = record['id']
        record['entrez'] = gene2entrez[gene]
        record['isProteinCoding'] = gene2pc[gene]
        record['gene'] = gene
        record['log2FC'] = record['log2FoldChange']
        record['pValue'],record['qValue'] = record['pvalue'],record['padj']

        # calculate fc
        log2FC = record['log2FC']
        if log2FC == 'NA':
            record['FC'] = 'NA'
            record['dir'] = 'NA'
        else:
            log2FC = float(log2FC)
            fc = pow(2,log2FC) if log2FC >= 0 else -pow(2,abs(log2FC))
            record['FC'] = str(fc)
            record['dir'] = 'up' if fc > 0 else 'down'

        # assemble and write line out
        lineOut = []
        for field in header:
            lineOut.append(record[field])
        out1.write('\t'.join(lineOut) + '\n')
