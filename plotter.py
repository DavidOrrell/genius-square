import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from copy import deepcopy

colours = []
# Black
colours.append(np.array([0, 0, 0, 1]))
# Navy
colours.append(np.array([0, 0, 0.5, 1]))
# Brown
colours.append(np.array([205.0/256.0, 133.0/256.0, 63.0/256.0]))
# Orange
colours.append(np.array([249.0/256.0, 105.0/256.0, 14.0/256.0, 1]))
# Purple
colours.append(np.array([0.5, 0, 0.5, 1]))
# Grey
colours.append(np.array([0.5, 0.5, 0.5, 1]))
# Yellow
colours.append(np.array([245.0/256.0, 229.0/256.0, 27.0/256.0, 1]))
# Green
colours.append(np.array([38.0/256.0, 166.0/256.0, 91.0/256.0, 1]))
# Blue
colours.append(np.array([34.0/256.0, 167.0/256.0, 240.0/256.0, 1]))
# Red
colours.append(np.array([217.0/256.0, 30.0/256.0, 24.0/256.0, 1]))


def plot_solution(solution):

    global colours

    # Convert the solution into a grid of numbers representing the colours
    grid_row = [0, 0, 0, 0, 0, 0]
    grid = [deepcopy(grid_row) for j in range(6)]
    for pnum, piece in enumerate(solution):
        (x, y) = piece[0]
        for (dx, dy) in piece[1]:
            grid[y + dy][x + dx] = pnum + 1
    grid_array = np.array(grid)

    # Generate and display the colourmap
    newcmp = ListedColormap(colours)
    fig, ax = plt.subplots(1, 1)
    psm = ax.pcolormesh(grid_array,
                        cmap=newcmp,
                        rasterized=True,
                        vmin=0,
                        vmax=10)
    plt.show()
