from copy import deepcopy

from src.model import solve


def fail_nodes(network, nodes):
    failed = deepcopy(network)
    for node in nodes:
        failed["capacity"][node] = 0
    return failed


def apply_protection(network, level):
    protected = deepcopy(network)
    for node in protected["capacity"]:
        protected["capacity"][node] = network["capacity"][node] * (1 + level)
    return protected


def protection_spend(network, level):
    return network["protection_cost_rate"] * level * sum(network["capacity"].values())


def evaluate_scenarios(network, scenarios):
    intact_cost = solve(network)["cost"]
    rows = []
    for nodes in scenarios:
        result = solve(fail_nodes(network, nodes))
        rows.append({
            "failed": nodes,
            "satisfaction": result["satisfaction"],
            "min_fill_rate": result["min_fill_rate"],
            "cost": result["cost"],
            "recovery_cost": result["cost"] - intact_cost,
        })
    return rows


def worst_case(rows):
    return min(rows, key=lambda row: row["satisfaction"])


def protection_sweep(base, levels, scenarios):
    sweep = []
    for level in levels:
        protected = apply_protection(base, level)
        rows = evaluate_scenarios(protected, scenarios)
        worst = worst_case(rows)
        sweep.append({
            "level": level,
            "spend": protection_spend(base, level),
            "worst_satisfaction": worst["satisfaction"],
            "worst_scenario": worst["failed"],
            "max_recovery_cost": max(row["recovery_cost"] for row in rows),
        })
    return sweep
