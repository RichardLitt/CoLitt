clean.data = read.table("data/geo-clean-30-datapoints-r-500",sep=",",header=F)

features = read.table("features.csv",header=T,sep=",",stringsAsFactors=F)

# Given a particular column in a dataset, find what
# feature it corresponds to. Can also shift, if
# the dataset still has the language and distance
# columns attached.
get.feature = function(column,shift=F) {
	if(shift) {
		return(features[column-5,2])
	}
	return(features[column,2])
}

remove.empty = function(data.subset) {
	# Remove empty columns
	data.subset = data.subset[,which(colMeans(is.na(data.subset)) < 1)]
	# Remove empty rows
	data.subset = data.subset[which(rowMeans(is.na(data.subset)) < 1),]
	return(data.subset)
}

make.heatmap = function(data,language,features) {
	shifted.features = features+4
	data.subset = clean.data[clean.data$V1==language,shifted.features]
	rownames(data.subset) = clean.data$V4[clean.data$V1==language]
	colnames(data.subset) = get.feature(shifted.features)
	data.subset = remove.empty(data.subset)
	heatmap(data.matrix(data.subset),Rowv=NA,Colv=NA,main=language)
}


pdf("data/ala.pdf")
make.heatmap(clean.data,"ala",1:14)
dev.off()

pdf("data/arp.pdf")
make.heatmap(clean.data,"arp",1:14)
dev.off()

pdf("data/awt.pdf")
make.heatmap(clean.data,"awt",1:14)
dev.off()

pdf("data/kew.pdf")
make.heatmap(clean.data,"kew",1:14)
dev.off()

pdf("data/kob.pdf")
make.heatmap(clean.data,"kob",1:14)
dev.off()

pdf("data/yim.pdf")
make.heatmap(clean.data,"yim",1:14)
dev.off()