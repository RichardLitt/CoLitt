'''
The purpose of this code is to clean WALS.

ok, so, you wanted the languages to be ordered by distances from each other. i presume the intention of that was so that all the close together language comparisons are on one end of the graph, and all the far away language comparisons are on the other end?
and that the intention is not to re-create a pseudomap of worldgeography
The intention was to make related languages appear in the graph
so that we can use it to look for linguistic areas
languages are generally related either geographically or phylogenetically

it would be REALLY INTERESTING if we did a contact model, as well
say, of English
now, this would be possible if we used, instead of features, a smaller subset, perhaps a single feature map

so i've realized the sorting method i outlined doesn't really work, because we're trying to sort two-dimensional data, not one-dimensional.
we could also combine features, create a feature similarity metric
so the issue i'm seeing is that their could be (will be) two pairs of languages - say, french and italian, and japanese and ainu - that have relatively small distances between them
these two comparisons would be right beside each other on the heat map
or at least, close
because they're both small distances
I was thinking we center the map on one language
aha, that sounds clever
and then either side will be the fallout
the issue is the ends - obviously, it means things aren't done possibly
like, connections won't be made between equidistant languages that may be related
and I don't have a solution to that.
what we could do
is sort it lattitudally or longitudally
or, connections WILL be made between languages that are both x km from the center language, even if they're both in different directions

if we center, we can say look at the centric maps
also, we don't want to have a graph with millions of languages
limiting it to a subset - say 30 language
should really elleviate the issue
we could also just get all the data, and then use some matrix reordering or seriation algorithm to cluster everything together (but that's kinda backwards)
haha, yes, currently we have a 2678x2678 matrix, which is a little large
also, because comparisons are symmetrical, the graph will be too - or one half will be blank
(assuming both x and y orders are the same)

we still need to clean the WALS data
what is it - 16% full at the moment?
76492 datapoints for 2678 languages.
(yeah, my sorting method doesn't work, as it's impossible to get it back into a sorted matrix)

we should cut out features
with less than a certain amount of languages per ____
phylogenetically, per family
let's say maybe 10 family members
is the minimum needed or 30
could be a ratio of the amount of languages divided against the amount of languages in the family
if over > 15

for gepographical distance
it should be languages with values in the area over the 60 closest languages
if over 15
that means that 25% of the languages in a given area have to have values in order for us to consider geographical contact
not that I'm setting 60 closest languages to deal with geographical differences - new guinea does not equal polynesia
make sense?
we can only test features that exist
and should only use features that have a certain amount of languages represented.
I think, for each matrix, yes, we can only count languages that have those
features
but not the overall proportion

'''

import sys

datapoints_file = "datapoints.csv"
languages_file = "languages.csv"
ethnologue = "ethnologue.csv"
root_file = "root_file.csv"
output_file = "cleaned_datapoints.csv"

#This function reads in the file
def read_file(x):
    f = open(x, 'r+')
    lineList = f.readlines()
    return lineList

#Splits the lines, if you wish. Probably a good thing.
def split_lines(x, y):
    lineList = []
    for line in x:
        line = line.split(y)
        lineList.append(line)
    return lineList


#Defines how you want to sort these things

def phylogenetic():

    #load languages, datapoints
    languagesList = split_lines(read_file(languages_file), '\t')
    dataList = split_lines(read_file(datapoints_file), ',')

    #load a dict of Wals codes
    wals_code = ['wals_code',]
    for x in range(len(languagesList)):
        lang_code = languagesList[x][0].replace('\"', '')
        wals_code.append(lang_code)

    #make sure that all of the data is accounted for in wals_code
    for line in range(len(dataList)):
        if dataList[line][0] not in wals_code:
            print 'Something is broken'
            break

    #If we're using ethnologue...
    if sys.argv[2] == 'e':
        print 'Using ethnologue for family relations.'
        ethnoList = split_lines(read_file(ethnologue), '\t')
        root_list = []
        h = open(root_e_file, 'a')
        for line in range(1,len(dataList)-1):
            for lines in range(1, len(languagesList)-1):
                lang_code = languagesList[lines][0].replace('\"', '')
                if dataList[line][0] == lang_code:
                    iso_code = languagesList[lines][7].replace('\"',\
                            '').replace("\n", '')
                    root = []
                    for lines in range(1, len(ethnoList)-1):
                        #print iso_code, ethnoList[lines][0]
                        if iso_code == ethnoList[lines][0]:
                            root = ethnoList[lines][1]
                            parents = ethnoList[lines][2]
                            print root
                            for lines in range(1, len(ethnoList)-1):
                                if root == ethnoList[lines][1]:
                                    new_e_iso_code = ethnoList[lines][0]
                                    if root not in root_list:
                                        root_list.append(root)
                                        for a in range(1, len(languagesList)-1):
                                            mult_codes = languagesList[a][7].replace('\"', '').replace("\n", '')
                                            mult_codes = mult_codes.split(' ')
                                            if new_e_iso_code in mult_codes:
                                                for b in range(1, len(dataList)):
                                                    final_code = languagesList[a][0].replace("\"", '')
                                                    if dataList[b][0] == final_code:
                                                        h.write(root + ', ')
                                                        h.write(', '.join(dataList[b]))
        h.close()

    if sys.argv[2] == 'w':
        print 'Using wals for family relations.'
        j = open("w_genus_datapoints.csv", 'a')
        k = open("w_family_datapoints.csv", 'a')
        for a in range(1, len(dataList)-1):
            wals_code = dataList[a][0]
            wals_code = '\"' + wals_code + '\"'
            for c in range(1, len(languagesList)-1):
                if wals_code == languagesList[c][0]:
                    family = languagesList[c][5]
                    genus = languagesList[c][4]
                    if sys.argv[3] == "family":
                        for d in range(1, len(languagesList)-1):
                            if languagesList[d][5] == family:
                                for e in range(1, len(dataList)-1):
                                        ethno_word = languagesList[d][0].replace('\"', '')
                                        if ethno_word == dataList[e][0]:
                                            print len(dataList)
                                            k.write(', '.join(dataList[e]))
                                            dataList = dataList[:e-1] + dataList[e:]
                                            a = 0
                    if sys.argv[3] == "genus":
                        for d in range(1, len(languagesList)-1):
                            if languagesList[d][4] == genus:
                                for e in range(1, len(dataList)-1):
                                        ethno_word = languagesList[d][0].replace('\"', '')
                                        if ethno_word == dataList[e][0]:
                                            k.write(', '.join(dataList[e]))
                                            dataList = dataList[:d-1] + dataList[d:]

        j.close()
        k.close()





def family_tree(x, y, depth=10):
    #if 
    j = open(family_file, 'r+')
    j.write(x[y])
    for z in range(1, len(x)-1):
        family_tree(x, y, depth=10)
    j.close


    #Or if we're using wals...
    if sys.argv[2] == 'w': 
        print 'Using wals for family relations.'



if __name__ == "__main__":
    if sys.argv[1] == 'test':
        phylogenetic()
    if sys.argv[1] == 'phy':
        print "Now sorting languages phylogenetically."
        phylogenetic()
    if sys.argv[1] == 'geo':
        print "Now sorting languages geograpically."
        geographic()
    if sys.argv[1] == 'pg':
        print "Now sorting with a mixture of phylogeneitc and geographically."
        phylogeo()
    if sys.argv[1] == 'contact':
        print "Now sorting by hard-coded contact languages."
        contact_lang()


















