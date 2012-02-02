'''
The purpose of this code is to clean and sort WALS.
Written by Richard Littauer. 

Released into the public domain like stocked trout into the sea.

The commands needed to run this file can be seen at the bottom of the file next
to the name_main function. 


Things to be improved upon:

    - The ethnologue parents function, while it sorts for immediate parent
      nodes, can't do more than that, and can't find the upper nodes. This
      means that when the languages mentioned aren't in the WALS data, there's
      not much left. Out of the top 9 parents that have more than 25 languages,
      only 28 languages are left after going back to WALS when the data has
      been cleaned to 15%. That's almost nothing.

      On the other hand, there's not much to be done about this. They .xml
      isn't in the ethnologue file we have, and involving this would involve
      adding in another document and crosschecking again. This can be done, but
      not neccessarily at the moment without that .xml file for the trees. If
      this is done, we can also integrate MultiTree. This is a good area for
      future work.

      Neither can you hard code in trees, which might be a nice idea.

    - There is no function currently to jointly graph phylogenetic and
      geographical information in some sort of dependent variable way. There
      should be one, as these are definitely linked together.

      However, doing one without seeing how the graphics work completely would
      be premature. It might be possible to feed the geo-sorted file into the
      phylogenetic code, but that would also be premature at this stage.

    - Dictionaries would have been a better way to do this, if you want to
      speed it up. As for now, it works, so I don't much see the need.

      The code is also inefficient, as there is a lot of repeated code. It
      would be better to take some of this out of the arg if statements and
      into separate functions, but I haven't had the time to rework this entire
      code - and if it works, it works.

    - This currently spits out distance lists sorted from least to first, not
      using the centric pairing on either side we're going to need for the heat
      graphs.

      This is the plan, as R will be enough to suitably deal with the code
      itself. It's most likely an easy function to do, but I haven't done it
      here, as I assume it can be easier done after writing to the file and
      feeding it into R, instead of here. This assumption may be wrong.

    - It would be nice to be able to select langauges and run a graph based on
      them, instead of doing all languages and then sorting through. It would
      also be nice to be able to selectively choose which languages you want to
      graph against which other ones, in order to test things such as contact.
      However, it is difficult to say whether we, or WALS, has enough
      diachronic data to show contact that couldn't simply be done with
      geographic distance, as large contact eras are, I assume, relatively
      recent (after the Age of Exploration.)

'''

import sys

datapoints_file = "datapoints.csv" # WALS data
languages_file = "languages.csv" # WALS language details, inc. ISO codes
ethnologue = "ethnologue.csv" # Ethnologue scraped data, 2005
distance_file = "distances.csv" # Distances file

w_genus_data = "w_genus_data.csv" # Data sorted by WALS hier. by genus
w_family_data = "w_family_data.csv" # Data sorted by WALS hier. by family
w_subfamily_data = "w_subfamily_data.csv" # WALS Data by subfamily hier

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

def phylogenetic(input_file):

    # load languages, datapoints
    languagesList = split_lines(read_file(languages_file), '\t')
    dataList = split_lines(read_file(input_file), ',')

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
    if sys.argv[3] == 'e':
        print 'Using ethnologue for family relations.'

        # Open the ethnologue file 
        ethnoList = split_lines(read_file(ethnologue), '\t')
        root_list = []

        # Used to avoid printing twice, repetition
        final_code_list = []

        # For the terminal count, to show completion
        print_count = 0

        # For use later in excluding small parent trees
        # Trained on a sort function for all parent nodes with 25+ leaves
        # This works for 15% filled - it may not for more. Keep that in mind. 
        parent_list = ['evan', 'ekir', 'mixt', 'aztc', 'zapc', \
                'arab', 'hkch', 'saun', 'lmal']

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

                            # If we're looking for the large root tree
                            if sys.argv[4] == 'root':

                                # Find all roots in E.
                                for lines in range(1, len(ethnoList)):
                                    if root == ethnoList[lines][1]:

                                        # For each root, find the ISO code
                                        new_e_iso_code = ethnoList[lines][0]

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

                                                            # Open the file
                                                            h = 'e-' + \
                                                            sys.argv[4] + '-'+\
                                                            sys.argv[2]

                                                            h = open(h, 'a')

                                                            # Write to file
                                                            h.write(root + ', ')
                                                            h.write(', '.join(dataList[b]))

                                                            # Update previous printing
                                                            final_code_list.append(final_code)

                                                            # For terminal.
                                                            print_count += 1
                                                            print print_count

                            # If we're looking for the smaller subfamily trees
                            if sys.argv[4] == 'parents':

                                # Find amount of immediate parent nodes
                                # repeated
                                parent_lines = 0

                                # For each language in Ethnologue
                                for lines in range(1, len(ethnoList)):

                                    #If the parent from above matches
                                    if parents == ethnoList[lines][2]:

                                        #Update the counter
                                        parent_lines += 1

                                        # This code was used to train the
                                        # parent_list seen above. Uncomment to
                                        # reuse.

                                        # if parent_lines >= 25:
                                        #    if parents not in parent_list:
                                        #        parent_list.append(parents)


                                        # If it is in one of the nine large
                                        # leaf families
                                        if parents in parent_list:

                                            # For each root, find the ISO code
                                            new_e_iso_code = ethnoList[lines][0]

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

                                                                # Rename the file
                                                                h = 'e-' + \
                                                                sys.argv[4] + '-'+\
                                                                sys.argv[2]

                                                                # Open file
                                                                h = open(h, 'a')

                                                                # Write to file
                                                                h.write(parents + ', ')
                                                                h.write(', '.join(dataList[b]))

                                                                # Update previous printing
                                                                final_code_list.append(final_code)

                                                                # For terminal.
                                                                print_count += 1
                                                                print print_count


        # Close the file.
        h.close()


    # If we're dragging from WALS
    if sys.argv[3] == 'w':
        print 'Using WALS for family relations.'

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

                    # Define family, Genus, and subfam per entry
                    family = languagesList[c][5]
                    genus = languagesList[c][4]
                    subfamily = languagesList[c][6]

                    # If we're outputting a family grouping
                    if sys.argv[4] == "family":

                        # For each entry in that family
                        for d in range(1, len(languagesList)):
                            if languagesList[d][5] == family:

                                # Go back to the WALS data
                                for e in range(1, len(dataList)):

                                        # Shim, find that entry
                                        fam_code = languagesList[d][0].replace('\"', '')
                                        if fam_code == dataList[e][0]:
                                            if fam_code not in printed_codes:

                                                # Append to already printed codes
                                                printed_codes.append(fam_code)

                                                # Open file
                                                j = open(w_family_data, 'a')

                                                # Write to file
                                                j.write(', '.join(dataList[e]))

                                                # Update print count
                                                print_count += 1
                                                print print_count

                                                j.close()

                    # If we're outputting for genus
                    if sys.argv[4] == "genus":

                        # For each entry in that genus
                        for d in range(1, len(languagesList)):
                            if languagesList[d][4] == genus:

                                # Go back to the WALS data
                                for e in range(1, len(dataList)):

                                        # Shim, find that entry
                                        gen_code = languagesList[d][0].replace('\"', '')
                                        if gen_code == dataList[e][0]:
                                            if gen_code not in printed_codes: 

                                                # Append to already printed codes
                                                printed_codes.append(gen_code)

                                                # Open file
                                                j = open(w_genus_data, 'a')

                                                # Write to file
                                                j.write(', '.join(dataList[e]))

                                                # Update print count
                                                print_count += 1
                                                print print_count

                                                j.close()

                    # If we're outputting for subfamily
                    if sys.argv[4] == "subfamily":

                        # For each entry in that subfamily
                        for d in range(1, len(languagesList)):
                            if languagesList[d][6] == subfamily:

                                # Go back to the WALS data
                                for e in range(1, len(dataList)):

                                        # Shim, find that entry
                                        subfam_code = languagesList[d][0].replace('\"', '')
                                        if subfam_code == dataList[e][0]:
                                            if subfam_code not in printed_codes:

                                                # Append to already printed codes
                                                printed_codes.append(subfam_code)

                                                # Open file
                                                j = open(w_subfamily_data, 'a')

                                                # Write to file
                                                j.write(', '.join(dataList[e]))

                                                # Update print count
                                                print_count += 1
                                                print print_count

                                                j.close()


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


# This will be fully added an integrated when we've run a few more of the other
# ones and know more fully how the graphics look, and what we can do with them.

def phylogeo(input_file, lower_threshhold):
     f = open(input_file, 'r+')
     g = open(distance_file, 'r+')



'''
This function cleans the data based on the amount of values it has filled.
Note - this is not feature kind at the moment, but applies to all values.

input_file = datapoints_file.csv # For now, this is a good idea. Eventually, more.
lower_threshhold = .5 # Lowest amount of data permitted, as a percentage.
output_file = "clean_data.csv" # Must be specified in argv.
'''

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
    print "Lines printed: " + str(lines_printed) + "."

    # Close file
    l.close()



if __name__ == "__main__":

    # If we're cleaning the data
    # Examples:

    # python clean.py clean .3 datapoints.csv

    if sys.argv[1] == 'clean':
        data_clean(sys.argv[2], sys.argv[3])

    # If we're just going with the hierarchies
    # Examples:

    # python clean.py phy clean-25-datapoints e root
    # python clean.py phy clean-25-datapoints e parents
    # python clean.py phy clean-25-datapoints w family
    # python clean.py phy clean-25-datapoints w subfamily
    # python clean.py phy clean-25-datapoints w genus


    if sys.argv[1] == 'phy':
        print "Now sorting languages phylogenetically."
        phylogenetic(sys.argv[2])

    # If we're sorting by distance (must be cleaned first)
    # Examples:

    # python clean.py geo clean-25-datapoints 15 radius 500
    # python clean.py geo clean-25-datapoints 15 languages 25

    if sys.argv[1] == 'geo':
        print "Now sorting languages geographically."
        geographic(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    # Not yet coded, and may not be. 
    if sys.argv[1] == 'pg':
        print "Now sorting with a mixture of phylogenetic and geographically."
        phylogeo(sys.argv[2], sys.argv[3])

'''
Commands to use:

    python clean.py clean .5 datapoints.csv

    python clean.py phy clean-25-datapoints e root
    python clean.py phy clean-25-datapoints e parents
    python clean.py phy clean-25-datapoints w family
    python clean.py phy clean-25-datapoints w subfamily
    python clean.py phy clean-25-datapoints w genus

    python clean.py geo clean-25-datapoints 15 radius 500
    python clean.py geo clean-5-datapoints 15 languages 25

'''
