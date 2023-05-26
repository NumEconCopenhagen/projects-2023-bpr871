import numpy as np
from types import SimpleNamespace
from scipy import optimize


import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
plt.style.use('seaborn-whitegrid')


#eta = 0.5
#w = 1.0
#rho = 0.9
#iota = 0.01
#R = (1+0.01)**(1/12)
#sigma_epsilon = 0.1

#kappa_init = 1
#T = 120




def kappas(par):

    """Draws epsilons from a normal distribution and calculates the kappa values
    """

    sigma_epsilon = par.sigma_epsilon
    kappa_init = par.kappa_init

    #draw epsilons
    epsilons = np.random.normal((0.5*sigma_epsilon**2), sigma_epsilon, (120,1))
    epsilon_list = epsilons.tolist()

    # Initialize the list with an empty array
    log_kappas = np.zeros((len(epsilons),)) 

    for i,epsilon in enumerate(epsilons):
        
        if i==0: 
            log_kappa_t = np.log(kappa_init) + epsilon
        else:
            # Calculate the autoregressive value at time t
            log_kappa_t = log_kappas[i-1] + epsilon

        # add log_kappa_t to the list of log_kappas
        log_kappas[i] = log_kappa_t

        # convert to the exponential values of log_kappa to get the kappa values
        kappas = np.exp(log_kappas)
        k_values = kappas.tolist()

    return k_values


def calculate_l(par, kappas):

    eta = par.eta
    w = par.w

    l_values = []

    for kappa in kappas:
        l = (((1-eta) * kappa) / w) ** (1 / eta)
        l_values.append(l)

    return l_values


def calculate_h(par, k_values, l_values, t_values):

    eta = par.eta
    w = par.w
    iota = par.iota
    r = par.r
    R = (1+r)**(1/12)
    delta = par.delta

    h_value = 0
    l_previous = 0


    for t, kappa, l in zip(t_values, k_values, l_values):
        lt_optimal = l

        if abs(l_previous - lt_optimal) > delta:
            lt = lt_optimal
        else:
            lt =  l_previous

        indicator = 1 if lt != l_previous else 0
        h_value += R ** (-t) * (kappa * lt**(1 - eta) - w * lt - indicator * iota)
        l_previous = lt

    return h_value
    
    

#, sigma_epsilon=0.1, kappa_init=1, eta=0.5, w=1.0, rho=0.9, iota=0.01, r=0.01, T=120

def calculate_H(K, par):


    par.eta = 0.5
    par.w = 1.0
    par.rho = 0.9
    par.iota = 0.01
    r = par.r = 0.01
    T = par.T

    t_values = list(range(T))
    K_list = range(K)

    # create empty h_values list
    h_sum = []
    mean_list = []

    np.random.seed(1998)

    for k in K_list:
        kappa_values = kappas(par)
        l_values_test = calculate_l(par, kappa_values)
        h_value_temp = calculate_h(par, kappa_values, l_values_test, t_values)

        h_sum.append(h_value_temp)
        mean_until_now = np.mean(h_sum)
        mean_list.append(mean_until_now)

    H = np.mean(h_sum)
    #print(f'at {K} the mean is')
    #print(H)

    #return mean_list

    return H
        

