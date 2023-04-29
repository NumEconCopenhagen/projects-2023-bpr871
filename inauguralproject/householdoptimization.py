from types import SimpleNamespace

import numpy as np
from scipy import optimize
import scipy.stats as stats

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
        """
        This function calculates the utility of the household. 

        Args:
            The inputs for the utility function consists of: 

                - HM: Hours worked in household for male agent.
                - LM: Hours worked in the market for male agent.
                - HF: Hours worked in household for female agent.
                - LF: Hours worked in the market for female agent. 

        Utility is calculated using labor hours as well as consumption. 
        Only labor hours in the market can be converted in to consumption. 

        Returns:
            utility - disutility: Returns net utility of the household as a whole.
        """
        
        par = self.par
        sol = self.sol

        # a. consumption of market goods
        C = par.wM*LM + par.wF*LF

        # b. home production
        if np.isclose(par.sigma, 0, atol=1e-08, equal_nan=False):
            H = min(HM,HF)
        elif np.isclose(par.sigma, 1, atol=1e-08, equal_nan=False):
        #par.sigma == 1:
            H = HM**(1-par.alpha)*HF**par.alpha
        else:
            H = ((1-par.alpha)*HM**((par.sigma-1)/(par.sigma + 1e-8)) + par.alpha*HF**((par.sigma-1)/(par.sigma + 1e-8)))**((par.sigma)/(par.sigma-1 + 1e-8))


        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho + 1e-8)

        # d. disutility of work
        epsilon_ = 1+1/(par.epsilon + 1e-8) # to shorten the function
        TM = LM+HM
        TF = LF+HF
        disutility = par.nu*(TM**epsilon_/(epsilon_+ 1e-8)+TF**epsilon_/(epsilon_+ 1e-8))

        return  utility - disutility 
    
    def solve_discrete(self,do_print=False):
        """
        This function solves the maximization problem of the household discretely.

        Utility is calculated using labor hours as well as consumption. 
        Only labor hours in the market can be converted in to consumption. 

        Returns:
            (LM, HM, LF, HF): Returns a NameSpace containing solutions to the discrete maximization problem. 
        """

        opt = SimpleNamespace()

        # a. possible choices of labor
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations

        LM = LM.ravel() # unravels LM from the meshgrid?
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        # b. utility
        u = self.utility(LM,HM,LF,HF)

        # c. if T > 24 return minus infinity (constraint broken)
        I = (LM+HM > 24) | (LF+HF > 24) 
        u[I] = -np.inf

        # d. find maximizing argument for endogenous variables
        j = np.argmax(u)
        
        opt.LM = LM[j] 
        opt.HM = HM[j]
        opt.LF = LF[j]
        opt.HF = HF[j]

        # e. print 
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')
        
        return opt

    def solve(self):
        """
        This function solves the maximization problem of the household continuously.

        Utility is calculated using labor hours as well as consumption. 
        Only labor hours in the market can be converted in to consumption. 

        Returns:
            LM, HM, LF, HF: Returns the four solutions to the continuous maximization problem. 
        """
    
        #par = self.par
        #sol = self.sol
        #opt = SimpleNamespace()

        def objective(x):
            return -self.utility(*x)    
        
        # d. constraints and bounds: if T > 24 return minus infinity (constraint broken)
        budget_constraint = lambda LM, HM, LF, HF: (LM+HM > 24) | (LF+HF > 24)  # violated if negative
        constraints = ({'type':'ineq','fun':budget_constraint})
        bounds = [(1e-8,24-1e-8),(1e-8,24-1e-8), (1e-8,24-1e-8),(1e-8,24-1e-8)]
        
        # c. call solver
        x0 = [2,2,2,2]
        result = optimize.minimize(objective,x0, method='Nelder-Mead', bounds = bounds, constraints=constraints)  #method='SLSQP',bounds=bounds,

        # d. unpack variables
        LM = result.x[0]
        HM = result.x[1]
        LF = result.x[2]
        HF = result.x[3]

        return LM, HM, LF, HF
   
    def get_ratios(self):
        """
        This function return the solution of the household maximization problem over a loop of values of wF. 

        Args:
            Parameters of the class.

        The function inputs a vector of values for wF in to the solve function and returns a vector of results. 
        Results and inputs are calculated as a log of the ratio between the value of the male and female agent (HF/HM), (wF/wM). 

        Returns:
            ratio_H, ratio_w.
        """
        sol = self.sol
        par = self.par

        sol.HM_wage_vec = []
        sol.HF_wage_vec = []
        sol.solution_wage = []
        par.wF_list = (0.8, 0.9, 1.0, 1.1, 1.2)


        # b. for loop
        for wages in par.wF_list:
            par.wF = wages
            LM, HM, LF, HF = self.solve()
                
            #extracting results
            sol.HM_wage_vec.append(HM)
            sol.HF_wage_vec.append(HF)
            
            #test: assesing the values of HM, HF and the utility
            print(HM, HF)
            print(self.utility(LM, HM, LF, HF))

            
        #c. extracting results
        #sol.HF_wage_vec = [ns[3] for ns in sol.solution_wage]
        #sol.HM_wage_vec = [ns[2] for ns in sol.solution_wage]

        ratio_H = [np.log(a/b) for a, b in zip(sol.HF_wage_vec, sol.HM_wage_vec)]
        ratio_w = np.log(par.wF_list)    

        return ratio_H, ratio_w

    def extension(self,LM,HM,LF,HF,mu):
        par = self.par
        sol = self.sol

        # Optimize over mu to implement the target parameters when alpha = 0.5
        disutility = self.nu*((mu*LM + HM)**self.epsilon_/(self.epsilon_+ 1e-8)+(LF + HF)**self.epsilon_/(self.epsilon_+ 1e-8))

        return  self.utility() - disutility 







            




