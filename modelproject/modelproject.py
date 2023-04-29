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

