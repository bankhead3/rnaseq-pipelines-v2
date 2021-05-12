# 20180622 arb
# special script because this is not something I can do easily in python without turning to python data frames

options(stringsAsFactors=F)

inFile1 = 'intermediate/09.txt'
outFile1 = 'intermediate/11.txt'

data1 = read.delim(inFile1)
data1 = data1[order(data1$sample,data1$log2FC,decreasing=T),]

write.table(data1,outFile1,quote=F,row.names=F,sep="\t")