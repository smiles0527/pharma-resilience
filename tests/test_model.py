from copy import deepcopy

import pytest

from src.model import solve
from src.network import base_network


def toy_chain(supplier_cap):
    return {
        "suppliers": ["S"],
        "factories": ["F"],
        "warehouses": ["W"],
        "hospitals": ["H"],
        "capacity": {"S": supplier_cap, "F": 10, "W": 10},
        "demand": {"H": 10},
        "arc_cost": {("S", "F"): 1, ("F", "W"): 2, ("W", "H"): 3},
        "penalty": 1000,
        "protection_cost_rate": 1.0,
    }


def test_toy_chain_exact_cost():
    result = solve(toy_chain(supplier_cap=10))
    assert result["status"] == "Optimal"
    assert result["satisfaction"] == pytest.approx(1.0)
    assert result["shipping_cost"] == pytest.approx(60)
    assert result["cost"] == pytest.approx(60)


def test_toy_chain_shortage_when_supply_capped():
    result = solve(toy_chain(supplier_cap=4))
    assert result["satisfaction"] == pytest.approx(0.4)
    assert result["unmet"]["H"] == pytest.approx(6)
    assert result["cost"] == pytest.approx(4 * 6 + 1000 * 6)
    assert result["shipping_cost"] == pytest.approx(24)


def test_baseline_meets_all_demand():
    result = solve(base_network())
    assert result["status"] == "Optimal"
    assert result["satisfaction"] == pytest.approx(1.0)
    assert all(u == pytest.approx(0) for u in result["unmet"].values())


def test_solve_does_not_mutate_input():
    net = base_network()
    snapshot = deepcopy(net)
    solve(net)
    assert net == snapshot


def test_destroyed_node_reports_shortage_not_infeasible():
    net = base_network()
    net["capacity"]["S1"] = 0
    result = solve(net)
    assert result["status"] == "Optimal"
    assert result["satisfaction"] < 1.0


def test_min_fill_rate_matches_satisfaction_for_single_hospital():
    result = solve(toy_chain(supplier_cap=4))
    assert result["min_fill_rate"] == pytest.approx(0.4)


def test_min_fill_rate_is_zero_when_a_hospital_is_disconnected():
    net = base_network()
    net["capacity"]["W1"] = 0
    net["capacity"]["W2"] = 0
    result = solve(net)
    assert result["satisfaction"] > 0.3
    assert result["min_fill_rate"] == pytest.approx(0.0)
