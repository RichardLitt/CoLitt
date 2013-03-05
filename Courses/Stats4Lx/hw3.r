# Richard Littauer, Grady Payson
# Homework 3 - Statistics

# Load in the data
wpmdata=read.table("Code/R/Stats4Lx/wpm_data.csv", sep=",", header = TRUE)
head(wpmdata)


# Question 1:
# This would be negatively skewed, given our data, as we had precoded it in R
# So as to be incrementally rising over the drinks given. So, for all participants
# for each drink, the mean wpm would rise in value.


# Question 2: Median and Mean for the whole data
attach(wpmdata)
median(wpm) #358.8463
mean(wpm) #356.6145


# Question 3
# Since our DV has twenty iterations, we just harcoded this and did it for all of them# We could have used loops and coding, but that's a bit beyond us now. 

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

# Compute the median and mean for each subset's wpm. 
median(noRB$wpm)
mean(noRB$wpm)
median(RB_1$wpm)
mean(RB_1$wpm)
median(RB_2$wpm)
mean(RB_2$wpm)
median(RB_3$wpm)
mean(RB_3$wpm)
median(RB_4$wpm)
mean(RB_4$wpm)
median(RB_5$wpm)
mean(RB_5$wpm)
median(RB_6$wpm)
mean(RB_6$wpm)
median(RB_7$wpm)
mean(RB_7$wpm)
median(RB_8$wpm)
mean(RB_8$wpm)
median(RB_9$wpm)
mean(RB_9$wpm)
median(RB_10$wpm)
mean(RB_10$wpm)
median(RB_11$wpm)
mean(RB_11$wpm)
median(RB_12$wpm)
mean(RB_12$wpm)
median(RB_13$wpm)
mean(RB_13$wpm)
median(RB_14$wpm)
mean(RB_14$wpm)
median(RB_15$wpm)
mean(RB_15$wpm)
median(RB_16$wpm)
mean(RB_16$wpm)
median(RB_17$wpm)
mean(RB_17$wpm)
median(RB_18$wpm)
mean(RB_18$wpm)
median(RB_19$wpm)
mean(RB_19$wpm)


# Question 4

# For the median, we would use this when there was only clear gausssian bell curve. If this was note case, and if there lots of variation in the data (such as, perhaps, what might lead to a bimodal distribution), this would not be the best choice.

# We use the mean here, as the data has little variation, and as it is a useful way to show the trend over time given the change in the IV. This data is very regular, and this is the best way to show it, therefore.

# We would not use the mode, as this data is very granular and there probably isn't any repeating values.

# It is important to note above that we're calculating the mean and median for each value of the IV - not for the whole dataset. Given that the IV causes a predictable shift in the DV, using the mean or median on the whole dataset would erase any useful information we could get out of it.


# Question 5

# See attached pdf for the table we used to present the data. Given that we're not yet graphing, that the influence of the IV on the DV is clear and unambigious, presenting data in a table like this is a fairly trivial manner that makes a lot of sense.
