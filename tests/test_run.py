import csv

from run import LEVELS, main


def test_main_writes_all_outputs(tmp_path):
    main(out_dir=tmp_path)
    for name in ["sweep.csv", "sensitivity.csv", "tradeoff.png", "sensitivity.png", "network.png"]:
        assert (tmp_path / name).exists(), f"missing {name}"
    with open(tmp_path / "sweep.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(LEVELS)
    assert float(rows[0]["worst_satisfaction_single"]) < 1.0
    assert float(rows[-1]["worst_satisfaction_single"]) >= 0.999
    for row in rows:
        assert float(row["worst_satisfaction_pairs"]) <= float(row["worst_satisfaction_single"]) + 1e-9
