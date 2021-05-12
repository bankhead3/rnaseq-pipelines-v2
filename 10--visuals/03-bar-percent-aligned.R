# 20180202 arb
# create barplot describing total fragment counts

library(ggplot2)

options(stringsAsFactors=F)

inFile1 = 'input/fragmentCounts.txt'
outFile1 = 'figs/03-bar-percent-aligned.png'
data1 = read.delim(inFile1)

means = aggregate(percentAligned ~ sample, data = data1, FUN='mean')

sem = function(x) { n = length(x); sd(x)/sqrt(n) } 
sems = aggregate(percentAligned ~ sample, data = data1, FUN='sem')

plotData = data.frame(sample=means$sample,mean=means$percentAligned,sem=sems$percentAligned)
samples = sort(plotData$sample)
plotData$sample = factor(plotData$sample,levels=samples)

# draw yo plot
title = paste0(signif(mean(plotData$mean),3), '% Average')
theme_set(theme_light(base_size=18)) 
ggplot(plotData,aes(sample,mean,fill=sample))  + 
  geom_bar(stat='identity') +
  geom_errorbar(aes(ymin=mean-sem,ymax=mean+sem),width=0.5) + 
  theme(axis.text.x = element_text(angle=45,vjust=1,hjust=1,size=12)) + 
  guides(fill=F) +
  labs(x='sample',y='Percent Aligned Reads',title=title) +
  geom_hline(yintercept=70, color = 'red',linetype = 'dashed') +
  geom_hline(yintercept=90, color = 'orange',linetype = 'dashed') +
  ylim(0,100)


ggsave(outFile1,height=5,width=5,dpi=200,units='in')
print(outFile1)
