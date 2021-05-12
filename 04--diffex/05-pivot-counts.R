# 20180202 arb
# pivot counts from expression data

options(stringsAsFactors=F)

library(dplyr)
library(reshape)

inFile1 = 'intermediate/04.txt'
outFile1 = 'intermediate/05.txt'
load = T
if(load) { data1 = read.delim(inFile1) }

data1a = dplyr::select(data1,sampleReplicate,gene,count)
data1b = cast(data1a, gene ~ sampleReplicate, value='count')
write.table(data1b,outFile1,quote=F,sep="\t",row.names=F)

