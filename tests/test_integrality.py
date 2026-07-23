import pytest

from src.experiment import fail_nodes
from src.integrality import integrality_gap, run_integrality_experiment
from src.model import solve
from src.network import base_network, integrality_gap_network
from src.robust import apply_allocation, min_spend_plan
from src.scenarios import single_node_failures


def test_base_instance_has_no_integrality_gap():
    net = base_network()
    result = integrality_gap(net, single_node_failures(net), 1.0)
    assert result["status"] == "Optimal"
    assert result["lp_spend"] == pytest.approx(170.0)
    assert result["gap"] == pytest.approx(0.0, abs=1e-6)


def test_experiment_runs_seeded_batch():
    summary = run_integrality_experiment(count=8, seed=3, gamma=1)
    assert summary["instances"] == 8
    assert 0 <= summary["feasible"] <= 8
    assert len(summary["rows"]) == 8
    for row in summary["rows"]:
        if row["status"] == "Optimal":
            assert row["gap"] >= -1e-6


def test_experiment_is_deterministic():
    a = run_integrality_experiment(count=4, seed=11, gamma=1)
    b = run_integrality_experiment(count=4, seed=11, gamma=1)
    assert a == b


def test_pinned_counterexample_has_fractional_gap():
    net = integrality_gap_network()
    result = integrality_gap(net, single_node_failures(net), 1.0)
    assert result["lp_spend"] == pytest.approx(106.5)
    assert result["ip_spend"] == pytest.approx(107.0)
    assert result["gap"] == pytest.approx(0.5)


def test_pinned_counterexample_fractional_plan_is_feasible():
    net = integrality_gap_network()
    scenarios = single_node_failures(net)
    lp = min_spend_plan(net, scenarios, 1.0)
    protected = apply_allocation(net, lp["extra"])
    for nodes in scenarios:
        assert solve(fail_nodes(protected, nodes))["satisfaction"] == pytest.approx(1.0)
