"""
Simple innate signalling simulation

ca_monte returns communicative accuracy between two signal systems using
monte carlo simulation. Systems are expressed as a list of lists of
association weights. Matrix rows are meanings, columns are signals. Production
and reception are winner-take-all.

Usage example:

system = [[1, 0, 0], [0, 1, 0], [0, 1, 1]]
ca_monte(system, system, 10000)

Returns expected communicative success of a homogenous population with
three meanings and three signals, but with some homonymy and synonymy.
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

def ca_monte(system1, system2, trials):
    total = 0.
    for n in range(trials):
        total += communicate(system1, system2, random.randrange(len(system1)))
    return total / trials
