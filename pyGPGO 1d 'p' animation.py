import numpy as np
import os
import json
from pyGPGO.covfunc import matern52
from pyGPGO.acquisition import Acquisition
from pyGPGO.surrogates.GaussianProcess import GaussianProcess
from pyGPGO.logger import EventLogger
from pyGPGO.GPGO import GPGO
import matplotlib.pyplot as plt
from scipy.stats import qmc
from matplotlib.animation import FuncAnimation

# Set random seed for reproducibility
np.random.seed(0)

# Redefine the acquisition function class to match the expressions in the BSc Thesis
from scipy.stats import norm
class Acquisition:
    def __init__(self, mode, eps, **params):
        """
        Acquisition function class.

        Parameters
        ----------
        mode: str
            Defines the behaviour of the acquisition strategy. Currently supported values are
            `ExpectedImprovement`, `IntegratedExpectedÌmprovement`, `ProbabilityImprovement`,
            `IntegratedProbabilityImprovement`, `UCB`, `IntegratedUCB`, `Entropy`, `tExpectedImprovement`,
            and `tIntegratedExpectedImprovement`. Integrated improvement functions are only to be used
            with MCMC surrogates.
        eps: float
            Small floating value to avoid `np.sqrt` or zero-division warnings.
        params: float
            Extra parameters needed for certain acquisition functions, e.g. UCB needs
            to be supplied with `beta`.
        """
        self.params = params
        self.eps = eps

        mode_dict = {
            'ModifiedExpectedImprovement': self.ModifiedExpectedImprovement,
            'ProbabilityImprovement': self.ProbabilityImprovement,
            'UCB': self.UCB,
        }

        self.f = mode_dict[mode]

    def ProbabilityImprovement(self, tau, mean, std):
        """
        Probability of Improvement acquisition function.

        Parameters
        ----------
        tau: float
            Best observed function evaluation.
        mean: float
            Point mean of the posterior process.
        std: float
            Point std of the posterior process.

        Returns
        -------
        float
            Probability of improvement.
        """
        z = (mean - tau - self.eps) / (std)
        return norm.cdf(z)

    def ModifiedExpectedImprovement(self, tau, mean, std):
        """
        Expected Improvement acquisition function.

        Parameters
        ----------
        tau: float
            Best observed function evaluation.
        mean: float
            Point mean of the posterior process.
        std: float
            Point std of the posterior process.

        Returns
        -------
        float
            Expected improvement.
        """
        a = mean - tau - self.eps
        z = a / std
        return a * norm.cdf(z) + std * norm.pdf(z)

    def UCB(self, tau, mean, std, beta=1.5):
        """
        Upper-confidence bound acquisition function.

        Parameters
        ----------
        tau: float
            Best observed function evaluation.
        mean: float
            Point mean of the posterior process.
        std: float
            Point std of the posterior process.
        beta: float
            Hyperparameter controlling exploitation/exploration ratio.

        Returns
        -------
        float
            Upper confidence bound.
        """
        return mean + beta * std

    def eval(self, tau, mean, std):
        """
        Evaluates selected acquisition function.

        Parameters
        ----------
        tau: float
            Best observed function evaluation.
        mean: float
            Point mean of the posterior process.
        std: float
            Point std of the posterior process.

        Returns
        -------
        float
            Acquisition function value.

        """
        return self.f(tau, mean, std, **self.params)

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
lb,ub = 250,1000

# Set the parameter search space
X = np.linspace(lb,ub,ub-lb+1)
Y = [f[str(x)] for x in X]

# Set the exploration parameter
eps = 1E-2

# Set the boundaries and steps for the optimization in alphabetical order
params = {'p': ('cont',[lb,ub])}

# Define the acquisition function
acq = Acquisition(mode='ModifiedExpectedImprovement',eps=eps) # eps typically between 0 and 0.1
#acq = Acquisition(mode='UCB',eps=0)

# Define the covariance function
l = 50 # l = length scale
sigmaf = 30 # sigmaf = output scale
cov = matern52(l=l,sigmaf=sigmaf,sigman=0)  # sigman = noise scale

# Set the initial data
# Make the LHS with correct boundaries
sampler = qmc.LatinHypercube(d=len(params),seed=0)
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

# Define the Gaussian process surrogate model
gp = GaussianProcess(cov,mprior=0)

# Update the GP with the initial data
initial_points = np.array(initial_points)
initial_points = initial_points[:, np.newaxis]
initial_targets = np.array(initial_targets)
gp.fit(initial_points,initial_targets)

# Set the optimizer with surrogate model, acquisition function, objective function and parameter search space
optimizer = GPGO(gp, acq, f, params)
optimizer.tau = np.max(initial_targets)            # tau = ymax

# Run the optimizaton for the number of total simulations
probed_points = initial_points
probed_targets = initial_targets

# Create the figure and subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]})

# Function to update the plots
def update(i):
    global probed_points
    global probed_targets
    axs[0].clear()
    axs[1].clear()

    mean, std = gp.predict(X.reshape(-1, 1), return_std=True)
    axs[0].plot(X, Y, color='blue')
    axs[0].plot(X, mean, color='orange', label='Mean')
    axs[0].fill_between(X, mean - std, mean + std, color='lightblue', alpha=0.4, label='Std. Dev.')
    axs[0].scatter(probed_points, probed_targets, c="red", s=20, zorder=10)
    axs[0].scatter(initial_points, initial_targets, c="black", s=20, zorder=10)
    axs[0].set_ylabel(r'$\Delta T^\text{ext}_0$ [K]') 
    axs[0].set_title(r'$r = 100$ nm & $h = 30$ nm')
    
    axs[0].legend(loc='upper right')

    optimizer._optimizeAcq()
    Z = [-optimizer._acqWrapper(x)[0] for x in X]
    z_min = np.min(Z)
    axs[1].fill_between(X, Z, [z_min for _ in X], facecolor='green', alpha=0.3)
    axs[1].plot(X, Z, color='green', label='Acquisition')
    axs[1].set_xlabel('pitch p [nm]')
    axs[1].set_ylabel('Acquisition Function')
    axs[1].legend(loc='upper right')
    
    if i <= total_sims - init_sims and i > 0:
        # Suggest the next point to probe
        next_point = optimizer.best
        x = round(next_point[0])
        x = float(x)

        j = 1
        while x in probed_points:
            if (x + j) not in probed_points and x+j <= ub:
                x = x + j
                break
            if (x - j) not in probed_points and x-j >= lb:
                x = x - j
                break
            j += 1

        target = f[str(x)]
        probed_targets = np.append(probed_targets,target)
        probed_points = np.append(probed_points,[[x]],axis=0)

        # Show point chosen for next iteration
        axs[1].scatter(x, -optimizer._acqWrapper(x), c="red", s=20, zorder=10)

        # Fit the GP with the new probed point and target
        gp.fit(probed_points, probed_targets)

    # Add a subtitle to the figure
    fig.suptitle(r'1d slice in p, pyGPGO $\ell=50$, $\lambda=30$, MEI $\varepsilon=10^{-2}$')
    
    plt.tight_layout()
    plt.savefig("pyGPGO 1d 'p' animation (250,1000)-"+str(i-1)+".png")  # For .png files only

"""
The code below is to produce a .gif file

# Create the animation
ani = FuncAnimation(fig, update, frames=total_sims - init_sims + 1, interval=500, repeat=False)

# Save as GIF using PillowWriter
ani.save("pyGPGO 1d 'p' animation (250,1000).gif", writer='pillow', fps=60)
"""

#The code below is to create is sequence of .png files

# Save each frame as a PNG file
for i in range(total_sims-init_sims+1):
    update(i)
