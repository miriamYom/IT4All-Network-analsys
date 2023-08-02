import networkx as nx
import matplotlib.pyplot as plt
import io


def draw(connection_data):
    # Create a graph G = nx.Graph()
    G = nx.DiGraph()
    # Add nodes for each device
    for connection in connection_data:
        G.add_node(connection["Mac"], IP=connection["IP"], ID=connection["ID"], Vendor=connection["Vendor"])
    # Add edges for each connection between devices
    for connection in connection_data:
        G.add_edge(connection["SourceMac"], connection["DestMac"], Protocol="Protocol", Length=connection["Length"])
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

    # img_buffer = io.BytesIO()
    # plt.savefig(img_buffer, format="png")
    # img_buffer.seek(0)
    #
    # # Include the image data in the response
    # response = img_buffer.read()
    #
    # return response

    plt.axis('off')
    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.show()
    # Clear the plot
    plt.clf()
    return buffer
