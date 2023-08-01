import networkx as nx
import matplotlib.pyplot as plt

# Sample query result (replace this with your actual query result)
query_result = [
    (1, 'AA:BB:CC:DD:EE:01', 'AA:BB:CC:DD:EE:02', 'TCP', 100, '2023-08-01 12:00:00'),
    (2, 'AA:BB:CC:DD:EE:02', 'AA:BB:CC:DD:EE:03', 'UDP', 50, '2023-08-01 12:05:00'),
    (3, 'AA:BB:CC:DD:EE:03', 'AA:BB:CC:DD:EE:04', 'UDP', 70, '2023-08-01 12:10:00'),
    (4, 'AA:BB:CC:DD:EE:04', 'AA:BB:CC:DD:EE:05', 'TCP', 120, '2023-08-01 12:15:00'),
    (5, 'AA:BB:CC:DD:EE:05', 'AA:BB:CC:DD:EE:06', 'UDP', 60, '2023-08-01 12:20:00'),
    (6, 'AA:BB:CC:DD:EE:06', 'AA:BB:CC:DD:EE:07', 'TCP', 90, '2023-08-01 12:25:00'),
    (7, 'AA:BB:CC:DD:EE:07', 'AA:BB:CC:DD:EE:08', 'UDP', 80, '2023-08-01 12:30:00'),
    (8, 'AA:BB:CC:DD:EE:08', 'AA:BB:CC:DD:EE:09', 'TCP', 150, '2023-08-01 12:35:00'),
    (9, 'AA:BB:CC:DD:EE:09', 'AA:BB:CC:DD:EE:10', 'UDP', 50, '2023-08-01 12:40:00'),
]

# Create a graph
G = nx.Graph()

# Add nodes for each device and connections
for row in query_result:
    device_id, source_mac, dest_mac, protocol, length, time = row

    # Add device node with a 'type' attribute set to 'device'
    G.add_node(source_mac, type='device', device_id=device_id)

    # Add connection edge with attributes for protocol, length, and time
    G.add_edge(source_mac, dest_mac, protocol=protocol, length=length, time=time)

# Plot the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Positions nodes using a spring layout algorithm

# Separate devices and connections for different visualization styles
device_nodes = [node for node, attr in G.nodes(data=True) if 'type' in attr and attr['type'] == 'device']
connection_edges = [(source, dest) for source, dest, attr in G.edges(data=True)]

# Draw devices
nx.draw_networkx_nodes(G, pos, nodelist=device_nodes, node_size=2000, node_color='skyblue')
nx.draw_networkx_labels(G, pos, labels={node: node for node in device_nodes}, font_size=8)

# Draw connections
nx.draw_networkx_edges(G, pos, edgelist=connection_edges, edge_color='gray', width=1)

# Draw edge labels (protocol)
edge_labels = {(source, dest): attr['protocol'] for source, dest, attr in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Connections between Devices")
plt.axis('off')
plt.show()
