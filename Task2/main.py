from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__, template_folder="templates")

# Graph & layout definition 

# Graph as adjacency list: node -> list of (neighbor, distance)
GRAPH = {
    "A": [("B", 2), ("D", 7)],
    "B": [("A", 2), ("C", 4), ("E", 2)],
    "C": [("B", 4), ("F", 6)],
    "D": [("A", 7), ("E", 2), ("G", 4)],
    "E": [("B", 2), ("D", 2), ("F", 3), ("H", 7)],
    "F": [("C", 6), ("E", 3), ("I", 5), ("J", 5)],
    "G": [("D", 4), ("H", 3)],
    "H": [("E", 7), ("G", 3), ("I", 2)],
    "I": [("F", 5), ("H", 2)],
    "J": [("F", 5)],
}

# Hard‑coded coordinates for drawing (x, y) on canvas
POSITIONS = {
    "A": (50, 50),
    "B": (130, 50),
    "C": (290, 50),
    "D": (50, 330),
    "E": (130, 130),
    "F": (250, 290),
    "G": (50, 490),
    "H": (210, 410),
    "I": (290, 490),
    "J": (450, 290),
}

# Dijkstra implementation 
def dijkstra(graph, start, end):
    # Priority queue of (distance, node)
    pq = [(0, start)]
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    while pq:
        dist, node = heapq.heappop(pq)
        if dist > distances[node]:
            continue
        if node == end:
            break
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    # Reconstruct path from end back to start
    if distances[end] == float("inf"):
        return float("inf"), []

    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = previous[cur]
    path.reverse()
    return distances[end], path


# Routes 
@app.route("/")
def index():
    buildings = sorted(GRAPH.keys())
    return render_template(
        "index.html",
        buildings=buildings,
        positions=POSITIONS,
        graph=GRAPH,
    )


@app.route("/shortest-path", methods=["POST"])
def shortest_path():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")

    distance, path = dijkstra(GRAPH, start, end)
    return jsonify({"distance": distance, "path": path})


if __name__ == "__main__":
    app.run(debug=True)
