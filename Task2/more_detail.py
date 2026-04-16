import heapq
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#  DRAW GRAPH FUNCTION 
def draw_graph(graph, is_weight, is_direct, filename):
    # Create the appropriate NetworkX graph type
    if is_direct:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    # Add edges from your graph dictionary
    for u in graph:
        for v, w in graph[u]:
            G.add_edge(u, v, weight=w)
    
    # Generate nice layout
    pos = nx.spring_layout(G, k=0.8)
    
    # Draw the graph
    plt.figure(figsize=(10, 8))
    
    # 1. Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=800, edgecolors="black")
    
    # 2. Draw edges
    if is_direct:
        nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, arrowsize=20,width=2)
    else:
        nx.draw_networkx_edges(G, pos, edge_color="gray", width=2)
    
    # 3. Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=12,  font_color="black",  font_weight="bold")
    
    # 4. Draw edge weight labels (if requested)
    if is_weight:
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10,label_pos=0.5)  # 0.5 = middle of edge
    
    # Final touches
    plt.title(f"{'Directed' if is_direct else 'Undirected'} Graph" + 
              f"{' with Weights' if is_weight else ''}", 
              fontsize=14, pad=20)
    plt.axis("off")
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(filename, format="png", dpi=300, bbox_inches="tight")
    plt.close()

#  DIJKSTRA 
def dijkstra(graph, start, target):
    """Dijkstra's algorithm with step recording"""

    # Step 1: Make a dictionary of distances. every node is "inf"
    dist = {node: float('inf') for node in graph}
    dist[start] = 0  # Distance to start node is 0 

    # Step 2: Priority queue : like a todo list, smallest distance first
    pq = [(0, start)]  # (distance, node)

    # Step 3: Keep track of previous node ,so we can rebuild the path later
    prev = {node: None for node in graph}

    # Step 4: For recording steps so we can see what happened.
    steps = []
    step_count = 0

    # Step 5: While we still have nodes to check
    while pq:
        d, u = heapq.heappop(pq)  # Take out the node with smallest distance.

        # If this distance is old/worse, skip it.
        if d > dist[u]:
            continue
        
        # Record what we are doing at this step.
        steps.append({
            "Step": step_count,
            "Current Node": u,
            "Distance": d,
            "Distances Snapshot": dist.copy()  # Copy current distances
        })
        step_count += 1

        # Step 6: Look at all neighbors of this node.
        for v, w in graph[u]:
            # If going through u gives a shorter path to v
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w  # Update distance
                prev[v] = u            # Remember we came from u
                heapq.heappush(pq, (dist[v], v))  # Add neighbor to queue

    # Step 7: Build the shortest path by walking backwards from target.
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()  # Flip it to get start → target order

    # Step 8: Make a DataFrame to show steps nicely.
    df = pd.DataFrame(steps)

    # Expand the "Distances Snapshot" column into separate columns.
    dist_df = df["Distances Snapshot"].apply(pd.Series)
    df_expanded = pd.concat([df.drop(columns=["Distances Snapshot"]), dist_df], axis=1)

    return dist.get(target, float('inf')), df_expanded, path


#  DRAW SHORTEST PATH 
def draw_shortest_graph(graph, path, filename):
    # Build a NetworkX graph
    G = nx.DiGraph()
    for u in graph:
        for v, w in graph[u]:
            G.add_edge(u, v, weight=w)

    # Get positions for nodes
    pos = nx.spring_layout(G, k=0.8)

    # Identify edges in shortest path
    path_edges = list(zip(path, path[1:]))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=800)

    # Draw all edges in gray
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="gray")

    # Draw shortest path edges in red
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, arrows=True, arrowsize=20,width=2)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    # Draw edge weights
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Save to PNG
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, format="png")
    plt.close()


# matrix to list for Dijkstra , but stop now , just print it
def matrix_to_adjlist(matrix, nodes, is_weight):
    """
    Convert adjacency matrix to adjacency list format.
    """
    n = len(nodes)
    adjlist = {nodes[i]: [] for i in range(n)}

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:  # edge exists
                w = matrix[i][j] if is_weight else 1
                adjlist[nodes[i]].append((nodes[j], w))
    return adjlist

# Draw graph from adjacency matrix
def draw_matrix_graph(matrix, nodes, filename):
    """
    Draw a directed weighted graph from an adjacency matrix.
    """
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    for node in nodes:
        G.add_node(node)

    # Add edges with weights
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            weight = matrix[i][j]
            if weight != 0:  # Only add edges with non-zero weight
                G.add_edge(nodes[i], nodes[j], weight=weight)

    # Layout for visualization
    pos = nx.spring_layout(G, seed=42)  # consistent layout

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000, font_size=12, arrows=True)

    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    # Save to file
    plt.savefig(filename)
    plt.close()



#  MAIN PROGRAM 
if __name__ == "__main__":
    # adjacency lists
    # a_graph = Directed Graph
    a_graph = {
        "A": [("B", 3), ("D", 2)],
        "B": [("C", 4), ("E", 2)],
        "C": [("F", 6)],
        "D": [("E", 4), ("G", 4)],
        "E": [("F", 3), ("H", 7)],
        "F": [("I", 5), ("J", 5)],
        "G": [("H", 3)],
        "H": [("I", 2)],
        "I": [],
        "J": [],
    }

    # b_graph = Undirected Graph (bidirectional edges)
    b_graph = {
        "A": [("B", 3), ("D", 2)],
        "B": [("A", 3), ("C", 4), ("E", 2)],
        "C": [("B", 4), ("F", 6)],
        "D": [("A", 2), ("E", 4), ("G", 4)],
        "E": [("B", 2), ("D", 4), ("F", 3), ("H", 7)],
        "F": [("C", 6), ("E", 3), ("I", 5), ("J", 5)],
        "G": [("D", 4), ("H", 3)],
        "H": [("E", 7), ("G", 3), ("I", 2)],
        "I": [("F", 5), ("H", 2)],
        "J": [("F", 5)],
    }

    # Define adjacency matrix (Directed Weighted)
    nodes = ['A','B','C','D']
    matrix_direct_weight = [
        [0, 4, 2, 0],  # A → B=4, A→C=2
        [0, 0, 0, 10], # B → D=10
        [0, 0, 0, 5],  # C → D=5
        [0, 0, 0, 0]   # D
    ]

    # Convert matrix to adjacency list
    adjlist_m = matrix_to_adjlist(matrix_direct_weight, nodes, is_weight=True)
    print("Convert matrix to adjacency list",adjlist_m )
    # Draw matrix graph
    draw_matrix_graph(matrix_direct_weight, nodes, filename="matrix.png")

    draw_graph(a_graph, is_weight=True, is_direct=True, filename="isweight_direct_graph.png")
    draw_graph(a_graph, is_weight=False, is_direct=True, filename="unweight_direct_graph.png")

    draw_graph(b_graph, is_weight=False, is_direct=False, filename="unweight_undirecte_graph.png")
    draw_graph(b_graph, is_weight=True, is_direct=False, filename="isweight_undirecte_graph.png")


    # Run Dijkstra on both graphs
    print("Dijkstra on a_graph (Directed)")
    dist_a, steps_a, path_a = dijkstra(a_graph, 'A', 'E')
    print(f"Shortest distance: {dist_a}")
    print(f"Shortest path: {path_a}")
    print(steps_a)
    draw_shortest_graph(a_graph, path_a, "shortest_path_a.png")


    print("\nDijkstra on b_graph (Undirected)")
    dist_b, steps_b, path_b = dijkstra(b_graph, 'A', 'E')
    print(f"Shortest distance: {dist_b}")
    print(f"Shortest path: {path_b}")
    print(steps_b)
    draw_shortest_graph(b_graph, path_b, "shortest_path_b.png")
