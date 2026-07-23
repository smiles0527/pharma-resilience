import random

from src.generator import random_layered_network
from src.robust import min_spend_plan
from src.scenarios import pair_failures, single_node_failures


def integrality_gap(network, scenarios, target):
    lp = min_spend_plan(network, scenarios, target)
    if lp["status"] != "Optimal":
        return {"status": lp["status"], "lp_spend": None, "ip_spend": None, "gap": None}
    ip = min_spend_plan(network, scenarios, target, integer=True)
    return {
        "status": "Optimal",
        "lp_spend": lp["spend"],
        "ip_spend": ip["spend"],
        "gap": ip["spend"] - lp["spend"],
    }


def run_integrality_experiment(count, seed, gamma):
    rng = random.Random(seed)
    rows = []
    for index in range(count):
        network = random_layered_network(rng)
        scenarios = (
            single_node_failures(network) if gamma == 1 else pair_failures(network)
        )
        result = integrality_gap(network, scenarios, 1.0)
        rows.append({"index": index, **result})
    feasible = [row for row in rows if row["status"] == "Optimal"]
    gaps = [row["gap"] for row in feasible if row["gap"] > 1e-6]
    return {
        "instances": count,
        "feasible": len(feasible),
        "rows": rows,
        "gap_count": len(gaps),
        "max_gap": max(gaps, default=0.0),
    }
