"""
app.py
WareBot AI - Automated Warehouse Sorting Robot Simulator
Main Streamlit UI
"""

import streamlit as st
import pandas as pd

from warehouse_utils import load_data, preprocess_data, generate_random_warehouse
from route_planner import plan_full_route
from explain import generate_explanation
from visuals import create_visuals

st.set_page_config(page_title="WareBot AI", layout="wide")
st.title("🤖 WareBot AI — Automated Warehouse Sorting Robot")
st.caption("Search & Optimization AI: a robot picks up multiple items across a warehouse floor and delivers them to a packing station")

# ---------------- Sidebar: Warehouse Setup ----------------
st.sidebar.header("1. Warehouse Setup")
rows = st.sidebar.slider("Warehouse Rows", 8, 25, 15)
cols = st.sidebar.slider("Warehouse Columns", 8, 25, 15)
num_items = st.sidebar.slider("Number of Items to Pick", 1, 8, 5)
seed = st.sidebar.number_input("Random Seed (for consistent layout)", 0, 9999, 42)

if st.sidebar.button("Generate New Warehouse") or "grid" not in st.session_state:
    grid, dock, station, shelves, items = generate_random_warehouse(
        rows=rows, cols=cols, num_items=num_items, seed=seed
    )
    st.session_state["grid"] = grid
    st.session_state["dock"] = dock
    st.session_state["station"] = station
    st.session_state["shelves"] = shelves
    st.session_state["items_list"] = items

st.sidebar.header("2. Algorithm Settings")
order_strategy = st.sidebar.selectbox(
    "Item Visit Order Strategy",
    ["Nearest Neighbor", "Optimal (Brute Force)"]
)
path_algo = st.sidebar.selectbox("Pathfinding Algorithm", ["A*", "Dijkstra", "BFS"])

# ---------------- Main: Problem Setup Display ----------------
st.subheader("Problem Setup")
col1, col2, col3 = st.columns(3)
col1.metric("Dock (Start)", str(st.session_state["dock"]))
col2.metric("Packing Station (End)", str(st.session_state["station"]))
col3.metric("Items to Collect", len(st.session_state["items_list"]))

if order_strategy == "Optimal (Brute Force)" and len(st.session_state["items_list"]) > 8:
    st.warning("Brute Force only works for 8 or fewer items. Reduce the item count or use Nearest Neighbor instead.")

run_disabled = order_strategy == "Optimal (Brute Force)" and len(st.session_state["items_list"]) > 8

# ---------------- Run Button ----------------
if st.button("🚀 Run Robot Mission", disabled=run_disabled):
    result = plan_full_route(
        st.session_state["grid"], st.session_state["dock"], st.session_state["station"],
        st.session_state["items_list"], order_strategy, path_algo
    )

    if not result["success"]:
        st.error("The robot could not find a complete path! Try reducing the number of shelves and run again.")
    else:
        st.success(f"Mission complete! Total distance: {result['total_distance']} cells")

        fig = create_visuals(st.session_state["grid"], st.session_state["dock"],
                              st.session_state["station"], st.session_state["items_list"], result)
        st.pyplot(fig)

        st.subheader("Explanation")
        explanation = generate_explanation(order_strategy, path_algo, result, len(st.session_state["items_list"]))
        st.write(explanation)

        st.subheader("Evaluation Metrics")
        total_explored = sum(len(e) for e in result["all_explored"])
        metrics = pd.DataFrame({
            "Metric": ["Total Path Length", "Total Nodes Explored", "Total Runtime (sec)", "Items Collected"],
            "Value": [result["total_distance"], total_explored,
                      round(result["total_runtime"], 5), len(st.session_state["items_list"])]
        })
        st.table(metrics)

        st.subheader("Item Visit Order")
        st.write(" → ".join([str(st.session_state["dock"])] +
                             [str(o) for o in result["order"]] +
                             [str(st.session_state["station"])]))

        st.subheader("Leg-by-Leg Breakdown")
        legs_df = pd.DataFrame(result["legs_info"])
        st.table(legs_df)

        st.session_state["last_result"] = result

st.markdown("---")

# ---------------- Comparison Section (Evaluation Module) ----------------
st.subheader("📊 Compare Approaches")
st.write("Lab requirement: compare at least 2 approaches. Here we compare both the item order strategy and the pathfinding algorithm.")

if st.button("Compare All Combinations"):
    comparison_rows = []
    strategies = ["Nearest Neighbor"]
    if len(st.session_state["items_list"]) <= 8:
        strategies.append("Optimal (Brute Force)")

    for strat in strategies:
        for algo in ["A*", "Dijkstra", "BFS"]:
            result = plan_full_route(
                st.session_state["grid"], st.session_state["dock"], st.session_state["station"],
                st.session_state["items_list"], strat, algo
            )
            total_explored = sum(len(e) for e in result["all_explored"]) if result["success"] else 0
            comparison_rows.append({
                "Order Strategy": strat,
                "Path Algorithm": algo,
                "Total Distance": result["total_distance"] if result["success"] else "No path",
                "Nodes Explored": total_explored,
                "Runtime (sec)": round(result["total_runtime"], 5)
            })

    st.table(pd.DataFrame(comparison_rows))


