"""
Matt Russell
AA556 HW2
Problem 2 Python Script
Plot Wave Normal Surfaces for an electron and single-ion species plasma given
fixed mu,Y, and a range of X
"""
import numpy as np
import matplotlib.pyplot as plt
mu = 1833.0 # mass ratio between ion and electrons

# Normalized density and magnetic field
Y = 0.1
X = np.array([0.75,0.85,0.95,1.05,1.15])

# Cold Plasma Dielectric Tensor terms
R = 1.0 - X/(Y+mu) + X/(Y-1.0)
L = 1.0 + X/(Y-mu) - X/(Y+1.0)
P = 1.0 - X/mu - X
S = 0.5*(R + L)
D = 0.5*(R - L)

theta = np.linspace(0,2*np.pi)

uplus = np.empty((np.size(X),np.size(theta)))
uminus = np.empty((np.size(X),np.size(theta)))
A = np.empty((np.size(X),np.size(theta))) # Aij is value of A for the ith value of X and the jth value of theta
B = np.empty((np.size(A,axis=0),np.size(A,axis=1)))
F = np.empty((np.size(A,axis=0),np.size(A,axis=1)))

for i in np.arange(np.size(X)):
    for j in np.arange(np.size(theta)):
        A[i,j] = S[i]*np.sin(theta[j])**2 + P[i]*np.cos(theta[j])**2
        B[i,j] = R[i]*L[i]*np.sin(theta[j])**2 + P[i]*S[i]*(1.0 + np.cos(theta[j])**2)
        F[i,j] = np.sqrt(((R[i]*L[i]-P[i]*S[i])**2)*np.sin(theta[j])**4 + 4*(P[i]**2)*(D[i]**2)*np.cos(theta[j])**2)
        uplus[i,j] = np.sqrt(np.abs(2.0*A[i,j]/(B[i,j] + F[i,j])))
        uminus[i,j] = np.sqrt(np.abs(2.0*A[i,j]/(B[i,j] - F[i,j])))

"""
Plotting
"""
## Figure shows that:
#  Region 1 of CMA diagram characterizes X = {0.75,0.85}
#  Region 2 of CMA diagram characterizes X = {0.95}
#  Region 4 of CMA diagram characterizes X = [1.05,1.15}]
fig_RLP = plt.figure()
plt.scatter(X,R,label='R(X)')
plt.scatter(X,L,label='L(X)')
plt.scatter(X,P,label='P(X)')
plt.scatter(X,0.5*(R+L),label='S(X)')
plt.plot(X,np.zeros(np.size(X)),label='0')
plt.title('Cold Plasma Dispersion Relation terms for a range of X and fixed mu and Y')
plt.legend(bbox_to_anchor=(1,1),loc="upper left")

## Problem 2 WNS'
for i in np.arange(np.size(X)):
    fig_wns = plt.figure()
    if i > 1:
        plt.polar(theta,uplus[i,:])
    else:
        plt.polar(theta,uplus[i,:],theta,uminus[i,:])
    plt.title('Wave Normal Surface for X = %f' %X[i])

## Problem 4 WNS
X = 1e-8
Y = 1e-5
R = 1.0 - X/(Y+mu) + X/(Y-1.0)
L = 1.0 + X/(Y-mu) - X/(Y+1.0)
P = 1.0 - X/mu - X
S = 0.5*(R + L)
D = 0.5*(R - L)

# Use A,B,F[0,j]
for j in np.arange(np.size(theta)):
    A[0,j] = S*np.sin(theta[j])**2 + P*np.cos(theta[j])**2
    B[0,j] = R*L*np.sin(theta[j])**2 + P*S*(1.0 + np.cos(theta[j])**2)
    F[0,j] = np.sqrt(((R*L-P*S)**2)*np.sin(theta[j])**4 + 4*(P**2)*(D**2)*np.cos(theta[j])**2)
    uplus[0,j] = np.sqrt(np.abs(2.0*A[0,j]/(B[0,j] + F[0,j])))
    uminus[0,j] = np.sqrt(np.abs(2.0*A[0,j]/(B[0,j] - F[0,j])))

fig_wnsp4 = plt.figure()
plt.polar(theta,uplus[0,:],theta,uminus[0,:])
plt.title('Wave Normal Surface for X = %f, Y = %f' %(X,Y))

plt.show()
