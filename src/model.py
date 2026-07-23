import pulp


def solve(network):
    arcs = network["arc_cost"]
    hospitals = network["hospitals"]
    demand = network["demand"]

    prob = pulp.LpProblem("min_cost_flow", pulp.LpMinimize)
    flow = {a: pulp.LpVariable(f"x_{a[0]}_{a[1]}", lowBound=0) for a in arcs}
    unmet = {h: pulp.LpVariable(f"u_{h}", lowBound=0) for h in hospitals}

    shipping = pulp.lpSum(cost * flow[a] for a, cost in arcs.items())
    prob += shipping + network["penalty"] * pulp.lpSum(unmet.values())

    def inflow(node):
        return pulp.lpSum(flow[a] for a in arcs if a[1] == node)

    def outflow(node):
        return pulp.lpSum(flow[a] for a in arcs if a[0] == node)

    for s in network["suppliers"]:
        prob += outflow(s) <= network["capacity"][s]
    for n in network["factories"] + network["warehouses"]:
        prob += inflow(n) == outflow(n)
        prob += inflow(n) <= network["capacity"][n]
    for h in hospitals:
        prob += inflow(h) + unmet[h] == demand[h]

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    unmet_values = {h: unmet[h].value() for h in hospitals}
    total_unmet = sum(unmet_values.values())
    total_demand = sum(demand.values())

    return {
        "status": pulp.LpStatus[prob.status],
        "cost": pulp.value(prob.objective),
        "shipping_cost": pulp.value(shipping),
        "flows": {a: flow[a].value() for a in arcs},
        "unmet": unmet_values,
        "satisfaction": 1 - total_unmet / total_demand,
        "min_fill_rate": min(1 - unmet_values[h] / demand[h] for h in hospitals),
    }
