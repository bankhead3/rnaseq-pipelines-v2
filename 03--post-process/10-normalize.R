# 20200708 arb
# update to work with a single quantifier

options(stringsAsFactors=F)

inFile1 = 'intermediate/09.txt'
outDir = '10-txts/'
data1 = read.delim(inFile1)

if(!file.exists(outDir)) { dir.create(outDir) }  # create if it's not there

# add in cell line information to normalize separate
data1$cellline = sub('_.*','',data1$sample)

# calculate and add muq to data.frame
data1 = data.frame(data1,muq=data1$uq)
types = unique(data1$type)
for(type in types) {
    idx = data1$type == type
    muq = mean(data1$uq[idx])
    data1$muq[idx] = muq
}

# for each quantifier type sample read and write a new normalized file
for(r1 in 1:nrow(data1)) { 
  # get sample information
  inFile = data1$file[r1]
  sample = data1$sample[r1]
  replicate = data1$replicate[r1]
  type = data1$type[r1]
  uq = data1$uq[r1]
  muq = data1$muq[r1]

  # read file
  data2 = read.delim(inFile)

  data2a = data.frame(data2,valueNorm=(data2$value/uq)*muq)
  data2b = data.frame(data2a,log2valueNorm=log2(data2a$valueNorm + 1))
  data2b = data.frame(data2b,uq=rep(uq,nrow(data2b)),muq=rep(muq,nrow(data2b)))

  # write data
  outFile = paste0(outDir,sample,'_',replicate,'-',type,'.txt')
  write.table(data2b,outFile,quote=F,row.names=F,sep="\t")
  print(outFile)
}

