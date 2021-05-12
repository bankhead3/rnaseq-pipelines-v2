options(stringsAsFactors=F)

# *** sets2table ***
# take a list of groups with values (used for venns)
# return a table with values,groups,numGroups
sets2table = function(sets) { 
  groups = names(sets) 
  values = sort(unique(as.vector(unlist(sets))))

  result = data.frame(value=values)
  result$groups = result$num = NULL

  # count the number of group memberships
  for(c1 in 1:nrow(result)) {
    value = result$value[c1]
    tmp_groups = c()
    for(group in groups) {
      if(value %in% sets[[group]]) { tmp_groups = c(tmp_groups,group) } 
    }

    tmp_group = paste(sort(tmp_groups),sep=',',collapse=',')
    result$group[c1] = tmp_group
    result$num[c1] = length(tmp_groups)
  }

  # return result
  result = result[order(result$num,decreasing=T),]
  return(result) 
}
# ***

# *** myMerge ***
# combine together rows that map to the same original gene
# a slow way to combine rows common unique fields
myMerge = function(data1,uniques) {
  # construct unique data frame
  data1a = NULL
  for(myUnique in uniques) { 
    data1a = cbind(data1a,data1[[myUnique]])
  }
  data1a = unique(data.frame(data1a))
  colnames(data1a) = uniques

  # columns that need to be pasted
  nonUniques = colnames(data1)[!colnames(data1) %in% uniques]

  # reorder data1 such that unique columns are first	
  data1 = data1[,c(uniques,nonUniques)]

  # create a new data frame
  data1c = data.frame(matrix(NA,nrow(data1a),ncol(data1)))
  colnames(data1c) = colnames(data1)

  # iterate through unique rows and construct a new version of original data frame
  for(c1 in 1:nrow(data1a)) {
    row = data1a[c1,]
    data1b = merge(row,data1)  # join back to original

    # add in merged columns
    for(field in nonUniques) { 
      result = paste0(sort(data1b[[field]]),collapse=',')
      row[[field]] = result
    }

    # add to updated data frame
    data1c[c1,] = row
  }

  data1c = data.frame(data1c)
  return(data1c)
}

# example call:
# uniques = c('gene','entrez','hgnc_id')
# result = myMerge(data1,uniques)

# *** venn3 ***
# draw a pretty 3-way non-scaled venn diagram
venn3 = function(sets, filename, title = '') { 

stopifnot(length(sets) == 3)

require(RColorBrewer)
require(VennDiagram)

# *** draw venn diagram ***
cols = brewer.pal(4,'Accent')
cols = cols[1:length(sets)]

  areas = 10
  n = length(sets)
  n12 = length(intersect(sets[[1]],sets[[2]]))
  n23 = length(intersect(sets[[2]],sets[[3]]))
  n13 = length(intersect(sets[[1]],sets[[3]]))
  n123 = length(intersect(sets[[1]],intersect(sets[[2]],sets[[3]])))

  g = draw.triple.venn(area1 = length(sets[[1]]), area2 = length(sets[[2]]), area3 = length(sets[[3]]), 
    n12 = n12, n23 = n23, n13 = n13, 
    n123 = n123,
    category = names(sets),
    fill = cols,
    lty = 'blank',
    cex = 3, 
    cat.dist = c(.1,.1,.075),
    cat.cex = 4,
    cat.col = 'black', 
    cat.fontface = 'bold',
    fontfamily = "sans",
    cat.fontfamily = "sans",
    scaled = FALSE,
    euler.d = FALSE,
    margin = .1,
    ind = FALSE
  )

  # write yo pdf
  pdf(filename)
  grid.draw(g) 
  grid.draw(grid.text(title, .5, .95, draw = F, gp = gpar(col = 'black', cex = 2, fontface = 'bold')))
  dev.off()
  print(filename)
}

