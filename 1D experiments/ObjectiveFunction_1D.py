import mph
import json
import numpy as np

client = mph.start()
model = client.load('Toy problem v2')

def objective_function_1D_p(p):
    h = 30
    r = 100
    '''Function with unknown internals we wish to maximize.'''
    # Set the condition for which to simulate
    if p >= 2*r:
        # Change the global parameters of the model
        model.parameter('H', f'{h}[nm]')
        model.parameter('P', f'{p}[nm]')
        model.parameter('R', f'{r}[nm]')

        # Resolve the study (also updates model)
        model.solve()

        # Select the volume average temperature evaluation
        #target = model/'evaluations'/'Volume Average 1'
        target = model/'evaluations'/'Reflectance (ewfd)'

        # Return the recalculated temperature
        return list(target.java.computeResult()[0])[0][1]
    
    else:
        # If condition is not satisfied, return the initial temperature
        return 0 # was 293.15

X = np.linspace(100,1000,901)
data = {}

for x in X:
    y = objective_function_1D_p(x)
    data[str(x)] = y    

with open("1d_slice_p.json", "w") as json_file:
    json.dump(data, json_file)
