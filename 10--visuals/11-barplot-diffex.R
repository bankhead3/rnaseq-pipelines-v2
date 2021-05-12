# 20170301 arb
# construct barplot showing differential expression per cell line

library(reshape)
library(ggplot2)

options(stringsAsFactors = F)

inFile = 'input/diffex.txt'

outFilePrefix = 'figs/11-de-barplot'

data1 = read.delim(inFile) 

data1a = data1[data1$isDE. == 'Y',]

# summarize
sig = table(data1a$sample,data1a$dir)
sig = as.data.frame.matrix(sig)
sig = data.frame(experiment=rownames(sig),sig)

plotData = melt(sig,id='experiment')
colnames(plotData)[2:3] = c('direction','value')
plotData$direction = factor(plotData$direction,levels=c('up','down'))

theme_set(theme_bw(base_size=18))
plotData$value = as.numeric(plotData$value)

ylabel = '# of DE Genes'

plotData$label = sub('.*SF','SF',plotData$experiment)

title = 'Differential Expression'
p = ggplot(plotData,aes(label,value, fill = direction)) + 
    geom_bar(stat='identity',position = 'dodge') +
    geom_text(aes(label=value),position=position_dodge(width=1),vjust=-0.25,size=2) + 
    theme(axis.text = element_text(color = 'black')) + 
#    theme(axis.text.x = element_text(color = 'black',angle=45,hjust = 1, vjust = 1,size=6)) + 
    theme(axis.text.x = element_text(color = 'black',hjust = 0.5, vjust = 1,size=12)) + 
    theme(axis.title = element_text(color = 'black')) + 
    theme(plot.title = element_text(hjust=1,color = 'black')) + 
    labs(x='treatment',y=ylabel,title=title) + 
    theme(plot.title = element_text(size=16,hjust=0.5)) +
    scale_fill_manual(values = c('red','blue'))

filename = paste0(outFilePrefix,'.png')
ggsave(filename,units='in',height=5,width=7,dpi=150)
print(filename)

