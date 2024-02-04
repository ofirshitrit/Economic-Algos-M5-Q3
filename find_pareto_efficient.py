import networkx as nx

def find_pareto_improvement(graph):
    n = len(graph.nodes)
    G = graph.copy()

    # Initialize value ratios
    value_ratios = {edge: G[edge[0]][edge[1]]['value_ratio'] for edge in G.edges}

    # Iterate until convergence
    while True:
        # Check if current distribution is Pareto efficient
        if is_pareto_efficient(G, n):
            break

        # Find edge with the minimum value ratio
        min_edge = min(value_ratios, key=value_ratios.get)

        # Calculate the transfer amount 'e' for the minimum edge
        e = calculate_transfer_amount(G, min_edge)

        # Update the graph with the transfer
        G = transfer_resources(G, min_edge, e)

        # Update value ratios
        value_ratios = {edge: G[edge[0]][edge[1]]['value_ratio'] for edge in G.edges}

    return G

def is_pareto_efficient(graph, n):
    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        for i in range(n):
            if sum(graph[node][neighbor]['value_ratio'] for neighbor in neighbors) < 1:
                return False
    return True

def calculate_transfer_amount(graph, edge):
    source, target = edge
    value_ratio = graph[source][target]['value_ratio']
    return 1 / value_ratio

def transfer_resources(graph, edge, e):
    source, target = edge
    graph.nodes[source]['resource'] -= e
    graph.nodes[target]['resource'] += e
    return graph

# Example usage
distribution_graph = nx.DiGraph()
distribution_graph.add_edges_from([('A', 'B', {'value_ratio': 0.5}),
                                   ('B', 'C', {'value_ratio': 0.3}),
                                   ('C', 'A', {'value_ratio': 0.2})])
nx.set_node_attributes(distribution_graph, 1, 'resource')

pareto_improvement_graph = find_pareto_improvement(distribution_graph)
print("Pareto Improvement Distribution:")
print(pareto_improvement_graph.edges(data=True))
