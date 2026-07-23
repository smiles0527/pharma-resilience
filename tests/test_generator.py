import random

from src.generator import random_layered_network

TIERS = ["suppliers", "factories", "warehouses", "hospitals"]


def test_same_seed_gives_same_network():
    a = random_layered_network(random.Random(7))
    b = random_layered_network(random.Random(7))
    assert a == b


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
