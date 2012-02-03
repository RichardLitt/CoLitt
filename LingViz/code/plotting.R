library(reshape)

clean.data = read.table("data/geo-clean-30-datapoints-r-500",sep=",",header=F)

feature.list = read.table("features.csv",header=T,sep=",",stringsAsFactors=F)
language.list = read.table("languages.csv",header=T,sep="\t",quote="\"",stringsAsFactors=F)

# Given a particular column in a dataset, find what
# feature it corresponds to. Can also shift, if
# the dataset still has the language and distance
# columns attached.
get.feature = function(column,shift=F) {
	if(shift) {
		return(feature.list[column-5,2])
	}
	return(feature.list[column,2])
}

# Given a particular language code, find the full
# language name
get.language = function(language) {
	names = rep(NA,length(language))
	for(i in 1:length(language)) {
		names[i] = language.list[which(language.list[,1]==language[i]),2]
	}
	return(names)
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
	data.subset = t(data[clean.data$V1==language,shifted.features])
	colnames(data.subset) = get.language(data$V4[data$V1==language])
	rownames(data.subset) = get.feature(shifted.features)
	data.subset = remove.empty((data.subset))
# Rescale the data
#	data.subset.m = melt(data.subset)
#	data.subset.m = ddply(data.subset.m, .(variable), transform, #rescale = rescale(value))
	par(oma=c(2,2,2,10))
	heatmap((data.matrix(data.subset)),Rowv=NA,Colv=NA,main=get.language(language),col=heat.colors(12),scale="none")
#	heatmap((data.matrix(data.subset)),main=get.language(language),col=heat.colors(12),scale="none")

#	image(t(data.matrix(data.subset)))
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