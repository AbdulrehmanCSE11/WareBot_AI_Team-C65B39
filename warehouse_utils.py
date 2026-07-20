

import numpy as np
import random


def load_data(rows=15, cols=15):
    """Naya khali warehouse grid banata hai"""
    grid = np.zeros((rows, cols), dtype=int)
    return grid


def preprocess_data(grid, dock, station, shelves, items):
    """
    User/auto-generated input se warehouse grid ko update karta hai.
    """
    grid = grid.copy()

    for s in shelves:
        grid[s[0]][s[1]] = 1

    for it in items:
        if grid[it[0]][it[1]] == 0:
            grid[it[0]][it[1]] = 4

    grid[dock[0]][dock[1]] = 2
    grid[station[0]][station[1]] = 3

    return grid


def get_neighbors(pos, grid):
    """Kisi cell ke valid (walkable, non-shelf) neighbors return karta hai"""
    rows, cols = grid.shape
    r, c = pos
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors


def generate_random_warehouse(rows=15, cols=15, num_shelves=18, num_items=5, seed=None):
    """
    Random warehouse layout generate karta hai testing/demo ke liye.
    """
    if seed is not None:
        random.seed(seed)

    grid = load_data(rows, cols)
    shelves = []

    for r in range(2, rows - 2, 3):
        for c in range(1, cols - 1):
            if random.random() < 0.7:
                shelves.append((r, c))

    dock = (0, 0)
    station = (rows - 1, cols - 1)

    shelves = [s for s in shelves if s != dock and s != station]

    free_cells = [(r, c) for r in range(rows) for c in range(cols)
                  if (r, c) not in shelves and (r, c) != dock and (r, c) != station]
    items = random.sample(free_cells, min(num_items, len(free_cells)))

    grid = preprocess_data(grid, dock, station, shelves, items)
    return grid, dock, station, shelves, items
