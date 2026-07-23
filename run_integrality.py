import csv
import sys
from pathlib import Path

from src.integrality import run_integrality_experiment

COUNT = 1000
SEED = 2026


def main(count=COUNT, seed=SEED, out_dir="results"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    with open(out / "integrality.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["gamma", "index", "status", "lp_spend", "ip_spend", "gap"])
        for gamma in [1, 2]:
            summary = run_integrality_experiment(count, seed, gamma)
            for row in summary["rows"]:
                writer.writerow([
                    gamma, row["index"], row["status"],
                    row["lp_spend"], row["ip_spend"], row["gap"],
                ])
            print(f"gamma={gamma}: {summary['instances']} instances, "
                  f"{summary['feasible']} feasible, "
                  f"{summary['gap_count']} with integrality gap, "
                  f"max gap {summary['max_gap']}")


if __name__ == "__main__":
    main(count=int(sys.argv[1]) if len(sys.argv) > 1 else COUNT)
