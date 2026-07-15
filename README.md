# 🤖 WareBot AI — Automated Warehouse Sorting Robot Simulator

> A Search & Optimization AI simulation of a warehouse robot that picks up multiple items and delivers them to a packing station — inspired by systems like Amazon Robotics.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![License](https://img.shields.io/badge/License-Educational-green.svg)

---

## 📖 About

Warehouses like Amazon Robotics use automated robots that pick items off shelves and bring them to a packing station. Every day these robots need to plan routes around obstacles and figure out the smartest order to collect multiple items instead of just going one by one randomly.

This project simulates that exact problem using classic **search and optimization algorithms** — no machine learning, no external APIs, just pure algorithmic decision-making.

The robot solves two problems on every run:

1. **What order** should it visit the items in?
2. **What path** should it take between each point, avoiding shelves?

---

## 🗺️ How the Warehouse Works

The warehouse is represented as a 2D grid, like graph paper. Each cell holds a value:

| Value | Meaning |
|:---:|---|
| `0` | Empty floor — robot can walk here |
| `1` | Shelf — robot **cannot** pass through |
| `2` | Dock — robot's starting point |
| `3` | Packing station — robot's final destination |
| `4` | Item pickup point — robot collects an item here |

---

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd WareBot_AI
pip install -r requirements.txt
```

## ▶️ Run

```bash
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`

---

## 🖥️ App Walkthrough

### Sidebar — Warehouse Setup

| Control | What it does |
|---|---|
| **Warehouse Rows** | Sets the grid's vertical size (more rows = taller warehouse) |
| **Warehouse Columns** | Sets the grid's horizontal size (more columns = wider warehouse) |
| **Number of Items to Pick** | How many items the robot must collect this run |
| **Random Seed** | Locks the layout — same seed always produces the same warehouse, useful for reproducible demos and testing |
| **Generate New Warehouse** | Builds a fresh warehouse using the current settings |

### Sidebar — Algorithm Settings

**Item Visit Order Strategy**
- `Nearest Neighbor` — greedy, always picks the closest remaining item. Fast, not always shortest overall.
- `Optimal (Brute Force)` — checks every possible order, guarantees the shortest total route. Practical only for ≤ 8 items.

**Pathfinding Algorithm**
- `BFS` — explores layer by layer, guarantees shortest path, explores many cells.
- `Dijkstra` — cost-based search, behaves like BFS here since all moves cost the same.
- `A*` — uses a Manhattan-distance heuristic to head toward the goal, exploring far fewer cells.

### Main Area

- **Problem Setup** — summary of dock location, station location, and item count
- **🚀 Run Robot Mission** — runs the simulation and shows:
  - Grid visualization (shelves, explored cells, final path, items, dock, station)
  - Plain-language explanation of the robot's decisions
  - Evaluation metrics: path length, nodes explored, runtime, items collected
  - Item visit order and a leg-by-leg distance breakdown
- **📊 Compare Approaches** — runs all 6 combinations (2 strategies × 3 algorithms) and displays them side by side

---

## 📁 Project Structure

```
WareBot_AI/
├── app.py                    # Streamlit UI
├── warehouse_utils.py         # Grid creation and setup
├── pathfinding.py              # BFS, Dijkstra, A*
├── route_planner.py            # Item order optimization + route planning
├── explain.py                    # Natural-language explanations
├── visuals.py                      # Matplotlib grid rendering
├── requirements.txt
├── data/
│   └── sample_warehouse.json
└── screenshots/
```

---

## 🧠 AI Methods Used

This project falls under **Search / Optimization AI**:

- **Pathfinding:** BFS (uninformed), Dijkstra (cost-based), A* (heuristic-informed)
- **Route optimization:** Nearest Neighbor (greedy heuristic) vs. Brute Force (guaranteed optimal for small N)

No training data, no ML models, no external APIs — which keeps the project lightweight and avoids issues like rate limits or API costs.

---

## 📊 Evaluation

The app compares algorithms and strategies on:

- Total path length
- Total nodes explored
- Runtime

**Sample result** (15×15 grid, 5 items, seed 42):

| Strategy | Algorithm | Distance | Nodes Explored |
|---|---|:---:|:---:|
| Nearest Neighbor | A* | 38 | **84** |
| Nearest Neighbor | Dijkstra | 38 | 256 |
| Nearest Neighbor | BFS | 38 | 246 |

Same path length across all three, but A* explores far fewer nodes — a direct demonstration of heuristic search efficiency.

---

## ⚠️ Limitations

- Single robot only — no multi-robot coordination or collision avoidance
- 4-directional movement only (no diagonals)
- Brute Force route planning only scales to ≤ 8 items

## 🔮 Future Improvements

- Multiple robots operating simultaneously with collision avoidance
- Weighted terrain (some paths cost more, e.g. busy aisles)
- Real-time dynamic obstacles (other robots blocking a path mid-mission)

---


