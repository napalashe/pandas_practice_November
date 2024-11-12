import pandas as pd
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
import matplotlib.pyplot as plt
import contextily as ctx

data = {
    'IP': ['192.168.1.1', '192.168.1.2', '192.168.2.1', '192.168.3.1'],
    'Latitude': [34.0522, 36.7783, 40.7128, 37.7749],
    'Longitude': [-118.2437, -119.4179, -74.0060, -122.4194],
    'Connected_IP': ['192.168.1.2', '192.168.2.1', '192.168.3.1', '192.168.1.1']
}
df = pd.DataFrame(data)

df['Coordinates'] = list(zip(df['Longitude'], df['Latitude']))
df['Coordinates'] = df['Coordinates'].apply(Point)
gdf = gpd.GeoDataFrame(df, geometry='Coordinates', crs="EPSG:4326")

G = nx.Graph()

for idx, row in df.iterrows():
    G.add_node(row['IP'], pos=(row['Longitude'], row['Latitude']))

for _, row in df.iterrows():
    if row['Connected_IP'] in df['IP'].values:
        G.add_edge(row['IP'], row['Connected_IP'])

positions = {ip: (lon, lat) for ip, lon, lat in zip(df['IP'], df['Longitude'], df['Latitude'])}

world = gpd.read_file("110m_cultural/ne_110m_admin_0_countries.shp")
us_boundary = world[world['NAME'] == "United States"]

us_boundary = us_boundary.to_crs(epsg=3857)
gdf = gdf.to_crs(epsg=3857)

fig, ax = plt.subplots(figsize=(12, 8))

us_boundary.plot(ax=ax, color='lightgrey')
gdf.plot(ax=ax, color='blue', markersize=50, label='IP Addresses')

nx_positions = {k: gdf[gdf['IP'] == k].geometry.values[0].coords[0] for k in G.nodes()}
nx.draw_networkx_nodes(G, nx_positions, node_size=100, node_color='red', ax=ax)
nx.draw_networkx_edges(G, nx_positions, edge_color='black', ax=ax)
nx.draw_networkx_labels(G, nx_positions, font_size=8, font_color='black', ax=ax)

ctx.add_basemap(ax, crs=gdf.crs.to_string(), zoom=4)

ax.set_xlim([-14000000, -7000000])
ax.set_ylim([2500000, 6500000])

plt.legend()
plt.show()
