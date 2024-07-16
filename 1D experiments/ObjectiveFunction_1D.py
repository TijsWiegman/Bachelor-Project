import mph
import json
import numpy as np
#from CreateModel import make_comsol

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
    print(x)
    y = objective_function_1D_p(x)
    print(y)
    data[str(x)] = y    

with open("1d_slice_p.json", "w") as json_file:
    json.dump(data, json_file)

#{"100.0": 0, "101.0": 0, "102.0": 0, "103.0": 0, "104.0": 0, "105.0": 0, "106.0": 0, "107.0": 0, "108.0": 0, "109.0": 0, "110.0": 0, "111.0": 0, "112.0": 0, "113.0": 0, "114.0": 0, "115.0": 0, "116.0": 0, "117.0": 0, "118.0": 0, "119.0": 0, "120.0": 0, "121.0": 0, "122.0": 0, "123.0": 0, "124.0": 0, "125.0": 0, "126.0": 0, "127.0": 0, "128.0": 0, "129.0": 0, "130.0": 0, "131.0": 0, "132.0": 0, "133.0": 0, "134.0": 0, "135.0": 0, "136.0": 0, "137.0": 0, "138.0": 0, "139.0": 0, "140.0": 0, "141.0": 0, "142.0": 0, "143.0": 0, "144.0": 0, "145.0": 0, "146.0": 0, "147.0": 0, "148.0": 0, "149.0": 0, "150.0": 0, "151.0": 0, "152.0": 0, "153.0": 0, "154.0": 0, "155.0": 0, "156.0": 0, "157.0": 0, "158.0": 0, "159.0": 0, "160.0": 0, "161.0": 0, "162.0": 0, "163.0": 0, "164.0": 0, "165.0": 0, "166.0": 0, "167.0": 0, "168.0": 0, "169.0": 0, "170.0": 0, "171.0": 0, "172.0": 0, "173.0": 0, "174.0": 0, "175.0": 0, "176.0": 0, "177.0": 0, "178.0": 0, "179.0": 0, "180.0": 0, "181.0": 0, "182.0": 0, "183.0": 0, "184.0": 0, "185.0": 0, "186.0": 0, "187.0": 0, "188.0": 0, "189.0": 0, "190.0": 0, "191.0": 0, "192.0": 0, "193.0": 0, "194.0": 0, "195.0": 0, "196.0": 0, "197.0": 0, "198.0": 0, "199.0": 0}
