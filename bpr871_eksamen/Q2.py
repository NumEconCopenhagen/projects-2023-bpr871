import numpy as np
from types import SimpleNamespace
from scipy import optimize


import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
plt.style.use('seaborn-whitegrid')


eta = 0.5
w = 1.0
rho = 0.9
iota = 0.01
R = (1+0.01)**(1/12)
sigma_epsilon = 0.1

kappa_init = 1
T = 120




def kappas():

    #draw epsilons
    epsilons = np.random.normal((0.5*sigma_epsilon**2), sigma_epsilon, (120,1))
    epsilon_list = epsilons.tolist()

    # Initialize the list with an empty array
    log_kappas = np.zeros((len(epsilons),)) 

    for i,epsilon in enumerate(epsilons):
        
        if i==0: 
            log_kappa_t = np.log(1) + epsilon
        else:
            # Calculate the autoregressive value at time t
            log_kappa_t = log_kappas[i-1] + epsilon

        # add log_kappa_t to the list of log_kappas
        log_kappas[i] = log_kappa_t

        # convert to the exponential values of log_kappa to get the kappa values
        kappas = np.exp(log_kappas)
        k_values = kappas.tolist()

    return k_values


def calculate_l(kappas):
    l_values = []

    for kappa in kappas:
        l = (((1-eta) * kappa) / w) ** (1 / eta)
        l_values.append(l)

    return l_values


def calculate_h(k_values, l_values, t_values):
    h_value = 0
    l_previous = 0


    for t, kappa, l in zip(t_values, k_values, l_values):
        lt = l
        indicator = 1 if lt != l_previous else 0
        h_value += R ** (-t) * (kappa * lt**(1 - eta) - w * lt - indicator * iota)
        l_previous = lt

    return h_value
    
    


def calculate_H(K):

    t_values = list(range(120))
    K_list = range(K)

    # create empty h_values list
    h_sum = []
    mean_list = []

    np.random.seed(1998)

    for k in K_list:
        kappa_values = kappas()
        ltest = calculate_l(kappa_values)
        htest = calculate_h(kappa_values, ltest, t_values)

        h_sum.append(htest)
        mean_until_now = np.mean(h_sum)
        mean_list.append(mean_until_now)

    H = np.mean(h_sum)
    #print(f'at {K} the mean is')
    #print(H)

    #return mean_list

    return H
        

