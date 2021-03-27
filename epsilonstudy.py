"""
Author:
Matt Russell

Source:
Part of an assignment for the AA560: Plasma Diagnostics class at the University
of Washington.

Description:
Program to study the effect of a perturbative constant, epsilon, that I introduced
into a trapezoidal integration algorithm in order to solve a divide-by-zero
problem at the boundaries. This small constant works by artifically moving the
boundaries from [0,a] to [eps_i,a-eps_i].
"""

"""
Functions:
- ConvexReconstruction(): Reconstructs convex density profile given an epsilon
                        and other arguments.
- dNdy(): Computes the y-derivative of N(y) = AbelTransform(n(r)=(1-r)^2)
- IAT_TrapezoidIntegrate(): Computes a single point of the inverse Abel Transform
                          using trapezoidal integration
"""
def ConvexReconstruction(eps_i,rsize,a):
    """
    Description:
    The assignment required me to perform Abel Inversion, a particular kind of
    technique used in plasma diagnostics to obtain line-integrated (chordal)
    measurements of cylindrially symmetric quanitites, like plasma density for
    example. The process involves performing an Abel Transform on the quanitty
    in order to obtain a new function expressed in terms of y. To obtain a
    representation of the original, desired signal, an integral must be computed
    that represents the inverse transform. This function automates the
    reconstruction process.

    ------
    Inputs
    eps_i - particular element of an ndarray of small parameters used to
            artifically move the boundaries of the system from [0,a]|->[eps_i,a-eps_i]
          in order to prevent divide-by-zero from occurring at these locations.
          Studying the impact the scale of this parameter has on the
          reconstruction of the signal is the objective of this code.
    rsize - number of elements in spatial grid
    a - radial length of cylindrical plasma under consideration
    --------
    Internal
    r - spatial grid
    recon - normalized, reconstructed signal
    ------
    Output
    I - trapezoidal approximation of \int_{ri}^{a} (...)dy [float]
    """
    r = np.linspace(eps_i,a-eps_i,rsize) # spatial grid
    recon = np.empty(rsize)

    for i in range(0,np.size(recon)):
        recon[i] = (-1/np.pi)*IAT_TrapezoidIntegrate(r[i],a,eps_i)

    return recon/np.amax(recon)

def dNdy(y,eps):
    """
    Function to calculate the derivative of the Abel-transformed density.
    Necessary for inverse transform.
    ------
    Inputs
    y - [float]
    eps - small parameter to avoid divide-by-zero at boundaries [float]
    --------
    Internal
    t_{1} - polynomial term
    l_{1,2} - natural log terms
    denom - denominator of expression
    """
    if y == 1.0:
        y = y - eps

    t_1 = 1 - y**2
    denom = t_1 + np.sqrt(t_1)
    l_1 = np.log(y)
    l_2 = np.log(1 + np.sqrt(t_1))

    result = 4.0*y*(t_1 + t_1**(3/2) + (t_1 + np.sqrt(t_1))*l_1 - \
        - (t_1 + np.sqrt(t_1))*l_2)/denom
    return result

def IAT_TrapezoidIntegrate(ri,ae,eps):
    """
    Inputs
    ri - lower bound of integration [float]
    a - upper bound of integration (=1 always) [float]
    eps - small parameter to prevent divide-by-zero from occurring [float]
    --------
    Internal
    N - number of steps [int]
    h - stepsize [float]
    y - argument for loop [float]
    ------
    Output
    I - trapezoidal approximation of \int_{ri}^{a} (...)dy [float]
    """
    if a != 1.0:
        print(" IAT_TrapezoidIntegrate: \"check what happened to a\"")
        return -1

    IntPoint = 0.0
    N = 10
    h = (a - ri)/float(N)
    y = 0.0

    # sum_{k=1}^{N-1} f(a+kh)
    for k in range(1,N):
        y = ri + float(k)*h
        IntPoint = IntPoint + dNdy(y,eps)*(1.0/np.sqrt(y**2 - ri**2))

    # Add boundary terms
    IntPoint = (h*(0.5)*(dNdy(ri,eps)*(1.0/np.sqrt(ri**2 - (ri - eps)**2)) \
    +dNdy(a,eps)*(1.0/np.sqrt(a**2 - (ri-eps)**2))) + IntPoint)
    return IntPoint

"""
Main Program
"""
import numpy as np
import matplotlib.pyplot as plt

a = 1.0 # Radial Boundary
rsize = 100 # Number of elements in spatial grid

r_anal = np.linspace(0,a,rsize)
n_cv_anal = np.empty(np.size(r_anal))
for i in range(0,rsize):
    n_cv_anal[i] = (1 - r_anal[i])**2

eps = np.logspace(-1,-15,15) # perturbative constants
len_eps = np.size(eps) # number of perturbative constants

n_cv_reconstruction = np.empty((rsize,len_eps)) # columns store reconstruction for particular epsilon

for i in range(0,len_eps):
    n_cv_reconstruction[:,i] = ConvexReconstruction(eps[i],rsize,a)

"""
Graphs
"""
fig_analreconvex = plt.figure()
for i in range(0,len_eps):
    r = np.linspace(eps[i],a-eps[i],rsize)
    plt.plot(r,n_cv_reconstruction[:,i], label='O(E%i)' %np.log10(eps[i]))

plt.plot(r_anal,n_cv_anal,':b',label='Analytical')
plt.title('Effect of perturbative scale on convex profile reconstruction')
plt.ylabel('normalized density')
plt.xlabel('radius')
plt.xlim(0.0,a)
plt.ylim(-2.5,5.0)
plt.legend(bbox_to_anchor=(1,1),loc="upper left")

fig_analreconvex2 = plt.figure()
for i in range(0,len_eps):
    r = np.linspace(eps[i],a-eps[i],rsize)
    plt.plot(r,n_cv_reconstruction[:,i], label='O(E%i)' %np.log10(eps[i]))

plt.plot(r_anal,n_cv_anal,':b',label='Analytical')
plt.title('Effect of perturbative scale on convex profile reconstruction')
plt.ylabel('normalized density')
plt.xlabel('radius')
plt.xlim(0.0,a)
plt.legend(bbox_to_anchor=(1,1),loc="upper left")

plt.show()
