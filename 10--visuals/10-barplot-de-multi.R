# 20170301 arb
# construct barplot showing differential expression per cell line

library(reshape)
library(ggplot2)
 
outFile1 = 'figs/10-barplot-de-multi.png'

load = T
if(load) {
  options(stringsAsFactors = F)
  inFile = 'input/diffexMultipleCriteria.txt'
  data1 = read.delim(inFile) 

  data1$criteria = factor(data1$criteria)
  data1$dir = factor(data1$dir,levels=c('up','down'))
}

data1a = data1[data1$isDE. == 'Y',]
sig = aggregate(data = data1a, gene ~ sample + criteria + dir, FUN = length)

sig = as.data.frame.matrix(sig)
plotData = sig
plotData$sample = factor(plotData$sample)
plotData$geneCount = plotData$gene
plotData$dir = factor(plotData$dir, levels = c('up','down'))

#title = paste0(cellline, ', ', method)

theme_set(theme_light(base_size = 18))
p = ggplot(plotData,aes(sample,geneCount, fill = dir)) + 
      geom_bar(stat='identity',position = 'dodge') +
      theme(axis.text.x = element_text(angle=45,vjust=1,hjust=1,size=12)) + 
      theme(title = element_text(size=14)) + 
      xlab('threshold') + 
      ylab('# of Differentially Expressed Genes') +
      theme(plot.title = element_text(size=16,hjust=0.5)) + 
      facet_grid(. ~ criteria) 
#      ggtitle(title)

filename = outFile1
ggsave(filename,units='in',height=5,width=8,dpi=200)
print(filename)
