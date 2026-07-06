from copy import deepcopy

from src.experiment import protection_sweep


def scale_costs(network, factor):
    scaled = deepcopy(network)
    scaled["arc_cost"] = {arc: cost * factor for arc, cost in network["arc_cost"].items()}
    return scaled


def scale_capacities(network, factor):
    scaled = deepcopy(network)
    scaled["capacity"] = {node: cap * factor for node, cap in network["capacity"].items()}
    return scaled


def run_sensitivity(base, levels, scenarios):
    variants = {
        "base": base,
        "cost_x0.8": scale_costs(base, 0.8),
        "cost_x1.2": scale_costs(base, 1.2),
        "capacity_x0.8": scale_capacities(base, 0.8),
        "capacity_x1.2": scale_capacities(base, 1.2),
    }
    return {
        name: protection_sweep(net, levels, scenarios)
        for name, net in variants.items()
    }
