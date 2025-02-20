import networkx as nx
import matplotlib.pyplot as plt


def build_graph():
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges with their capacities
    edges = [
        ('Terminal 1', 'Warehouse 1', 25),
        ('Terminal 1', 'Warehouse 2', 20),
        ('Terminal 1', 'Warehouse 3', 15),
        ('Terminal 2', 'Warehouse 3', 15),
        ('Terminal 2', 'Warehouse 4', 30),
        ('Terminal 2', 'Warehouse 2', 10),
        ('Warehouse 1', 'Store 1', 15),
        ('Warehouse 1', 'Store 2', 10),
        ('Warehouse 1', 'Store 3', 20),
        ('Warehouse 2', 'Store 4', 15),
        ('Warehouse 2', 'Store 5', 10),
        ('Warehouse 2', 'Store 6', 25),
        ('Warehouse 3', 'Store 7', 20),
        ('Warehouse 3', 'Store 8', 15),
        ('Warehouse 3', 'Store 9', 10),
        ('Warehouse 4', 'Store 10', 20),
        ('Warehouse 4', 'Store 11', 10),
        ('Warehouse 4', 'Store 12', 15),
        ('Warehouse 4', 'Store 13', 5),
        ('Warehouse 4', 'Store 14', 10)
    ]
    G.add_weighted_edges_from(edges, weight='capacity')
    return G

def visualize_graph(G):
    # Set positions for each node (keys correspond to node names)
    pos = {
        'Store 1': (0, 7),
        'Store 2': (1, 7),
        'Store 3': (2, 7),
        'Warehouse 1': (1, 5),

        'Store 4': (4, 7),
        'Store 5': (5, 7),
        'Store 6': (6, 7),
        'Warehouse 2': (5, 5),

        'Terminal 1': (2, 4),
        'Terminal 2': (4, 4),

        'Warehouse 3': (1, 3),
        'Store 7': (0, 1),
        'Store 8': (1, 1),
        'Store 9': (2, 1),

        'Warehouse 4': (5, 3),
        'Store 10': (3, 1),
        'Store 11': (4, 1),
        'Store 12': (5, 1),
        'Store 13': (6, 1),
        'Store 14': (7, 1),
    }

    plt.figure(figsize=(12, 8))
    nx.draw(
        G, pos,
        with_labels=True,
        node_size=2000,
        node_color="skyblue",
        font_size=12,
        font_weight="bold",
        arrows=True
    )

    # Edge labels (capacities)
    labels = nx.get_edge_attributes(G, "capacity")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Logistic Network")
    plt.show()

def calculate_max_flow(G):
    # The Edmonds-Karp algorithm requires a single source and sink, we create a copy of graph and add a single source and sink
    H = G.copy()
    H.add_node("Source")
    H.add_node("Sink")

    # Connect the source to terminals with no capacity limit
    H.add_edge('Source', 'Terminal 1', capacity=float('Inf'))
    H.add_edge('Source', 'Terminal 2', capacity=float('Inf'))

    #
    # Connect stores to the sink with no capacity limit
    for i in range(1, 15):
        H.add_edge(f'Store {i}', 'Sink', capacity=float('Inf'))

    # Calculate the maximum flow
    flow_value, flow_dict = nx.maximum_flow(H, 'Source', 'Sink', flow_func=nx.algorithms.flow.edmonds_karp)
    print(f"Maximum flow: {flow_value}")
    return flow_dict, flow_value

def build_flow_table(flow_dict):
    terminals = ["Terminal 1", "Terminal 2"]
    warehouses = ["Warehouse 1", "Warehouse 2", "Warehouse 3", "Warehouse 4"]
    stores = [f"Store {i}" for i in range(1, 15)]

    rows = []
    for terminal in terminals:
        for store in stores:
            total_flow_ts = 0.0

            # Check which warehouses the flow might pass through
            for w in warehouses:
                flow_tw = flow_dict[terminal].get(w, 0)  # Flow terminal->warehouse
                flow_ws = flow_dict[w].get(store, 0)     # Flow warehouse->store

                # Total flow arriving at warehouse w from all terminals
                inflow_w = sum(flow_dict[t].get(w, 0) for t in terminals)

                # If warehouse w actually receives flow, partially from this terminal
                if inflow_w > 0:
                    fraction = flow_tw / inflow_w
                    total_flow_ts += flow_ws * fraction


            rows.append((terminal, store, f"{total_flow_ts:.2f}"))

    # Print table
    print(f"| {'-'*10} | {'-'*10} | {'-'*22} |")
    print("| Terminal   | Store      | Actual Flow (units)    |")
    print(f"| {'-'*10} | {'-'*10} | {'-'*22} |")
    for terminal, store, flow in rows:
        print(f"| {terminal:<10} | {store:<10} | {flow:<22} |")
    print(f"| {'-'*10} | {'-'*10} | {'-'*22} |")

if __name__ == "__main__":
    G = build_graph()
    flow_dict, flow_value = calculate_max_flow(G)
    build_flow_table(flow_dict)

# Conclusion is added to readme
