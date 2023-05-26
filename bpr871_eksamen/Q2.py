import numpy as np
from types import SimpleNamespace
from scipy import optimize
import copy


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

    # unpack parameters
    sigma_epsilon = par.sigma_epsilon
    kappa_init = par.kappa_init
    T = par.T

    # draw epsilons
    epsilons = np.random.normal((0.5*sigma_epsilon**2), sigma_epsilon, (T,1))
    #epsilon_list = epsilons.tolist()

    # initialize the list with an empty array
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

    """calculates l for each kappa value"""

    # unpack parameters
    eta = par.eta
    w = par.w

    # initialise l values
    l_values = []

    # loop over the kappa list and calculate l for each period
    for kappa in kappas:
        l = (((1-eta) * kappa) / w) ** (1 / eta)
        l_values.append(l)

    return l_values


def calculate_h(par, k_values, l_values, t_values):

    """calculates the profit in each period"""

    # unpack parameters
    eta = par.eta
    w = par.w
    iota = par.iota
    r = par.r
    R = (1+r)**(1/12)
    delta = par.delta

    # initialise h and l values
    h_value = 0
    l_previous = 0

    # loop over the different t, k and l values
    for t, kappa, l in zip(t_values, k_values, l_values):
        lt_optimal = l


        # delta if statement for Q3 and Q4
        if abs(l_previous - lt_optimal) > delta:
            lt = lt_optimal
        else:
            lt =  l_previous

        # using an indicator to account for changes in l    
        indicator = 1 if lt != l_previous else 0        

        # adding the return for the current period to the h sum
        h_value += R ** (-t) * (kappa * lt**(1 - eta) - w * lt - indicator * iota)
        
        # set l_previous for the next loop
        l_previous = lt

    return h_value
    
    

#sigma_epsilon=0.1, kappa_init=1, eta=0.5, w=1.0, rho=0.9, iota=0.01, r=0.01, T=120

def calculate_H(par):

    """loops over different shock scenarios and takes the mean of all scenarios"""

    # set seed
    np.random.seed(2023)

    # unpacking the T parameter and creating lists for looping over
    T = par.T
    K = par.K
    t_values = list(range(T))
    K_list = range(K)

    # create empty h_values list
    h_sum = []
    mean_list = []

    # looping over each shock scenario and finding the return for each series of kappa
    for k in K_list:
        kappa_values = kappas(par)
        l_values_test = calculate_l(par, kappa_values)
        h_value_temp = calculate_h(par, kappa_values, l_values_test, t_values)
        h_sum.append(h_value_temp)

        # creating a list of cumulative means for plotting
        mean_until_now = np.mean(h_sum)
        mean_list.append(mean_until_now)

    H = np.mean(h_sum)
    print(f'H is = {H} for K = {K}')

    return H, mean_list
        

def optimal_delta(par):

    # create delta values and initialise H_values
    delta_values = np.linspace(0.0, 1.0, num=1000)
    H_values = []

    # create a copy of the par namespace and set K to 10 for speed
    par_copy = copy.copy(par)
    par_copy.K = 10

    # loop over the delta values
    for delta in delta_values:
        par_copy.delta = delta
        H, _ = calculate_H(par_copy)
        H_values.append(H)
    
    # find the maximum H value and the corresponding delta value
    max_index = np.argmax(H_values)
    max_delta = delta_values[max_index]
    max_H = H_values[max_index]

    # plot delta against H
    plt.plot(delta_values, H_values)
    plt.scatter(max_delta, max_H, color='red', label=f'Max H = {max_H:.3f}')
    plt.axvline(x=max_delta, color='red', linestyle='--', label=f'Delta = {max_delta:.3f}')
    plt.xlabel('$\Delta$')
    plt.ylabel('h')
    plt.title('Ex post value of salon, h($\epsilon_0,\epsilon_1,...,\epsilon_{119}$), given values of $\Delta$')
    plt.grid(True)
    plt.legend()
    plt.show()



