SUPPLIERS = ["S1", "S2", "S3"]
FACTORIES = ["F1", "F2", "F3"]
WAREHOUSES = ["W1", "W2", "W3"]
HOSPITALS = ["H1", "H2", "H3", "H4"]

CAPACITY = {
    "S1": 80, "S2": 70, "S3": 60,
    "F1": 90, "F2": 80, "F3": 60,
    "W1": 85, "W2": 75, "W3": 60,
}

DEMAND = {"H1": 60, "H2": 50, "H3": 40, "H4": 30}

ARC_COST = {
    ("S1", "F1"): 2, ("S1", "F2"): 3,
    ("S2", "F2"): 2, ("S2", "F3"): 4,
    ("S3", "F1"): 3, ("S3", "F3"): 2,
    ("F1", "W1"): 2, ("F1", "W2"): 4,
    ("F2", "W2"): 2, ("F2", "W3"): 3,
    ("F3", "W1"): 3, ("F3", "W3"): 2,
    ("W1", "H1"): 1, ("W1", "H2"): 2, ("W1", "H4"): 3,
    ("W2", "H1"): 3, ("W2", "H2"): 1, ("W2", "H3"): 2,
    ("W3", "H3"): 2, ("W3", "H4"): 1,
}

SHORTAGE_PENALTY = 1000
PROTECTION_COST_RATE = 1.0


def base_network():
    return {
        "suppliers": list(SUPPLIERS),
        "factories": list(FACTORIES),
        "warehouses": list(WAREHOUSES),
        "hospitals": list(HOSPITALS),
        "capacity": dict(CAPACITY),
        "demand": dict(DEMAND),
        "arc_cost": dict(ARC_COST),
        "penalty": SHORTAGE_PENALTY,
        "protection_cost_rate": PROTECTION_COST_RATE,
    }
