# This is R code for the Stats in Linguistics Class.
# Each day will have a separate section or document. 
# This code is available from Richard Littauer, and
# has been released under no license whatsoever. 

#================
# Class 1, Monday

# Install packages
install.packages(c("part", "chron", "Hmisc", "Design", "Matrix", "lme4", "coda", "e1071", "zipfR", "ape", "languageR"), repos = https://cran.r-project.org)

# Load the library
library(languageR)

# Detach the package, if you're done with it.
# detach(package: languageR)

# See the head values of the example dataset heid.
head(heid)

# Write it to a table
# write.table(heid,file="/users/pirita/rcourse/example.txt")

dir()

# And read it from that table
example=read.table("Code/R/Stats4Lx/wpm_data.csv", sep=",", header = TRUE)

# Find the structure of the data
str(heid)

# Find the column names
colnames(heid)

# ======================================
# Day 3: Wednesday

# Renaming a column for each experimenter, as strings. 
example$person = as.factor(example$person)
fnew <- factor(example[,1],levels=0:19)
levels(fnew) <- c("steve", "john", "casey","neytiri","jake","sully","grace","augustine","norm","sigourney","weaver","nantang","palulukan","daisy","moat","eyktukan","pandora","utral","cameron","ipxa")
example$person <- fnew



# How to create a data file in R
# =====
# Create a data frame with 20 subjects, 20 observations each
createdata - data.framce(Subject = rep(1:20, each=20)) 

# Add 20 participants
createdata$Subject = rep(1:20)

# Add 20 items
createdata$Item = rep(1:20)

# Concreteness
createdata$AC = rep(c('Abstract', 'Concrete'), each = 20)

# Frequency
createdata$Freq = c('High', 'Low')

# Random numbers for all rows .. amount, mean, and std
createdata$RTs = rnorm(400,650,0.15)

head(createdata)
str(createdata)

# Subject and itemsa as factors
createdata$Subject = as.factor(createdata$Subject)
createdata$Item = as.factor(createdata$Item)

# === 

example = heid
mean(example$RT)
median(example$RT)

# Since it's fun, here's a nice histogram. 

draw_axis = opts(axis.line=theme_segment(colour="black",linetype="solid",size=0.8))
axis_labels=  opts(axis.text.x=theme_text(size=11),axis.text.y=theme_text(size=11))
no_bg = opts(panel.background=theme_rect(colour=NA))

library(ggplot2)
qplot(example$RT, data=example, geom="histogram")
RT_histogram = ggplot(example,aes(x=RT)) +geom_histogram(binwidth=.05)  + opts(title="Reaction Times Histogram") + opts(plot.title=theme_text(size = 12, face ='bold')) + opts(panel.grid.major=theme_line(colour=NA)) + opts(panel.grid.minor=theme_line(colour=NA)) + no_bg + draw_axis + axis_labels
RT_histogram


# And here's how to find the median and means for frequency subsets
more <- subset(example, BaseFrequency >= 4.5)
less <- subset(example, BaseFrequency <= 4.5)
head(more)
head(less)
median(more$RT)
mean(more$RT)
median(less$RT)
median(more$RT)

max(example$RT)
min(example$RT)
sd(example$RT)

example1 = example
example2 = example
example3 = aggregate(example1,example2)
head(example3)
head(example1)
head(example2)


# ==================================================
# Day 4 Thursday

sd(more$RT)
var(more$RT)
sd(less$RT)
var(less$RT)

head(lexdec)
xtabs(~Correct, data=lexdec)
barplot(xtabs(~lexdec$Correct), xlab='Responses', main = 'My graph',
        col = 'blue', ylab = 'Number of observations')

hist(lexdec$RT, xlab='RTs', ylab='Number of observations', col ='pink')
#qplot(example$RT, data=example, geom="histogram")
RT_histogram = ggplot(lexdec,aes(x=RT, fill=Correct)) +geom_histogram(colour='darkgreen', binwidth=.05)  + opts(title="Reaction Times Histogram") + opts(plot.title=theme_text(size = 12, face ='bold')) + opts(panel.grid.major=theme_line(colour=NA)) + opts(panel.grid.minor=theme_line(colour=NA)) + no_bg + draw_axis + axis_labels
RT_histogram

correct  <- subset(lexdec, Correct == 'correct')
incorrect <- subset(lexdec, Correct == 'incorrect')

ggplot(correct,aes(x=RT)) +geom_histogram(colour='darkgreen')  + opts(title="Reaction Times Histogram") + opts(plot.title=theme_text(size = 12, face ='bold')) + opts(panel.grid.major=theme_line(colour=NA)) + opts(panel.grid.minor=theme_line(colour=NA)) + no_bg + draw_axis + axis_labels
ggplot(incorrect,aes(x=RT)) +geom_histogram(colour='darkgreen')  + opts(title="Reaction Times Histogram") + opts(plot.title=theme_text(size = 12, face ='bold')) + opts(panel.grid.major=theme_line(colour=NA)) + opts(panel.grid.minor=theme_line(colour=NA)) + no_bg + draw_axis + axis_labels

par(mfrow = c(2,2))

correct  <- lexdec[lexdec$Correct == "correct", ]
hist(correct$RT, xlab='RT', ylab='Number of observations', col='pink', main='RTs for correct responses')
incorrect  <- lexdec[lexdec$Correct == "incorrect", ]
hist(incorrect$RT, xlab='RT', ylab='Number of observations', col='pink', main='RTs for incorrect responses')


boxplot(correct$RT, col='pink')
boxplot(incorrect$RT, col='darkgreen')

boxplot(lexdec$RT~lexdec$Correct, data=lexdec, col='pink')

data <- xtabs(~NativeLanguage+Sex, data=lexdec[lexdec$Correct == 'correct',])
barplot(data, legend.text=c('English','Other'))
barplot(data, beside=T, legend.text=rownames(data), col=(c("gold","darkgreen")))
# T is just the shortcut for TRUE

# ===

wpmdata = lamarscode

wpmdata = read.table("Code/R/Stats4Lx/wpm_data.csv", sep=",", header = TRUE)
str(wpmdata)

png('wpm_boxplot.png')
boxplot(wpmdata$wpm~wpmdata$num_drinks, col='magenta', xlab='Amount of 100ml Shots of Red Bull', ylab='Spoken WPM', main='Change in WPM per Red Bull Shots')
dev.off()

# Make subsets for each IV change
noRB <- subset(wpmdata, num_drinks == 0)
RB_1 <- subset(wpmdata, num_drinks == 1)
RB_2 <- subset(wpmdata, num_drinks == 2)
RB_3 <- subset(wpmdata, num_drinks == 3)
RB_4 <- subset(wpmdata, num_drinks == 4)
RB_5 <- subset(wpmdata, num_drinks == 5)
RB_6 <- subset(wpmdata, num_drinks == 6)
RB_7 <- subset(wpmdata, num_drinks == 7)
RB_8 <- subset(wpmdata, num_drinks == 8)
RB_9 <- subset(wpmdata, num_drinks == 9)
RB_10 <- subset(wpmdata, num_drinks == 10)
RB_11 <- subset(wpmdata, num_drinks == 11)
RB_12 <- subset(wpmdata, num_drinks == 12)
RB_13 <- subset(wpmdata, num_drinks == 13)
RB_14 <- subset(wpmdata, num_drinks == 14)
RB_15 <- subset(wpmdata, num_drinks == 15)
RB_16 <- subset(wpmdata, num_drinks == 16)
RB_17 <- subset(wpmdata, num_drinks == 17)
RB_18 <- subset(wpmdata, num_drinks == 18)
RB_19 <- subset(wpmdata, num_drinks == 19)

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

# ==================================================
# Day 5 2012-02-21

library(languageR)
attach(lexdec)
shapiro.test(RT)

m2 <- lm(RT~Correct)
summary(m2)
anova(m2)

str(lexdec)

m3 <- lm(RT~PrevType)
summary(m3)
anova(m3)

attach(auxiliaries)
m4 <- lm(VerbalSynsets~Aux)
anova(m4)
summary(m4)

attach(lexdec)
m5 <- lm(RT~Correct+Complex)
anova(m5)
summary(m5)

m6 <- lm(RT~Correct*Complex)
anova(m6)
summary(m6)


# ==========
hw5=read.table("Code/Stats4Lx/hw5_data.csv", sep=",", header = TRUE)

attach(weightRatings)

im <- lm(Rating~Sex+Class)
anova(im)
summary(im)

me <- lm(Rating~Sex*Class)
anova(me)
summary(me)

attach(lexdec)
m1 <- lm(RT~Complex)
m2 <- lm(RT~Frequency*Complex)
m3 <- lm(RT~Correct*Complex*Sex*Frequency)
anova(m3)
summary(m3)
anova(m1,m2,m3)


# -------------------------------------------
# 22/02 Wednesday 

library(languageR)
attach(auxiliaries)
pairwise.t.test(VerbalSynsets,Aux,p.adj="bonferroni")

attach(lexdec)
m6 <- aov(RT~Complex*Correct)
anova(m6)
TukeyHSD(aov(m6))

attach(ratings)
m1 <- lm(meanWeightRating~meanSizeRating)
anova(m1)
summary(m1)

library(Design)
attach(lexdec)
ml <- lrm(Correct~Complex)
ml
attach(english)
str(english)
#IncorrectLexdec <- abs(CorrectLexdec-30)
#IncorrectLexdec
#mr <- lrm(CorrectLexdec~IncorrectLexdec)
#lmg
#lmr

cbind(CorrectLexdec, 30-CorrectLexdec)
m10 <- glm(cbind(CorrectLexdec, 30-CorrectLexdec)~Voice,family="binomial")
summary(m10, test="Chisq")

attach(ratings)
cor(meanWeightRating, meanSizeRating)

cor(meanWeightRating, meanSizeRating, method="spearman")

attach(trees)
ml  <- lrm(Height~Girth)
ml

attach(CO2)
str(CO2)
#ml <- lrm(


# ================
# 23/02/2012

library(languageR)
library(lme4)
attach(lexdec)
ml <- lm(RT~Correct)
qqnorm(resid(ml)) # A plot
qqline(resid(ml)) # A superimposed line

# If you don't have random effects, than you can't use mixed models
m7 <- lmer(RT~Complex+(1|Subject)+(1|Word),data=lexdec)
summary(m7)
pvals.fnv(m7)$fixed


m8 <- lmer(Correct~Complex + (1|Subject)+(1|Word),family=binomial, data=lexdec)
summary(m8)

d
