import csv
import random
import sys
import time
from pathlib import Path

from src.experiment import evaluate_scenarios, worst_case
from src.generator import random_layered_network
from src.model import solve
from src.robust import ccg_plan, min_spend_plan
from src.scenarios import pair_failures, single_node_failures

SIZES = (10, 10, 10, 12)
SEED = 2026


def main(sizes=SIZES, seed=SEED, include_pairs=False, out_dir="results"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    net = random_layered_network(random.Random(seed), sizes)
    scenarios = single_node_failures(net)
    base = solve(net)
    rows = evaluate_scenarios(net, scenarios)
    worst = worst_case(rows)

    start = time.perf_counter()
    full = min_spend_plan(net, scenarios, 1.0)
    full_seconds = time.perf_counter() - start

    start = time.perf_counter()
    iterative = ccg_plan(net, scenarios, 1.0)
    ccg_seconds = time.perf_counter() - start

    pair_worst = None
    if include_pairs:
        pair_worst = worst_case(evaluate_scenarios(net, pair_failures(net)))

    with open(out / "scaled.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["failed", "satisfaction", "min_fill_rate", "recovery_cost"])
        for row in rows:
            writer.writerow([
                "+".join(row["failed"]), row["satisfaction"],
                row["min_fill_rate"], row["recovery_cost"],
            ])

    summary = {
        "sizes": tuple(sizes),
        "seed": seed,
        "nodes": sum(len(net[t]) for t in ["suppliers", "factories", "warehouses", "hospitals"]),
        "arcs": len(net["arc_cost"]),
        "scenarios": len(scenarios),
        "baseline_satisfaction": base["satisfaction"],
        "worst_scenario": worst["failed"],
        "worst_satisfaction": worst["satisfaction"],
        "full_spend": full["spend"],
        "full_seconds": full_seconds,
        "ccg_spend": iterative["spend"],
        "ccg_iterations": iterative["iterations"],
        "ccg_seconds": ccg_seconds,
        "pair_worst_satisfaction": pair_worst["satisfaction"] if pair_worst else None,
    }

    print(f"network {summary['sizes']} seed {seed}: "
          f"{summary['nodes']} nodes, {summary['arcs']} arcs, "
          f"{summary['scenarios']} single-failure scenarios")
    print(f"baseline satisfaction {summary['baseline_satisfaction']:.3f}, "
          f"worst failure {'+'.join(summary['worst_scenario'])} "
          f"-> {summary['worst_satisfaction']:.3f}")
    print(f"full LP: spend {summary['full_spend']:.1f} in {full_seconds:.2f}s")
    print(f"C&CG:    spend {summary['ccg_spend']:.1f} in {ccg_seconds:.2f}s "
          f"({summary['ccg_iterations']} iterations)")
    if pair_worst:
        print(f"worst pair failure -> {pair_worst['satisfaction']:.3f}")
    print(f"outputs written to {out}/")
    return summary


if __name__ == "__main__":
    positional = [a for a in sys.argv[1:] if a != "--pairs"]
    chosen_sizes = tuple(int(a) for a in positional[:4]) if len(positional) >= 4 else SIZES
    chosen_seed = int(positional[4]) if len(positional) > 4 else SEED
    main(chosen_sizes, chosen_seed, include_pairs="--pairs" in sys.argv)
