"""
Simple innate signalling system simulation - evolving population

simulation creates an initial population of random agents and evolves this
population over a number of generations, printing total fitness at each
generation. Fitness is calculated after a certain number of random interactions
among the population and is determined by the proportion of successful 'sends' 
and successful 'receives' each scaled by a weighting factor. Parents are 
selected with a probability proportional to their fitness and there is a chance
of mutation of each weight in the vocabulary. simulation returns
the final population.
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

def pop_update(population):
    s = random.randrange(len(population))
    h = random.randrange(len(population) - 1) 
    if h >= s: 
        h += 1     # ensure speaker and hearer are different
    speaker = population[s]
    hearer = population[h]
    meaning = random.randrange(len(speaker[0]))
    success = communicate(speaker[0], hearer[0], meaning)
    speaker[1][0] += success
    speaker[1][1] += 1
    hearer[1][2] += success
    hearer[1][3] += 1

# ----- new code below -----

from copy import deepcopy

mutation_rate = 0.01   # probability of mutation per weight
mutation_max = 1       # maximum value for a weight
send_fitness = 5       # weighting factor for send score
receive_fitness = 5    # weighting factor for receive score
meanings = 3           # number of meanings
signals = 3            # number of signals
interactions = 5000    # number of interactions per generation
size = 100             # size of population

def fitness(agent):
    s = agent[1][0]
    sn = agent[1][1]
    r = agent[1][2]
    rn = agent[1][3]
    if sn == 0: 
        sn = 1
    if rn == 0: 
        rn = 1
    return ((s/sn) * send_fitness + (r/rn) * receive_fitness) + 1

def sum_fitness(population):
    total = 0
    for agent in population:
        total += fitness(agent)
    return total
    
def mutate(system):
    for m in range(meanings):
        for s in range(signals):
            if random.random() < mutation_rate:
                system[m][s] = random.randint(0, mutation_max)

def pick_parent(population,sum_f):
    accum = 0
    r = random.uniform(0, sum_f)
    for agent in population:
        accum += fitness(agent)
        if r < accum:
            return agent

def new_population(population):
    new_p = []
    sum_f = sum_fitness(population)
    print(sum_f)
    for i in range(len(population)):
        system = deepcopy(pick_parent(population, sum_f)[0])
        mutate(system)
        new_p.append([system, [0., 0., 0., 0.]])
    return new_p

def random_system():
    system = []
    for i in range(meanings):
        meaning = []
        for j in range(signals):
            meaning.append(random.randint(0, mutation_max))
        system.append(meaning)
    return system

def random_population(size):
    population = []
    for i in range(size):
        population.append([random_system(), [0., 0., 0., 0.]])
    return population

def simulation(generations):
    population = random_population(size)
    for i in range(generations):
        for j in range(interactions):
            pop_update(population)
        population = new_population(population)
    return population
