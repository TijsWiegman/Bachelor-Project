import os
import json
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

s = 1

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "mei xi=1E-4 #7.json")

targets = []
locations = []

with open(file_path, 'r') as logs_file:
    for line in logs_file:
        data = json.loads(line)
        targets.append(data['target'])
        locations.append(data['params'])

for i in range(len(locations)):
    h = locations[i]['h']
    p = locations[i]['p']
    r = locations[i]['r']
    locations[i] = tuple([p, r, h])

# Separate the p, h, and r coordinates from the locations list
p, h, r = zip(*locations)

# Create a figure and 2x2 grid of subplots
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(221, projection='3d')  # Top-left subplot (3D)
ax2 = fig.add_subplot(222)  # Top-right subplot (2D)
ax3 = fig.add_subplot(223)  # Bottom-left subplot (2D)
ax4 = fig.add_subplot(224)  # Bottom-right subplot (2D)

# Plot the 3D scatter plot with colors representing target values
scatter = ax1.scatter(p, r, h, c=targets, cmap='coolwarm',s=s, depthshade=False)
ax1.set_xlabel('p [nm]')
ax1.set_ylabel('h [nm]')
ax1.set_zlabel('r [nm]')
ax1.set_title('3D Plot')

# Create a ScalarMappable object for the 2D scatter plots
sm = ScalarMappable(cmap='coolwarm')
sm.set_array(targets)

# Plot the 2D scatter plots
ax2.scatter(p, r, c=targets, cmap='coolwarm',s=s)
ax2.set_xlabel('p [nm]')
ax2.set_ylabel('h [nm]')
ax2.set_title('p vs h')

ax3.scatter(p, h, c=targets, cmap='coolwarm',s=s)
ax3.set_xlabel('p [nm]')
ax3.set_ylabel('r [nm]')
ax3.set_title('p vs r')

ax4.scatter(r, h, c=targets, cmap='coolwarm',s=s)
ax4.set_xlabel('h [nm]')
ax4.set_ylabel('r [nm]')
ax4.set_title('h vs r')

# Adjust spacing between subplots
plt.subplots_adjust(wspace=0.4, hspace=0.4)

# Create a big color bar for the entire figure
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
fig.colorbar(sm, cax=cbar_ax, label=r'$\Delta T_0^\text{ext}$ [K]')

# Save the plot
plt.savefig('3d plot winner.png', dpi=300)

# Show the plot
plt.show()

