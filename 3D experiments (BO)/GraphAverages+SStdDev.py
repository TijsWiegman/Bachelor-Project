import os
import json
import matplotlib.pyplot as plt
import numpy as np

X = np.linspace(1, 250, 250)
script_dir = os.path.dirname(__file__)

# Set up the figure and subplots
fig = plt.figure(figsize=(12, 18))
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])

# List to store file names and colors
file_names = ['ei xi=0','mei xi=1E-4','mei xi=1E-2','mei xi=0.1','dmei','LHS random']
colors = ['blue', 'tab:cyan', 'tab:orange', 'tab:red', 'tab:pink', 'tab:grey']

# Smaller plots for means and standard deviations
for i, (file_name, color) in enumerate(zip(file_names, colors)):
    row = i // 2 + 1
    col = i % 2

    ax = fig.add_subplot(gs[row - 1, col])
    ax.set_title(file_name)
    ax.set_xlabel('Iterations')
    ax.set_ylabel(r'$\Delta T_0^\text{ext}$ [K]')
    ax.axvline(x=10, linestyle='--', color='gray')
    ax.set_ylim(0, 270)  # Set the y-axis limits

    # Load average data
    file_path = os.path.join(script_dir, 'average ' + file_name + '.json')
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]
    temps = data[0]
    maximum = 0
    maxs = []
    for k in range(250):
        maximum = max(maximum, temps[k])
        maxs.append(maximum)

    maxs = np.array(maxs)

    # Plot all average plots
    for j, fname in enumerate(file_names):
        other_maxs = []

        file_path = os.path.join(script_dir, 'average ' + fname + '.json')
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
        temps = data[0]
        maximum = 0
        for k in range(250):
            maximum = max(maximum, temps[k])
            other_maxs.append(maximum)

        other_maxs = np.array(other_maxs)
        ax.plot(X, other_maxs, label=fname if j == i else None, color=colors[j])

    # Load standard deviation data
    file_path2 = os.path.join(script_dir, 'sample std dev ' + file_name + '.json')
    with open(file_path2, 'r') as file:
        line = file.readline()
        std = json.loads(line)

    std = np.array(std)
    ax.fill_between(X, maxs + std, maxs - std, alpha=0.2, color=color, label='Std. Dev.')
    ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig('EI v MEI v MEI v MEI v DMEI v LHS averages+std.png', dpi=300)
plt.show()
