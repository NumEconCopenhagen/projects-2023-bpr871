# Importing packages
import numpy as np
from scipy import optimize
from copy import deepcopy
import matplotlib.pyplot as plt
from types import SimpleNamespace

# local modules
from types import SimpleNamespace
import ipywidgets as widgets
import matplotlib.gridspec as gridspec

class q1:
    def __init__(self, tau):

        """
        Initializes the q1 class with the specified tau value.
        
        Args:
            tau (float): The tau value.
        """

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
        Calculates and returns the utility using the expressions for L and G.
        
        Args:
            tau (float): The tau value.
        
        Returns:
            float: The utility value.
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

        """
        Optimizes tau and prints the optimal tau and worker utility at the socially optimal tax rate.
        """

        bounds = [(0, 1)]
        x0 = 0.9

        results = optimize.minimize(self.calculate_objective_cobbdoug, x0, method='Nelder-Mead', bounds=bounds)

        self.optimal_tau = results.x[0]
        objective_value = -results.fun

        print(f"Optimal tau is: {round(self.optimal_tau, 2)}")
        print(f"Worker utility at the socially optimal tax rate is: {round(objective_value, 2)}")

    def illustrate_optimal_tau_cobbdoug(self):
        """
        Illustrates the optimal tau for the Cobb-Douglas utility function.
        """
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
        Calculates and returns the utility using the CES (Constant Elasticity of Substitution) function.
        
        Args:
            x (list): List containing the values of the endogenous variables.
            par (str): Parameter set ('par1' or 'par2').
            var (str): Endogenous variable ('L' or 'L_tau').
        
        Returns:
            float: The utility value.
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
        utility = ((((params.alpha * C ** ((params.sigma - 1) / params.sigma) + (1 - params.alpha) * G ** ((params.sigma - 1) / params.sigma))) ** (params.sigma / (params.sigma - 1))) ** (1 - params.rho) - 1) / (1 - params.rho)
        disutility = params.nu * (L ** (1 + params.epsilon) / (1 + params.epsilon))

        # C = params.kappa + (1 - tau) * params.w * L
        # G = tau * params.w * L 
        # utility = ((((params.alpha * C**((params.sigma-1) / params.sigma) + (1 - params.alpha) * G**((params.sigma-1) / params.sigma)))**(params.sigma/params.sigma-1))**(1-params.rho) - 1) / (1 - params.rho)
        # disutility = params.nu * (L**(1 + params.epsilon) / (1 + params.epsilon))

        return -utility + disutility

    def optimize_and_print_ces(self,par,var):

        """
        Optimizes the endogenous variable and prints the optimal values and the corresponding objective function value.
        
        Args:
            par (str): Parameter set ('par1' or 'par2').
            var (str): Endogenous variable ('L' or 'L_tau').
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
        print(f"Objective function value: {round(-results.fun, 2)}")
        print(f"Optimal G: {round(G, 2)}")

    def illustrate_optimal_ces(self, par, var):

        """
        Illustrates the optimal values for the CES function.
        
        Args:
            par (str): Parameter set ('par1' or 'par2').
            var (str): Endogenous variable ('L' or 'L_tau').
        """

        # Modifying parameters to fit Set1 or Set2
        if par == 'par1':
            params = self.par1
        elif par == 'par2':
            params = self.par2
        else:
            raise ValueError("Invalid parameter set specified.")

        # Generate a range of L values
        L_values = np.linspace(1e-08, 24-1e-08, 100)

        # Calculate the utility values for each L
        utility_values = [-self.calculate_objective_ces([L, params.w, params.tau], par, var) for L in L_values]

        # Calculate the corresponding G values for each L
        G_values = [params.tau * params.w * L for L in L_values]

        # Set the figure size to fit the notebook width
        plt.figure(figsize=(12, 4))

        # Create a gridspec layout with 1 row and 2 columns
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.2])

        # Plot utility against L
        ax1 = plt.subplot(gs[0])
        ax1.plot(L_values, utility_values)
        ax1.set_xlabel('L')
        ax1.set_ylabel('Utility')
        ax1.set_title('Utility for different labor hours')
        ax1.grid(True)

        # Plot G against L
        ax2 = plt.subplot(gs[1])
        ax2.plot(L_values, G_values)
        ax2.set_xlabel('L')
        ax2.set_ylabel('G')
        ax2.set_title('Government Spending for different labor hours')
        ax2.grid(True)

        # Adjust the spacing between subplots
        plt.tight_layout()

        # Adjust the layout to fit the notebook width
        plt.subplots_adjust(left=0.05, right=0.95)

        # Display the plots
        plt.show()