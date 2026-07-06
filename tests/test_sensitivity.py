import pytest

from src.network import base_network
from src.scenarios import single_node_failures
from src.sensitivity import run_sensitivity, scale_capacities, scale_costs

LEVELS = [0.0, 0.25, 0.5]


def test_scale_costs_only_touches_arc_costs():
    net = base_network()
    scaled = scale_costs(net, 1.2)
    for arc, cost in net["arc_cost"].items():
        assert scaled["arc_cost"][arc] == pytest.approx(cost * 1.2)
    assert scaled["capacity"] == net["capacity"]


def test_scale_capacities_only_touches_capacities():
    net = base_network()
    scaled = scale_capacities(net, 0.8)
    for node, cap in net["capacity"].items():
        assert scaled["capacity"][node] == pytest.approx(cap * 0.8)
    assert scaled["arc_cost"] == net["arc_cost"]


def test_run_sensitivity_returns_all_variants():
    net = base_network()
    results = run_sensitivity(net, LEVELS, single_node_failures(net))
    assert set(results) == {"base", "cost_x0.8", "cost_x1.2", "capacity_x0.8", "capacity_x1.2"}
    for sweep in results.values():
        assert len(sweep) == len(LEVELS)


def test_cost_scaling_leaves_satisfaction_curve_unchanged():
    net = base_network()
    results = run_sensitivity(net, LEVELS, single_node_failures(net))
    base_curve = [row["worst_satisfaction"] for row in results["base"]]
    for variant in ["cost_x0.8", "cost_x1.2"]:
        curve = [row["worst_satisfaction"] for row in results[variant]]
        assert curve == pytest.approx(base_curve)


def test_capacity_scaling_shifts_curve_in_right_direction():
    net = base_network()
    results = run_sensitivity(net, LEVELS, single_node_failures(net))
    base0 = results["base"][0]["worst_satisfaction"]
    assert results["capacity_x1.2"][0]["worst_satisfaction"] >= base0
    assert results["capacity_x0.8"][0]["worst_satisfaction"] <= base0
