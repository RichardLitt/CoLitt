"""
Cross-situational learning.

In this simulation, the learner doesn't have direct access to the speaker's meaning - instead the
context of use provides a set of candidate meanings. Each learning episode may provide a different
set of candidate meanings.

Over multiple learning episodes, the learner makes use of the cross-situational information,
by assuming that the 'true' meaning lies at the intersection of these sets of candidate meanings.

There are a number of global simulation parameters commented below.
Data is printed out after every (samples/datapoints)th episode.

Usage example:

xsl_simulation(10000,20)

This runs the simulation with the default global parameters, using 10000 trials for the monte carlo
calculation of communicative accuracy, and outputting 20 data points for plotting.
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

# ------- new code below ------------

meanings = 5               # number of meanings
signals = 5                   # number of signals
context_size = 3          # context size
samples = 500             # number of data samples to learn/produce in total
rule = [1, 0, 0, 1]         # learning rule

def new_agent(type):
    "create a new agent with an optimal or random signalling system"
    system = []
    for i in range(meanings):
        meaning = []
        for j in range(signals):
            if type == 'optimal':
                if i == j:
                    meaning.append(1)
                else:
                    meaning.append(0)
            if type == 'random':
                meaning.append(0)
        system.append(meaning)
    return system

def add_context(m):
    "add random context to meaning m"
    m_list = list(range(meanings))
    if m in m_list:
        m_list.remove(m)
    random.shuffle(m_list)
    context = m_list[ : (context_size-1)]
    context.append(m)
    return context
       
def produce_data(system, n):
    "produce data from system"
    data = []
    for i in range(n):
        meaning = random.randrange(len(system))
        signal = wta(s_weights(system,meaning))
        context = add_context(meaning)
        data.append([context,signal])
    return data
              
def multiple_meaning_learn(system,meaning_list,signal,rule):
    "learn a signal paired with multiple meanings"
    for m in range(len(system)):
        for s in range(len(system[m])):
            if m in meaning_list and s == signal: system[m][s] += rule[0]
            if m in meaning_list and s != signal: system[m][s] += rule[1]
            if m not in meaning_list and s == signal: system[m][s] += rule[2]
            if m not in meaning_list and s != signal: system[m][s] += rule[3]

def learn_data(system, data, n):
    "learn from data"
    for i in range(n):
        utterance = random.choice(data)
        multiple_meaning_learn(system, utterance[0], utterance[1], rule)

def xsl_simulation(trials, datapoints):
    "run cross-situational learning simulation"
    speaker = new_agent('optimal')
    hearer = new_agent('random')
    for i in range(datapoints):
        data = produce_data(speaker, int(samples/datapoints))
        learn_data(hearer, data, int(samples/datapoints))
        print(ca_monte(speaker, hearer, trials))
    return hearer
    
    
