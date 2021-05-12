# 20161006 arb
# generate a dendrogram for every pipeline comparing replicates

library(reshape)
#library(ggdendro)
library(ggplot2)

options(stringsAsFactors=F)
inFile1 = 'input/geneExpression.txt'
outFile1 = 'figs/06-dendro-replicates.png'

load = T
if(load) { data1 = read.delim(inFile1) } 

if(1) { 
  data2 = data.frame(sampleReplicate=data1$sampleReplicate,id=data1$gene,log2value=data1$log2value)
  data3 = cast(data2,id ~ sampleReplicate,value='log2value')
  idx = which(is.na(data3$id))
  if(length(idx) != 0) { data3 = data3[-idx,]; }
} 

rownames(data3) = data3[,1]
data4 = data3[,-1]
myMax = apply(data4,1,max)
data5 = data.frame(data4[myMax != 0,])

# cluster here
dissimilarity = 1 - abs(cor(data5))
distance = as.dist(dissimilarity)
hc = hclust(distance)

png(outFile1,width=750,height=750,pointsize=18)  
plot(hc,xlab='',ylab='dis-similarity')
dev.off()
print(outFile1)