"""
pathfinding.py
Robot ke liye 2 points ke darmiyan raasta dhundne wale algorithms.
Teeno algorithms same output format return karte hain taake compare karna
aasan ho: {"path": [...], "explored": [...], "runtime": float}
"""

import heapq
import time
from warehouse_utils import get_neighbors


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def bfs(grid, start, end):
    start_time = time.time()
    queue = [start]
    visited = {start}
    came_from = {}
    explored = []

    while queue:
        current = queue.pop(0)
        explored.append(current)
        if current == end:
            path = reconstruct_path(came_from, current)
            return {"path": path, "explored": explored,
                    "runtime": time.time() - start_time}
        for nxt in get_neighbors(current, grid):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = current
                queue.append(nxt)

    return {"path": [], "explored": explored, "runtime": time.time() - start_time}


def dijkstra(grid, start, end):
    start_time = time.time()
    pq = [(0, start)]
    dist = {start: 0}
    came_from = {}
    explored = []
    visited = set()

    while pq:
        cost, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        explored.append(current)

        if current == end:
            path = reconstruct_path(came_from, current)
            return {"path": path, "explored": explored,
                    "runtime": time.time() - start_time}

        for nxt in get_neighbors(current, grid):
            new_cost = cost + 1
            if nxt not in dist or new_cost < dist[nxt]:
                dist[nxt] = new_cost
                came_from[nxt] = current
                heapq.heappush(pq, (new_cost, nxt))

    return {"path": [], "explored": explored, "runtime": time.time() - start_time}


def heuristic(a, b):
    """Manhattan distance heuristic A* ke liye"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, end):
    start_time = time.time()
    pq = [(0, start)]
    g_score = {start: 0}
    came_from = {}
    explored = []
    visited = set()

    while pq:
        _, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        explored.append(current)

        if current == end:
            path = reconstruct_path(came_from, current)
            return {"path": path, "explored": explored,
                    "runtime": time.time() - start_time}

        for nxt in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1
            if nxt not in g_score or tentative_g < g_score[nxt]:
                g_score[nxt] = tentative_g
                f_score = tentative_g + heuristic(nxt, end)
                came_from[nxt] = current
                heapq.heappush(pq, (f_score, nxt))

    return {"path": [], "explored": explored, "runtime": time.time() - start_time}


def run_model_or_algorithm(algo_name, grid, start, end):
    """Naam ke hisaab se sahi pathfinding algorithm chalata hai"""
    if algo_name == "BFS":
        return bfs(grid, start, end)
    elif algo_name == "Dijkstra":
        return dijkstra(grid, start, end)
    elif algo_name == "A*":
        return astar(grid, start, end)
    else:
        raise ValueError(f"Unknown algorithm: {algo_name}")