import networkx as nx
from is_pareto_efficient import is_pareto_efficient


def pareto_improvement(valuations, allocation, transfer_amount=0.001, min_transfer_amount=0.001):
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
    return [G.nodes[i]['allocation'] for i in range(len(allocation))]


valuations = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
initial_allocation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

final_allocation = pareto_improvement(valuations, initial_allocation, transfer_amount=0.01, min_transfer_amount=0.001)
print("Final Pareto efficient allocation:", final_allocation)
