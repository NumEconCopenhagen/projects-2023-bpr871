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

def demand_Q(a, b, p_i, p_j):
    """ Returns demand faced by firm i: Return the quantity demanded

    Args:
        p_i (float): price for firm i 
        p_j (float): price for firm j

    Returns:
        demand (RootResults): the return is demand

    """ 
    
    # a. Objective function
    if p_i > p_j: 
        demand_Q = 0
    elif p_i == p_j: 
        demand_Q = 1/2*(a-b*p_i)
    else:
        demand_Q = (a-b*p_i)

    return demand_Q

def demand_P(a, q_1, q_2):
    """ Returns total demand: Return the willingness to pay at a given quantity
    Args:
        q_1 (float): quantity produced for firm 1
        q_2 (float): quantity produced for firm 2

    Returns:
        demand (RootResults): the return is demand

    """ 
    
    # a. Objective function
    demand_P = a - (q_1 + q_2)

    return demand_P

def profit(p_i, p_j, c, demand_Q):
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
        profit = (p_i-c)*1/2*demand_Q
    else:
        profit = (p_i-c)*1/2*demand_Q

    return profit

def stackelberg_reaction(q_1, a, c):
    """ Returns optimal quantities produced for firm 1 and firm 2
    Firm 1: Leader
    Firm 2: Follower

    Args:
        demand (function): function for demand from consumers of the homogenous good
        c (float): marginal costs

    Returns:
        q_1: optimal quantity produced by firm 1 (leader)
        q_2: optimal quantity produced by firm 2 (follower)
    """ 
    q_2 = (a-q_1-c)/2

    return q_2

def sol_stackelberg(demand_Q, c):
    """ Returns optimal quantities produced for firm 1 and firm 2
    Firm 1: Leader
    Firm 2: Follower

    Args:
        demand (function): function for demand from consumers of the homogenous good
        c (float): marginal costs

    Returns:
        q_1: optimal quantity produced by firm 1 (leader)
        q_2: optimal quantity produced by firm 2 (follower)
    """ 





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

        par.alpha = 1 # preference for good 1
        par.beta = 1 # preference for good 2
        par.X = 20 # demand for p=0
        par.c  = [0,0] # marginal cost
        
    def demand_function(self, q1, q2):
        # the inverted demand function
        par = self.par
        demand = par.X-par.alpha*q1-par.beta*q2 
        return demand

    def cost_function(self, q, c):
        return c*q # marginal cost times quantity

    def profits(self, c, q1, q2): 
        # income - costs
        income = self.demand_function(q1,q2)*q1
        cost = self.cost_function(q1,c)
        profit = income - cost
        return profit
    
    def reaction(self, q1,c2):
        # company 2 reacts to price of company 1
        response =  optimize.minimize(lambda x: - self.profits(c2,x,q1), x0=0, method = 'SLSQP')
        return response.x # best response

    def fixed_point(self, q):
        par = self.par
        # the fixed point is the q that equals the reaction.
        return np.array((q[0]-self.reaction(q[1],par.c[0]),q[1]-self.reaction(q[0],par.c[1]))).reshape(2)


    def solve_eq(self):
        initial_guess = np.array([0,0])
        # solve system of equations.
        res = optimize.fsolve(lambda q: self.fixed_point(q), initial_guess)
        return res