import os
import json
import matplotlib.pyplot as plt
import numpy as np

script_dir = os.path.dirname(__file__)

plt.figure(figsize=(12, 6))
file_names = ['ei xi=0','mei xi=1E-4','mei xi=1E-2','mei xi=0.1','dmei','lhs random']  # List to store file names
colors = ['blue', 'tab:cyan', 'tab:orange', 'tab:red', 'tab:pink', 'tab:grey']

for k, file_name in enumerate(file_names):
    maxs = []
    for i in range(1,6):
        file_path = os.path.join(script_dir, 'average '+file_name+'.json')

        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]

    temps = data[0]
    maximum = 0
    for j in range(250):
        maximum = max(maximum,temps[j])
        maxs.append(maximum)

    plt.plot(maxs,color=colors[k])

plt.axvline(x=10, linestyle='--', color='gray')
plt.xticks(np.arange(0, 251, 10))
plt.xlabel('Iterations')
plt.ylim(0, 270)
plt.ylabel(r'$\Delta T_0^\text{ext}$ [K]')

plt.legend(file_names, loc='upper right')

plt.title('EI v MEI v MEI v MEI v DMEI v LHS averages')
#plt.title('extremely fine meshing',fontsize=12)
plt.savefig('EI v MEI v MEI v MEI v DMEI v LHS averages.png',dpi=300)

plt.show()
