from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class HouseholdOptimizationClass:

    def __init__(self):
        """ definition of parameters """
        

        # a. gen namespaces
        par = self.par = SimpleNamespace() #exogenous
        sol = self.sol = SimpleNamespace() #endogenous

        # b. preferences
        par.rho = 2.0
        par.nu = 0.001
        par.epsilon = 1.0
        par.omega = 0.5 

        # c. household production
        par.alpha = 0.5
        par.sigma = 1.0

        # d. wages
        par.wM = 1.0
        par.wF = 1.0
        par.wF_vec = np.linspace(0.8,1.2,5) # different values for wF (Q2)

        # e. targets
        par.beta0_target = 0.4  # targets from Siminski & Yetsenga for Q4
        par.beta1_target = -0.1 # targets from Siminski & Yetsenga for Q4

        # f. solution
        sol.LM_vec = np.zeros(par.wF_vec.size)
        sol.HM_vec = np.zeros(par.wF_vec.size)
        sol.LF_vec = np.zeros(par.wF_vec.size)
        sol.HF_vec = np.zeros(par.wF_vec.size)
