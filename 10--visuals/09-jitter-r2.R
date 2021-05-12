# 20170223 arb
# generates scatter plots comparing replicates

library(ggplot2)

options(stringsAsFactors=F)
inFile1 = 'intermediate/08.txt'
data1 = read.delim(inFile1)

filename = 'figs/08-jitter-r2.png'
p1 = ggplot(data1,aes(x=sample,y=R2,color=sample)) + 
       geom_jitter(aes(fill = factor(sample)),height=0,width=.25) + 
       theme_set(theme_gray(base_size=18)) + 
       theme(axis.text.x = element_text(angle=45,vjust=1,hjust=1,size=12)) + 
       ylim(.7,1) + 
       guides(fill=F,sample=F,color=F) + 
       geom_hline(yintercept=0.9,color='red',linetype='dashed')
       
ggsave(filename,device='png',width=5,height=5,units='in',dpi=200)
print(filename)

