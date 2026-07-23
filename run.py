import csv
from pathlib import Path

from src.experiment import evaluate_scenarios, protection_sweep, worst_case
from src.model import solve
from src.network import base_network, equity_paradox_network
from src.plots import frontier_plot, network_diagram, sensitivity_plot, tradeoff_plot
from src.robust import apply_allocation, ccg_plan, min_spend_plan
from src.scenarios import pair_failures, single_node_failures
from src.sensitivity import run_sensitivity

LEVELS = [round(i * 0.05, 2) for i in range(11)]
TARGETS = [0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
PARADOX_TARGET = 0.55
PARADOX_SCENARIOS = [("W2",)]


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

    frontier = []
    for target in TARGETS:
        plan = ccg_plan(net, single_node_failures(net), target)
        protected = apply_allocation(net, plan["extra"])
        achieved = worst_case(evaluate_scenarios(protected, single_node_failures(net)))
        frontier.append({
            "target": target,
            "spend": plan["spend"],
            "iterations": plan["iterations"],
            "worst_satisfaction": achieved["satisfaction"],
        })

    with open(out / "frontier.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["target", "spend", "iterations", "worst_satisfaction"])
        for row in frontier:
            writer.writerow([
                row["target"], row["spend"], row["iterations"], row["worst_satisfaction"],
            ])

    robust_plan = ccg_plan(net, single_node_failures(net), 1.0)
    robust_net = apply_allocation(net, robust_plan["extra"])
    normal_rows = evaluate_scenarios(net, single_node_failures(net))
    robust_rows = evaluate_scenarios(robust_net, single_node_failures(net))

    with open(out / "plans.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "scenario",
            "cost_normal", "satisfaction_normal", "equity_normal", "recovery_cost_normal",
            "cost_robust", "satisfaction_robust", "equity_robust", "recovery_cost_robust",
        ])
        for normal, robust in zip(normal_rows, robust_rows):
            writer.writerow([
                "+".join(normal["failed"]),
                normal["cost"], normal["satisfaction"],
                normal["min_fill_rate"], normal["recovery_cost"],
                robust["cost"], robust["satisfaction"],
                robust["min_fill_rate"], robust["recovery_cost"],
            ])

    paradox_net = equity_paradox_network()
    paradox_plan = min_spend_plan(paradox_net, PARADOX_SCENARIOS, PARADOX_TARGET)
    paradox_rows = [
        ("unprotected", 0.0, solve(paradox_net)),
        ("protected", paradox_plan["spend"],
         solve(apply_allocation(paradox_net, paradox_plan["extra"]))),
    ]

    with open(out / "paradox.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["plan", "spend", "satisfaction", "min_fill_rate"])
        for name, spend, result in paradox_rows:
            writer.writerow([
                name, spend, result["satisfaction"], result["min_fill_rate"],
            ])

    tradeoff_plot(singles, pairs, out / "tradeoff.png")
    sensitivity_plot(sensitivity, out / "sensitivity.png")
    frontier_plot(singles, frontier, out / "frontier.png")
    network_diagram(net, out / "network.png")

    unprotected = singles[0]
    fully_protected_level = next(
        (row["level"] for row in singles if row["worst_satisfaction"] >= 0.999), None
    )
    print(f"worst scenario at p=0: {unprotected['worst_scenario']} "
          f"(satisfaction {unprotected['worst_satisfaction']:.3f})")
    print(f"worst case fully protected from level: {fully_protected_level}")
    print(f"optimized full protection: spend {robust_plan['spend']:.1f} "
          f"in {robust_plan['iterations']} C&CG iterations "
          f"(uniform needs {protection_spend_at_full(singles):.1f})")
    print(f"outputs written to {out}/")


def protection_spend_at_full(singles):
    return next(
        row["spend"] for row in singles if row["worst_satisfaction"] >= 0.999
    )


if __name__ == "__main__":
    main()
