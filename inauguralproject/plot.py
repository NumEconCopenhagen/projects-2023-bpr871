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

# a. create the figure
fig = plt.figure()

# b. plot
ax = fig.add_subplot(1,1,1)

ratio = HF/HM # where do we put the definition of ratio?
ax.plot(ratio,alpha) # where do we put input of alphas?

ax.set_title('Household hours ratio, $\frac{HF}{HM}$')
ax.set_xlabel('$\alpha$')
ax.set_ylabel('$\frac{HF}{HM}$')



