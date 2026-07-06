from itertools import combinations


def _failable_nodes(network):
    return network["suppliers"] + network["factories"] + network["warehouses"]


def single_node_failures(network):
    return [(node,) for node in _failable_nodes(network)]


def pair_failures(network):
    return list(combinations(_failable_nodes(network), 2))
