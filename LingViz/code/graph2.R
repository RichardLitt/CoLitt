source("subs.R")

geo_data = read.table("data_new/geo-clean-30-datapoints-r-500-fixed.csv",sep="\t",quote="\"",header=T)

# Let's determine which features to plot. We want to use
# the features with the fewest most data, i.e. fewest NAs 
# in them. First, we take the relevant columns (11 and up)
# and ensure that they are numeric.
width = ncol(geo_data)
geo_data[,11:width] = sapply(geo_data[,11:width],as.numeric)

# Normalize all the feature columns.
geo_data[,11:width] = scale(geo_data[,11:width])

# Change the feature column names to simple numbers. This
# aids the lookup process later.
names(geo_data)[11:width] = as.character((11:width))

#This function sorts all the columns of the data
# by how many NAs they have. The numbers in this
# vector are the proportion of the column that is
# NA.
sorted.features = sort(colMeans(is.na(geo_data[,11:ncol(geo_data)])))

# Remove the V's from the colnames
#names(sorted.features) = substr(names(sorted.features),2,4)

# Get the 15 best-represented features
best.features = sorted.features[1:15]


make.feature.subset = function(language) {
# Get the subset of the features we want, relative to
# the center language we want
	data.subset = geo_data[which(geo_data$center.language==language),c(1:10,(as.numeric(names(best.features))))]

## Re-order the rows in terms of distance from center
## (This is being done simply for now)
#	data.subset = data.subset[order(data.subset$X.distance.from.centre),]

# Remove the non-feature columns and transpose the data
	data.subset = t(data.subset[,11:ncol(data.subset)])

# Set the names of the columns and rows
	colnames(data.subset) = get.language(geo_data$wals_code[as.numeric(colnames(data.subset))])
	rownames(data.subset) = get.feature(names(best.features),shift=10)

# And voila!
	return(data.subset)
}

data.subset.ala = make.feature.subset("ala")
data.subset.arp = make.feature.subset("arp")
data.subset.awt = make.feature.subset("awt")
data.subset.kew = make.feature.subset("kew")
data.subset.kob = make.feature.subset("kob")
data.subset.yim = make.feature.subset("yim")

pdf("graphs/graph2ala.pdf")
par(oma=c(2,2,2,16))
heatmap(data.subset.ala,Rowv=NA,Colv=NA)
dev.off()

pdf("graphs/graph2arp.pdf")
par(oma=c(2,2,2,16))
heatmap(data.subset.arp,Rowv=NA,Colv=NA)
dev.off()

pdf("graphs/graph2awt.pdf")
par(oma=c(2,2,2,16))
heatmap(data.subset.awt,Rowv=NA,Colv=NA)
dev.off()

pdf("graphs/graph2kew.pdf")
par(oma=c(2,2,2,16))
heatmap(data.subset.kew,Rowv=NA,Colv=NA)
dev.off()

pdf("graphs/graph2kob.pdf")
par(oma=c(2,2,2,16))
heatmap(data.subset.kob,Rowv=NA,Colv=NA)
dev.off()

pdf("graphs/graph2yim.pdf")
par(oma=c(2,2,2,16))
heatmap(data.subset.yim,Rowv=NA,Colv=NA)
dev.off()

#rownames(data.subset) = paste("F",names(best.features),sep="")
#pdf("graphs/graph2wnumbers.pdf")
#par(oma=c(2,2,2,2))
#heatmap(data.subset,Rowv=NA,Colv=NA)
#dev.off()