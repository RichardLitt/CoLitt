'''
Code code code code
By Matrim Cauthon and Ilyena Lews Telamon

'''
from __future__ import division
import sys
import math

CLASS = ['versicolor', 'virginica']
F_LEN = 1
CL_POSS = 2
N = 50
data = [[] for i in range(len(CLASS))]
k = 15

def dist(x,y):
    res = math.fabs(x-y)
    if res == 0: res = 0.0001
    return res

def get_p_mass(file_name):
    #read in the data
    f = open(file_name, 'r')
    f_data = [l.split() for l in f.readlines()]
    f.close()
    
    # group according to classes
    for l in f_data[:N]: 
        cl_id = CLASS.index(l[CL_POSS])
        data[cl_id].append(l[1])
    
    #calculate the probability mass for 
    #each point of each class
    p_mass = []
    for cl in data:
        p = []
        cl = sorted(cl)
        clen = len(cl)
        
        #for each x select closest neighbors
        for i in range(clen):
            x = float(cl[i])
            candidates = []
            for j in range(1,k+1):
                if (i+j < clen): candidates.\
                append(dist(float(cl[i+j]),x))
                if (i-j >= 0): candidates.\
                append(dist(float(cl[i-j]),x))
            #p(x) = k/N*vol where vol = |x-x_k|
            p.append((x,(k/(N*2*sorted(candidates)[k-1])))) 
        
        p_mass.append(p)     
        
    #write result to file to plot in R 
    out_f = open(file_name+".pmass", 'w')
    for i in range(len(p_mass)):
        for e in p_mass[i]:
            l = "%s\t%s\t%s\n" %(e[0],e[1],i)
            out_f.write(l)


if __name__ == "__main__":
    get_p_mass(sys.argv[1])

