import io
import networkx as nx
import matplotlib.pyplot as plt
from typing import List


def draw(lst_connections: List):
    G = nx.DiGraph()
    edge_labels = {}
    for connection in lst_connections:
        is_router = connection["Name"] == "Router"
        source_mac = connection["SourceMac"]
        destination_mac = connection["DestMac"]
        G.add_edge(source_mac, destination_mac)
        G.nodes[source_mac]['label'] = source_mac
        G.nodes[destination_mac]['label'] = destination_mac
        edge_labels[(source_mac, destination_mac)] = "protocol"
    # Draw nodes with labels
    node_labels = nx.get_node_attributes(G, 'label')
    pos = nx.circular_layout(G)
    node_color='red' if is_router else 'skyblue'
    nx.draw_networkx(G, pos, labels=node_labels, with_labels=True, node_size=3000, font_size=9, node_color=node_color)
    nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.7)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=8)
    plt.axis('off')
    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()  # Clear the plot
    return buffer
