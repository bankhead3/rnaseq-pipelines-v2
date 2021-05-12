# 20190207 arb
# construct a volcano plot
# ymmv

options(stringsAsFactors=F)

library(ggplot2)
library(ggrepel)

inFile1 = 'input/rnaseq.txt'
num = '02'
outFile1 = paste0('figs/',num,'-volcano.png')

data1 = read.delim(inFile1) 

data1a = data1[!is.na(data1$FC) & !is.na(data1$qValue),]
data1a$isDE. = factor(data1a$isDE., levels = c('Y','N'))

# adjust zeros to be next smallest #
if(min(data1a$qValue) == 0) { 
  nextSmallest = sort(unique(data1a$qValue))[2]
  data1a$qValue[data1a$qValue == 0] = nextSmallest
}

plotData = data1a
plotData = data1a[order(data1a$qValue),]
plotData$qval2 = -log10(plotData$qValue)

max_y = max(-log10(plotData$qValue))*1.01

theme_set(theme_bw(base_size=18))
ggplot(plotData,aes(log2FC,qval2, color = isDE.)) +
  geom_point(shape = 1) + 
  theme(text = element_text(color = 'black',face = 'bold')) + 
  theme(axis.text = element_text(color = 'black',face = 'bold')) + 
  labs(x = 'log2 FC', y = '-log10(q-value)') + 
  ylim(0,max_y) + 
  guides(color = F) + 
  scale_color_manual(values = c('red','grey')) + 
  geom_text_repel(data = plotData[1:20,], aes(label = gene),segment.color = 'black',color = 'black') +  #filter(plotData, qValue < 0.01), aes(label=gene)) 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())

filename = outFile1
ggsave(filename,height=5,width=5,units='in',dpi=200)
print(filename)
