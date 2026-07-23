import pytest

from src.model import solve
from src.network import equity_paradox_network
from src.robust import apply_allocation, min_spend_plan


def test_unprotected_instance_splits_delivery_across_hospitals():
    net = equity_paradox_network()
    result = solve(net)
    assert result["satisfaction"] == pytest.approx(0.5)
    assert result["min_fill_rate"] == pytest.approx(0.4)


def test_optimal_protection_raises_satisfaction_but_collapses_equity():
    net = equity_paradox_network()
    plan = min_spend_plan(net, [("W2",)], 0.55)
    assert plan["status"] == "Optimal"
    protected = solve(apply_allocation(net, plan["extra"]))
    assert protected["satisfaction"] > 0.5
    assert protected["min_fill_rate"] < 0.4
