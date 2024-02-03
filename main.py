import networkx as nx
import matplotlib.pyplot as plt
import math


# Create dictionary like this: {0:{inf,inf,inf..},1:{inf,inf..},..., num_players:{inf,..}}
def create_bundle_ratios(num_players):
    bundle_ratios = {}
    for player in range(num_players):
        bundle_ratios[player] = {}
        for inner_player in range(num_players):
            bundle_ratios[player][inner_player] = float('inf')
    return bundle_ratios


def build_exchanging_graph(valuations, allocation):
    G = nx.DiGraph()
    num_players = len(valuations)
    bundle_ratios = create_bundle_ratios(num_players)
    min_ratio = float('inf')

    for player in range(num_players):
        min_ratio = float('inf')
        for other_player in range(num_players):
            if other_player != player:
                for object in range(len(allocation[player])):
                    if allocation[player][object] > 0:
                        ratio = valuations[player][object] / valuations[other_player][object]
                        if ratio < min_ratio:
                            min_ratio = ratio
                bundle_ratios[player][other_player] = min_ratio
                G.add_edge(player, other_player, weight=min_ratio)
    return G


def log_transform_weights(graph):
    new_weights = []

    for edge in graph.edges(data=True):
        weight = edge[2].get('weight', 1.0)  # Default weight to 1.0 if not specified

        # Check if the weight is positive before taking the logarithm
        if weight > 0:
            log_weight = math.log(weight)
            new_weights.append(log_weight)
            # Update the graph with the log-transformed weight
            graph[edge[0]][edge[1]]['weight'] = log_weight
    print("new weights: ", new_weights)

    # return new_weights


def has_negative_weight(graph):
    log_transform_weights(graph)
    num_nodes = graph.number_of_nodes()

    for source in graph.nodes:
        distances = {node: float('inf') for node in graph.nodes}
        distances[source] = 0

        for _ in range(num_nodes - 1):
            for u, v, data in graph.edges(data=True):
                weight = data.get('weight', 0)
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 0)
            if distances[u] + weight < distances[v]:
                return True  # Detected a negative weight cycle

    return False  # No negative weight cycle found


#
# valuations = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
# allocation = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]

valuations = [[10, 20, 30, 40], [40, 30, 20, 10]]
allocation = [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]

graph = build_exchanging_graph(valuations, allocation)

for i, j, data in graph.edges(data=True):
    if i != j:
        print(f"{i} -> {j} = {data['weight']:.2f}")

has_negative_cycle = has_negative_weight(graph)
if has_negative_cycle:
    print("IS NOT PARETO EFFICIENT")
else:
    print("IS PARETO EFFICIENT ")
