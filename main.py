import networkx as nx
import matplotlib.pyplot as plt


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
        for other_player in range(num_players):
            if other_player != player:
                for object in range(len(allocation[player])):
                    if allocation[player][object] > 0:
                        ratio = valuations[player][object] / valuations[other_player][object]
                        if ratio < min_ratio:
                            min_ratio = ratio
                bundle_ratios[player][other_player] = min_ratio
                G.add_edge(player, other_player, weight=min_ratio)
                min_ratio = float('inf')
    return G


def visualize_graph(graph):
    for i, j, data in graph.edges(data=True):
        if i != j:
            print(f"{i} -> {j} = {data['weight']:.2f}")

    pos = nx.spring_layout(graph)
    labels = {(i, j): f'{graph[i][j]["weight"]:.2f}' for i, j in graph.edges}

    for node in graph.nodes:
        # Ensure i -> i edge
        graph.add_edge(node, node, weight=0.0)

        # Ensure j -> i edge for all other nodes
        for other_node in graph.nodes:
            if other_node != node:
                graph.add_edge(other_node, node, weight=0.0)

    nx.draw(graph, pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.show()



# Example usage:
valuations = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
allocation = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]

graph = build_exchanging_graph(valuations, allocation)

visualize_graph(graph)
