"""Meaning Creation

Meanings are no longer provided innately, but are created by agents in order to discriminate
between objects in the world.

Objects are lists of (feature id, feature value) pairs.

Corresponding to each feature of an object, an agent has a sensory channel, which contains a set
of categories. Categories are lists of (channel id, lower bound, upper bound). New categories are
created by splitting the range of an existing category into two equal parts.

An agent has two parts: a list of categories, and a list of stats.

A discrimination games works as follows:
1. agent categorises all objects in the context.
2. if any of the target's categories uniquely identifies it in the context, the game succeeds.
3. if the game fails, split a category to create two new categories.

Usage:
disc_simulation(100,10) runs 100 discrimination games, outputting the results after every 10 games
"""

import random
import math

# ------- global parameters ---------

features = 5                    # number of features
context_size = 3                # context size
objects = 10                    # number of objects in world

def new_object():
    "create new object"
    f = []
    for i in range(features):
        f.append([i, random.random()])
    return f

def new_world():
    "create new world"
    world = []
    for i in range(objects):
        world.append(new_object())
    return world

def new_agent():
    "create new agent with sensory channels"
    categories = []
    for i in range(features):
        categories.append([i, 0.0, 1.0])
    return categories

def create_context(w,n):
    "create context of n meanings from world"
    random.shuffle(w)
    return w[0:n]

def categorise(agt, obj):
    "categorise object"
    m = []
    for c in agt:
        for f in obj:
            if (f[0] == c[0]) and (c[1] <= f[1] <= c[2]):
                m.append(c)
    return m

def distinctive_meanings(agt, tgt, dst):
    "distinctive meanings for target compared to distractors"
    m_distinctive = []
    m_distractor = []
    m_target = categorise(agt, tgt)
    for o in dst:
        m_distractor.extend(categorise(agt, o))
    for m in m_target:
        if m not in m_distractor:
            m_distinctive.append(m)
    return m_distinctive

def most_specific(cats):
    "choose most specific category from cats"
    min_range = 1.0
    for c in cats:
        this_range = c[2] - c[1]
        if  this_range < min_range:
            min_range = this_range
    candidates = []
    for c in cats:
        if (c[2] - c[1]) == min_range:
            candidates.append(c)
    return random.choice(candidates)

def max_depth(cats):
    "maximum tree depth of cats"
    x = most_specific(cats)
    return math.log((x[2]-x[1]), 0.5)

def refine_channel(agt, obj):
    "refine the node representing object on a random channel"
    ch = random.choice(range(len(obj)))
    mch = []
    mlist = categorise(agt, obj)
    for m in mlist:
        if m[0] == ch:
            mch.append(m)
    node = most_specific(mch)
    new_cats = [[node[0], node[1], (node[1] + ((node[2]-node[1])/2))],
                [node[0],(node[1]+((node[2]-node[1])/2)),node[2]]]
    agt.extend(new_cats)

def discrimination_game(agt, wld, cxt):
    "discrimination game"  
    c = create_context(wld, cxt)
    random.shuffle(c)
    t = c[0]
    d = c[1:]
    if distinctive_meanings(agt, t, d) == []:
        refine_channel(agt, t)
        return 0
    else:
        return 1

def disc_simulation(games,datapoints):
    "discrimination games simulation"
    a = new_agent()
    w = new_world()
    ngames = nsuccess = 0.0
    for i in range(games):
        ngames += 1
        nsuccess += discrimination_game(a,w,context_size)
        if (i % (games/datapoints) == 0):
            print(nsuccess / ngames)
            ngames = nsuccess = 0.0
    return a

def avg(x):
    total = 0
    for i in x: #range creates a list: in x goes through all elements
        total += i
    return (total/len(x))

def run_simul(x): #creating a function that outputs the max depth repeatedly
    list = []
    for i in range(x): #creating a loop
        z = disc_simulation(500,10)
        list.extend([max_depth(z)])
    print(list, avg(list))



    
