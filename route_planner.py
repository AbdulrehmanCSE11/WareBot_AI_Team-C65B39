

import time
from itertools import permutations
from pathfinding import run_model_or_algorithm, heuristic


def nearest_neighbor_order(start, items):
    """
    Greedy approach: har baar sabse qareeb (Manhattan distance) item choose karo.
    Fast hai lekin hamesha optimal (sabse chota total route) guarantee nahi karta.
    """
    remaining = items.copy()
    order = []
    current = start

    while remaining:
        nearest = min(remaining, key=lambda item: heuristic(current, item))
        order.append(nearest)
        remaining.remove(nearest)
        current = nearest

    return order


def brute_force_order(start, items):
    """
    Saare possible orders check karke sabse chota total (Manhattan) distance
    wala order dhundta hai. Guaranteed optimal hai lekin sirf chote item count
    (<= 7-8) ke liye practical hai kyunke permutations exponentially barhti hain.
    """
    best_order = None
    best_distance = float("inf")

    for perm in permutations(items):
        total = 0
        current = start
        for item in perm:
            total += heuristic(current, item)
            current = item
        if total < best_distance:
            best_distance = total
            best_order = list(perm)

    return best_order


def get_order(strategy, start, items):
    """strategy ke hisaab se item-visit order decide karta hai"""
    if not items:
        return []
    if strategy == "Nearest Neighbor":
        return nearest_neighbor_order(start, items)
    elif strategy == "Optimal (Brute Force)":
        if len(items) > 8:
            raise ValueError("Brute Force sirf 8 ya kam items ke liye chalta hai (bohot slow ho jata hai zyada items ke liye).")
        return brute_force_order(start, items)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def plan_full_route(grid, dock, station, items, order_strategy, path_algo):
    """
    Poora robot mission plan karta hai:
    dock -> item1 -> item2 -> ... -> itemN -> station
    """
    start_time = time.time()
    order = get_order(order_strategy, dock, items)

    stops = [dock] + order + [station]
    full_path = []
    all_explored = []
    legs_info = []

    for i in range(len(stops) - 1):
        leg_start = stops[i]
        leg_end = stops[i + 1]
        result = run_model_or_algorithm(path_algo, grid, leg_start, leg_end)

        if not result["path"]:
            return {
                "full_path": [], "all_explored": all_explored, "order": order,
                "total_distance": 0, "total_runtime": time.time() - start_time,
                "legs_info": legs_info, "success": False
            }

        if i == 0:
            full_path.extend(result["path"])
        else:
            full_path.extend(result["path"][1:])

        all_explored.append(result["explored"])
        legs_info.append({
            "from": leg_start, "to": leg_end,
            "length": len(result["path"]) - 1,
            "nodes_explored": len(result["explored"])
        })

    total_distance = len(full_path) - 1
    total_runtime = time.time() - start_time

    return {
        "full_path": full_path, "all_explored": all_explored, "order": order,
        "total_distance": total_distance, "total_runtime": total_runtime,
        "legs_info": legs_info, "success": True
    }
