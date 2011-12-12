'''
Code code code code
By Matrim Cauthon and Ilyena Lews Telamon

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
    '''
    How to train your dragon. 
    '''
    #data = [l for l in data]
    #p(x) = K/N / V


if __name__ == "__main__":
    train(sys.argv[1])


    0010100101 = .2
    1100001010 = .2
