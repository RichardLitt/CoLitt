"""
Cultural evolution simulation

simulation creates an initial population of agent with zero-ed out systems and
uses this to produce a data set of utterances. These utterances are used to train the
population at the next time step. Different methods to update the population are
included:

chain - this implements a 'transmission chain' in which, at each time step the whole
population is replaced

replacement - this implements the 'replacement method' whereby the oldest agent is
replaced by a new one each generation

closed - this implements the 'closed group' method, in which the population is static
and no new individuals are ever added

There are a number of global simulation parameters for simulation commented below.

Usage example:

simulation(20, 10000, 20)

This runs the simulation for 20 generations, with 10000 trials for the monte carlo 
calculation, and gives 20 points back for a graph.
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

# ----- new code below -----

meanings = 4          # number of meanings
signals = 4           # number of signals
interactions = 5000   # both the number of utterances produced and the number of times
                      # this set is randomly sampled for training.
size = 100            # size of population
method = 'closed'     # method of population update
rule = [0, 0, 0, 1]   # learning rule (alpha, beta, gamma, delta)

def new_agent():
    system = []
    for i in range(meanings):
        meaning = []
        for j in range(signals):
            meaning.append(0)
        system.append(meaning)
    return system

def new_population(size):
    population = []
    for i in range(size):
        population.append(new_agent())
    return population

def simulation(generations, trials, points):
    population = new_population(size)
    for i in range(generations):
        data = pop_produce(population, interactions)
        if method == 'chain': 
            population = new_population(size)
        if method == 'replacement':
            population = population[1:]   # This removes the first item of the list
            population.append(new_agent())
        pop_learn(population, data, interactions, rule)
        if (i % (generations/points) == 0):
            print(ca_monte_pop(population, trials))
    return population
