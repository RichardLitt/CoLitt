# Load in a script that defines three distance functions
# and a degrees-to-radians function.
# (see http://www.r-bloggers.com/great-circle-distance-calculations-in-r/)
source("gcd.R")

setwd("../wals_data")

wals_data = read.table("datapoints.csv",header=TRUE,sep=",")
languages = read.table("languages.csv",header=TRUE,sep="\t",quote="\"")

size = nrow(languages)
languages$longitude.rad = deg2rad(languages$longitude)
languages$latitude.rad = deg2rad(languages$latitude)

distances=matrix(NA,nrow=size,ncol=size)

# This calculates distances. It is slow and unweildy, and 
# should be refactored using some *apply functions. It also
# generates diagonal symmetry, so it's doing twice as much
# work as it needs to.
# (Seriously, it's hella slow. Takes several minutes.)
for(l1 in 1:size) {
	for(l2 in 1:size) {
#		compare l1 with l2
		distances[l1,l2] = gcd.hf(languages$longitude.rad[l1],languages$latitude.rad[l1],languages$longitude.rad[l2],languages$latitude.rad[l2])
	}
}
