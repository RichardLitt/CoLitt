'''
The purpose of this code is to clean WALS.

Rough notes from Rory and Richard Skype Chat:
    ====================================

ok, so, you wanted the languages to be ordered by distances from each other. i presume the intention of that was so that all the close together language comparisons are on one end of the graph, and all the far away language comparisons are on the other end?
and that the intention is not to re-create a pseudomap of worldgeography
The intention was to make related languages appear in the graph
so that we can use it to look for linguistic areas
languages are generally related either geographically or phylogenetically

it would be REALLY INTERESTING if we did a contact model, as well, say, of English
now, this would be possible if we used, instead of features, a smaller subset, perhaps a single feature map

so i've realized the sorting method i outlined doesn't really work, because we're trying to sort two-dimensional data, not one-dimensional.
we could also combine features, create a feature similarity metric
so the issue i'm seeing is that their could be (will be) two pairs of languages - say, french and italian, and japanese and ainu - that have relatively small distances between them
these two comparisons would be right beside each other on the heat map
or at least, close, because they're both small distances
I was thinking we center the map on one language, and then either side will be the fallout
the issue is the ends - obviously, it means things aren't done possibly
like, connections won't be made between equidistant languages that may be related
and I don't have a solution to that.
what we could do is sort it lattitudally or longitudally
or, connections WILL be made between languages that are both x km from the center language, even if they're both in different directions

if we center, we can say look at the centric maps
also, we don't want to have a graph with millions of languages
limiting it to a subset - say 30 language
should really elleviate the issue
we could also just get all the data, and then use some matrix reordering or seriation algorithm to cluster everything together (but that's kinda backwards)
haha, yes, currently we have a 2678x2678 matrix, which is a little large
also, because comparisons are symmetrical, the graph will be too - or one half will be blank
(assuming both x and y orders are the same)

we still need to clean the WALS data: what is it - 16% full at the moment?
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

datapoints_file = "datapoints.csv" # WALS data
languages_file = "languages.csv" # WALS language details, inc. ISO codes
ethnologue = "ethnologue.csv" # Ethnologue scraped data, 2005
root_e_file = "root_e_file.csv" # The phylo file for ethnologue data for root entries
#output_file = "cleaned_datapoints.csv" # The final file for...
w_genus_data = "w_genus_datapoints.csv" # Data sorted by WALS hier. by genus
w_genus_data = "w_family_datapointss.csv" # Data sorted by WALS hier. by family

# This function reads in the file
def read_file(x):
    f = open(x, 'r+')
    lineList = f.readlines()
    return lineList

# Splits the lines, if you wish. Probably a good thing.
def split_lines(x, y):
    lineList = []
    for line in x:
        line = line.split(y)
        lineList.append(line)
    return lineList


# Defines how you want to sort these things

def phylogenetic():

    # load languages, datapoints
    languagesList = split_lines(read_file(languages_file), '\t')
    dataList = split_lines(read_file(datapoints_file), ',')

    # load a dict of Wals codes
    wals_code = ['wals_code',]
    for x in range(len(languagesList)):
        lang_code = languagesList[x][0].replace('\"', '')
        wals_code.append(lang_code)

    # make sure that all of the data is accounted for in wals_code
    for line in range(len(dataList)):
        if dataList[line][0] not in wals_code:
            print 'Something is broken'
            break


    # If we're dragging from Ethnologue and not WALS hierarchies
    if sys.argv[2] == 'e':
        print 'Using ethnologue for family relations.'

        #Open the ethnologue file 
        ethnoList = split_lines(read_file(ethnologue), '\t')
        root_list = []
        # Open the file
        h = open(root_e_file, 'a')

        # Used to avoid printing twice, repetition
        final_code_list = []

        # For the terminal count, to show completion
        print_count = 0

        # For line in the WALS data
        for line in range(1,len(dataList)-1):

            # Cross check with the WALS language file
            for lines in range(1, len(languagesList)-1):
                # shimming
                lang_code = languagesList[lines][0].replace('\"', '')
                if dataList[line][0] == lang_code:

                    # convert to ISO code from the language file
                    iso_code = languagesList[lines][7].replace('\"',\
                            '').replace("\n", '')
                    root = []

                    # Cross check with the ethnologue file
                    for lines in range(1, len(ethnoList)-1):
                        if iso_code == ethnoList[lines][0]:

                            # Choose out the roots and parents from Ethnologue
                            root = ethnoList[lines][1]
                            parents = ethnoList[lines][2]

                            # Find all roots in E.
                            for lines in range(1, len(ethnoList)-1):
                                if root == ethnoList[lines][1]:

                                    # For each root, find the ISO code
                                    new_e_iso_code = ethnoList[lines][0]

                                    # Why is this here? To stop repetition?
                                    #if root not in root_list:
                                    #root_list.append(root)

                                    # Take the new ISO codes back to the
                                    # Wals languaage list
                                    for a in range(1, len(languagesList)-1):
                                        # Shim for multiple ISO codes
                                        mult_codes = languagesList[a][7].replace('\"', '').replace("\n", '')
                                        mult_codes = mult_codes.split(' ')
                                        # shimming, selecting WALS code
                                        final_code = languagesList[a][0].replace("\"", '')

                                        # Compare, find the right one
                                        if new_e_iso_code in mult_codes:

                                            # For all of the WALS data
                                            for b in range(1, len(dataList)):

                                                # Find the right line
                                                if dataList[b][0] == final_code:

                                                    # If not already printed
                                                    if final_code not in \
                                                            final_code_list:

                                                        # Write to file
                                                        h.write(root + ', ')
                                                        h.write(', '.join(dataList[b]))

                                                        # Update previous printing
                                                        final_code_list.append(final_code)

                                                        # For terminal.
                                                        print_count += 1
                                                        print print_count

        # Close the file.
        h.close()


    # If we're dragging from WALS
    if sys.argv[2] == 'w':
        print 'Using wals for family relations.'

        #Open the two relevant output files
        j = open(w_genus_data, 'a')
        k = open(w_family_data, 'a')

        # Used to show in terminal what is happening 
        printed_codes = []
        print_count = 0

        # For every WALS data line
        for a in range(1, len(dataList)-1):
            # Find a code, shim it
            wals_code = dataList[a][0]
            wals_code = '\"' + wals_code + '\"'

            # Find the language line
            for c in range(1, len(languagesList)-1):
                if wals_code == languagesList[c][0]:

                    # Define family and Genus per entry
                    family = languagesList[c][5]
                    genus = languagesList[c][4]

                    # If we're outputting a family grouping
                    if sys.argv[3] == "family":

                        # For each entry in that family
                        for d in range(1, len(languagesList)-1):
                            if languagesList[d][5] == family:

                                # Go back to the WALS data
                                for e in range(1, len(dataList)-1):

                                        # Shim, find that entry
                                        fam_word = languagesList[d][0].replace('\"', '')
                                        if fam_word == dataList[e][0]:
                                            if fam_word not in printed_codes:

                                                # Append to already printed codes
                                                printed_codes.append(fam_word)

                                                # Write to file
                                                k.write(', '.join(dataList[e]))

                                                # Update print count
                                                print_count += 1
                                                print print_count

                    # If we're outputting for genus
                    if sys.argv[3] == "genus":

                        # For each entry in that genus
                        for d in range(1, len(languagesList)-1):
                            if languagesList[d][4] == genus:

                                # Go back to the WALS data
                                for e in range(1, len(dataList)-1):

                                        # Shim, find that entry
                                        fam_word = languagesList[d][0].replace('\"', '')
                                        if fam_word not in printed_codes: 

                                            # Append to already printed codes
                                            printed_codes.append(fam_word)

                                            # Write to file
                                            j.write(', '.join(dataList[e]))

                                            # Update print count
                                            print_count += 1
                                            print print_count

        j.close()
        k.close()




# Was going to be used in the ethnologue familie data, hasn't been worked yet.
def family_tree(x, y, depth=10):
    # if 
    j = open(family_file, 'r+')
    j.write(x[y])
    for z in range(1, len(x)-1):
        family_tree(x, y, depth=10)
    j.close




# This function cleans the data based on the amount of values it has filled.
# Note - this is not feature kind at the moment, but applies to all values.

#input_file = datapoints_file.csv # For now, this is a good idea. Eventually, more.
#lower_threshhold = .5 # Lowest amount of data permitted, as a percentage.
#output_file = "clean_data.csv" # Must be specified in argv.

def data_clean(lower_threshhold, input_file):

    output_file = 'clean-' + sys.argv[2].replace('.','') + '-' + sys.argv[3].replace('.csv', '')

    # Open files
    f = open(input_file, 'r+')
    l = open(output_file, 'a')
    lineList = f.readlines()

    # For printing on the terminal
    lines_printed = 0

    # For each language
    for line in lineList:
        line = line.split(',')
        values = 0

        # For each value recorded 
        for value in line:

            # If it isn't nothing, note that
            if value != '':
                values += 1

        # If it is more filled than the threshhold
        if values >= (float(lower_threshhold)*len(line)):
            # Write values
            l.write(','.join(line))

            # Print the amount of lines printed
            lines_printed += 1
            print lines_printed

    #Close file
    l.close()







if __name__ == "__main__":
    if sys.argv[1] == 'clean':
        data_clean(sys.argv[2], sys.argv[3])
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


















