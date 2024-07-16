import os
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

s=1

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

# Create a figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize the scatter plot object
scatter = None

# Create a colorbar with the full range of target values
norm = plt.Normalize(vmin=0, vmax=270)
cmap = plt.cm.coolwarm
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, pad=0.15, label=r'$\Delta T_0^\text{ext}$ [K]')

# Function to update the scatter plot for each frame
def update(frame):
    global scatter
    ax.clear()  # Clear the previous plot

    # Make the plot rotate in the xy-axis
    ax.view_init(elev=30, azim=frame * 0.5)

    # Plot the scatter plot with the current frame's data
    scatter = ax.scatter(p[:frame+10], r[:frame+10], h[:frame+10], c=targets[:frame+10], cmap='coolwarm', vmin=0, vmax=270, s=s)

    # Set labels and title
    ax.set_xlabel('p [nm]')
    ax.set_ylabel('h [nm]')
    ax.set_zlabel('r [nm]')
    ax.set_title('3D Scatter Plot with Target Values')

    # Set the axis limits to the maximum and minimum values
    ax.set_xlim(100, 1000)
    ax.set_ylim(15, 60)
    ax.set_zlim(15, 150)

    # Only for .png files
    # Add the colorbar to the figure
    plt.savefig("3d animation winner (spinning)-"+str(i)+".png")  

    return scatter,

"""
The code below is to produce a .gif file

# Create the animation
ani = FuncAnimation(fig, update, frames=len(targets)-10, interval=500, blit=True)  # blit for speed-up

# Add the colorbar to the figure
cbar = fig.colorbar(sm, ax=ax, pad=0.15, label=r'$\Delta T_0^\text{ext}$ [K]')

# Save the animation as a GIF
ani.save('3d animation winner (spinning).gif', writer='pillow', fps=60, dpi=300)
"""


#The code below is to create is sequence of .png files

# Save each frame as a PNG file
for i in range(len(targets)-10+1):
    update(i)

