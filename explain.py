


def generate_explanation(order_strategy, path_algo, route_result, num_items):
    if not route_result["success"]:
        return ("The robot could not find a complete path. The shelves might be "
                "blocking the entire route - try reducing the number of shelves and run again.")

    total_dist = route_result["total_distance"]
    total_explored = sum(len(e) for e in route_result["all_explored"])

    explanation = (
        f"The robot picked up {num_items} items using the '{order_strategy}' strategy, "
        f"and used the {path_algo} algorithm to find the path between each pair of points. "
        f"The full mission (from the dock, through all items, to the packing station) "
        f"covered {total_dist} cells, and explored {total_explored} cells in total along the way. "
    )

    if order_strategy == "Nearest Neighbor":
        explanation += ("Nearest Neighbor always picks whichever item is closest at each step - "
                         "this is fast, but it doesn't always guarantee the shortest overall route, "
                         "since a 'greedy' choice now can lead to a longer detour later.")
    elif order_strategy == "Optimal (Brute Force)":
        explanation += ("Brute Force checked every possible order and found the one with the "
                         "guaranteed shortest total distance - but this only works well for a small "
                         "number of items, since the number of orders grows extremely fast.")

    if path_algo == "A*":
        explanation += (" A* used a heuristic (Manhattan distance) to estimate how far the goal is, "
                         "so it usually explores fewer cells than the other algorithms.")
    elif path_algo == "Dijkstra":
        explanation += (" Dijkstra guaranteed the lowest-cost path to every cell, without using "
                         "any heuristic guess.")
    elif path_algo == "BFS":
        explanation += (" BFS explored all nearby cells layer by layer, which also finds the "
                         "shortest path but explores more cells overall.")

    return explanation
