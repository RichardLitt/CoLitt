'''
Code code code code
By Richard Littauer and Iliana Simova



To run:
    k is a variable. 

python psr_ex_6.py prob iris.txt k
python psr_ex_6.py cont iris.txt k
python psr_ex_6.py disc congress-train.txt congress-test.txt k

'''


from __future__ import division
import sys
import math


CLASS = ['versicolor', 'virginica']
F_LEN = 1
CL_POSS = 2
N = 50
data = [[] for i in range(len(CLASS))]

def dist(x,y):
    res = math.fabs(x-y)
    if res == 0: res = 0.0001
    return res

def get_p_mass(file_name, k):
    k = int(k)
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

'''
The following is for question 2.1 and 2.2.
'''


def cont_features(file_name, k):
    #read in the file
    f = open(file_name,'r+').readlines()
    versicolor = []
    virginica = []
    error_rate = 0
    for i in range(50,100):
        #Using the test plots to test the groups in the training data.
        test_line = f[i].replace('\n', '').split()
        xy_distance = [[],[]]
        euclid = [] 
        #Making it run faster shouldn't matter so much here,
        #so lets just call this again
        for j in range(50):
            train_line = f[j].replace('\n', '').split()
            #calculate the distance
            xy_distance[0] = math.fabs(float(train_line[0])-float(test_line[0]))
            xy_distance[1] = math.fabs(float(train_line[1])-float(test_line[1]))
            euclid.append( (
                    (math.sqrt(float(xy_distance[0])**2+float(xy_distance[1])**2)),
                    train_line[2]) )
            #make a list of the neatest neighbors
            k_nearest_neighbors = sorted(euclid, key=lambda species: species[0])[:int(k)]
        k_class = 0
        #This is for the error function. 
        for i in range(len(k_nearest_neighbors)):
            if k_nearest_neighbors[i][1] == "versicolor":
                k_class += 1
        if k_class >= (len(k_nearest_neighbors)/2):
            if test_line[2] != "versicolor":
                error_rate += 1
    print error_rate


#The distance function for discrete values. 
def discrete_distance(line, line2):
    distance = 0
    for x in range(1,len(line)-1):
        if line[x] != line2[x]:
            distance += 1
    return (line[0], line2[0], distance)

def discrete_features(train_name,test_name,k):
    #read in both files
    f = open(test_name,'r+').readlines()
    g = open(train_name, 'r+').readlines()
    versicolor = []
    virginica = []
    error_rate = 0
    for i in range(len(f)):
        #calculate the distances
        test_line = f[i].replace('\n', '').split(',')
        xy_distance = [[],[]]
        euclid = [] 
        for j in range(len(g)):
            train_line = g[j].replace('\n', '').split(',')
            euclid.append(discrete_distance(test_line, train_line))
        k_nearest_neighbors = sorted(euclid, key=lambda partay: partay[2])[:int(k)]
        #the error function
        k_class = 0
        for i in range(len(k_nearest_neighbors)):
            if k_nearest_neighbors[i][1] == "democrat":
                k_class += 1
        if k_class >= (len(k_nearest_neighbors)/2):
            if test_line[0] != "democrat":
                error_rate += 1
    print error_rate



#The commands used. 
if __name__ == "__main__":
    if (sys.argv[1]) == "prob":
        get_p_mass(sys.argv[2], sys.argv[3])
    if (sys.argv[1] == "train"):
        train(sys.argv[2])
    if (sys.argv[1] == "cont"):
        cont_features(sys.argv[2], sys.argv[3])    
    if (sys.argv[1] == "disc"):
        discrete_features(sys.argv[2], sys.argv[3], sys.argv[4])
