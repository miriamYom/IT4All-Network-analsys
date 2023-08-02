import networkx as nx
import matplotlib.pyplot as plt
import json

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
def drew(connection_data):
    # Create a graph
    G = nx.Graph()

    # Add nodes for each device
    for connection in connection_data:
        G.add_node(connection["Mac"], IP=connection["IP"], ID=connection["ID"], Vendor=connection["Vendor"])

    # Add edges for each connection between devices
    for connection in connection_data:
        G.add_edge(connection["SourceMac"], connection["DestMac"], Protocol=connection["ProtocolName"],
                   Length=connection["Length"])

    # Plot the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)

    # Draw devices
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue")
    nx.draw_networkx_labels(G, pos, font_size=8)

    # Draw connections
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=1)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, "Protocol")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

    plt.title("Connections between Devices")
    plt.axis("off")
    plt.show()

    # Assuming you have G defined
    graph_data = nx.node_link_data(G)
    json_graph_data = json.dumps(graph_data)
    print(json_graph_data)  # Return this JSON data as part of your API response
