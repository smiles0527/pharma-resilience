import random

from src.generator import random_layered_network

TIERS = ["suppliers", "factories", "warehouses", "hospitals"]


def test_same_seed_gives_same_network():
    a = random_layered_network(random.Random(7))
    b = random_layered_network(random.Random(7))
    assert a == b


def test_explicit_sizes_control_tier_widths():
    net = random_layered_network(random.Random(1), sizes=(6, 5, 7, 9))
    assert len(net["suppliers"]) == 6
    assert len(net["factories"]) == 5
    assert len(net["warehouses"]) == 7
    assert len(net["hospitals"]) == 9


def test_large_network_keeps_valid_schema():
    net = random_layered_network(random.Random(2), sizes=(12, 12, 12, 15))
    nodes_with_in = {b for _, b in net["arc_cost"]}
    for tier in TIERS[1:]:
        assert set(net[tier]) <= nodes_with_in
    for node in net["suppliers"] + net["factories"] + net["warehouses"]:
        assert net["capacity"][node] >= 1


def test_generated_network_has_valid_schema():
    for seed in range(20):
        net = random_layered_network(random.Random(seed))
        for tier in TIERS:
            assert len(net[tier]) >= 2
        for node in net["suppliers"] + net["factories"] + net["warehouses"]:
            assert net["capacity"][node] >= 1
        for h in net["hospitals"]:
            assert net["demand"][h] >= 1
        tier_of = {n: i for i, tier in enumerate(TIERS) for n in net[tier]}
        for (src, dst), cost in net["arc_cost"].items():
            assert tier_of[dst] == tier_of[src] + 1
            assert cost >= 1
        nodes_with_out = {a for a, _ in net["arc_cost"]}
        nodes_with_in = {b for _, b in net["arc_cost"]}
        for tier in TIERS[:-1]:
            assert set(net[tier]) <= nodes_with_out
        for tier in TIERS[1:]:
            assert set(net[tier]) <= nodes_with_in
