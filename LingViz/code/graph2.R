source("subs.R")

geo_data = read.table("data_new/geo-clean-30-datapoints-r-500-fixed.csv",sep="\t",quote="\"")

# Let's determine which features to plot. We want to use
# the features with the fewest most data, i.e. fewest NAs 
# in them. First, we take the relevant columns (V11 and up)
# and ensure that they are numeric.
geo_data[,11:ncol(geo_data)] = sapply(geo_data[,11:ncol(geo_data)],as.numeric)

# Normalize all the feature columns.
geo_data[,11:ncol(geo_data)] = scale(geo_data[,11:ncol(geo_data)])

#This function sorts all the columns of the data
# by how few NAs they have.
sorted.features = sort(colMeans(is.na(geo_data[,11:ncol(geo_data)])))

# Remove the V's from the colnames
names(sorted.features) = substr(names(sorted.features),2,4)

# Get the 15 best-represented features
best.features = sorted.features[1:15]



# Make our subset of data to plot
data.subset = t(geo_data[,as.numeric(names(best.features))])

colnames(data.subset) = get.language(geo_data$V10)
rownames(data.subset) = get.feature(names(best.features),shift=10)

# Now to re-order the columns (the languages) of the subset
# so that they are arranged in order.
# Oh, we can't do that, because we don't know what everything
# is relative to.

# The data have lots of repetitions. I'm not 100% sure what's
# going on; each language seems to be in there 6 times. The 
# difference is in columns V4 through V8, so I presume that's
# geographic distance to some language; but the language is
# unspecified, which is annoying. Richard, you need to learn
# how to make column headers, or provide the information in 
# a comment or file somewhere.
# Remove the duplicates.
data.subset = t(unique(t(data.subset)))

pdf("graphs/graph2.pdf")
par(oma=c(2,2,2,20))
heatmap(data.subset,Rowv=NA,Colv=NA)
dev.off()

rownames(data.subset) = paste("F",names(best.features),sep="")
pdf("graphs/graph2wnumbers.pdf")
par(oma=c(2,2,2,2))
heatmap(data.subset,Rowv=NA,Colv=NA)
dev.off()