import os

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import image as mpimg

current_dir = os.path.dirname(os.path.abspath(__file__))
node_image_path = os.path.join(current_dir, "nodes_icons", "computer-screen_2493283.png")
router_image_path = os.path.join(current_dir, "nodes_icons", "internet_9536354.png")
image_size = (0.1, 0.1)


def visualize_network_graph(connections_lst):
    G = nx.Graph()

    for connection in connections_lst:
        device1, device2 = connection.src_device, connection.dst_device
        mac_address_1, vendor_1 = device1.mac_address, device1.vendor
        mac_address_2, vendor_2 = device2.mac_address, device2.vendor

        G.add_edge(mac_address_1, "main router")
        G.add_edge(mac_address_2, "main router")
        G.add_edge(mac_address_1, mac_address_2, label=connection.protocol)  # Label for edge between devices

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=900)  # You can try different layout algorithms here

    # Load the image for the "main router" node
    main_router_image = mpimg.imread(router_image_path)
    G.nodes["main router"]['image'] = main_router_image

    # Draw the nodes using pictures
    nx.draw_networkx_nodes(G, pos, nodelist=["main router"], node_size=0, node_color='skyblue', alpha=0.7)
    for node in G.nodes():
        if node != "main router" and node in pos:
            plt.imshow(mpimg.imread(node_image_path),
                       extent=[pos[node][0] - image_size[0] / 2, pos[node][0] + image_size[0] / 2,
                               pos[node][1] - image_size[1] / 2, pos[node][1] + image_size[1] / 2],
                       aspect='auto', zorder=0)
        elif node == "main router" and node in pos:
            plt.imshow(G.nodes[node]['image'],
                       extent=[pos[node][0] - image_size[0] / 2, pos[node][0] + image_size[0] / 2,
                               pos[node][1] - image_size[1] / 2, pos[node][1] + image_size[1] / 2],
                       aspect='auto', zorder=0)

    nx.draw_networkx_edges(G, pos, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.axis('off')
    plt.savefig('network_graph.png')
    plt.show()

