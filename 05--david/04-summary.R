# 20180705 arb
# commonly significant gene sets

options(stringsAsFactors=F)
source('../utils/myUtils.R')

library(dplyr)

inFile1 = 'intermediate/03.txt'
outFile1 = 'intermediate/04.txt'

data1 = read.delim(inFile1)

data1a = data1[data1$isSig == 'Y',]

data1b = select(data1a,label,source,geneset)

data1c = myMerge(data1b,c('source','geneset'))
data1c$frequency = unlist(lapply(strsplit(data1c$label,','),length))
data1c = data1c[order(data1c$frequency,decreasing=T),]

write.table(data1c,outFile1,quote=F,row.names=F,sep="\t")
