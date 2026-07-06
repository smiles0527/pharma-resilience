import csv
from pathlib import Path

from src.experiment import protection_sweep
from src.network import base_network
from src.plots import network_diagram, sensitivity_plot, tradeoff_plot
from src.scenarios import pair_failures, single_node_failures
from src.sensitivity import run_sensitivity

LEVELS = [round(i * 0.05, 2) for i in range(11)]


def main(out_dir="results"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    net = base_network()

    singles = protection_sweep(net, LEVELS, single_node_failures(net))
    pairs = protection_sweep(net, LEVELS, pair_failures(net))
    sensitivity = run_sensitivity(net, LEVELS, single_node_failures(net))

    with open(out / "sweep.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "level", "spend",
            "worst_satisfaction_single", "worst_scenario_single", "max_recovery_cost_single",
            "worst_satisfaction_pairs", "worst_scenario_pairs",
        ])
        for single_row, pair_row in zip(singles, pairs):
            writer.writerow([
                single_row["level"], single_row["spend"],
                single_row["worst_satisfaction"], "+".join(single_row["worst_scenario"]),
                single_row["max_recovery_cost"],
                pair_row["worst_satisfaction"], "+".join(pair_row["worst_scenario"]),
            ])

    with open(out / "sensitivity.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["variant", "level", "spend", "worst_satisfaction"])
        for variant, sweep in sensitivity.items():
            for row in sweep:
                writer.writerow([variant, row["level"], row["spend"], row["worst_satisfaction"]])

    tradeoff_plot(singles, pairs, out / "tradeoff.png")
    sensitivity_plot(sensitivity, out / "sensitivity.png")
    network_diagram(net, out / "network.png")

    unprotected = singles[0]
    fully_protected_level = next(
        (row["level"] for row in singles if row["worst_satisfaction"] >= 0.999), None
    )
    print(f"worst scenario at p=0: {unprotected['worst_scenario']} "
          f"(satisfaction {unprotected['worst_satisfaction']:.3f})")
    print(f"worst case fully protected from level: {fully_protected_level}")
    print(f"outputs written to {out}/")


if __name__ == "__main__":
    main()
