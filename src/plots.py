import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def tradeoff_plot(sweep, path):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(
        [row["spend"] for row in sweep],
        [row["worst_satisfaction"] for row in sweep],
        marker="o",
    )
    ax.set_xlabel("Protection spend")
    ax.set_ylabel("Worst-case demand satisfaction")
    ax.set_title("The cost of resilience")
    ax.grid(True, alpha=0.3)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def sensitivity_plot(variants, path):
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, sweep in variants.items():
        ax.plot(
            [row["spend"] for row in sweep],
            [row["worst_satisfaction"] for row in sweep],
            marker="o",
            label=name,
        )
    ax.set_xlabel("Protection spend")
    ax.set_ylabel("Worst-case demand satisfaction")
    ax.set_title("Sensitivity of the trade-off curve")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
