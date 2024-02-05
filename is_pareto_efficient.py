import networkx as nx
import sys
import doctest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Comment this line to see prints of the logger
logger.setLevel(logging.WARNING)


def build_exchanging_graph(valuations, allocation):
    G = nx.DiGraph()
    num_players = len(valuations)

    for player in range(num_players):
        for other_player in range(num_players):
            if other_player != player:
                min_ratio = min(
                    valuations[player][object] / valuations[other_player][object]
                    for object in range(num_players) if allocation[player][object] != 0)
                G.add_edge(player, other_player, weight=min_ratio)

    return G


def has_cycle_with_small_product(graph):
    def dfs(node, visited, product):
        if node in visited:
            return product < 1
        visited.add(node)

        for neighbor, data in graph[node].items():
            weight = data.get('weight', 1)
            new_product = product * weight
            if dfs(neighbor, visited.copy(), new_product):
                return True
        return False

    for node in graph.nodes:
        if dfs(node, set(), 1):
            return True
    return False


def is_pareto_efficient(valuations, allocation):
    """
    Check if the allocation is Pareto efficient based on valuations.

    Parameters:
    - valuations (list): List of lists representing valuations of players for each object.
    - allocation (list): List of lists representing the allocation of objects to players.

    Prints:
    - str: Output indicating whether the allocation is Pareto efficient or not.

    >>> valuations = [[10, 20, 30, 40], [40, 30, 20, 10]]
    >>> allocation = [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]
    >>> is_pareto_efficient(valuations, allocation)
    Yes! - The allocation is pareto efficient

    >>> valuations = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
    >>> allocation = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    >>> is_pareto_efficient(valuations, allocation)
    Yes! - The allocation is pareto efficient

    >>> valuations = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
    >>> allocation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    >>> is_pareto_efficient(valuations, allocation)
    No! - The allocation is NOT pareto efficient

    """

    graph = build_exchanging_graph(valuations, allocation)
    has_negative_cycle = has_cycle_with_small_product(graph)
    if has_negative_cycle:
        print("No! - The allocation is NOT pareto efficient")
    else:
        print("Yes! - The allocation is pareto efficient")



if __name__ == '__main__':
    doctest.testmod()
