from scipy import optimize

def solve_ss(alpha, c):
    """ Example function. Solve for steady state k. 

    Args:
        c (float): costs
        alpha (float): parameter

    Returns:
        result (RootResults): the solution represented as a RootResults object.

    """ 
    
    # a. Objective function, depends on k (endogenous) and c (exogenous).
    f = lambda k: k**alpha - c
    obj = lambda kss: kss - f(kss)

    #. b. call root finder to find kss.
    result = optimize.root_scalar(obj,bracket=[0.1,100],method='bisect')
    
    return result

def demand(a, b, p_i, p_j):
    """ Returns demand faced by firm i

    Args:
        p_i (float): price for firm i 
        p_j (float): price for firm j

    Returns:
        demand (RootResults): the return is demand

    """ 
    
    # a. Objective function
    if p_i > p_j: 
        demand = 0
    elif p_i == p_j: 
        demand = 1/2*(a-b*p_i)
    else:
        demand = (a-b*p_i)

    return demand

def profit(p_i, p_j, c, demand):
    """ Returns profit for firm i

    Args:
        c (float): marginal costs
        p_i (float): price for firm i 
        p_j (float): price for firm j

    Returns:
        profit (RootResults): the return is profit

    """ 
    
    # a. Objective function
    if p_i > p_j: 
        profit = 0
    elif p_i == p_j: 
        profit = (p_i-c)*1/2*demand
    else:
        profit = (p_i-c)*1/2*demand

    return profit

# def differentiated_goods():





# fra hold 6-7
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from types import SimpleNamespace
import ipywidgets as widgets

class CournotNashEquilibriumSolver:
    def __init__(self):
        """ setup model """

        par = self.par = SimpleNamespace()

        par.a = 1 # demand for good 1
        par.b = 1 # demand for good 2
        par.X = 20 # demand for p=0
        par.c  = [0,0] # marginal cost
        
    def demand_function(self, q1, q2):
        par = self.par
        demand = par.X-par.a*q1-par.b*q2 # inverted demand function
        return demand

    def cost_function(self, q, c):
        return c*q # marginal cost times quantity

    def profits(self, c, q1, q2): 
        # income - expenditures
        return self.demand_function(q1,q2)*q1-self.cost_function(q1,c)
    
    def reaction(self, q2,c1):
        # Maaaaaaax profit
        responce =  optimize.minimize(lambda x: - self.profits(c1,x,q2), x0=0, method = 'SLSQP')
        return responce.x # best responce

    def fixed_point(self, q):
        par = self.par
        # the fixed point is the q that equals the reaction.
        return np.array((q[0]-self.reaction(q[1],par.c[0]),q[1]-self.reaction(q[0],par.c[1]))).reshape(2)


    def solve_eq(self):
        initial_guess = np.array([0,0])
        # solve system of equations.
        res = optimize.fsolve(lambda q: self.fixed_point(q), initial_guess)
        return res