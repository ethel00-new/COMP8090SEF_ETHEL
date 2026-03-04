# 📦 Warehouse Picking Route Planner

**Warehouse Picking Route Planner** that demonstrates how to compute the shortest path between two buildings using **Dijkstra’s Algorithm** on a **graph data structure**. It also visualizes the graph layout on a canvas with predefined coordinates.

---

## 🚀 Features
- Interactive web interface built with **Flask**.
- Graph represented as an **adjacency list**.
- Hard-coded coordinates for visualization because the buildings are fixed.
- **Dijkstra’s Algorithm** implementation for shortest path calculation.
- REST API endpoint (`/shortest-path`) returning JSON results.

---

# Graph Data Structure & Dijkstra’s Algorithm

## 📌 Graph Data Structure

In this project, the **graph** is represented using an **adjacency list**.  
Each node (building) is a key in a dictionary, and its value is a list of tuples representing **neighbors** and the **distance (weight)** to them.

### Example Representation

```python
GRAPH = {
    "A": [("B", 3), ("D", 2)],
    "B": [("A", 3), ("C", 4), ("E", 2)],
    "C": [("B", 4), ("F", 6)],
    ...
}
```

- **Nodes**: Buildings labeled `A, B, C, ... J`
- **Edges**: Weighted connections between nodes (e.g., `A → B` has weight `3`)
- **Weights**: Distances between buildings

### Graph Visualization

|Node|Neighbors (with distance)|
|---|---|
|A|B (3), D (2)|
|B|A (3), C (4), E (2)|
|C|B (4), F (6)|
|D|A (2), E (4), G (4)|
|E|B (2), D (4), F (3), H (7)|
|F|C (6), E (3), I (5), J (5)|
|G|D (4), H (3)|
|H|E (7), G (3), I (2)|
|I|F (5), H (2)|
|J|F (5)|

This structure is efficient because:

- It stores only existing edges (no wasted space).
- It allows quick traversal of neighbors.

---

## 📌 Dijkstra’s Algorithm

Dijkstra’s Algorithm is used to find the **shortest path** between two nodes in a weighted graph (with non-negative weights).

### Steps of the Algorithm

1. **Initialization**:
    
    - Set all distances to infinity (`∞`), except the start node (distance = 0).
    - Use a **priority queue (min-heap)** to always expand the node with the smallest known distance.
2. **Relaxation**:
    
    - For each neighbor of the current node, calculate the new distance.
    - If the new distance is smaller than the previously recorded distance, update it and push the neighbor into the priority queue.
3. **Termination**:
    
    - Continue until the destination node is reached or all nodes are processed.

### Example Walkthrough

Suppose we want the shortest path from **A → F**:

1. Start at **A** (distance = 0).
2. Neighbors:
    - B = 3
    - D = 2
3. Next smallest: **D (2)**.
    - From D → E = 6, G = 6
4. Next smallest: **B (3)**.
    - From B → C = 7, E = 5
5. Next smallest: **E (5)**.
    - From E → F = 8, H = 12
6. Next smallest: **F (8)** → Destination reached.

**Shortest Path**: `A → B → E → F`  
**Distance**: `8`

---

## 📌 Time Complexity

- **Using Min-Heap (Priority Queue)**:
    - Each edge is relaxed once → (O(E \log V))
    - Each node is extracted from the heap → (O(V \log V))

Overall complexity:

[ O((V + E) \cdot \log V) ]

Where:

- (V) = number of vertices (nodes)
- (E) = number of edges

### Space Complexity

- Distance dictionary: (O(V))
- Previous node dictionary: (O(V))
- Priority queue: up to (O(V))

---

## 📌 Graph Illustration

Here’s a simple sketch of the graph structure:

```
   A --3-- B --4-- C
   |       |       |
   2       2       6
   |       |       |
   D --4-- E --3-- F --5-- J
   |       |       |
   4       7       5
   |       |       |
   G --3-- H --2-- I
```

---

## 🖥️ How to Run
```bash
cd Task2
pip install -r requirements.txt
python main.py
```

Access the app at:  
👉 http://127.0.0.1:5000
