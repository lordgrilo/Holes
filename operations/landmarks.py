
import networkx as nx 
import numpy as np
import Holes as ho
import random 


def F_Z(z, L, distance_matrix,verbose=False):
    d=[]
    for l in L:
        d.append(distance_matrix[z,l]);
    if verbose:
        print d;
    return np.min(d), z;
    

def max_min_step(L, nodes, distance_matrix,verbose=False):
    f_values=[]
    index_f_values=[]
    for n in nodes:
        if n not in L:
            deh=F_Z(n,L,distance_matrix);
            f_values.append(deh[0]);
            index_f_values.append(deh[1]);
        else:
            f_values.append(-1);
            index_f_values.append(NaN);
    if verbose:
        print 'L',L, 'fvals' ,f_values,'index', index_f_values, 'agmax', np.argmax(f_values)
    return index_f_values[np.argmax(f_values)]
    

def minmax_selector(distance_matrix, num_landmarks,verbose=False):
    landmarks=[];
    nodes=range(distance_matrix.shape[0]);
    landmarks.append(random.choice(range(distance_matrix.shape[0])));
    nodes.pop(nodes.index(landmarks[-1]))
    while len(landmarks)<num_landmarks:
        landmarks.append(max_min_step(landmarks,nodes,distance_matrix));
        nodes.pop(nodes.index(landmarks[-1]))
    if verbose: print len(nodes)
    print 'Landmarks: ' , landmarks
    return landmarks;