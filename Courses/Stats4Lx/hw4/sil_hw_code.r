# Load file
example = read.table("Code/R/Stats4Lx/wpm_data.csv",, header = TRUE, sep = ",")

# Make subsets for each stage of redbull consumption
rb_0 <-example[example$num_drinks == 0,]
rb_1 <-example[example$num_drinks == 1,]
rb_2 <-example[example$num_drinks == 2,]
rb_3 <-example[example$num_drinks == 3,]
rb_4 <-example[example$num_drinks == 4,]
rb_5 <-example[example$num_drinks == 5,]
rb_6 <-example[example$num_drinks == 6,]
rb_7 <-example[example$num_drinks == 7,]
rb_8 <-example[example$num_drinks == 8,]
rb_9 <-example[example$num_drinks == 9,]
rb_10 <-example[example$num_drinks == 10,]
rb_11 <-example[example$num_drinks == 11,]
rb_12 <-example[example$num_drinks == 12,]
rb_13 <-example[example$num_drinks == 13,]
rb_14 <-example[example$num_drinks == 14,]
rb_15 <-example[example$num_drinks == 15,]
rb_16 <-example[example$num_drinks == 16,]
rb_17 <-example[example$num_drinks == 17,]
rb_18 <-example[example$num_drinks == 18,]
rb_19 <-example[example$num_drinks == 19,]

par(mfrow = c(3,7))


# Make individual boxplots for each stage of redbull consumption
#png("rb_0.png")
boxplot(rb_0$wpm, ylab="Spoken wpm", main = "0 ml", col="pink")
boxplot(rb_1$wpm, ylab="Spoken wpm", main = "100 ml", col="pink")
boxplot(rb_1$wpm, ylab="Spoken wpm", main = "200 ml", col="pink")
boxplot(rb_2$wpm, ylab="Spoken wpm", main = "200 ml", col="pink")
boxplot(rb_3$wpm, ylab="Spoken wpm", main = "300 ml", col="pink")
boxplot(rb_4$wpm, ylab="Spoken wpm", main = "400 ml", col="pink")
boxplot(rb_5$wpm, ylab="Spoken wpm", main = "500 ml", col="pink")
boxplot(rb_6$wpm, ylab="Spoken wpm", main = "600 ml", col="pink")
boxplot(rb_7$wpm, ylab="Spoken wpm", main = "700 ml", col="pink")
boxplot(rb_8$wpm, ylab="Spoken wpm", main = "800 ml", col="pink")
boxplot(rb_9$wpm, ylab="Spoken wpm", main = "900 ml", col="pink")
boxplot(rb_10$wpm, ylab="Spoken wpm", main = "1000 ml", col="pink")
boxplot(rb_11$wpm, ylab="Spoken wpm", main = "1100 ml", col="pink")
boxplot(rb_12$wpm, ylab="Spoken wpm", main = "1200 ml", col="pink")
boxplot(rb_13$wpm, ylab="Spoken wpm", main = "1300 ml", col="pink")
boxplot(rb_14$wpm, ylab="Spoken wpm", main = "1400 ml", col="pink")
boxplot(rb_15$wpm, ylab="Spoken wpm", main = "1500 ml", col="pink")
boxplot(rb_16$wpm, ylab="Spoken wpm", main = "1600 ml", col="pink")
boxplot(rb_17$wpm, ylab="Spoken wpm", main = "1700 ml", col="pink")
boxplot(rb_18$wpm, ylab="Spoken wpm", main = "1800 ml", col="pink")
boxplot(rb_19$wpm, ylab="Spoken wpm", main = "1900 ml", col="pink")

savePlot("yes.png", type = "png")

:
#example = read.table("Code/R/Stats4Lx/wpm_data.csv", sep=",", header = TRUE)
str(example)

png('wpm_boxplot.png')
boxplot(example$wpm~example$num_drinks, col='magenta', xlab='Amount of 100ml Shots of Red Bull', ylab='Spoken WPM', main='Change in WPM per Red Bull Shots')
dev.off()

# Make subsets for each IV change
noRB <- subset(example, num_drinks == 0)
RB_1 <- subset(example, num_drinks == 1)
RB_2 <- subset(example, num_drinks == 2)
RB_3 <- subset(example, num_drinks == 3)
RB_4 <- subset(example, num_drinks == 4)
RB_5 <- subset(example, num_drinks == 5)
RB_6 <- subset(example, num_drinks == 6)
RB_7 <- subset(example, num_drinks == 7)
RB_8 <- subset(example, num_drinks == 8)
RB_9 <- subset(example, num_drinks == 9)
RB_10 <- subset(example, num_drinks == 10)
RB_11 <- subset(example, num_drinks == 11)
RB_12 <- subset(example, num_drinks == 12)
RB_13 <- subset(example, num_drinks == 13)
RB_14 <- subset(example, num_drinks == 14)
RB_15 <- subset(example, num_drinks == 15)
RB_16 <- subset(example, num_drinks == 16)
RB_17 <- subset(example, num_drinks == 17)
RB_18 <- subset(example, num_drinks == 18)
RB_19 <- subset(example, num_drinks == 19)

var(noRB$wpm)
sd(noRB$wpm)
var(RB_1$wpm)
sd(RB_1$wpm)
var(RB_2$wpm)
sd(RB_2$wpm)
var(RB_3$wpm)
sd(RB_3$wpm)
var(RB_4$wpm)
sd(RB_4$wpm)
var(RB_5$wpm)
sd(RB_5$wpm)
var(RB_6$wpm)
sd(RB_6$wpm)
var(RB_7$wpm)
sd(RB_7$wpm)
var(RB_8$wpm)
sd(RB_8$wpm)
var(RB_9$wpm)
sd(RB_9$wpm)
var(RB_10$wpm)
sd(RB_10$wpm)
var(RB_11$wpm)
sd(RB_11$wpm)
var(RB_12$wpm)
sd(RB_12$wpm)
var(RB_13$wpm)
sd(RB_13$wpm)
var(RB_14$wpm)
sd(RB_14$wpm)
var(RB_15$wpm)
sd(RB_15$wpm)
var(RB_16$wpm)
sd(RB_16$wpm)
var(RB_17$wpm)
sd(RB_17$wpm)
var(RB_18$wpm)
sd(RB_18$wpm)
var(RB_19$wpm)
sd(RB_19$wpm)

