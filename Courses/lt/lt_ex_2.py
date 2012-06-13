import re

# Open the files
fen = open('europarl.de-en.tok.en', 'r+').readlines()
fde = open('europarl.de-en.tok.de', 'r+').readlines()
# Training files
en = open('en', 'r+').readlines()
fr = open('fr', 'r+').readlines()

o = open('RL_output', 'w+')

def update_prob(word_freq):
    word_prob = word_freq
    #print ''
    #o.write('\n')
    #print 'Global probabilities: '
    #o.write('Global probabilities: \n')

    # This may be a lazy way, but it works.
    # Use the frequency list to update accordingly
    for word in word_prob.iterkeys():
        if (word == ' '): continue
        # The sum of the frequencies
        frequency_sum = 0

        # Add them on
        for fword in word_prob[word].iterkeys():
            if (fword == ' '): continue
            frequency_sum += word_prob[word][fword]

        # and then divide by the amount total
        for fword in word_prob[word].iterkeys():
            if (fword == ' '): continue
            word_prob[word][fword] = word_prob[word][fword] /\
                    frequency_sum

        # #print it out
        #print word, word_prob[word]
        #o.write(word + str(word_prob[word]) + '\n')
    #print ''
    #o.write('\n')

    return word_freq, word_prob

# Global Frequency Estimates
def gfe(language1, language2):
    #print 'Global frequencies: '
    #o.write('Global frequencies: \n')
    # Dictionaries are the way to go.
    word_freq = {}
    # For each line
    for idx, line in enumerate(language1):
        # Shim the lines
        line = line.replace('\n', '').split(' ')
        fline = language2[idx].replace('\n', '').split(' ')
        # For each word in the other language, for each first lang word
        for word in line:

            #Some cleaning regex
            word = re.sub(r'(^[^A-Za-z]+|[^A-Za-z]+$)',' ', word).lower()

            # This text is not aligned properly. Here is a workaround. 
            if (len(line) == 1) and (line[0] == '\n'): continue
            if word == ' ': continue

            for fword in fline:

                #Regexing
                fword = re.sub(r'(^[^A-Za-z]+|[^A-Za-z]+$)',' ', fword).lower()
                # Because in this universe, silences are not words. 
                if (fword == ' ') or (word == ' '): continue

                # Create a dictionary if it doesn't have it already
                if not word_freq.has_key(word):
                    word_freq[word] = {}
                if not word_freq[word].has_key(fword):
                    # Add it to the word frequency list
                    word_freq[word][fword] = 1/float(len(fline))
                else:
                    word_freq[word][fword] = word_freq[word][fword] +\
                    1/float(len(fline))
            # #print it out
            #print word, word_freq[word]
            #o.write(word + str(word_freq[word]) + '\n')
    return update_prob(word_freq)

def iterate(language1, language2, iterations):
    # Get the first iterations
    word_freq, word_prob = gfe(language1, language2)
    for i in range(iterations-1):
        print 'Iteration ' + str(i+2)
        #print 'New frequency updates: '
        #o.write('New frequency updates: \n')
        new_freq = {}

        # This is the local frequency estimates
        for idx, line in enumerate(language1):

            # Shim the lines
            line = line.replace('\n', '').split(' ')
            fline = language2[idx].replace('\n', '').split(' ')
            for fword in fline:

                #Tyrannosaurus regex
                fword = re.sub(r'(^[^A-Za-z]+|[^A-Za-z]+$)',' ', fword).lower()

                total_prob = 0
                for word in line:

                    # This text is not aligned properly. Here is a workaround. 
                    if (len(line) == 1) and (line[0] == '\n'): continue

                    # Because in this universe, silences are not words. 
                    if (fword == ' ') or (word == ' '): continue

                    word = re.sub(r'(^[^A-Za-z]+|[^A-Za-z]+$)',' ', word).lower()
                    if word_prob.has_key(word):
                        if word_prob[word].has_key(fword):
                            total_prob += word_prob[word][fword]
                #print fword + ': '
                #o.write(fword + ': \n')

                for word in line:

                    #All hail Regex!
                    word = re.sub(r'(^[^A-Za-z]+|[^A-Za-z]+$)',' ', word).lower()

                    # Because in this universe, silences are not words. 
                    if (fword == ' ') or (word == ' '): continue

                    # Create a dictionary if it doesn't have it already
                    if not new_freq.has_key(word):
                        new_freq[word] = {}
                    # Add it to the word frequency list
                    new_freq[word][fword] = word_prob[word][fword]\
                            /total_prob
                    #print '\t', word, '\t', new_freq[word][fword]
                    #o.write('\t' + word + '\t' + str(new_freq[word][fword]) +\
                    #'\n')



        # And here we get the global frequency estimates
        agg_freq = {}
        for idx, line in enumerate(language1):

            # Shim the lines
            line = line.replace('\n', '').split(' ')
            fline = language2[idx].replace('\n', '').split(' ')
            # For each word in the other language, for each first lang word
            for word in line:

                # This text is not aligned properly. Here is a workaround. 
                if (len(line) == 1) and (line[0] == '\n'): continue

                # Oedipus regex
                word = re.sub(r'(^[^A-Za-z]+|[^A-Za-z]+$)',' ', word).lower()

                for fword in fline:
                    fword = re.sub(r'(^[^A-Za-z]+|[^A-Za-z]+$)',' ', fword).lower()

                    # Because in this universe, silences are not words. 
                    if (fword == ' ') or (word == ' '): continue

                    # Create a dictionary if it doesn't have it already
                    if not agg_freq.has_key(word): agg_freq[word] = {}

                    # Add it to the word frequency list
                    if not agg_freq[word].has_key(fword):
                        agg_freq[word][fword] = new_freq[word][fword]

                    else:
                        agg_freq[word][fword] = agg_freq[word][fword] +\
                        new_freq[word][fword] 

        word_freq, word_prob = update_prob(agg_freq)

        if i == 1:
            for word in word_prob.iterkeys():
                o.write(word + ' ' + str(word_prob[word]) + '\n')


'''
# Failed attempt to write this in a table. Am I missing a package or something?
        if i == 0:
            fd = []
            for word in sorted(word_prob.iterkeys()):
                for fword in word_prob[word]:
                    fd.append(fword)
            o.write('\t,')
            fd = sorted(set(fd))
            for x in range(len(fd)): o.write(fd[x] + ',')
            o.write('\n')
            for word in word_prob.iterkeys():
                o.write(word + ',')
                prev_index = 0
                for fword in word_prob[word]:
                    windex = fd.index(fword)-prev_index
                    for x in range(windex-1): 
                        o.write(',')
                    o.write(str(word_prob[word][fword])+',')
                    prev_index = fd.index(fword)+1
                for x in range(len(fd)-prev_index): 
                    o.write(',')
                o.write('\n')
'''

        # And then loop...


if __name__ == "__main__":
    iterate(fen, fde, 3)
