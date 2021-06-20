import numpy as np 
from numpy.linalg import inv
import pandas as pd
import matplotlib.pyplot as plt 
import sys
import matrix
import import_data
from numpy.linalg import svd

class Acc :

    def __init__(self,path,N) :

        data = pd.read_csv(path,header=None)
        index_list = []
        for i in range(int(len(data)/2)):
            index_list.append("Vertical_No.{}".format(i+1))
            index_list.append("Rotation_No.{}".format(i+1))
        data.index = index_list

        self.data = data.values
        self.N = N
        self.num_sample = data.shape[1]
        

    def extract_bounce(self):
        acc_bounce = []
        
        for i in range(int(self.data.shape[0]/2)):
            acc_bounce =np.append(acc_bounce,self.data[2*i,:],axis=0)      
        acc_bounce = np.array(acc_bounce.reshape([(self.N)+1,self.num_sample]))
        
        return acc_bounce
        

    def mode_shape(self):
        
        U,S,Vt=svd(self.extract_bounce(),full_matrices=False)
        V = Vt.T
        S = np.diag(S)

        return U
