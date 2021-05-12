# 20180730 arb
# use david to perform enrichment on differentially expressed genes


options(stringsAsFactors=F)

library(RDAVIDWebService)
library(dplyr)

inFile1 = 'input/rnaseq.txt'  # original genes (to ignore for enrichment)
inFile2 = 'input/hgnc.txt'
platform = 'rnaseq'

threshold = 0.05
size_threshold = 500

outFile1 = 'intermediate/02.txt'
outFileTmp = 'intermediate/tmp.txt'

data1 = read.delim(inFile1)
data2 = read.delim(inFile2)

out = NULL

samples = sort(unique(data1$sample))
criteria = unique(data1$criteria)
data1a = data1[data1$isDE. == 'Y',]

background = unique(data1$entrez)
background = background[!is.na(background)]

# establish connection, genesets, etc
loadBackground = T
if(loadBackground) {
  # establish connection and universe
  david = DAVIDWebService(email="bankhead@umich.edu", url="https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap12Endpoint/")
  setTimeOut(david,500000)
  bg = addList(david,as.character(background),idType='ENTREZ_GENE_ID',listName='myUniverse',listType='Background')
}

for(sample in samples) { 

  entrezes = data1a$entrez[data1a$sample == sample]

  label = paste0(sample,'_',criteria,'_',platform)
  print(label)

  # provide annotations to david
  result = addList(david,as.character(entrezes),idType='ENTREZ_GENE_ID',listName=label,listType='Gene')
  setCurrentBackgroundPosition(david,2)  # set background to be custom myUniverse

  cats = c('GOTERM_BP_ALL')
  setAnnotationCategories(david,cats)

  # enrich for go bp
  result = getFunctionalAnnotationChart(david,threshold=1)

  # polish
  if(nrow(result) > 0) {
    write.table(result,outFileTmp,quote=F,row.names=F,sep="\t")  # non-elegant way to get rid of factors
    result2 = read.delim(outFileTmp)
    result3 = select(result2,source=Category,geneset = Term, pval = PValue, qval = Benjamini,num=Count,total=Pop.Hits,foldEnrichment = Fold.Enrichment,entrezes=Genes)
    result3$entrezes = gsub('[ ]','',result3$entrezes)
    result3 = result3[result3$total <= size_threshold,]
    result4 = data.frame(isSig = ifelse(result3$qval < threshold, 'Y','N'),label = rep(label,nrow(result3)),result3)
    out = rbind(out,result4)
  }

  # enrich for kegg
  cats = c('KEGG_PATHWAY')
  setAnnotationCategories(david,cats)
  result = getFunctionalAnnotationChart(david,threshold=1)

  # polish
  if(nrow(result) > 0) {
    write.table(result,outFileTmp,quote=F,row.names=F,sep="\t")  # non-elegant way to get rid of factors
    result2 = read.delim(outFileTmp)
    result3 = select(result2,source=Category,geneset = Term, pval = PValue, qval = Benjamini,num=Count,total=Pop.Hits,foldEnrichment = Fold.Enrichment,entrezes=Genes)
    result3$entrezes = gsub('[ ]','',result3$entrezes)
    result3 = result3[result3$total <= size_threshold,]
    result4 = data.frame(isSig = ifelse(result3$qval < threshold, 'Y','N'),label = rep(label,nrow(result3)),result3)
    out = rbind(out,result4)
  }

}

out$source[out$source == 'GOTERM_BP_ALL'] = 'goBP'
out$source[out$source == 'KEGG_PATHWAY'] = 'kegg'

write.table(out,outFile1,quote=F,row.names=F,sep="\t")
