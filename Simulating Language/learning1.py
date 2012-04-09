"""
Simple learned signalling system simulation

learn takes a signalling system, a meaning, and a signal and increases the weight for that
meaning, signal pair. 

train does the same but for a list of meaning-signal pairs.

Usage example:

system = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
train(system, [[0, 0], [1, 1], [2, 2]])

This example changes the signalling system so that it has 1s on the diagonal.
ca_monte can be used as before to test whether an agent that has learned a particular 
signalling system can talk to another one.
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

# ----- new code below -----

def learn(system, meaning, signal):
    system[meaning][signal] += 1

def train(system, word_list):
    for pair in word_list:
        learn(system, pair[0], pair[1])

#>>> train(s,[[0,1],[1,0]]) <this is how you call up word_list, since it is essentially only a matrix
#>>> s <if you then look, as in here, you'll find that s (or whatever) has learnt.
#[[0, 1, 2], [1, 1, 0], [0, 0, 0], [1, 0, 0]]

