sys = ['She cannot be used as a basis for the installation of a European constitution .', \
    'It cannot a basis for the establishment of a European constitution .', \
    'It can form the basis for a European constitution .']

refs = ['It cannot serve as a basis for the establishment of a European constitution .', \
        'It can not serve as a basis for the introduction of a European \
        constitution .']

def count():
    # Split the lines into words
    for ref in range(len(refs)):
        refs[ref] = refs[ref].split()
    for output in range(len(sys)):
        sys[output] = sys[output].split()

    # Set the n-gram length
    for output in sys:
        for w in range(1,5):
            matches = 0
            for ngram in range(len(output)):
                first_ref = 0
                sec_ref = 0
                for ref in refs:
                    for match in range(len(ref)-w):
                        # Let's hitch!
                        if output[ngram:ngram+w] == ref[match:match+w]:
                            #print output[ngram:ngram+w], ref[match:match+w]
                            if refs.index(ref) == 0: first_ref += 1
                            if refs.index(ref) == 1: sec_ref += 1
                if (first_ref > 0) or (sec_ref > 0): matches += 1
            # And not waste paper
            print 'Score for sys' + str(sys.index(output)+1) + ' n-gram ' \
                    + str(w) + ':' + '\t' + str(matches) + '/' + str(len(output)-w+1)

# Obscure comment to obscure code.
if __name__ == '__main__':
    count()
