import mph
#from CreateModel import make_comsol

client = mph.start()
model = client.load('Toy problem v2')

def objective_function(h, p, r):
    '''Function with unknown internals we wish to maximize.'''
    # Set the condition for which to simulate
    if p >= 2*r + 50:
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
