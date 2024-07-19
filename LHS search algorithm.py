# Import the required libraries
import mph
import os
import numpy as np
from scipy.stats import qmc

# Set the COMSOL model you want to load as a string
comsol = 'Toy problem v2'  # was None

for i in range(1,11):
    # Set different random seed for each
    np.random.seed(seed=i)

    # Set the filename of the logs file as a string
    logfile = 'LHS random #'+str(i)

    # Create empty .json file named logs
    load = 'logs'
    file_path = f'./{load}.json'

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as file:
        pass

    # Set the number of total simulations
    total_sims = 250

    # Set the boundaries and steps for the optimization in alphabetical order
    pbounds = {'h': (15, 60), 'p': (100, 1000), 'r': (15, 150)}
    steps = {'h': 1, 'p': 1, 'r': 1}

    # Define the COMSOL model
    client = mph.start()

    # If a comsol file is give load it, otherwise make from function
    if comsol != None:
        model = client.load(comsol)
    else:
        print('model not found')

    from ObjectiveFunction import objective_function

    # Rename the logs file so it does not get overwritten before loading
    if load != None:
        os.rename(f'./{load}.json', f'./{load}_old.json')

    probed_points = {}

    # Get parameters and temperatures from the optimizer to store them in the probed points
    params = np.array([res['params'][v] for res in optimizer.res for v in res['params']]).reshape(-1,len(pbounds))
    obs = np.array([res['target'] for res in optimizer.res])
    probed_points = {tuple(row): obs[idx] for idx, row in enumerate(params)}

    # Remove the old log file
    os.remove(f'./{load}_old.json')

    # All 250 points are done by LHS
    # Make the LHS with correct boundaries
    sampler = qmc.LatinHypercube(d=len(pbounds),seed=i)
    samples = sampler.random(n=total_sims)     # The LHS space is made for 250 points
    l_bounds = [pbounds[p][0] for p in pbounds]
    u_bounds = [pbounds[p][1] for p in pbounds]
    samples = qmc.scale(samples, l_bounds, u_bounds)

    # Loop over the LHS
    for s in samples:
        # Round the parameters to the step sizes
        params = {p: round(s[idx]/steps[p])*steps[p] for (idx, p) in enumerate(pbounds)}

        # Simulate the rounded parameters
        target = objective_function(**params)

        # Register the rounded parameters with the found temperature
        optimizer.register(params=params, target=target)
        probed_points[tuple(params.values())] = target

    # Print the final found maximum tempature with the according parameters
    print(optimizer.max['target'], 'is the maximum found temperature with these parameters')
    print({p: round(v/steps[p])*steps[p] for (p, v) in optimizer.max['params'].items()})
