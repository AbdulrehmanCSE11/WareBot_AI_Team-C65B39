WareBot AI - Project Report



Problem



Warehouses like Amazon Robotics use automated robots to pick items off shelves and bring them to a packing station. Every day these robots need to plan routes around obstacles and figure out the smartest order to collect multiple items instead of just going one by one randomly. This project is a simulation of that exact problem, built as a search and optimization AI task.



Method



The project has two main decisions the "robot" makes. First, it decides what order to visit the items in - I implemented two approaches for this. Nearest Neighbor just keeps picking whatever item is closest at each step, which is fast but not always the shortest overall route. Brute Force checks literally every possible order and picks the one with the smallest total distance, which is guaranteed optimal but only works for a small number of items (I capped it at 8) because the number of combinations grows really fast.



Second, once the order is decided, the robot needs an actual path between each pair of points on the grid, avoiding shelves. For this I implemented three classic search algorithms - BFS, Dijkstra, and A\*. BFS explores everything layer by layer. Dijkstra is basically the same here since all moves cost the same, but it uses a priority queue. A\* is the smartest one because it uses a heuristic (Manhattan distance to the goal) so it explores fewer cells while still finding the shortest path.



AI used



This is Search/Optimization AI - no machine learning model or external API was used, it's all algorithmic decision making. This actually made the project simpler to build and there were no rate limit or API cost issues to deal with.



Results



I tested this on a 15x15 warehouse with 5 items (seed 42). Both Nearest Neighbor and Brute Force ended up picking the same order for this particular layout, giving a total distance of 38 cells. Where the algorithms really differed was in nodes explored - A\* only explored 84 cells to find the path, while Dijkstra explored 256 and BFS explored 246. This clearly shows that A\*'s heuristic makes it more efficient even though all three algorithms find paths of the same length.



Limitations



The simulation only handles one robot at a time, so there's no collision avoidance or multi-robot coordination. Movement is restricted to up/down/left/right, no diagonal movement. Brute Force route planning only works for 8 or fewer items before it becomes too slow to run in reasonable time.



Future improvements



Given more time I would want to add multiple robots working in the same warehouse at once, which would need some kind of collision avoidance between them. Another idea is weighted terrain, where some paths take longer than others (like a busy aisle), which would make Dijkstra more useful than it currently is. Real-time obstacle changes, like another robot temporarily blocking a path, would also make the simulation more realistic.

