import random
from copy import deepcopy 

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

def new_object(nfeat):
    "create new object"
    features = []
    for i in range(nfeat):
        features.append((i, random.random())) # can't be list - needed as hashkey
    return features

def new_world(nobj, nfeat):
    "create new world"
    world = []
    for i in range(nobj):
        world.append(new_object(nfeat))
    return world

def create_context(w,n):
    "create context of n meanings from world"
    random.shuffle(w)
    return w[0:n]

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

def distinctive_meanings(agt, tgt, dst):
    "distinctive meanings for target compared to distractors"
    m_distinctive = []
    m_distractor = []
    m_target = categorise(agt, tgt)
    for o in dst:
        m_distractor.extend(categorise(agt, o))
    for m in m_target:
        if (m not in m_distractor):
            m_distinctive.append(m)
    return m_distinctive

def multiple_meaning_learn(system,meaning_list,signal,rule):
    "learn a signal paired with multiple meanings"
    for m in range(len(system)):
        for s in range(len(system[m])):
            if m in meaning_list and s == signal: system[m][s] += rule[0]
            if m in meaning_list and s != signal: system[m][s] += rule[1]
            if m not in meaning_list and s == signal: system[m][s] += rule[2]
            if m not in meaning_list and s != signal: system[m][s] += rule[3]


#------ new code -----

# global parameters

objects = 5
features = 1
context_size = 3
rule = [1, 0, 0, 0]

# initialisation

def new_agent(f):
    "create new agent"
    categories = []
    for i in range(f):
        categories.append((i, 0.0, 1.0)) # can't be list as needed as hashkey
    stats = [0., 0.,0.,0.]
    system = [[0]]
    signal_dict = {'UNSEEN' : 0}
    meaning_dict = {'UNSEEN MNG' : 0}
    return [categories,stats,system,signal_dict,meaning_dict]

def new_signal(n=2):
    "new signal with n CV syllables"
    s = ''
    con = 'bcdfghjklmnpqrstvwxyz'
    vow = 'aeiou'
    for i in (range(n)):
        s += random.choice(con) + random.choice(vow)
    return s

# dictionary access

def find_key(dic, val):
    "return the key of dictionary dic given the value"
    return [k for k, v in dic.iteritems() if v == val][0]

# modified agent functions

def categorise(agt, obj):
    "categorise object"
    m = []
    for c in agt[0]: # added as agt def changed
        for f in obj:
            if ((f[0] == c[0]) & (c[1] <= f[1] <= c[2])):
                m.append(c)
    return m

def refine_channel(agt, tgt):
    "refine the node representing t on a random channel"
    ch = random.choice(range(len(tgt)))
    mch = []
    mlist = categorise(agt, tgt)
    for m in mlist:
        if (m[0] == ch):
            mch.append(m)
    node = most_specific(mch)
    new_cats = [(node[0], node[1], (node[1] + ((node[2]-node[1])/2))),
                (node[0],(node[1]+((node[2]-node[1])/2)),node[2])] # now tuples not lists
    agt[0].extend(new_cats)

# choose signal, meaning from lexicon

def most_general(cats):
    "choose most general category from cats"
    max_range = 0.0
    for c in cats:
        this_range = c[2] - c[1]
        if this_range > max_range:
            max_range = this_range
    candidates = []
    for c in cats:
        if (c[2] - c[1]) == max_range:
            candidates.append(c)
    return random.choice(candidates)

def choose_signal(agt, mng):
    "choose signal from agt to express mng"
    if mng in agt[4]:
        sig =  find_key(agt[3], wta(s_weights(agt[2], agt[4][mng])))
    else:
        sig = new_signal()
    return sig

def choose_meaning(agt, sig):
    "choose meaning from agt to interpret sig"
    if sig in agt[3]:
        mng = find_key(agt[4], wta(m_weights(agt[2], agt[3][sig])))
    else:
        mng = None
    return mng

# add signal, meaning to lexicon

def add_signal(agt, sig):
    "add signal to agent's lexicon"
    sigs = len(agt[2][0])
    agt[3][sig] = sigs
    unseen = agt[2][0][0]
    for m in agt[2]:
        m.append(unseen)

def add_meaning(agt, mng):
    "add meaning to agent's lexicon"
    mngs = len(agt[4])
    sigs = len(agt[3])
    agt[4][mng] = mngs
    unseen = agt[2][0][0]
    agt[2].append([unseen] * sigs) 


# learning

def update_lexicon(agt, mlist, sig):
    "agt learns each item in mlist paired with sig"
    if sig not in agt[3]: 
        add_signal(agt, sig)
    sig_index = agt[3][sig]
    mng_indices = []
    for item in mlist:
        if item not in agt[4]:
            add_meaning(agt, item)
        mng_indices.append(agt[4][item])
    multiple_meaning_learn(agt[2], mng_indices, sig_index, rule)

# production

def produce(agt, tgt, dst, cxt):
    "produce signal to describe target against distractors"
    candidates = []
    for s in agt[3]:
        if (s != 'UNSEEN'):
            [obj, mng] = interpret(agt, s, cxt, False)
            if tgt == obj:
                candidates.append([s, mng])
    if candidates == []:
        m_dist = distinctive_meanings(agt, tgt, dst)
        if m_dist == []:
            refine_channel(agt, tgt)
            m = None
            s = ''
        else:
            m = most_general(m_dist)
            s = new_signal()
        signal_meaning = [s, m]
    else:
        signal_meaning = random.choice(candidates)
    return signal_meaning

# interpretation

def all_possible_meanings(agt, cxt):
    "all possible meanings in context"
    m_poss = []
    for obj in cxt:
        distractors = filter(lambda x:x!= obj, cxt) 
        m_dist = distinctive_meanings(agt, obj, distractors)
        m_poss.extend(m_dist)
    return m_poss

def interpret(agt, sig, cxt, update_agent=True):
    "interpet signal in context"
    a = agt if update_agent else deepcopy(agt)  
    m_poss = all_possible_meanings(a, cxt)
    if (m_poss == []):
        refine_channel(a, random.choice(cxt))
    else:
        update_lexicon(a, m_poss, sig)
    hr_mng = choose_meaning(a, sig)
    hr_ref = None
    for obj in cxt:
        distractors = filter(lambda x: x != obj, cxt)
        m_dist = distinctive_meanings(a, obj, distractors)
        if hr_mng in m_dist:
            hr_ref = obj
    return [hr_ref, hr_mng]
            
# communication

def choose_speaker_hearer(pop):
    "choose different speaker and hearer from population pop"        
    s = random.randrange(len(pop))
    h = random.randrange(len(pop) - 1)
    if h >= s: h += 1
    speaker = pop[s]
    hearer = pop[h]
    return [speaker,hearer]

def discrimination_game(agt, wld, cxt):
    "discrimination game"  
    c = create_context(wld, cxt)
    random.shuffle(c)
    t = c[0]
    d = c[1:]
    m_dist = distinctive_meanings(agt, t, d)
    if m_dist == []:
        refine_channel(agt, t)
        succ = False
    else:
        succ = True   
    return succ
    

def communication_game(s, h, wld, csize):
    "communication game between speaker and hearer about objects in world"
    c = create_context(wld, csize)
    random.shuffle(c)
    t = c[0]
    d = c[1:]
    [sig, sp_mng] = produce(s, t, d, c)
    if sig == '':
        succ = False
    else:
        update_lexicon(s, [sp_mng], sig)
        [hr_ref, hr_mng] = interpret(h, sig, c)
        if (t == hr_ref):
            succ = True
        else:
            succ = False
    s[1][0] += succ
    s[1][1] += 1
    h[1][2] += succ
    h[1][3] += 1
    return succ

def print_system(a):
    print '\t\t',
    for i in range(len(a[3])):
        print find_key(a[3],i),'\t',
    print
    for j in range(len(a[4])):
        print find_key(a[4],j), '\t',
        for k in a[2][j]:
            print k, '\t',
        print

def comm_simulation(games, datapoints):
    "communication game simulation"
    speaker = new_agent(features)
    hearer = new_agent(features)
    w = new_world(objects, features)
    ngames = nsuccess = 0.0
    for i in range(100):
        discrimination_game(random.choice([speaker,hearer]), w, context_size)
    for i in range(games):
        ngames += 1
        nsuccess += communication_game(speaker, hearer, w, context_size)
        if ((i+1) % (games/datapoints) == 0):
            print nsuccess / ngames
            ngames = nsuccess = 0.0
    print_system(speaker)
    print_system(hearer)
    return [speaker,hearer]
        
