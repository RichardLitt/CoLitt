'''
The purpose of this code is to clean and sort WALS.
    ====================================

Ordering:
    For vector relations, we have an issue where to center the matrix.
    If centred on a point, both ends may be close or far apart - one
    can only stare at the center of the graph for information.

    We could sort them lattitudinally or longitudinally - consider the case of
    a Dravidian language at the south of India. This would work well, here. Or
    Patagonian. Japanese would work - but we don't have the dialect scales, so
    this may not show us anything, especially not with WALS. This helps us in
    forcing our hand to make smaller maps - say, 30 languages - instead of
    massive ones. 


    We could also plot on a world map, but that would not be a heat map. An
    option for this would be to color gradiantly based on certain featurs - for
    instance, color could indicate phoneme size. 

    Another option would be a matrix map of some sort - Again, not a heat map,
    and beyond the scale of this current study.

Relations:
    Languages are related either phylogenetically, or geographically. There is
    also a possible Contact option, but we do not have the proper typological
    details for this, nor historic details.

    Relations are defined by features. A possibility is combining features, and
    creating a feature similarity metric - for instance, aligning various types
    of syntactic universals together.

    Here, it is possible to sort phylogenetically by WALS hierarchies, or by
    ethnologue hierarchies. There is no real difference between them. Another
    option would be to use MultiTree for identified trees. WALS data can be
    sorted by Family or Genus, not yet by subfamily. Ethnologue data can
    currently only be calibrated by the overarching parents, and not by
    sub-roots, although this would be useful.

Distance:
    For each language, the distance has been calculated. Currently we have a
    2678x2678 matrix, which is a little large.

    Geographical distances can be calculated by radius distance from the
    centroid, or the amount of languages specified that pass the cleaning test
    and are closes to the centroid. 

Cleaning:
    The WALS data can be cleaned with the data_clean() function. It should be
    noted that WALS is sparse, with only 76492 datapoints for 2678 languages,
    which, at 144 features, is only 19% full. This may not even be the right
    way of seeing it, however. 



'''

import sys

datapoints_file = "datapoints.csv" # WALS data
languages_file = "languages.csv" # WALS language details, inc. ISO codes
ethnologue = "ethnologue.csv" # Ethnologue scraped data, 2005
distance_file = "distances.csv" # Distances file

root_e_file = "root_e_file.csv" # The phylo file for ethnologue data for root entries
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
        for line in range(1,len(dataList)):

            # Cross check with the WALS language file
            for lines in range(1, len(languagesList)):
                # shimming
                lang_code = languagesList[lines][0].replace('\"', '')
                if dataList[line][0] == lang_code:

                    # convert to ISO code from the language file
                    iso_code = languagesList[lines][7].replace('\"',\
                            '').replace("\n", '')
                    root = []

                    # Cross check with the ethnologue file
                    for lines in range(1, len(ethnoList)):
                        if iso_code == ethnoList[lines][0]:

                            # Choose out the roots and parents from Ethnologue
                            root = ethnoList[lines][1]
                            parents = ethnoList[lines][2]

                            # Find all roots in E.
                            for lines in range(1, len(ethnoList)):
                                if root == ethnoList[lines][1]:

                                    # For each root, find the ISO code
                                    new_e_iso_code = ethnoList[lines][0]

                                    # Why is this here? To stop repetition?
                                    #if root not in root_list:
                                    #root_list.append(root)

                                    # Take the new ISO codes back to the
                                    # Wals languaage list
                                    for a in range(1, len(languagesList)):
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
        for a in range(1, len(dataList)):
            # Find a code, shim it
            wals_code = dataList[a][0]
            wals_code = '\"' + wals_code + '\"'

            # Find the language line
            for c in range(1, len(languagesList)):
                if wals_code == languagesList[c][0]:

                    # Define family and Genus per entry
                    family = languagesList[c][5]
                    genus = languagesList[c][4]

                    # If we're outputting a family grouping
                    if sys.argv[3] == "family":

                        # For each entry in that family
                        for d in range(1, len(languagesList)):
                            if languagesList[d][5] == family:

                                # Go back to the WALS data
                                for e in range(1, len(dataList)):

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
                        for d in range(1, len(languagesList)):
                            if languagesList[d][4] == genus:

                                # Go back to the WALS data
                                for e in range(1, len(dataList)):

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



'''
# Was going to be used in the ethnologue familie data, hasn't been worked yet.
def family_tree(x, y, depth=10):
    j = open(family_file, 'r+')
    j.write(x[y])
    for z in range(1, len(x)-1):
        family_tree(x, y, depth=10)
    j.close
'''


'''
This function will sort according to geographic distance

Geographical distance:
    Instead, going for a set number of languages with full data in a given
    area. This can be manually reset as desired. One should only run
    geographic() on cleaned data.
'''

def geographic(input_file, lower_threshhold, top_bound, top_bound_value):

    # Open files
    f = open(input_file, 'r+')
    g = open(distance_file, 'r+')

    # For printing in the terminal
    lines_sorted = 0

    # Makes a list of all of the languages in the distance file, for sorting.
    language_row = []
    geoList = split_lines(read_file(distance_file), '\t')
    for x in range(len(geoList[0])):
        code = geoList[0][x].replace('\n', '')
        language_row.append(code)

    # For each language in input file
    lineList = f.readlines()

    # Makes a list of each language in the cleaned input data.
    language_f_low = []
    for line in lineList:
        line = line.split(',')
        language_f_low.append(line[0])

    # For each language
    for line in lineList[1:]:
        line = line.split(',')

        # Find the wals_code
        wals_code = line[0]

        # Find where it is in the distance file
        x = language_row.index(wals_code)

        # Make an empty list to be populated by language distances
        stored_values = []

        # For every distance measurement (all languages)
        for value in range(1, len(geoList[x])):
            # shim
            if geoList[x][value] != 'NA':
                if geoList[x][value] != '0.0':

                    # Append horiztonal distance measures
                    stored_values.append([value, float(geoList[x][value])])

            # shim
            if geoList[value][x] != 'NA':
                if geoList[value][x] != '0.0':

                # Make sure the crux value isn't repeated
                    if geoList[x][value] != geoList[value][x]:

                        # Append vertical distance measures
                        stored_values.append([value, float(geoList[value][x])])

        # Sort the values and their indices
        sorted_values = sorted(stored_values, key=lambda x: x[1])


        # The amount of languages searched through
        total_searched = 0

        # If we're measuring amounts of languages by radius
        if top_bound == 'radius':

            # The maximum amount allowable
            maximum_radius = top_bound_value

            # To be populated by the closest, non-sparse languages
            languages_list = []

            # Going through the sorted distance lists
            for y in sorted_values:

                # If the top bound hasn't been met yet, cont. Shim.
                if y[1] != float(0.0):
                    if int(y[1]) <= int(maximum_radius):

                        # If 25 are met, cut it off. The heat maps we're using
                        # won't accept much more.
                        if len(languages_list) <= int(24):

                            # If in the cleaned file
                            target_wals_code = language_row[y[0]]
                            if target_wals_code in language_f_low:

                                # Add to lang_list
                                languages_list.append(y)

                            # Add to the total amount known, to see sparseness
                            total_searched += 1

            # If there aren't enough languages that fit, delete entry
            if len(languages_list) <= int(lower_threshhold):
                languages_list = []

        # If we're measuring merely by amount near
        if top_bound == 'languages':

            # The amount in the area we'll take
            maximum_areal_languages = int(top_bound_value)

            # List to be populated by the chosen
            languages_list = []

            # Starting with the closest languages
            for y in sorted_values:

                # Shim
                if y[1] != float(0.0):

                    # If in cleaned data
                    target_wals_code = language_row[y[0]]
                    if target_wals_code in language_f_low:

                        # If we haven't got enough yet
                        if len(languages_list) <= int(maximum_areal_languages-1):

                            # Add it in.
                            languages_list.append(y)

                    # Add to the total amount known, to see sparseness
                    total_searched += 1

            # If there aren't enough.
            if len(languages_list) <= int(lower_threshhold):
                languages_list = []

        # For the languages chosen
        for language in languages_list:

            # Find the WALS code
            wals_code = language_row[language[0]]

            # Find the index where its information lies
            wals_index = language_f_low.index(wals_code)

            # Make the output name. 
            output_file = 'geo-' + sys.argv[2] + '-' + sys.argv[4][0] + '-' +\
            sys.argv[5] + '-' + str(total_searched)

            h = open(output_file, 'a')
            h.write(line[0] + ',' + str(language[1]) + ',' + lineList[wals_index])

    h.close()






# This function cleans the data based on the amount of values it has filled.
# Note - this is not feature kind at the moment, but applies to all values.

# input_file = datapoints_file.csv # For now, this is a good idea. Eventually, more.
# lower_threshhold = .5 # Lowest amount of data permitted, as a percentage.
# output_file = "clean_data.csv" # Must be specified in argv.

def data_clean(lower_threshhold, input_file):

    # The name of the output file changes for variables involved
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

    # If we're cleaning the data
    if sys.argv[1] == 'clean':
        data_clean(sys.argv[2], sys.argv[3])

    # If we're just going with the hierarchies
    if sys.argv[1] == 'phy':
        print "Now sorting languages phylogenetically."
        phylogenetic()

    # If we're sorting by distance (must be cleaned first)
    if sys.argv[1] == 'geo':
        print "Now sorting languages geograpically."
        geographic(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    # Not yet coded, may not be. 
    if sys.argv[1] == 'pg':
        print "Now sorting with a mixture of phylogenetic and geographically."
        phylogeo()
        contact_lang()
