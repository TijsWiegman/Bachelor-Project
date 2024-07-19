# Import the required libraries
import mph
import os
import numpy as np
from bayes_opt import BayesianOptimization
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
from bayes_opt import UtilityFunction
from scipy.stats import qmc

np.random.seed(seed=0)

# Set the COMSOL model you want to load as a string
comsol = 'Toy problem v2'  # was None

kinds = ['poi','ucb']

for i in range(2):
    for j in range(1,11):

        # Set the filename of the logs file as a string
        logfile = kinds[i]+' #'+str(j)

        # Create empty .json file named logs
        load = 'logs'
        file_path = f'./{load}.json'

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as file:
            pass

        # Set the number of simulations per dimension for the initial population
        sims_dims = 10

        # Set the number of total simulations
        total_sims = 250

        # Set the boundaries and steps for the optimization in alphabetical order
        pbounds = {'h': (15, 60), 'p': (100, 1000), 'r': (15, 150)}
        steps = {'h': 1, 'p': 1, 'r': 1}

        # Initializing the BayesianOptimization object
        optimizer = BayesianOptimization(f=None, pbounds=pbounds,allow_duplicate_points=True)

        # Make the utility function to optimize with, the kind can be: 'ucb', 'ei', 'poi'
        if kinds[i] == 'poi':
            utility = UtilityFunction(kind='poi', xi=1e-2)
        elif kinds[i] == 'ucb':
            utility = UtilityFunction(kind='ucb', xi=1)

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

        # Make a logger to save the simulated points
        # Caveat: The logger will not look back at previously probed points.
        logger = JSONLogger(path=f'./{logfile}.json')
        optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)
        probed_points = {}

        # Load in old logs
        if load != None:
            load_logs(optimizer, logs=[f'./{load}_old.json'])

        # Get parameters and temperatures from the optimizer to store them in the probed points
        params = np.array([res['params'][v] for res in optimizer.res for v in res['params']]).reshape(-1,len(pbounds))
        obs = np.array([res['target'] for res in optimizer.res])
        probed_points = {tuple(row): obs[idx] for idx, row in enumerate(params)}

        # Remove the old log file
        os.remove(f'./{load}_old.json')

        # Make the LHS with correct boundaries
        sampler = qmc.LatinHypercube(d=len(pbounds),seed=0)
        samples = sampler.random(n=sims_dims)
        l_bounds = [pbounds[p][0] for p in pbounds]
        u_bounds = [pbounds[p][1] for p in pbounds]
        samples = qmc.scale(samples, l_bounds, u_bounds)

        print('check')

        # Loop over the LHS
        for s in samples:
            # Round the parameters to the step sizes
            params = {p: round(s[idx]/steps[p])*steps[p] for (idx, p) in enumerate(pbounds)}
            print(params)

            # Simulate the rounded parameters
            target = objective_function(**params)

            # Register the rounded parameters with the found temperature
            optimizer.register(params=params, target=target)
            probed_points[tuple(params.values())] = target

        # Run the optimizaton for the number of total simulations
        for _ in range(total_sims - samples.shape[0]):
            # Suggest the next point to probe
            next_point = optimizer.suggest(utility)  # dictionary, {'h': 50.663, 'p': 474.790, 'r': 127.672}

            # Round the given parameters to step sizes
            round_next_point = {p: round(v/steps[p])*steps[p] for (p, v) in next_point.items()}
            round_params = tuple(round_next_point.values())

            print(round_params)

            # See if the rounded parameters are already simulated
            if round_params in probed_points:
                # If so, register the point with the known value
                optimizer.register(params=round_params, target=probed_points[round_params])

            else:
                # If not, simulate the parameters
                target = objective_function(**round_next_point)

                # Register the unrounded parameters with the found temperature
                optimizer.register(params=round_params, target=target)

                # Add the rounded parameters with the found temperature
                probed_points[round_params] = target

        # Print the final found maximum tempature with the according parameters
        print(optimizer.max['target'], 'is the maximum found temperature with these parameters')
        print({p: round(v/steps[p])*steps[p] for (p, v) in optimizer.max['params'].items()})
