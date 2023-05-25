from types import SimpleNamespace
import time

import numpy as np
import sympy as sm

from scipy import linalg
from scipy import optimize

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D



def griewank(x):
    return griewank_(x[0],x[1])
    
def griewank_(x1,x2):
    A = x1**2/4000 + x2**2/4000
    B = np.cos(x1/np.sqrt(1))*np.cos(x2/np.sqrt(2))
    return A-B+1

def chi(k, K_ = 10):
    chi_value = 0.5 * 2 / (1 + np.exp((k - K_) / 100))
    return chi_value

def x_k0(chi_k, xs_k, xopt):
    xs_k0 = chi_k * xs_k + (1 - chi_k) * xopt
    return xs_k0

def optimizer(K_=10, K=1000, x_bound=600, tau=1e-10, _Print=True, _Plot=True):

    # draw x values for the multi-start
    np.random.seed(1998)
    x0s = -x_bound + (2*x_bound)*np.random.uniform(size=(K,2)) # in [-600,600]
    xs = np.empty((K,2))
    fs = np.empty(K)

    # setting up empty optimization parameters
    fopt = np.inf 
    xopt = np.nan

    # setting up containers for plotting 
    k_values = []
    x0_values = []
    x0k_values = []
    #x0k_values222 = np.empty((2,1000)) 

    # for loop for optimizing over different x values
    for k,x0 in enumerate(x0s):
        #K_ = 10 # NEEDS TO BE ABLE TO UPDATE AUTOMATICALLY FROM THE GLOBAL SCOPE


        if k < K_:                          # skip if warm-up iterations
            x0_k = x0  
        elif k > K_ or k == K_:             # refined x values 
            chi_k = chi(k, K_)
            x0_k = x_k0(chi_k, x0, xopt)
        else:   
            print('Error with k')

        # save the values for plotting
        k_values.append(k)
        x0_values.append(x0s)
        x0k_listformat = x0_k.tolist()
        x0k_values.append(x0k_listformat)
        #x0k_values222.extend(x0_k)
        
        # optimization
        result = optimize.minimize(griewank,x0_k,method='BFGS',tol=tau)
        xs[k,:] = result.x
        f = result.fun

        # print first 10 or if better than seen yet
        if k < 10 or f < fopt: # plot 10 first or if improving
            if f < fopt:
                fopt = f
                xopt = xs[k,:]
                
            if _Print:
                print(f'{k:4d}: x0 = ({x0[0]:7.2f},{x0[1]:7.2f})',end='')
                print(f' -> x0_k = ({x0_k[0]:7.2f},{x0_k[1]:7.2f})',end='')
                print(f' -> converged at ({xs[k][0]:7.2f},{xs[k][1]:7.2f}) with f = {f:12.8f}')
            
    # best solution
    print(f'\nbest solution:\n x = ({xopt[0]:7.2f},{xopt[1]:7.2f}) -> f = {fopt:12.8f}  )')

    if _Plot:
        # plotting
        plt.plot(k_values, x0k_values)
        plt.title('Effective $x^{k0}$ values for the iteration counter $k$')
        plt.xlabel('$k$')
        plt.ylabel('$x^{k0}$ values')
        plt.show()
