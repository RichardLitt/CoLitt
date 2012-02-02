clean.data = read.table("data/geo-clean-30-datapoints-r-500",sep=",",header=F)

clean.data.phono = clean.data[5:18]
heatmap((data.matrix(clean.data.phono)),Rowv=NA,Colv=NA)

lang1 = clean.data[clean.data$V1=="yim",5:18]
heatmap((data.matrix(lang1)),Rowv=NA,Colv=NA)

lang2 = clean.data[clean.data$V1=="kob",5:18]
heatmap((data.matrix(lang2)),Rowv=NA,Colv=NA)

lang3 = clean.data[clean.data$V1=="kew",5:18]
heatmap((data.matrix(lang3)),Rowv=NA,Colv=NA)

lang4 = clean.data[clean.data$V1=="awt",5:18]
heatmap((data.matrix(lang4)),Rowv=NA,Colv=NA)

lang5 = clean.data[clean.data$V1=="arp",5:18]
heatmap((data.matrix(lang5)),Rowv=NA,Colv=NA)

lang6 = clean.data[clean.data$V1=="ala",5:18]
heatmap((data.matrix(lang6)),Rowv=NA,Colv=NA)


# TO DO:
# Make the feature names and the language names populate
# the col and row names
#
# Write functions to remove any rows/columns that are all NA.