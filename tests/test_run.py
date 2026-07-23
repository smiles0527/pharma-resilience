import csv

from run import LEVELS, main


def read_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def test_main_writes_all_outputs(tmp_path):
    main(out_dir=tmp_path)
    names = [
        "sweep.csv", "sensitivity.csv", "frontier.csv", "plans.csv", "paradox.csv",
        "tradeoff.png", "sensitivity.png", "frontier.png", "network.png",
    ]
    for name in names:
        assert (tmp_path / name).exists(), f"missing {name}"

    rows = read_rows(tmp_path / "sweep.csv")
    assert len(rows) == len(LEVELS)
    assert float(rows[0]["worst_satisfaction_single"]) < 1.0
    assert float(rows[-1]["worst_satisfaction_single"]) >= 0.999
    for row in rows:
        assert float(row["worst_satisfaction_pairs"]) <= float(row["worst_satisfaction_single"]) + 1e-9

    frontier = read_rows(tmp_path / "frontier.csv")
    assert float(frontier[-1]["worst_satisfaction"]) >= 0.999
    assert float(frontier[-1]["spend"]) < 330.0

    plans = read_rows(tmp_path / "plans.csv")
    assert len(plans) == 9
    for row in plans:
        assert (
            float(row["satisfaction_robust"])
            >= float(row["satisfaction_normal"]) - 1e-9
        )

    paradox = {row["plan"]: row for row in read_rows(tmp_path / "paradox.csv")}
    assert (
        float(paradox["protected"]["satisfaction"])
        > float(paradox["unprotected"]["satisfaction"])
    )
    assert (
        float(paradox["protected"]["min_fill_rate"])
        < float(paradox["unprotected"]["min_fill_rate"])
    )
