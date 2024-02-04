import networkx as nx
import math

def build_exchanging_graph(valuations, allocation):
    G = nx.DiGraph()
    num_players = len(valuations)

    for player in range(num_players):
        for other_player in range(num_players):
            if other_player != player:
                min_ratio = min(
                    valuations[player][k] / valuations[other_player][k]
                    for k in range(num_players) if allocation[player][k] != 0
                )
                G.add_edge(player, other_player, weight=min_ratio)

    return G

# def log_weights(graph):
#     new_weights = []
#
#     for edge in graph.edges(data=True):
#         weight = edge[2].get('weight', 1.0)  # Default weight to 1.0 if not specified
#
#         # Check if the weight is positive before taking the logarithm
#         if weight > 0:
#             log_weight = math.log(weight)
#             new_weights.append(log_weight)
#             # Update the graph with the log-transformed weight
#             graph[edge[0]][edge[1]]['weight'] = log_weight
#     print("new weights: ", new_weights)
#
#     return new_weights
#
# def has_negative_weight(graph):
#     log_weights(graph)
#     num_nodes = graph.number_of_nodes()
#
#     for source in graph.nodes:
#         distances = {node: float('inf') for node in graph.nodes}
#         distances[source] = 0
#
#         for _ in range(num_nodes - 1):
#             for u, v, data in graph.edges(data=True):
#                 weight = data.get('weight', 0)
#                 if distances[u] + weight < distances[v]:
#                     distances[v] = distances[u] + weight
#
#         for u, v, data in graph.edges(data=True):
#             weight = data.get('weight', 0)
#             if distances[u] + weight < distances[v]:
#                 return True  # Detected a negative weight cycle
#
#     return False  # No negative weight cycle found

def is_pareto_efficient(valuations, allocation):
    graph = build_exchanging_graph(valuations, allocation)
    for i, j, data in graph.edges(data=True):
        if i != j:
            print(f"{i} -> {j} = {data['weight']:.2f}")
    has_negative_cycle = has_negative_weight(graph)
    if has_negative_cycle:
        print("The allocation is NOT pareto efficient")
    else:
        print("The allocation is pareto efficient")

if __name__ == '__main__':
    valuations = [[10, 20, 30, 40], [40, 30, 20, 10]]
    allocation = [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]

    # valuations = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
    # allocation = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]

    is_pareto_efficient(valuations, allocation)
