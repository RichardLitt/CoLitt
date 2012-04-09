"""
Simple innate signalling simulation - communicating population

pop_update takes a list of agents and picks two at random to be
signaller and receiver for a random meaning. Each agent consists of 
a signalling system and 4 scores: the number of times 
they have successfully been understood, the number of times they have spoken,
the number of times they have successfully understood an interaction, and the
number of times they have heard an interaction, respectively.

Usage example:

population = [[[[3, 1], [0, 2]], [0, 0, 0, 0]],
              [[[1, 0], [0, 1]], [0, 0, 0, 0]],
              [[[0, 1], [1, 0]], [0, 0, 0, 0]]]

for i in range(10000): pop_update(population)

print population

Will pick one of these three agents to be speaker and another to be
hearer, and update scores accordingly, for 10000 interactions.
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
    if wta(m_weights(system2, signal)) == meaning: return 1
    else: return 0

# ----- new code below -----

def pop_update(population):
    s = random.randrange(len(population))
    h = random.randrange(len(population) - 1) 
    if h >= s: h += 1     # ensure speaker and hearer are different
    speaker = population[s]
    hearer = population[h]
    meaning = random.randrange(len(speaker[0]))
    success = communicate(speaker[0], hearer[0], meaning)
    speaker[1][0] += success
    speaker[1][1] += 1
    hearer[1][2] += success
    hearer[1][3] += 1
