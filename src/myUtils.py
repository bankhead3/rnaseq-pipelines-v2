#!/usr/bin/python

import re

def readRecords(fileName,uniqFields,header=None,maxRecords=None,sep='\t'):
    records = dict()
    orderedKeys = []
    count = 0
    
    # read yo file
    with open(fileName,'r') as in1:
        if header == None:
            header = in1.readline().strip().split(sep)

        # check that all uniqFields are in header
        for field in uniqFields:
            assert field in header, 'CANT FIND UNIQ FIELD'

        # iterate through file
        for line in in1:
            count += 1 

            # only remove the last character if there is no new line
            if line[-1] == '\n':
                line = line[:-1]

            parse1 = line.split(sep)

            assert len(parse1) == len(header), 'LINE HAS DIFFERENT NUMBER OF FIELDS THAN HEADER'
            record = dict(zip(header,parse1))

            # create key
            myKeyList = []
            for field in uniqFields:
                myKeyList.append(record[field])
            myKey = '!'.join(myKeyList)
            assert myKey not in records, 'KEY NOT UNIQUE!! ' + myKey 

            records[myKey] = record
            orderedKeys.append(myKey)

            if maxRecords and count >= maxRecords:
                break
            
    return (records,header,orderedKeys)

# logTime time
def logTime(out,label):
    out.write('echo ' + label + ' $(date +%s)' + ' \n')

# write command and echo it time
def writeCmd(out,cmd):
    out.write('echo "' + cmd + '" \n')
    out.write(cmd + ' \n')

# parses an attribute field from a gtf
def parseAttribute(attribute):
    myDict = dict()

    # split your attributes
    parse1 = attribute.split(';')
    parse1 = [field for field in parse1 if field != '']  # hopefully deals with trailing semicolon issue

    # split yo fields
    for field in parse1:
        # parse yo field
        parse2 = field.strip()

        # exceptions 
        if parse2 == 'level 2':
            continue

        parse3 = re.findall('(.*?)[ ]["]*(.*)',parse2)
        
        # assigne property value
        assert len(parse3[0]) == 2, 'CANT PARSE PROPERTY!'
        property = parse3[0][0]
        value = parse3[0][1]
        value = value.replace('"','')
        
        # load into dictionary
        myDict[property] = value

    return myDict
