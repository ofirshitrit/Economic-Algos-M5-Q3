import networkx as nx
from is_pareto_efficient import is_pareto_efficient

def pareto_improvement(valuations, allocation, transfer_amount=0.001, min_transfer_amount=0.001):
    """
    Perform Pareto improvement on the given allocation.

    Parameters:
    - valuations (List[List[int]]): A list of lists representing the valuations of players for each item.
    - allocation (List[List[int]]): The initial allocation of resources to players.
    - transfer_amount (float): The amount of resources to transfer in each step.
    - min_transfer_amount (float): The minimum transfer amount required for a transfer to be considered.

    Returns:
    List[List[int]]: The final Pareto efficient allocation.

    Examples:
    >>> valuations = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
    >>> allocation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    >>> pareto_improvement(valuations, allocation, transfer_amount=0.01, min_transfer_amount=0.001)
    No! - The allocation is NOT pareto efficient
    [['0.99', '0.00', '0.00'], ['0.00', '1.00', '0.00'], ['0.01', '0.01', '1.01']]

     >>> valuations = [[10, 20, 30, 40], [40, 30, 20, 10]]
    >>> allocation = [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]
    >>> pareto_improvement(valuations, allocation, transfer_amount=0.01, min_transfer_amount=0.001)
    Yes! - The allocation is pareto efficient
    Initial allocation is already Pareto efficient.
    """
    if is_pareto_efficient(valuations, allocation):
        print("Initial allocation is already Pareto efficient.")
        return allocation

    # Create a directed graph to represent the players and their allocations
    G = nx.DiGraph()

    # Add nodes for each player and allocate their resources
    for i, player_allocation in enumerate(allocation):
        G.add_node(i, allocation=player_allocation)

    # Add edges to represent the direction of resource transfers
    for i in range(len(allocation) - 1):
        G.add_edge(i, i + 1)

    # Perform Pareto improvement
    for i in range(len(allocation) - 1):
        # Get the current and next player's allocation
        current_allocation = G.nodes[i]['allocation']
        next_allocation = G.nodes[i + 1]['allocation']

        # Check if the transfer is feasible
        if any(x > min_transfer_amount for x in current_allocation):
            updated_current_allocation = [max(x - transfer_amount, 0) for x in current_allocation]
            updated_next_allocation = [x + transfer_amount for x in next_allocation]

            G.nodes[i]['allocation'] = updated_current_allocation
            G.nodes[i + 1]['allocation'] = updated_next_allocation

    # Return the final allocation after Pareto improvement
    return [[format(x, '.2f') for x in G.nodes[i]['allocation']] for i in range(len(allocation))]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
