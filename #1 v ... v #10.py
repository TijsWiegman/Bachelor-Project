import os
import json
import matplotlib.pyplot as plt
import numpy as np

X = np.linspace(1,250,250)

script_dir = os.path.dirname(__file__)

file_names = ['ei xi=0', 'mei xi=1E-4', 'mei xi=1E-2', 'mei xi=0.1', 'dmei', 'lhs random']

for file_name in file_names:
    plt.figure(figsize=(12, 6))
    legend = ['#1','#2','#3','#4','#5','#6','#7','#8','#9','#10']

    for i in range(1,11):
        maxs = []
        targets = []
        file_path = os.path.join(script_dir,file_name+' #'+str(i)+'.json')

        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
            for j in range(len(data)):
                targets.append(data[j]['target'])

        maximum = 0
        for j in range(250):
            maximum = max(maximum,targets[j])
            maxs.append(maximum)

        plt.plot(maxs)

    plt.axvline(x=10, linestyle='--', color='gray')
    plt.xticks(np.arange(0, 251, 10))
    plt.xlabel('Iterations')
    plt.ylabel(r'$\Delta T_0^\text{ext}$ [K]')
    plt.legend(legend, loc='lower right')
    plt.title(file_name+' #1 v ... v #10')
    plt.ylim(0,270)
    plt.savefig(file_name+' #1 v ... v #10.png',dpi=300)

    plt.show()
