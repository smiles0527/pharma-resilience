from src.network import base_network
from src.scenarios import pair_failures, single_node_failures


def test_single_failures_cover_all_non_hospital_nodes():
    net = base_network()
    scenarios = single_node_failures(net)
    assert len(scenarios) == 9
    failed = {nodes[0] for nodes in scenarios}
    assert failed == set(net["suppliers"] + net["factories"] + net["warehouses"])
    assert all(len(nodes) == 1 for nodes in scenarios)


def test_pair_failures_are_all_combinations():
    net = base_network()
    scenarios = pair_failures(net)
    assert len(scenarios) == 36
    assert len(set(map(frozenset, scenarios))) == 36
    for nodes in scenarios:
        assert len(nodes) == 2
        for n in nodes:
            assert n not in net["hospitals"]
