# Importing packages
import numpy as np
from scipy import optimize
from copy import deepcopy
import matplotlib.pyplot as plt
from types import SimpleNamespace

# local modules
from types import SimpleNamespace
import ipywidgets as widgets

class q1:
    def __init__(self, tau):
        self.par = SimpleNamespace()
        self.par.a0 = 0.5
        self.par.alpha = 0.5
        self.par.kappa = 1.0
        self.par.nu = 1/(2 * 16**2)
        self.par.w = 1.0 
        self.optimal_tau = None

        # Adding parameters: Set 1
        self.par1 = deepcopy(self.par)
        self.par1.sigma = 1.001
        self.par1.rho = 1.001
        self.par1.epsilon = 1.0
        self.par1.kappa = 1.0

        # Adding parameters: Set 2
        self.par2 = deepcopy(self.par)
        self.par2.sigma = 1.5
        self.par2.rho = 1.5
        self.par2.epsilon = 1.0
        self.par2.kappa = 1.0


    def calculate_objective_cobbdoug(self, tau):
        """

            This code calculates and returns utility using the expressions for L and G. 
            The code snippet involves a way of detecting any RunTimeErrors. 

        """
        L_expr = (-self.par.kappa * self.par.nu + np.sqrt(self.par.nu * (4 * self.par.alpha * self.par.w**2 * (1 - tau)**2 + self.par.kappa**2 * self.par.nu))) / (2 * self.par.nu * self.par.w * (1 - tau) + 1e-08)
        G_expr = tau * (-self.par.kappa * self.par.nu + np.sqrt(self.par.nu * (4 * self.par.alpha * self.par.w**2 * (1 - tau)**2 + self.par.kappa**2 * self.par.nu))) / (2 * self.par.nu * (1 - tau) + 1e-08)

        if np.isnan(L_expr) or np.isnan(G_expr) or np.isinf(L_expr) or np.isinf(G_expr):
            return -np.inf

        V = -L_expr**2 * self.par.nu / 2 + np.log(G_expr**(1 - self.par.alpha) * (L_expr * self.par.w * (1 - tau) + self.par.kappa)**self.par.alpha)
        
        if np.isnan(V) or np.isinf(V):
            return -np.inf

        return -V

    def optimize_tau_and_print_cobbdoug(self):
        bounds = [(0, 1)]
        x0 = 0.9

        results = optimize.minimize(self.calculate_objective_cobbdoug, x0, method='Nelder-Mead', bounds=bounds)

        self.optimal_tau = results.x[0]
        objective_value = -results.fun

        print(f"Optimal tau is: {round(self.optimal_tau, 2)}")
        print(f"Worker utility at the socially optimal tax rate is: {round(objective_value, 2)}")

    def illustrate_optimal_tau_cobbdoug(self):
        if self.optimal_tau is None:
            print("Optimal tau is not available. Please run optimize_tau_and_print first.")
            return

        # Generate a range of tau values
        tau_values = np.linspace(0, 1, 100)

        # Calculate the objective function values for each tau
        objective_values = [-self.calculate_objective_cobbdoug(t) for t in tau_values]

        # Plot the objective function values against tau
        plt.plot(tau_values, objective_values)
        plt.xlabel('tau')
        plt.ylabel('Objective Function Value')
        plt.title('Utility Maximization')
        plt.grid(True)

        # Mark the optimal tau
        plt.axvline(x=self.optimal_tau, color='r', linestyle='--', label='Optimal tau')
        plt.legend()

        # Display the plot
        plt.show()

   # Define the objective function
    def calculate_objective_ces(self,x,par,var):

        """

            This code calculates and returns utility using the expressions for L and G. 
            The code snippet involves a way of detecting any RunTimeErrors. 

        """
    
        # Modifying parameters to fit Set1 or Set2
        if par == 'par1':
            params = self.par1
        elif par == 'par2':
            params = self.par2
        else:
            raise ValueError("Invalid parameter set specified.")
        
        # Modifying endogenous variables in question
        if var == 'L':

            L = x[0]
            tau = params.tau

        elif var == 'L_tau':

            L   = x[0]
            tau = x[1]

        else:
            raise ValueError("Invalid endogenous variable specified.")
        
        C = params.kappa + (1 - tau) * params.w * L
        G = tau * params.w * L 
        utility = ((params.alpha * C**((params.sigma-1) / params.sigma) + (1 - params.alpha) * G**((params.sigma-1) / params.sigma))**(1-params.rho) - 1) / (1 - params.rho)
        disutility = params.nu * (L**(1 + params.epsilon) / (1 + params.epsilon))

        return -utility + disutility

    def optimize_and_print_ces(self,par,var):
        """

            This code calculates and returns utility using the expressions for L and G. 
            The code snippet involves a way of detecting any RunTimeErrors. 

        """
        # Modifying parameters to fit Set1 or Set2
        if par == 'par1':
            params = self.par1
        elif par == 'par2':
            params = self.par2
        else:
            raise ValueError("Invalid parameter set specified.")
        
        # Modifying endogenous variables in question
        if var == 'L':

            tau = params.tau

            # Set the bounds for L
            bounds = [(1e-08, 24 + 1e-08)]

            # Initial guess for L
            x0 = [15]

        elif var == 'L_tau':

            # Set the bounds for L and tau
            bounds = [(1e-08, 24 + 1e-08), (1e-08, 1-1e-08)]

            # Initial guess for L and tau
            x0 = [15, 0.5]

        else:
            raise ValueError("Invalid endogenous variable specified.")
        
        # Perform the optimization to maximize obj with respect to L and w
        results = optimize.minimize(self.calculate_objective_ces, x0, args=(par,var), method='Nelder-Mead', bounds=bounds)

        # Get the optimal values of L 
        optimal_L = results.x[0]

        # Modifying results to fit the estimation
        if var == 'L':
            optimal_tau = tau

        elif var == 'L_tau':
            optimal_tau = results.x[1]

        else:
            raise ValueError("Invalid endogenous variable specified.")
        

        # Now find G using the obtained optimal_L and optimal_w
        G = optimal_tau * params.w * optimal_L

        # Print the optimal L, w, and the corresponding objective function value
        print(f"Optimal L: {round(optimal_L, 2)}")
        #print(f"Optimal w: {round(optimal_w, 2)}")
        print(f"Objective function value: {round(-results.fun, 2)}")
        print(f"Optimal G: {round(G, 2)}")

    def illustrate_optimal_ces(self, par, var):
        # Modifying parameters to fit Set1 or Set2
        if par == 'par1':
            params = self.par1
        elif par == 'par2':
            params = self.par2
        else:
            raise ValueError("Invalid parameter set specified.")

        # Generate a range of L values
        L_values = np.linspace(1e-08, 24-1e-08, 100)

        # Calculate the objective function values for each L
        objective_values = [-self.calculate_objective_ces([L, params.w, params.tau], par, var) for L in L_values]

        # Calculate G values for each L
        G_values = [params.tau * params.w * L for L in L_values]

        # Plot the objective function values against L
        plt.plot(L_values, objective_values, label='Objective Function')
        plt.plot(L_values, G_values, label='G')
        plt.xlabel('L')
        plt.ylabel('Value')
        plt.title('Government spending and Utility for different labor hours')
        plt.grid(True)
        plt.legend()

        # Display the plot
        plt.show()


