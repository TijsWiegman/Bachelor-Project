import mph
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
from scipy.stats import norm
from datetime import datetime
import logging

# Fix random seed for reproducibility
np.random.seed(0)

# Redefine the acquisition function class to match the expressions in the BSc Thesis
class Acquisition:
    def __init__(self, mode, **params):
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

        mode_dict = {
            'ModifiedExpectedImprovement': self.ModifiedExpectedImprovement,
            'ProbabilityImprovement': self.ProbabilityImprovement,
            'UCB': self.UCB,
        }

        self.f = mode_dict[mode]

    def ProbabilityImprovement(self, tau, mean, std, eps):
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
        z = (mean - tau - eps) / (std)
        return norm.cdf(z)

    def ModifiedExpectedImprovement(self, tau, mean, std, eps):
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
        a = mean - tau - eps
        z = a / std
        return a * norm.cdf(z) + std * norm.pdf(z)

    def UCB(self, tau, mean, std, beta):
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

# Define a logger
    def format(self, record):
        log_entry = {
            'target': record.levelname,
            'params': record.getMessage(),
            'datetime': datetime.fromtimestamp(record.created).isoformat(),
            'elapsed': record.elapsed,
            'delta': record.relativeCreated / 1000.0  # Convert from ms to s
        }
        return log_entry

# Define the function used to log results
def log(target, p, r, h):
    log_entry = {
        'target': target,
        'params': {'p': p, 'r': r, 'h': h},
        'datetime': str(datetime.now()),
        'elapsed': str((datetime.now() - start_time).total_seconds())}

    with open(file_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    return

# Set the start time for the logs
start_time = datetime.now()

# Set the COMSOL model you want to load as a string
comsol = 'Toy problem v2'

# Set the filename of the logs file as a string
logfile = 'logfile'

# Create empty .json file named logs
load = 'logs'
file_path = f'./{load}.json'

os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, 'w') as file:
    pass

# Define the COMSOL model
client = mph.start()

# If a comsol file is give load it, otherwise make from function
if comsol != None:
    model = client.load(comsol)
else:
    print('model not found')

# Define the objective function
from ObjectiveFunction import objective_function
f = objective_function

# Set the number of simulations per dimension for the initial population
init_sims = 10

# Set the number of total simulations
total_sims = 250

# Set the exploration parameter
eps = 1E-2

# Set the boundaries and steps for the optimization in alphabetical order
params = {'p': ('cont',[100,1000]), 'r': ('cont',[15,150]), 'h': ('cont',[15,60])}

# Define the acquisition function
acq = Acquisition(mode='ModifiedExpectedImprovement',eps=eps) # eps typically between 0 and 0.1
#acq = Acquisition(mode='UCB',eps=0)

# Define the covariance function
l = 30 # l = length scale
sigmaf = 150 # sigmaf = output scale
cov = matern52(l=l,sigmaf=sigmaf,sigman=0)  # sigman = noise scale

# Set the initial data
# Make the LHS with correct boundaries
sampler = qmc.LatinHypercube(d=len(params),seed=0)
samples = sampler.random(n=init_sims)
l_bounds = [params[p][1][0] for p in params]
u_bounds = [params[p][1][1] for p in params]
samples = qmc.scale(samples, l_bounds, u_bounds)

# Initialize the probed points and targets list
probed_points = []
probed_targets = []

# Loop over the LHS
for s in samples:
    # Round the parameters to the step size of 1
    p = round(s[0])
    r = round(s[1])
    h = round(s[2])
    probed_points.append(tuple([p,r,h]))
    
    # Simulate the rounded parameters
    target = f(p,r,h)

    # Register the rounded parameters with the found temperature
    probed_targets.append(target)

    # Log the points in the .json logs file
    exec('log(target, p, r, h)')

# Define the Gaussian process surrogate model
gp = GaussianProcess(cov,mprior=0)

# Recast the probed_points and probed_targets in the proper format
probed_points = np.array(probed_points)
probed_points = probed_points.reshape(-1,3)
probed_targets = np.array(probed_targets)

# Fit the model to the probed points
gp.fit(probed_points,probed_targets)

# Set the optimizer with surrogate model, acquisition function, objective function and parameter search space
optimizer = GPGO(gp, acq, f, params)
optimizer.tau = np.max(probed_targets)            # tau = ymax

# For the remaing iterations, we run the BO algorithm
for i in range(total_sims-init_sims):
    optimizer._optimizeAcq()
    # Suggest the next point to probe
    optimizer._optimizeAcq()
    next_point = optimizer.best
    p = round(next_point[0])
    r = round(next_point[1])
    h = round(next_point[2])

    target = f(p,r,h)

    # Find unprobed point closest to point suggested by acquisition function
    j = 1
    while [p,r,h] in probed_points:
        if (p + j) not in probed_points and p+j <= params['p'][1][1]:
            p = p + j
            break
        if (p - j) not in probed_points and p-j >= params['p'][1][0]:
            p = p - j
            break
        if (r + j) not in probed_points and r+j <= params['r'][1][1]:
            r = r + j
            break
        if (r - j) not in probed_points and r-j >= params['r'][1][0]:
            r = r - j
            break
        if (h + j) not in probed_points and h+j <= params['h'][1][1]:
            h = h + j
            break
        if (h - j) not in probed_points and h-j >= params['h'][1][0]:
            h = h - j
            break
        print(j)
        j += 1

    # Store probed point and target in respective lists
    probed_targets = np.append(probed_targets,target)
    probed_points = np.append(probed_points,[[p,r,h]],axis=0)

    # Update the GP with the new point and target
    gp.fit(probed_points, probed_targets)

    # Log the points in the .json logs file
    exec('log(target, p, r, h)')
