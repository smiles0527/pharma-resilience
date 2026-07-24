import pytest

from run_scaled import main


def test_scaled_run_writes_outputs_and_matches_ccg_to_full_lp(tmp_path):
    summary = main(sizes=(3, 3, 3, 3), seed=1, out_dir=tmp_path)
    assert (tmp_path / "scaled.csv").exists()
    assert summary["ccg_spend"] == pytest.approx(summary["full_spend"], abs=1e-4)
    assert summary["worst_satisfaction"] <= 1.0
    assert summary["ccg_iterations"] >= 1


def test_scaled_run_is_deterministic(tmp_path):
    a = main(sizes=(3, 3, 3, 3), seed=5, out_dir=tmp_path / "a")
    b = main(sizes=(3, 3, 3, 3), seed=5, out_dir=tmp_path / "b")
    for key in ["full_spend", "ccg_spend", "worst_satisfaction", "baseline_satisfaction"]:
        assert a[key] == b[key]
