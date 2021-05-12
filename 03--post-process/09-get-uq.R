# 20170711 arb
# generate a file containing patient and uq for uq normalization
# not worrying about genes or isoforms that are all zero since they happen so rarely across larger sample populations (<1%)

options(stringsAsFactors=F)

inDir = '02-txts/'
outFile = 'intermediate/09.txt'

header = as.matrix(t(c('sample','replicate','type','uq','file')))
write.table(header,outFile,quote=F,row.names=F,sep="\t",col.names=F)

files = dir(inDir)
for(file in files) {
  # read in data
  print(file)
  inFile = paste0(inDir,file)
  data1 = read.delim(inFile)

  parse1 = gsub('-(gene|transcript).txt','',file)        
  sample = gsub('_.$','',parse1)        
  replicate = gsub('^.*_','',parse1)

  myType = gsub('.*-','',file)
  myType = gsub('.txt','',myType)          
  uq = quantile(data1$value,.75)

  lineOut = as.matrix(t(c(sample,replicate,myType,uq,inFile)))
  write.table(lineOut,outFile,quote=F,row.names=F,sep="\t",col.names=F,append=T)
}
