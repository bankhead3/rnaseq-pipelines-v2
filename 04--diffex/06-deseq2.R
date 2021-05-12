# 20170220 arb 
# perform diffex using deseq2

library('DESeq2')
library(stringr)
library(reshape)
library(dplyr)

options(stringsAsFactors=FALSE)

inFile1 = 'intermediate/04.txt'
inFile2 = 'input/combos.txt'
outFile1 = 'intermediate/06.txt'
method = 'deseq2'

load = T
if(load) { data1 = read.table(inFile1,header=T); data2 = read.delim(inFile2) }

combos = list()
for(c1 in 1:nrow(data2)) { 
  combos[[c1]] = as.character(data2[c1,])
}

if(exists('outData')) { rm(outData) }

outData = NULL
for(c1 in 1:length(combos)) { 
  print(combos[[c1]])

  treatment = combos[[c1]][1]
  tx = sub('.*_','',treatment)
  control = combos[[c1]][2]
  ctrl = sub('.*_','',control)

  # *** note from DESeq2 tutorial: In order to benefit from the default seetings of the package, you should put the variable of interest at the end of the formula and make sure the control leve is the first level ***
  treatmentReplicates = sort(unique(data1$sampleReplicate[data1$sample == treatment]))
  controlReplicates = sort(unique(data1$sampleReplicate[data1$sample == control]))
  data1a = data1[data1$sample %in% c(treatment,control),]
  data1a$sampleReplicate = factor(data1a$sampleReplicate,levels=c(controlReplicates,treatmentReplicates))

  data1b = dplyr::select(data1a,sampleReplicate,gene,count)
  data1c = cast(data1b, gene ~ sampleReplicate, value='count')

  rownames(data1c) = data1c$gene
  data1c$gene = NULL

  cellline = unique(sub('_.*','',treatment))
  stopifnot(length(cellline) == 1)

  treatments = str_match(colnames(data1c),'.*_(.*)_.*')[,2]
  treatments = sub('-','.',treatments)
  ctrl = sub('-','.',ctrl)
  tx = sub('-','.',tx)

  # build colData
  colData = data.frame(condition=treatments)
  rownames(colData) = colnames(data1c)
  colData$condition = factor(colData$condition,levels=c(ctrl,tx))

  # build DESeqDataSet object from count data
  dds = DESeqDataSetFromMatrix(countData = data1c,colData = colData, ~ condition)

  # perform deseq here
  dds = DESeq(dds)

  # maximum likelihood fold change estimates
  results1 = results(dds,contrast=c('condition',tx,ctrl))
  results2 = data.frame(cellline = rep(cellline,nrow(results1)),	
                       tx = rep(tx,nrow(results1)),
		       id = rownames(results1),
                       results1)

  # shrinkage adjusted fold change estimates
  results3 = lfcShrink(dds,coef=2,type="apeglm")
  results4 = data.frame(id = rownames(results3),
                       shrunkLFC=results3$log2FoldChange)

  # add shrinkage to mle fold change estimates
  results = merge(results2,results4,by='id')
  stopifnot(nrow(results) == nrow(results2) && nrow(results) == nrow(results4))

  # add to the diffex results
  results$tx = sub('[.]','-',results$tx)
  outData = rbind(outData,results)
}

write.table(outData,file=outFile1,sep="\t",quote=F,row.names=F)
