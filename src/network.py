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


def equity_paradox_network():
    return {
        "suppliers": ["S"],
        "factories": ["F"],
        "warehouses": ["W1", "W2"],
        "hospitals": ["H1", "H2"],
        "capacity": {"S": 10, "F": 10, "W1": 4, "W2": 6},
        "demand": {"H1": 10, "H2": 10},
        "arc_cost": {
            ("S", "F"): 1,
            ("F", "W1"): 1, ("F", "W2"): 1,
            ("W1", "H1"): 1, ("W1", "H2"): 3,
            ("W2", "H2"): 5,
        },
        "penalty": SHORTAGE_PENALTY,
        "protection_cost_rate": PROTECTION_COST_RATE,
    }


def integrality_gap_network():
    return {
        "suppliers": ["S1", "S2", "S3"],
        "factories": ["F1", "F2", "F3", "F4"],
        "warehouses": ["W1", "W2", "W3", "W4"],
        "hospitals": ["H1", "H2", "H3", "H4"],
        "capacity": {
            "S1": 27, "S2": 40, "S3": 36,
            "F1": 37, "F2": 81, "F3": 25, "F4": 86,
            "W1": 25, "W2": 91, "W3": 100, "W4": 69,
        },
        "demand": {"H1": 21, "H2": 32, "H3": 47, "H4": 15},
        "arc_cost": {
            ("S1", "F1"): 3, ("S1", "F2"): 2, ("S1", "F4"): 3,
            ("S2", "F2"): 4, ("S2", "F3"): 2, ("S2", "F4"): 5,
            ("S3", "F1"): 5, ("S3", "F3"): 2,
            ("F1", "W2"): 4, ("F1", "W3"): 5,
            ("F2", "W1"): 3, ("F2", "W3"): 3, ("F2", "W4"): 2,
            ("F3", "W1"): 1, ("F3", "W2"): 5, ("F3", "W3"): 1, ("F3", "W4"): 3,
            ("F4", "W3"): 5, ("F4", "W4"): 3,
            ("W1", "H1"): 1, ("W1", "H3"): 2, ("W1", "H4"): 3,
            ("W2", "H1"): 5, ("W2", "H2"): 3,
            ("W3", "H1"): 1, ("W3", "H2"): 3,
            ("W4", "H1"): 3, ("W4", "H3"): 1, ("W4", "H4"): 4,
        },
        "penalty": SHORTAGE_PENALTY,
        "protection_cost_rate": PROTECTION_COST_RATE,
    }


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
