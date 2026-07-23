TIER_NAMES = ["S", "F", "W", "H"]


def random_layered_network(rng):
    sizes = [rng.randint(3, 4), rng.randint(3, 4), rng.randint(3, 4), rng.randint(2, 4)]
    tiers = [
        [f"{prefix}{i + 1}" for i in range(size)]
        for prefix, size in zip(TIER_NAMES, sizes)
    ]
    suppliers, factories, warehouses, hospitals = tiers

    capacity = {}
    for node in suppliers + factories + warehouses:
        capacity[node] = rng.randint(20, 100)
    demand = {h: rng.randint(10, 60) for h in hospitals}

    arc_cost = {}
    for upstream, downstream in zip(tiers[:-1], tiers[1:]):
        for src in upstream:
            degree = rng.randint(2, len(downstream))
            for dst in rng.sample(downstream, degree):
                arc_cost[(src, dst)] = rng.randint(1, 5)
        for dst in downstream:
            have = [s for s in upstream if (s, dst) in arc_cost]
            candidates = [s for s in upstream if (s, dst) not in arc_cost]
            while len(have) < min(2, len(upstream)) and candidates:
                src = candidates.pop(rng.randrange(len(candidates)))
                arc_cost[(src, dst)] = rng.randint(1, 5)
                have.append(src)

    return {
        "suppliers": suppliers,
        "factories": factories,
        "warehouses": warehouses,
        "hospitals": hospitals,
        "capacity": capacity,
        "demand": demand,
        "arc_cost": arc_cost,
        "penalty": 1000,
        "protection_cost_rate": 1.0,
    }
