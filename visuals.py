"""
visuals.py
Matplotlib se warehouse grid draw karta hai: shelves, items, dock, station,
explored cells, aur robot ka final combined route.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np


def create_visuals(grid, dock, station, items, route_result):
    rows, cols = grid.shape
    display = np.zeros((rows, cols), dtype=int)

    # 0 = floor, 1 = shelf, 2 = explored, 3 = path, 4 = item, 5 = dock, 6 = station
    display[grid == 1] = 1

    if route_result.get("success"):
        for leg_explored in route_result["all_explored"]:
            for cell in leg_explored:
                if display[cell[0]][cell[1]] == 0:
                    display[cell[0]][cell[1]] = 2

        for cell in route_result["full_path"]:
            display[cell[0]][cell[1]] = 3

    for it in items:
        display[it[0]][it[1]] = 4

    display[dock[0]][dock[1]] = 5
    display[station[0]][station[1]] = 6

    colors = ["#f5f5f5", "#4a4a4a", "#cfe8ff", "#2e7d32", "#ffb300", "#1565c0", "#c62828"]
    cmap = ListedColormap(colors)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(display, cmap=cmap, vmin=0, vmax=6)

    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Warehouse: Robot Route & Explored Cells")

    legend_items = [
        mpatches.Patch(color="#4a4a4a", label="Shelf"),
        mpatches.Patch(color="#cfe8ff", label="Explored"),
        mpatches.Patch(color="#2e7d32", label="Robot Path"),
        mpatches.Patch(color="#ffb300", label="Item Pickup"),
        mpatches.Patch(color="#1565c0", label="Dock (Start)"),
        mpatches.Patch(color="#c62828", label="Packing Station (End)"),
    ]
    ax.legend(handles=legend_items, loc="upper center",
              bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=8)

    return fig