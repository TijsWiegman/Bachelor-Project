# Import the required libraries
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from bayes_opt import BayesianOptimization
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
from bayes_opt import UtilityFunction
from scipy.stats import qmc
from scipy.stats import norm
from matplotlib.animation import FuncAnimation

np.random.seed(seed=0)

# Define the acquisition functions
def MEI(mean,std,ymax,eps,x):
    x = np.where(X == x)[0][0]
    mean,std = list(mean),list(std)
    a = mean[x] - ymax - eps
    z = a / std[x]
    return a*norm.cdf(z) + std[x]*norm.pdf(z)

# Find file path to objective function data set
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '1d_slice_p.json')

# Load the data of the objective function
with open(file_path, 'r') as json_file:
    # Load the dictionary from the first line of the file
    f = json.load(json_file)

# Set the number of simulations per dimension for the initial population
init_sims = 3

# Set the number of total simulations
total_sims = 30

# Set lower and upper bounds for search space
lb,ub = 100,1000

# Set the boundaries and steps for the optimization in alphabetical order
pbounds = {'p': (lb, ub)}

# Set the parameter search space
X = np.linspace(lb,ub,ub-lb+1)
Y = [f[str(x)] for x in X]

# Set the exploration parameter
eps = 1E-2

# Initializing the BayesianOptimization object
optimizer = BayesianOptimization(f=None, pbounds=pbounds,allow_duplicate_points=True,random_state=0)

# Make the utility function to optimize with, the kind can be: 'ucb', 'ei', 'poi'
utility = UtilityFunction(kind='ei', xi=eps)

# Set the initial data
# Make the LHS with correct boundaries
sampler = qmc.LatinHypercube(d=len(pbounds),seed=0)
samples = sampler.random(n=init_sims)
samples = qmc.scale(samples, lb, ub)

initial_points = []
initial_targets = []

# Loop over the LHS
for s in samples:
    # Round the parameters to the step size of 1
    x = round(s[0])
    x = float(x)
    initial_points.append(x)
    
    # Simulate the rounded parameters
    x = str(x)
    target = f[x]

    # Register the rounded parameters with the found temperature
    initial_targets.append(target)

    # Register the observation with the optimizer
    optimizer.register(params=x, target=target)

probed_points = initial_points
probed_targets = initial_targets

# Create the figure and subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]})

"""
The code below is to produce a .gif file

# Function to update the plots
def update(i):
    global probed_points
    global probed_targets
    axs[0].clear()
    axs[1].clear()

    mean, std = optimizer._gp.predict(X.reshape(-1, 1), return_std=True)  # Compute mean and std prediction
    axs[0].plot(X, Y, color='blue')
    axs[0].plot(X, mean, color='orange', label='Mean')
    axs[0].fill_between(X, mean - std, mean + std, color='lightblue', alpha=0.4, label='Std. Dev.')
    axs[0].scatter(probed_points, probed_targets, c="red", s=20, zorder=10)
    axs[0].scatter(initial_points, initial_targets, c="black", s=20, zorder=10)
    axs[0].set_ylabel(r'$\Delta T^\text{ext}_0$ [K]')
    axs[0].set_title('1d bo plot, EI xi=1E-4')
    axs[0].legend()

    ymax = np.max(probed_targets)
    xmax = probed_points[np.where(probed_targets == ymax)[0][0]]
    Z = [MEI(mean,std,ymax,eps,x) for x in X]
    #axs[1].scatter(xmax, ymax, c="red", s=20, zorder=10)
    zmin = np.min(Z)
    axs[1].fill_between(X, Z, [0 for _ in X], facecolor='green', alpha=0.3)
    axs[1].plot(X, Z, color='green')
    axs[1].set_xlabel('pitch p [nm]')
    axs[1].set_ylabel('Acquisition Function')

    if i <= total_sims - init_sims:
        # Suggest the next point to probe
        next_point = optimizer.suggest(utility)
        x = round(next_point['p'])
        x = float(x)

        if x in probed_points:
            return
        
        else:
            target = f[str(x)]
            optimizer.register(params=x, target=target)
            probed_targets = np.append(probed_targets,target)
            probed_points = np.append(probed_points,x)
        
        # Register the observation with the optimizer
        optimizer.register(params=x, target=target)

    plt.tight_layout()

# Create the animation
ani = FuncAnimation(fig, update, frames=total_sims - init_sims + 1, interval=5000, repeat=False)

# Save as GIF using PillowWriter
ani.save('BO 1d animation (100,1000).gif', writer='pillow', fps=60)

"""

"""
The code below is to create is sequence of .png files
"""
# Function to update the plots
def update(i):
    global probed_points
    global probed_targets
    axs[0].clear()
    axs[1].clear()

    mean, std = optimizer._gp.predict(X.reshape(-1, 1), return_std=True)  # Compute mean and std prediction
    axs[0].plot(X, Y, color='blue')
    axs[0].plot(X, mean, color='orange', label='Mean')
    axs[0].fill_between(X, mean - std, mean + std, color='lightblue', alpha=0.4, label='Std. Dev.')
    axs[0].scatter(probed_points[:-1], probed_targets[:-1], c="red", s=20, zorder=10)
    axs[0].scatter(initial_points, initial_targets, c="black", s=20, zorder=10)
    axs[0].set_ylabel(r'$\Delta T^\text{ext}_0$ [K]')
    axs[0].set_ylim(-110,160)
    axs[0].set_title(r"1d slice in p, BO, MEI  $\varepsilon = 10^{-2}$")

    axs[0].legend(loc='upper right')

    y_max = np.max(probed_targets)
    Z = [MEI(mean, std, y_max, eps, x) for x in X]
    z_min = np.min(Z)
    axs[1].fill_between(X, Z, [z_min for _ in X], facecolor='green', alpha=0.3)
    axs[1].plot(X, Z, color='green',label='Acquisition')
    axs[1].set_xlabel('pitch p [nm]')
    axs[1].set_ylabel('Acquisition Function')
    axs[1].legend(loc='upper right')

    # Find the maximum of the acquisition function
    max_acq_value = np.max(Z)
    max_acq_index = np.argmax(Z)
    max_acq_x = X[max_acq_index]
    axs[1].scatter(max_acq_x, max_acq_value, c="red", s=20, zorder=10)

    if i <= total_sims - init_sims and i > 0:
        # Suggest the next point to probe
        next_point = optimizer.suggest(utility)
        x = round(next_point['p'])
        x = float(x)

        target = f[str(x)]
        probed_targets = np.append(probed_targets, target)
        probed_points = np.append(probed_points, x)

        # Update the GP with the new probed point and target
        optimizer.register(params=x, target=target)

    plt.tight_layout()
    plt.savefig("BO 1d 'p' animation (100,1000)-"+str(i-2)+".png")

# Save each frame as a PNG file
for i in range(total_sims - init_sims + 2):
    update(i)
