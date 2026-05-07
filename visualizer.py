from pyvis.network import Network
import json

# Create a network
net = Network(height="1500px", width="100%", directed=True)
net.toggle_physics(False)

with open('graph.json') as graph:
    data = json.load(graph)
    for entry in data["nodes"]:
        net.add_node(int(entry["identifier"][4:]), label=entry["title"], color="grey")
    for entry in data["nodes"]:
        for connection in entry["connected_to"]:
            net.add_edge(int(entry["identifier"][4:]), int(connection[4:]), color="grey")

net.barnes_hut()
net.set_edge_smooth("discrete")
net.write_html("graph.html")