import numpy as np
from random import *
seed(20231016)
##print(random())
def random_point(number,x_low,x_high,y_low,y_high): ##随机产生问题规模
    X = []
    Y = []
    P = []
    x_base = x_high - x_low
    y_base = y_high - y_low
    for i in range(number):
        P.append(i+1)
        x = random()*x_base + x_low
        y = random()*y_base + y_low
        x_init = [x,i+1]
        y_init = [y,i+1]
        X.append(x_init)
        Y.append(y_init)
    tuple_result = (P,X,Y)
    return tuple_result

def distance(x1,y1,x2,y2):
    dis = (x1-x2)**2 + (y1-y2)**2
    dis = np.sqrt(dis)
    return dis

def MinDistance(P,X,Y):
    length = len(P)
    if length <= 3:
        x = [0]*length
        y = [0]*length
        for i in range(length):
            x[X[i][1]-1] = X[i][0]
            y[Y[i][1]-1] = Y[i][0]
        distace0 = distance(x[0], y[0],x[1],y[1])
        distace1 = distance(x[0], y[0], x[2], y[2])
        distace2 = distance(x[1], y[1], x[2], y[2])
        mindistance = min(distace0,distace1,distace2)
        return mindistance
    else:


