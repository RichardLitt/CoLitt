require(maps)

geo_yim = read.table("data_new/geo-yim",sep=",",quote="\"")

yimx = geo_yim$V8[which(geo_yim$V1=="yim")]
yimy = geo_yim$V7[which(geo_yim$V1=="yim")]


pdf("graphs/graph1.pdf")

# Columns V7 and V8 are long and lat respectively
plot(geo_yim$V8,geo_yim$V7,xlab="Latitude",ylab="Longitude",type="n",main="TITLE HERE")

color_scaling = geo_yim$V5*255/max(geo_yim$V5)

families = c("Trans-New Guinea","Austronesian","Sepik","Torricelli","Other")

geo_tg = geo_yim[geo_yim$V10==families[1],]
geo_au = geo_yim[geo_yim$V10==families[2],]
geo_sp = geo_yim[geo_yim$V10==families[3],]
geo_tr = geo_yim[geo_yim$V10==families[4],]
geo_ot = geo_yim[geo_yim$V10!=families[1] & geo_yim$V10!=families[2] & geo_yim$V10!=families[3] & geo_yim$V10!=families[4],]


points(geo_tg$V8,geo_tg$V7,col=rgb(0,0,0,color_scaling,maxColorValue=255),pch=15)
points(geo_au$V8,geo_au$V7,col=rgb(0,0,0,color_scaling,maxColorValue=255),pch=16)
points(geo_sp$V8,geo_sp$V7,col=rgb(0,0,0,color_scaling,maxColorValue=255),pch=17)
points(geo_tr$V8,geo_tr$V7,col=rgb(0,0,0,color_scaling,maxColorValue=255),pch=18)
points(geo_ot$V8,geo_ot$V7,col=rgb(0,0,0,color_scaling,maxColorValue=255),pch=14)

points(yimx,yimy,pch=11)

# Add an overlay of the landmass, although it doesn't
# quite line up :(
3map("world","papua new guinea",add=TRUE)
#map("world","indonesia",add=TRUE)

legend("topright",pch=c(15,16,17,18,14),c("Trans-New Guinea","Austronesian","Sepik","Torricelli","Other"))
dev.off()
