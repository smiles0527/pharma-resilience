from src.plots import sensitivity_plot, tradeoff_plot

SWEEP = [
    {"level": 0.0, "spend": 0.0, "worst_satisfaction": 0.72,
     "worst_scenario": ("S1",), "max_recovery_cost": 50000.0},
    {"level": 0.5, "spend": 330.0, "worst_satisfaction": 1.0,
     "worst_scenario": ("S1",), "max_recovery_cost": 100.0},
]


def test_tradeoff_plot_writes_file(tmp_path):
    out = tmp_path / "tradeoff.png"
    tradeoff_plot(SWEEP, out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_sensitivity_plot_writes_file(tmp_path):
    out = tmp_path / "sensitivity.png"
    sensitivity_plot({"base": SWEEP, "capacity_x1.2": SWEEP}, out)
    assert out.exists()
    assert out.stat().st_size > 0
