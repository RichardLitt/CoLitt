"""
Simple learned signalling simulation with different biases

learn takes a signalling system, a meaning, a signal, and a learning rule of the form
[alpha, beta, gamma, delta] and adjusts the weights in that system appropriately
meaning, signal pair.

alpha refers to both meaning and signal active, beta refers to just meaning,
gamma to just signal, and delta to neither

pop_learn uses a list of meaning, signal pairs to train a whole population of
systems. pop_produce uses a population of systems to produce a list of 
meaning, signal pairs

ca_monte_pop lets us test the communicative accuracy of the whole population

Usage example:

population = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
pop_learn(population, pop_produce(population, 100), 100, [1, 0, 0, 0])
ca_monte_pop(population,10000)

Takes a population of two agents that will generate random data and uses 100 instances
of this random data to train the members of the same population a 100 times, using
a frequency-counting rule, and then tests the communicative accuracy of the resulting 
population.
"""

import random

def m_weights(system, signal):
    weights = []
    for m in system:
        weights.append(m[signal])
    return weights

def s_weights(system, meaning):
    return system[meaning]

def wta(items):
    maxweight = max(items)
    candidates = []
    for i in range(len(items)):
        if items[i] == maxweight:
            candidates.append(i)
    return random.choice(candidates)

def communicate(system1, system2, meaning):
    signal = wta(s_weights(system1, meaning))
    if wta(m_weights(system2, signal)) == meaning: 
        return 1
    else: 
        return 0

# ----- new code below -----

def learn(system, meaning, signal, rule):
    for m in range(len(system)):
        for s in range(len(system[m])):
            if m == meaning and s == signal: system[m][s] += rule[0]
            if m == meaning and s != signal: system[m][s] += rule[1]
            if m != meaning and s == signal: system[m][s] += rule[2]
            if m != meaning and s != signal: system[m][s] += rule[3]

def pop_learn(population, data, interactions, rule):
    for n in range(interactions):
        utterance = random.choice(data)
        learn(random.choice(population), utterance[0], utterance[1], rule)

def pop_produce(population, interactions):
    utterances = []
    for n in range(interactions):
        agent = random.choice(population)
        meaning = random.randrange(len(agent))
        signal = wta(s_weights(agent, meaning))
        utterances.append([meaning,signal])
    return utterances

def ca_monte_pop(population, trials):
    total = 0.
    for n in range(trials):
        speaker = random.choice(population)
        hearer = random.choice(population)
        total += communicate(speaker, hearer, random.randrange(len(speaker)))
    return total / trials
