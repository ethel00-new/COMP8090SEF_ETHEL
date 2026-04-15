from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__, template_folder="templates")

# Graph & layout definition 

# Graph as adjacency list: node -> list of (neighbor, distance)
GRAPH = {
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

# Hard‑coded coordinates for drawing (x, y) on canvas
POSITIONS = {
    "A": (50, 50),
    "B": (170, 50),
    "C": (330, 50),
    "D": (50, 130),
    "E": (210, 130),
    "F": (250, 290),
    "G": (50, 290),
    "H": (210, 410),
    "I": (290, 490),
    "J": (450, 290),
}

# Dijkstra implementation 
def dijkstra(graph, start, end):
    # Priority queue of (distance, node)
    pq = [(0, start)] # step 1 : init 0
    distances = {node: float("inf") for node in graph} # Step 2 : explore node and get float , other inf
    previous = {node: None for node in graph} # step 3 : mark previous , for draw a graph
    distances[start] = 0

    while pq: # step 4 : if list still have data , keep going
        dist, node = heapq.heappop(pq) # get the shorter distance 1st
        if dist > distances[node]: # not better skip
            continue
        if node == end: # done all
            break
        for neighbor, weight in graph[node]: # step 5 : have neighbor ?
            new_dist = dist + weight # add dist
            if new_dist < distances[neighbor]: # shorter record replace it 
                distances[neighbor] = new_dist  # update shorter
                previous[neighbor] = node # remember prev node
                heapq.heappush(pq, (new_dist, neighbor)) # new finding on list

    # Step 6 : until end still inf
    if distances[end] == float("inf"):
        return float("inf"), []
    # step 7 : go back and find the shorter path
    path = []
    cur = end
    while cur is not None:
        path.append(cur) # save path
        cur = previous[cur] # go back 
    path.reverse() # just reverse
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
