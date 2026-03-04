# Task 2 Warehouse Picking

## System Overview
Warehouse Picking Route Planner helps find the **shortest path** between two zone using **Dijkstra's algorithm**.
- Models a warehouse as an **undirected weighted graph**
- Lets user select **From** and **To** zone (A–J)
- Computes the shortest path and total distance using Dijkstra's algorithm
- Visualizes the graph and highlights the found path on a canvas

## Data Structure : Graph
The warehouse is modeled as an **undirected graph** using a Python dictionary (adjacency list):

**[image explain later]** : undirected graph vs directed graph , Vertices , Edges

### Abstract Data Type (ADT)
- Vertices (V): set of nodes {"A", "B", ..., "J"}
- Edges (E): weighted connections between vertices
- Main operations used:
    Get neighbors of a node → GRAPH[node]
    Get weight of edge (u,v) → loop through neighbors

```python
GRAPH = {
    "A": [("B", 2), ("D", 7)],
    "B": [("A", 2), ("C", 4), ("E", 2)],
    ...
    "J": [("F", 5)],
}
```

### possible applications
- Google Map find the shortest path
- Networking
- Gaming - shortest steps to win the game

## Algorithm : Dijkstra's Algorithm
Dijkstra finds the shortest path from a start node to all other nodes.

**[image explain later]** : Table in each step A>B 2, A>C ∞

1. Initialize:
    - Distance to start = 0
    - Distance to everyone else = ∞
    - Previous node dictionary (for path reconstruction) = None
    - Priority queue (min-heap) with (distance, node) → start with (0, start)

2. While priority queue is not empty:
    - Pop node with smallest current distance
    - If this distance > known best distance → skip
    - For each neighbor:
        - Calculate new possible distance = current dist + edge weight
        - If better than known distance → update distance + previous + push to queue


3. After algorithm finishes:
    Reconstruct path by backtracking from end using `previous` dictionary

Example Draft

| From → To         | Shortest Distance | Path          | Explanation                                 |
| ----------------- | ----------------- | ------------- | ------------------------------------------- |
| A → F             | **7**             | A → B → E → F | 2 + 2 + 3 = 7                               |
| A → B             | **2**             | A → B         | Direct edge                                 |
| E → E             | **0**             | [E]           | Distance to self is always 0                |
| E → F             | **3**             | E → F         | Direct edge (best)                          |
| A → F via A→D→E→F | **12** (worse)    | A → D → E → F | 7 + 2 + 3 = 12 → **not** chosen by Dijkstra |

**Why A→D→E→F (12) is NOT chosen, but A→B→E→F (7) is?**

Dijkstra **greedily** always expands the currently closest known node.

- From A, it first discovers B (dist 2) and D (dist 7)
- It processes B **much earlier** (because 2 < 7)
- From B it reaches E at distance **4** (A→B→E: 2+2)
- Later when it processes D (dist 7), it tries to update E → 7+2=9 → but 9 > 4, so **ignored**
- Then from E (best dist 4), it reaches F at 4+3 = **7**

→ The path via D is **sub-optimal** and correctly discarded.

### Time complexity

This implementation uses Python's `heapq` (binary min-heap).

| Operation                  | Single call       | Total over algorithm              |
|----------------------------|-------------------|------------------------------------|
| Extract-min (`heappop`)    | O(log V)          | O(V log V)                         |
| Decrease-key / Insert (`heappush`) | O(log V)  | O(E log V)                         |
| **Overall time complexity** | —                | **O((V + E) log V)**              |

- V = number of vertices (warehouse zones / nodes)  
- E = number of edges (aisle connections)

## How to run source code
Follow these steps to set up and launch the app.
```
cd Task2
pip install -r requirements.txt
python main.py
```
Access at http://127.0.0.1:5000