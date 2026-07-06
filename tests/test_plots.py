from src.network import base_network
from src.plots import (
    coinciding_variants,
    network_diagram,
    sensitivity_plot,
    tradeoff_plot,
)

SWEEP = [
    {"level": 0.0, "spend": 0.0, "worst_satisfaction": 0.72,
     "worst_scenario": ("S1",), "max_recovery_cost": 50000.0},
    {"level": 0.5, "spend": 330.0, "worst_satisfaction": 1.0,
     "worst_scenario": ("W1",), "max_recovery_cost": 100.0},
]

PAIR_SWEEP = [
    {"level": 0.0, "spend": 0.0, "worst_satisfaction": 0.33,
     "worst_scenario": ("S1", "S2"), "max_recovery_cost": 60000.0},
    {"level": 0.5, "spend": 330.0, "worst_satisfaction": 0.39,
     "worst_scenario": ("W1", "W2"), "max_recovery_cost": 40000.0},
]

SHIFTED = [
    {"level": 0.0, "spend": 0.0, "worst_satisfaction": 0.65,
     "worst_scenario": ("S1",), "max_recovery_cost": 55000.0},
    {"level": 0.5, "spend": 330.0, "worst_satisfaction": 0.95,
     "worst_scenario": ("W1",), "max_recovery_cost": 900.0},
]


def test_tradeoff_plot_writes_file(tmp_path):
    out = tmp_path / "tradeoff.png"
    tradeoff_plot(SWEEP, PAIR_SWEEP, out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_sensitivity_plot_writes_file(tmp_path):
    out = tmp_path / "sensitivity.png"
    sensitivity_plot(
        {"base": SWEEP, "cost_x1.2": list(SWEEP), "capacity_x0.8": SHIFTED},
        out,
    )
    assert out.exists()
    assert out.stat().st_size > 0


def test_coinciding_variants_folds_identical_curves_only():
    variants = {"base": SWEEP, "cost_x1.2": list(SWEEP), "capacity_x0.8": SHIFTED}
    assert coinciding_variants(variants) == ["cost_x1.2"]


def test_network_diagram_writes_file(tmp_path):
    out = tmp_path / "network.png"
    network_diagram(base_network(), out)
    assert out.exists()
    assert out.stat().st_size > 0
