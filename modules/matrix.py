from matplotlib.pyplot import axis
import numpy as np
from numpy.linalg import inv
from numpy.linalg import svd

# M-file which contains the properties of a fully loaded 2DOF truck model
# Truck dimensions modelled are for two axle DAF LF55 E18-475
# Created by Patrick McGetrick September 2011
 
# ----- Vehicle properties (Based partially on Cebon 1999 & Harris) assuming doubled wheeled rear axle ------

veh = 'DAF_E18-475'
n = 2                          # Number of axles (2 axles)
Gvw = 18000                    # Gross Vehicle Weight (mass as units in [kg]) (18000)
ms = Gvw                       # Sprung mass [kg]
# ks = [4e51e6] ktn = [1.75e63.5e6] # 4dof Half suspension and tire stiffnesses
# kn_equiv =  roundn((ks.*ktn)./(ks+ktn),3) # Equivalent 2DOF Suspension spring constant
kn = [2e6,5e6]                 # Suspension spring constant (or Ks) [N/m] [2e65e6]
cn = [10e3,20e3]               # Suspension viscous damping [Ns/m] (10e3,20e3)
whb = 4.75                     # Wheelbase (4.75) [m]
Tr = 1.8                       # Track width (1.82) [m]
Ax_sp = [0,whb]                # Distance between axles (0,whb) or distance from axle i to axle 1
 
m_ratio = 0.5                  # Proportion of sprung mass on rear axle
xg = m_ratio*Ax_sp[1]          # Position of centre of gravity from first axle (If Offcentre) [m]
m=[m_ratio*ms,m_ratio*ms]
#m = [1,1]*m_ratio*ms      # SDOF Axle masses [kg]
 
wn = (np.array(kn)/np.array(m))**0.5               # SDOF Axle Natural frequency [rad/s]
fn = wn/(2*np.pi)                 # SDOF Axle Natural frequency [Hz]
                                # Generally should be Bounce <= 1.2*Pitch
 
Lv = 8.26                      # Total Length of Vehicle (8.26) [m]
Hv = 1                         # Total Equivalent height of vehicle (1) [m]
Is = ms*((Lv**2)+(Hv**2))/12     # Sprung mass Moment of Inertia [kgm^2]
# GVW=round(Gvw/1000)            # Gross Vehicle Weight (kg) in tonnes
D = [xg,whb-xg]
# Static Axle loads and spacing calculations
#if n==1 bn = 0 else bn = xg - Ax_sp end # bn = [D1-D2]
#for i = 1:n
 #   axle_loads(i,1) = (( ms*(abs(bn(i-(-1)^i))/Ax_sp(2)) )) * 9.806    # Proportion weight between front & rear axle
#end
 
#clear Hv Lv Gvw wn m_ratio i

def Mv():
    
    Mv = np.array([[ms,0],[0,Is]])
    
    return Mv

def Kv():

    Kv = np.array([[kn[0]+kn[1],D[0]*kn[0]-D[1]*kn[1]],[D[0]*kn[0]-D[1]*kn[1],(D[0]**2)*kn[0]-(D[1]**2)*kn[1]]])

    return Kv

def Cv():
        
    Cv = np.array([[cn[0]+cn[1],D[0]*cn[0]-D[1]*cn[1]],[D[0]*cn[0]-D[1]*cn[1],(D[0]**2)*cn[0]-(D[1]**2)*cn[1]]])

    return Cv


def A(N):
    A = np.append(np.eye(N),np.zeros([N,1]),axis=1)
    for i in range(N):
        A[i,i+1] = -1

    return A

"""
def H(length):
    G = np.eye(length)
    for i in [0,1]:
        Hj[i,i+4] = 1
        Hj[i,i+4] = 1
    H = Hj
    for j in range(length-1):
        H = np.append(H,Hj,axis=0)

    return H
"""

def PLSM(lamda,data_size,d,Mv,Cv,Kv):
    
    Q_dash = np.append(np.append(inv(Mv)@Kv,inv(Mv)@Cv,axis=1),inv(Mv),axis=1)
    Q = Q_dash[0,:].reshape([1,6])
    #H = np.append(np.zeros([2,4]),np.eye(2),axis=1)
    H = np.array([0,0,0,0,1,1]).reshape([1,6])
    U1 = Q.T@Q
    U2 = H.T@H
    #print(U1)
    #print(U2)
    U = np.linalg.pinv(U1-lamda*U2)
    N = data_size -1
    X = np.zeros([6,data_size])
    for i in range(N-1,-1,-1):
        R1 = Q.T*d[i,0]
        R2 = (H.T@H)@X[:,i+1].reshape([6,1])
        X[:,i] = U@(R1+lamda*R2).reshape(-1)
    
    return X

def mode_shape(d):
    U,S,Vt=svd(d,full_matrices=False)
    V = Vt.T
    S = np.diag(S)

    return U