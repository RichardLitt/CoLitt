data = read.table("Code/Stats4Lx/hw5_data.csv", sep=",", header = TRUE)
attach(data)

t.test(data$RT1,mu=670)
wilcox.test(data$RT1,mu=670)
