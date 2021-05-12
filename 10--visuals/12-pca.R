# generates scatter plots comparing replicates

library(ggplot2)
library(reshape)
library(dplyr)

options(stringsAsFactors=F)
inFile1 = 'input/geneExpression.txt'
num = '12'
outFile1 = paste0('figs/',num,'-pca1.png')
outFile2 = paste0('figs/',num,'-pca2.png')

data1 = read.delim(inFile1)
data1 = select(data1,sampleReplicate,sample,cellline,tx,replicate,gene,log2value)
data1$sampleReplicate = sub('.*?_','',data1$sampleReplicate)

metadata = unique(select(data1,sampleReplicate,cellline,tx,replicate,sample))

# iterate through samples
data1a = data1
data1b = cast(data1a, gene ~ sampleReplicate, value = 'log2value')
data1c = data1b
rownames(data1c) = data1b$gene

data1c = data1c[,-1]
data1c = data.frame(data1c)

result1 = prcomp(data1c,center=T,scale=T)

plotData = data.frame(result1$rotation[,1:2])
plotData = data.frame(sampleReplicate = gsub('[.]','-',rownames(plotData)), plotData)
plotData = merge(plotData,metadata,value='sampleReplicate')
plotData$cellline = factor(plotData$cellline)
plotData$tx = factor(plotData$tx)
plotData$replicate = factor(plotData$replicate,level=c(1,2,3))
plotData$sample = factor(plotData$sample)

# build elbow plot
png(outFile1,units='px',height=480,width=480,pointsize=12)
plot(result1,main='Principal Component Variance',type='l')
dev.off()
print(outFile1)

# construct pca plot
p1 = ggplot(plotData,aes(PC1,PC2)) +
     geom_point(aes(color = sample,shape=replicate),size=3) +
     scale_colour_brewer(palette = "Paired")
ggsave(outFile2,device='png',width=7.5,height=5,units='in',dpi=200)
print(outFile2)


