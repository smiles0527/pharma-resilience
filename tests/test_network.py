from src.network import base_network


def test_total_demand_is_180():
    net = base_network()
    assert sum(net["demand"].values()) == 180


def test_arcs_reference_known_nodes():
    net = base_network()
    nodes = set(net["suppliers"] + net["factories"] + net["warehouses"] + net["hospitals"])
    for (src, dst) in net["arc_cost"]:
        assert src in nodes
        assert dst in nodes


def test_arcs_only_connect_adjacent_tiers():
    net = base_network()
    tier = {}
    for name, group in [("supplier", net["suppliers"]), ("factory", net["factories"]),
                        ("warehouse", net["warehouses"]), ("hospital", net["hospitals"])]:
        for n in group:
            tier[n] = name
    allowed = {("supplier", "factory"), ("factory", "warehouse"), ("warehouse", "hospital")}
    for (src, dst) in net["arc_cost"]:
        assert (tier[src], tier[dst]) in allowed


def test_every_hospital_has_two_sources():
    net = base_network()
    for h in net["hospitals"]:
        incoming = [a for a in net["arc_cost"] if a[1] == h]
        assert len(incoming) >= 2


def test_every_non_hospital_node_has_capacity():
    net = base_network()
    for n in net["suppliers"] + net["factories"] + net["warehouses"]:
        assert net["capacity"][n] > 0


def test_each_tier_can_cover_demand_but_not_after_worst_loss():
    net = base_network()
    for group in [net["suppliers"], net["factories"], net["warehouses"]]:
        caps = [net["capacity"][n] for n in group]
        assert sum(caps) >= 180
        assert sum(caps) - max(caps) < 180


def test_base_network_returns_fresh_copies():
    a = base_network()
    a["capacity"]["S1"] = 0
    b = base_network()
    assert b["capacity"]["S1"] > 0
