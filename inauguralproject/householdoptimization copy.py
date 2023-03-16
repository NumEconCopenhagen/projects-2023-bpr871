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

        sol.beta0 = np.nan
        sol.beta1 = np.nan

    def utility(self,LM,HM,LF,HF):
        """ calculating utility 
        args: self, LM, HM, LF, HF
        tilføj?"""

        par = self.par
        sol = self.sol

        # a. consumption of market goods
        C = par.wM*LM + par.wF*LF

        # b. home production
        if par.sigma == 0:
            H = min(HM,HF)
        elif par.sigma == 1:
            H = HM**(1-par.alpha)*HF**par.alpha
        else:
            ((1-par.alpha)*HM**((par.sigma-1)/(par.sigma))
            + par.alpha*HF**((par.sigma-1)/(par.sigma)))**((par.sigma)/(par.sigma-1))

        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho)

        # d. disutility of work
        epsilon_ = 1+1/par.epsilon # shorten function?
        TM = LM+HM
        TF = LF+HF
        disutility = par.nu*(TM**epsilon_/epsilon_+TF**epsilon_/epsilon_)

        return  utility - disutility 
    
    def solve_discrete(self,do_print=False):
        """ solve model discretely """

        par = self.par
        sol = self.sol
        opt = SimpleNamespace()

        # a. possible choices of labor
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations

        LM = LM.ravel() # unravels LM from the meshgrid?
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        # b. utility
        u = self.utility(self,LM,HM,LF,HF)

        # c. if T > 24 return minus infinity (constraint broken)
        I = (LM+HM > 24) | (LF+HF > 24) 
        u[I] = -np.inf

        # d. find maximizing argument for endogenous variables
        j = np.argmax(u)
        
        opt.LM = LM[j] #from unravel function ?
        opt.HM = HM[j]
        opt.LF = LF[j]
        opt.HF = HF[j]

        # e. print ? does the dictionary need to be pre-defined ? 
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')
        
        return opt

    def solve_cont(self,do_print=False):
    
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()

        def objective(x):
            return -self.utility(*x)    
        
        # d. constraints and bounds: if T > 24 return minus infinity (constraint broken)
        budget_constraint = lambda LM, HM, LF, HF: (LM+HM > 24) | (LF+HF > 24)  # violated if negative
        constraints = ({'type':'ineq','fun':budget_constraint})
        bounds = ((1e-8,24-1e-8),(1e-8,24-1e-8), (1e-8,24-1e-8),(1e-8,24-1e-8))
        
        # c. call solver
        x0 = [2,2,2,2]
        #method='SLSQP',bounds=bounds,constraints=constraints
        result = optimize.minimize(objective,x0)

        return result


        """
        # f. save the results
        LM = sol.LM = result.x[1]
        HM = sol.HM = result.x[2]
        LF = sol.LF = result.x[3]
        HF = sol.HF = result.x[3]

        # e. print ? does the dictionary need to be pre-defined ? 
        #if do_print:
        #    for k,v in opt.__dict__.items():
        #        print(f'{k} = {v:6.4f}')
        
        return result   
        
        # a. objective function (to minimize) 
        #obj = lambda x: -model.utility(x[0],x[1]) # minimize -> negtive of utility
            
        # b. constraints and bounds
        #budget_constraint = lambda x: par.m-par.p1*x[0]-par.p2*x[1] # violated if negative
        #constraints = ({'type':'ineq','fun':budget_constraint})
        #bounds = ((1e-8,par.m/par.p1-1e-8),(1e-8,par.m/par.p2-1e-8))
        # d. save
        #sol.x1 = result.x[0]
        #sol.x2 = result.x[1]
        #sol.u = model.u_func(sol.x1,sol.x2)
        """


            




