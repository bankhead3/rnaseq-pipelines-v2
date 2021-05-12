#!/usr/bin/python
# add is de using 3 different criteria

import sys
sys.path.append('src')
import myUtils as mu

inFile1 = 'intermediate/11.txt'
outFile1 = 'intermediate/12.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['sample','gene'])

criteria = dict()
# criteria['FC1.1'] = { 'FC':1.1, 'qValue':0.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
# criteria['FC1.25'] = { 'FC':1.25, 'qValue':0.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC1.05_q'] = { 'FC':1.05, 'qValue':0.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC1.1_q'] = { 'FC':1.1, 'qValue':0.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC1.25_q'] = { 'FC':1.25, 'qValue':0.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC1.5_q'] = { 'FC':1.5, 'qValue':0.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC1.75_q'] = { 'FC':1.75, 'qValue':0.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC2_q'] = { 'FC':2, 'qValue':0.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 

criteria['FC1.05'] = { 'FC':1.05, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC1.1'] = { 'FC':1.1, 'meanTPM':0.5,'isProteinCoding':'Y' } 
criteria['FC1.25'] = { 'FC':1.25, 'meanTPM':0.5,'isProteinCoding':'Y' } 
criteria['FC1.5'] = { 'FC':1.5, 'meanTPM':0.5,'isProteinCoding':'Y' } 
criteria['FC1.75'] = { 'FC':1.75, 'meanTPM':0.5,'isProteinCoding':'Y' } 
criteria['FC2'] = { 'FC':2, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC3'] = { 'FC':3, 'meanTPM':0.5, 'isProteinCoding':'Y' } 
criteria['FC4'] = { 'FC':4, 'meanTPM':0.5, 'isProteinCoding':'Y' } 

#criteria['log2FC1.5'] = { 'log2FC':1.5, 'qValue':0.05, 'meanTPM':0.5,'isProteinCoding':'Y' } 
#criteria['log2FC2'] = { 'log2FC':2, 'qValue':0.05, 'meanTPM':0.5,'isProteinCoding':'Y' } 
criteriaList = sorted(criteria.keys())

# write yo file
with open(outFile1,'w') as out1:

    # write yo header
    header = ['isDE?','criteria'] + header1
    out1.write('\t'.join(header) + '\n')

    for criterion in criteriaList:
        criteriaDetails = criteria[criterion]
        criteriaFields = sorted(criteriaDetails.keys())
        
        for key in keys1:
            record = records1[key]
#            print record
            
            # determine if de and update record
            # fold change
            isDE = 'Y'
            if 'FC' in criteriaFields:
                if record['FC'] == 'NA' or abs(float(record['FC'])) < criteriaDetails['FC']:
                    isDE = 'N'
            elif record['log2FC'] == 'NA' or abs(float(record['log2FC'])) < criteriaDetails['log2FC']:
                    isDE = 'N'                
            # qvalue
            if 'qValue' in criteriaFields and (record['qValue'] == 'NA' or float(record['qValue']) > criteriaDetails['qValue']):
                isDE = 'N'

            # minMean
            if 'meanTPM' in criteriaFields and float(record['meanTPM']) < criteria[criterion]['meanTPM']:
                isDE = 'N'

            # minMean
            if 'isProteinCoding' in criteriaFields and record['isProteinCoding'] != criteria[criterion]['isProteinCoding']: 
                isDE = 'N'
                     
            record['criteria'] = criterion
            record['isDE?'] = isDE

#            print isDE
#            raise

            # assemble and write line out
            lineOut = []
            for field in header:
                lineOut.append(record[field])
            out1.write('\t'.join(lineOut) + '\n')
            
