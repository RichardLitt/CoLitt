import random

noise = 0.2       # The probability of a random utterance
variables = 2     # The number of different variables in the language
variants = 2      # The number of different variants each variable can take
learning = 'map'  # The type of learning ('map' or 'sample')
bias = 0.6        # The preference for completely regular languages relative to others

def produce(lang, variable):
    "Produces a variant for a particular language and variable"
    if random.random() < noise:
        return random.randrange(variants)
    else:
        return lang[variable]

def generate_data(lang, n):
    "Generate a list of n [variable, variant] pairs from a language"
    data = []
    for i in range(n):
        variable = random.randrange(len(lang))
        variant = produce(lang, variable)
        data.append([variable, variant])
    return data

def prior(lang):
    "Gives the prior bias for a particular language. Note that this must sum to 1 for all languages"
    for v in lang:
        if v != lang[0]:
            return (1 - bias) / (pow(variants, variables) - variants)
    else:
        return bias / variants 

def likelihood(lang, data):
    "Calculates P(data | lang)"
    total = 1
    for pair in data:
        if pair[1] == lang[pair[0]]:
            total = total * ((1 - noise) + (noise / variants))
        else:
            total = total * (noise / variants)
    return total

def all_langs(length):
    "Returns a list of all the possible languages"
    if length == 0:
        return [[]]
    else:
        result = []
        smaller_langs = all_langs(length - 1)
        for l in smaller_langs:
            for v in range(variants):
                result.append(l + [v])
        return result

def map_lang(data):
    "Picks the maximum a posteriori language for a given list of [variable, variant] pairs"
    maxp = 0
    candidates = []
    for l in all_langs(variables):
        posterior = likelihood(l, data) * prior(l)
        if posterior == maxp:
            candidates.append(l)
        if posterior > maxp: 
            maxp = posterior
            candidates=[l]
    return random.choice(candidates)

def roulette_wheel(scores):
    "Given a list of scores, returns a position in that list randomly in proportion to its score"
    total = 0
    for s in scores:
        total += s
    r = random.uniform(0,total)
    total = 0
    for i in range(len(scores)):
        total += scores[i]
        if r < total:
            return i

def sample_lang(data):
    "Picks a language proportional to it's posterior probability given a list of [variable, variant] pairs"
    scores = []
    for l in all_langs(variables):
        posterior = likelihood(l, data) * prior(l)
        scores.append(posterior)
    return all_langs(variables)[roulette_wheel(scores)]    

def simulation(generations, bottleneck, points):
    "Run a single chain for a particular bottleneck"
    lang=random.choice(all_langs(variables))
    for i in range(generations):
        if points != 0:
            if (i % (generations/points)) == 0:
                print lang
        data = generate_data(lang, bottleneck)
        if learning == 'map':
            lang=map_lang(data)
        if learning == 'sample': 
            lang=sample_lang(data)
    return lang

def simulation_distribution(generations, bottleneck, trials):
    "Run a lot of simulations and report the distribution of final languages"
    langs=all_langs(variables)
    counts=[]
    for l in langs:
        counts.append([l,0])
    for i in range(trials):
        lang=simulation(generations, bottleneck, 0)
        for c in counts:
            if c[0] == lang:
                c[1] += 1
    return counts
