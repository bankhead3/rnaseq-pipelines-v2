# generates scatter plots comparing replicates

library(ggplot2)

options(stringsAsFactors=F)
inFile1 = 'input/geneExpression.txt'
outFile1 = 'intermediate/08.txt'
load = T

measure = 'TPM'

if(load) { data1 = read.delim(inFile1) }

samples = sort(unique(data1$sample))

if(!dir.exists('figs/scatter')) { dir.create('figs/scatter') }

summaryTable = matrix(NA,0,4)
colnames(summaryTable) = c('sample','replicates','R2','p-value')

# iterate through samples
for(sample in samples) {
  data1a = data1[data1$sample == sample,]
  replicates = sort(unique(data1a$replicate))
  combs = t(combn(replicates,2))

  # iterate through replicate pair combinations
  for(r1 in 1:nrow(combs)) {
      rep1 = combs[r1,1]
      rep2 = combs[r1,2]

      idx1 = data1a$replicate == rep1
      idx2 = data1a$replicate == rep2
      
      label1 = paste(sample,'_',rep1,' log2(',measure,')',sep='')
      label2 = paste(sample,'_',rep2,' log2(',measure,')',sep='')

      plotData1 = data.frame(sample=data1a$sample[idx1],id=data1a$gene[idx1],value=data1a$log2value[idx1])
      plotData2 = data.frame(sample=data1a$sample[idx2],id=data1a$gene[idx2],value=data1a$log2value[idx2])

      maxValue = ceiling(max(plotData1$value,plotData2$value))

      names(plotData1)[3] = 'x'
      names(plotData2)[3] = 'y'
      plotData = merge(plotData1,plotData2,by=c('sample','id'))

      result = cor.test(plotData$x,plotData$y,method='pearson')
      r2 = round(result$estimate ^ 2,3)
      pValue = sprintf("%0.3g",result$p.value)
      title = paste('Pearson R^2 = ', r2,'\n p-value = ', pValue, sep='')

      filename = paste('figs/scatter/',sample,'-',paste(rep1,rep2,sep='v'),'.png',sep='')

      # write your plot
      p1 = ggplot(plotData,aes(x=x,y=y,xlab = 'blah')) +
             labs(x=label1,y=label2) +
             xlim(0,maxValue) + ylim(0,maxValue) + 
	     ggtitle(title) +
             geom_point(shape=1) + 
	     geom_smooth(method=lm,fullrange=T) + 
	     theme(title = element_text(size=16),axis.title = element_text(size=14),axis.text=element_text(size=14)) + 
	     theme(plot.margin=unit(c(.5,.5,.5,.5),"cm"))		    
      ggsave(filename,device='png',width=5,height=5,units='in',dpi=200)
      print(filename)

      lineOut = c(sample,paste(rep1,rep2,sep=','),r2,pValue)
      summaryTable = rbind(summaryTable,lineOut)
  }
}

write.table(summaryTable,outFile1,quote=F,row.names=F,sep='\t')