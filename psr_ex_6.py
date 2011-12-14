'''
Code code code code
By Matrim Cauthon and Ilyena Therin Telamon

'''


from __future__ import division
import sys
import math


def train(file_name):
    #data = [[l[0], l[2]] for l == line.strip().split() in f[50]] 
    f = open(file_name,'r+').readlines()
    versicolor = []
    virginica = []
    for i in range(50):
        line = f[i]
        line = line.strip().split()
        v = line[0]
        c = line[2]
        if c == 'versicolor': versicolor.append(v)
        else: virginica.append(v)
    print versicolor
    print virginica
    for i in range(len(versicolor)):
        x = versicolor[i]
        distance = [[],[]]
        for j in range(len(versicolor)):
            y = versicolor[j]
            if i != j:
                distance[0].append(y)
                distance[1].append(math.fabs(float(x)-float(y)))
        print distance
    #data = [l for l in data]
    #p(x) = K/N / V


def cont_features(file_name, k):
    f = open(file_name,'r+').readlines()
    versicolor = []
    virginica = []
    error_rate = 0
    for i in range(50,100):
        test_line = f[i].replace('\n', '').split()
        xy_distance = [[],[]]
        euclid = [] 
        #Making it run faster shouldn't matter so much here,
        #so lets just call this again
        for j in range(50):
            train_line = f[j].replace('\n', '').split()
            xy_distance[0] = math.fabs(float(train_line[0])-float(test_line[0]))
            xy_distance[1] = math.fabs(float(train_line[1])-float(test_line[1]))
            euclid.append( (
                    (math.sqrt(float(xy_distance[0])**2+float(xy_distance[1])**2)),
                    train_line[2]) )
            k_nearest_neighbors = sorted(euclid, key=lambda species: species[0])[:int(k)]
        k_class = 0
        for i in range(len(k_nearest_neighbors)):
            if k_nearest_neighbors[i][1] == "versicolor":
                k_class += 1
        if k_class >= (len(k_nearest_neighbors)/2):
            if test_line[2] != "versicolor":
                error_rate += 1
    print error_rate


def discrete_distance(line, line2):
    distance = 0
    for x in range(1,len(line)-1):
        if line[x] != line2[x]:
            distance += 1
    return (line[0], line2[0], distance)

def discrete_features(train_name,test_name,k):
    f = open(test_name,'r+').readlines()
    g = open(train_name, 'r+').readlines()
    versicolor = []
    virginica = []
    error_rate = 0
    for i in range(len(f)):
        test_line = f[i].replace('\n', '').split(',')
        xy_distance = [[],[]]
        euclid = [] 
        for j in range(len(g)):
            train_line = g[j].replace('\n', '').split(',')
            euclid.append(discrete_distance(test_line, train_line))
        k_nearest_neighbors = sorted(euclid, key=lambda partay: partay[2])[:int(k)]
        k_class = 0
        for i in range(len(k_nearest_neighbors)):
            if k_nearest_neighbors[i][1] == "democrat":
                k_class += 1
        if k_class >= (len(k_nearest_neighbors)/2):
            if test_line[0] != "democrat":
                error_rate += 1
    print error_rate




if __name__ == "__main__":
    if (sys.argv[1] == "train"):
        train(sys.argv[2])
    if (sys.argv[1] == "cont"):
        cont_features(sys.argv[2], sys.argv[3])    
    if (sys.argv[1] == "disc"):
        discrete_features(sys.argv[2], sys.argv[3], sys.argv[4])
