from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt


# Predefine options for all plots
%matplotlib inline
from   mpl_toolkits.mplot3d import Axes3D # Used implictely when doing 3D plots
import matplotlib.pyplot as plt # baseline module

plt.rcParams.update({"axes.grid":True,"grid.color":"black","grid.alpha":"0.25","grid.linestyle":"-"})
plt.rcParams.update({'font.size': 14})

def plot_Q1():
    # a. create the figure
    fig = plt.figure()

    # b. plot
    ax = fig.add_subplot(1,1,1)

    ax.plot(HM_vec,HF_vec) 

    #label for alpha-values?

    ax.set_title('Household hours ratio, $\frac{HF}{HM}$')
    ax.set_xlabel('$HM$')
    ax.set_ylabel('$HF$')





