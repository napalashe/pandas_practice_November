import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

data = {
    "IP": ["192.168.0.1", "10.0.0.1", "172.16.0.1"],
    "Latitude": [34.0522, 36.1699, 40.7128],
    "Longitude": [-118.2437, -115.1398, -74.0060]
}

df = pd.DataFrame(data)

G = nx.Graph()

for idx, row in df.iterrows():
    G.add_node(row["IP"], pos=(row["Longitude"], row["Latitude"]))

distance_threshold = 3000

for i, node1 in df.iterrows():
    for j, node2 in df.iterrows():
        if i < j:
            distance = geodesic((node1["Latitude"], node1["Longitude"]),
                                (node2["Latitude"], node2["Longitude"])).km
            if distance <= distance_threshold:
                G.add_edge(node1["IP"], node2["IP"])

pos = nx.get_node_attributes(G, 'pos')

plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("IP Geolocation Network (Edges based on proximity)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
