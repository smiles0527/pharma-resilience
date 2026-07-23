import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.ticker import PercentFormatter

INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SINGLE_COLOR = "#2a78d6"
PAIR_COLOR = "#1baf7a"
VARIANT_ORDER = ["capacity_x0.8", "cost_x0.8", "base", "cost_x1.2", "capacity_x1.2"]
VARIANT_COLORS = {
    "capacity_x0.8": "#86b6ef",
    "base": "#2a78d6",
    "capacity_x1.2": "#104281",
    "cost_x0.8": "#1baf7a",
    "cost_x1.2": "#eda100",
}
TIER_COLORS = {
    "suppliers": "#2a78d6",
    "factories": "#1baf7a",
    "warehouses": "#eda100",
    "hospitals": "#008300",
}
TIERS = ["suppliers", "factories", "warehouses", "hospitals"]


def _styled_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelsize=9)
    return fig, ax


def _line(ax, sweep, color, label):
    ax.plot(
        [row["spend"] for row in sweep],
        [row["worst_satisfaction"] for row in sweep],
        color=color,
        linewidth=2,
        marker="o",
        markersize=6,
        markeredgecolor="white",
        markeredgewidth=1.5,
        label=label,
        solid_joinstyle="round",
    )


def _end_label(ax, sweep, text):
    last = sweep[-1]
    ax.annotate(
        text,
        (last["spend"], last["worst_satisfaction"]),
        xytext=(8, 0),
        textcoords="offset points",
        fontsize=8.5,
        color=SECONDARY_INK,
        va="center",
    )


def tradeoff_plot(singles, pairs, path):
    fig, ax = _styled_axes((7.5, 4.5))
    ax.axhline(1.0, color=BASELINE, linewidth=1, zorder=1)
    _line(ax, singles, SINGLE_COLOR, "worst single failure")
    _line(ax, pairs, PAIR_COLOR, "worst pair failure")
    _end_label(ax, singles, "single")
    _end_label(ax, pairs, "pair")
    switch = next(
        (
            row
            for prev, row in zip(singles, singles[1:])
            if row["worst_scenario"] != prev["worst_scenario"]
        ),
        None,
    )
    if switch:
        ax.annotate(
            f"binding failure becomes {'+'.join(switch['worst_scenario'])}",
            (switch["spend"], switch["worst_satisfaction"]),
            xytext=(10, -28),
            textcoords="offset points",
            fontsize=8.5,
            color=SECONDARY_INK,
            arrowprops=dict(arrowstyle="-", color=BASELINE, linewidth=1),
        )
    ax.set_xlabel("Protection spend", fontsize=10.5, color=SECONDARY_INK)
    ax.set_ylabel("Worst-case demand satisfaction", fontsize=10.5, color=SECONDARY_INK)
    ax.set_title(
        "Worst-case satisfaction vs. protection spend",
        fontsize=12,
        color=INK,
        loc="left",
        pad=12,
    )
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    floor = min(
        row["worst_satisfaction"] for sweep in [singles, pairs] for row in sweep
    )
    ax.set_ylim(max(0.0, floor - 0.08), 1.06)
    ax.margins(x=0.1)
    ax.legend(frameon=False, fontsize=9, labelcolor=SECONDARY_INK, loc="center right")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def frontier_plot(uniform_sweep, frontier, path):
    fig, ax = _styled_axes((7.5, 4.5))
    ax.axhline(1.0, color=BASELINE, linewidth=1, zorder=1)
    _line(ax, uniform_sweep, SINGLE_COLOR, "uniform protection")
    ax.plot(
        [row["spend"] for row in frontier],
        [row["worst_satisfaction"] for row in frontier],
        color=PAIR_COLOR,
        linewidth=2,
        marker="o",
        markersize=6,
        markeredgecolor="white",
        markeredgewidth=1.5,
        label="optimized allocation (C&CG)",
        solid_joinstyle="round",
    )
    _end_label(ax, uniform_sweep, "uniform")
    last = frontier[-1]
    ax.annotate(
        "optimized",
        (last["spend"], last["worst_satisfaction"]),
        xytext=(8, -12),
        textcoords="offset points",
        fontsize=8.5,
        color=SECONDARY_INK,
        va="center",
    )
    ax.set_xlabel("Protection spend", fontsize=10.5, color=SECONDARY_INK)
    ax.set_ylabel("Worst-case demand satisfaction", fontsize=10.5, color=SECONDARY_INK)
    ax.set_title(
        "Uniform protection vs. optimized allocation",
        fontsize=12,
        color=INK,
        loc="left",
        pad=12,
    )
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    floor = min(
        [row["worst_satisfaction"] for row in uniform_sweep]
        + [row["worst_satisfaction"] for row in frontier]
    )
    ax.set_ylim(max(0.0, floor - 0.08), 1.06)
    ax.margins(x=0.1)
    ax.legend(frameon=False, fontsize=9, labelcolor=SECONDARY_INK, loc="lower right")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def coinciding_variants(variants):
    base_curve = [row["worst_satisfaction"] for row in variants["base"]]
    return [
        name
        for name, sweep in variants.items()
        if name != "base"
        and [row["worst_satisfaction"] for row in sweep] == base_curve
    ]


def sensitivity_plot(variants, path):
    fig, ax = _styled_axes((7.5, 4.5))
    coinciding = coinciding_variants(variants)
    ordered = sorted(
        variants,
        key=lambda name: VARIANT_ORDER.index(name) if name in VARIANT_ORDER else 99,
    )
    for name in ordered:
        if name in coinciding:
            continue
        label = name.replace("capacity_x", "capacity ×").replace("cost_x", "cost ×")
        if name == "base" and coinciding:
            folded = ", ".join(
                n.replace("capacity_x", "capacity ×").replace("cost_x", "cost ×")
                for n in coinciding
            )
            label = f"base ({folded} coincide)"
        _line(ax, variants[name], VARIANT_COLORS.get(name, MUTED), label)
    ax.set_xlabel("Protection spend", fontsize=10.5, color=SECONDARY_INK)
    ax.set_ylabel("Worst-case demand satisfaction", fontsize=10.5, color=SECONDARY_INK)
    ax.set_title(
        "Sensitivity of the trade-off curve",
        fontsize=12,
        color=INK,
        loc="left",
        pad=12,
    )
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    ax.legend(frameon=False, fontsize=9, labelcolor=SECONDARY_INK, loc="lower right")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def _node_positions(network):
    positions = {}
    for col, tier in enumerate(TIERS):
        nodes = network[tier]
        step = 1.2 if len(nodes) == 3 else 1.0
        top = 1.2 + (len(nodes) - 1) * step / 2
        for i, node in enumerate(nodes):
            positions[node] = (col * 1.6, top - i * step)
    return positions


def network_diagram(network, path):
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")
    positions = _node_positions(network)
    for (src, dst), cost in network["arc_cost"].items():
        (x0, y0), (x1, y1) = positions[src], positions[dst]
        ax.plot(
            [x0 + 0.33, x1 - 0.33],
            [y0, y1],
            color=BASELINE,
            linewidth=1.2,
            zorder=1,
        )
        t = 0.5 if y0 == y1 else (0.3 if y1 < y0 else 0.7)
        ax.text(
            x0 + 0.33 + t * (x1 - x0 - 0.66),
            y0 + t * (y1 - y0),
            str(cost),
            fontsize=7.5,
            color=MUTED,
            ha="center",
            va="center",
            zorder=2,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"),
        )
    tier_of = {node: tier for tier in TIERS for node in network[tier]}
    for node, (x, y) in positions.items():
        hue = TIER_COLORS[tier_of[node]]
        value = network["demand"].get(node, network["capacity"].get(node))
        ax.text(
            x,
            y,
            f"{node}\n{value}",
            fontsize=9,
            color=INK,
            ha="center",
            va="center",
            linespacing=1.5,
            zorder=3,
            bbox=dict(
                boxstyle="round,pad=0.45",
                facecolor=to_rgba(hue, 0.14),
                edgecolor=hue,
                linewidth=1.4,
            ),
        )
    headers = {
        "suppliers": "Suppliers\n(capacity)",
        "factories": "Factories\n(capacity)",
        "warehouses": "Warehouses\n(capacity)",
        "hospitals": "Hospitals\n(demand)",
    }
    for col, tier in enumerate(TIERS):
        ax.text(
            col * 1.6,
            3.6,
            headers[tier],
            fontsize=10,
            color=SECONDARY_INK,
            ha="center",
            va="center",
            linespacing=1.4,
        )
    ax.text(
        2.4,
        -1.15,
        "arc labels: unit shipping cost",
        fontsize=8.5,
        color=MUTED,
        ha="center",
    )
    ax.set_xlim(-0.6, 5.4)
    ax.set_ylim(-1.4, 4.1)
    ax.set_title(
        "Supply chain network",
        fontsize=12,
        color=INK,
        loc="left",
        pad=6,
    )
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
