from copy import deepcopy

import pytest

from src.experiment import (
    apply_protection,
    evaluate_scenarios,
    fail_nodes,
    protection_spend,
    protection_sweep,
    worst_case,
)
from src.model import solve
from src.network import base_network
from src.scenarios import single_node_failures


def test_calibration_every_single_failure_causes_shortage():
    net = base_network()
    for nodes in single_node_failures(net):
        result = solve(fail_nodes(net, nodes))
        assert result["satisfaction"] < 1.0, f"failure of {nodes} causes no shortage"


def test_fail_nodes_zeroes_capacity_without_mutating_original():
    net = base_network()
    snapshot = deepcopy(net)
    failed = fail_nodes(net, ("S1", "W2"))
    assert failed["capacity"]["S1"] == 0
    assert failed["capacity"]["W2"] == 0
    assert net == snapshot


def test_apply_protection_scales_all_capacities():
    net = base_network()
    snapshot = deepcopy(net)
    protected = apply_protection(net, 0.2)
    for node, cap in net["capacity"].items():
        assert protected["capacity"][node] == pytest.approx(cap * 1.2)
    assert net == snapshot


def test_protection_spend_is_linear_in_level():
    net = base_network()
    total_capacity = sum(net["capacity"].values())
    assert protection_spend(net, 0.0) == pytest.approx(0.0)
    assert protection_spend(net, 0.1) == pytest.approx(
        net["protection_cost_rate"] * 0.1 * total_capacity
    )


def test_evaluate_scenarios_reports_nonnegative_recovery_cost():
    net = base_network()
    rows = evaluate_scenarios(net, single_node_failures(net))
    assert len(rows) == 9
    for row in rows:
        assert row["recovery_cost"] >= -1e-6
        assert 0.0 <= row["satisfaction"] < 1.0


def test_worst_case_picks_minimum_satisfaction():
    rows = [
        {"failed": ("A",), "satisfaction": 0.9, "recovery_cost": 1.0},
        {"failed": ("B",), "satisfaction": 0.7, "recovery_cost": 2.0},
    ]
    assert worst_case(rows)["failed"] == ("B",)


def test_sweep_worst_case_improves_with_protection():
    net = base_network()
    scenarios = single_node_failures(net)
    sweep = protection_sweep(net, [0.0, 0.25, 0.5], scenarios)
    satisfactions = [row["worst_satisfaction"] for row in sweep]
    assert satisfactions == sorted(satisfactions)
    assert satisfactions[0] < 1.0
    assert satisfactions[-1] == pytest.approx(1.0, abs=1e-6)
    spends = [row["spend"] for row in sweep]
    assert spends[0] == pytest.approx(0.0)
    assert spends == sorted(spends)
