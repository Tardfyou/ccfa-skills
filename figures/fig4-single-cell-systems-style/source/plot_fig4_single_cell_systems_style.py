#!/usr/bin/env python3
"""Create Fig. 4: MLCommons Inference v5.1 benchmark landscape.

The figure is derived only from the audited CSV in ../data. No numeric values are
invented; panels use pivots, counts, and tokens/s per accelerator computed from
the provided columns.
"""

from __future__ import annotations

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Patch, Rectangle
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "mlcommons_inference_v5_1_public_summary_audited.csv"
STYLE_PATH = Path(__file__).resolve().with_name("ccfa_matplotlib.mplstyle")
EXPORT_DIR = ROOT / "exports"

SCENARIO_ORDER = ["Offline", "Server", "Interactive"]
EXACT_MODEL_ORDER = [
    "deepseek-r1",
    "llama3.1-8b",
    "llama2-70b-99",
    "llama2-70b-99.9",
]
EXACT_MODEL_LABELS = {
    "deepseek-r1": "DeepSeek-R1",
    "llama3.1-8b": "Llama 3.1 8B",
    "llama2-70b-99": "Llama 2 70B 99",
    "llama2-70b-99.9": "Llama 2 70B 99.9",
}
FAMILY_ORDER = ["DeepSeek-R1", "Llama 3.1 8B", "Llama 2 70B"]
FAMILY_COLORS = {
    "DeepSeek-R1": "#0072B2",
    "Llama 3.1 8B": "#009E73",
    "Llama 2 70B": "#E69F00",
}
EXACT_MARKERS = {
    "deepseek-r1": "o",
    "llama3.1-8b": "s",
    "llama2-70b-99": "^",
    "llama2-70b-99.9": "D",
}
EXACT_LINESTYLES = {
    "deepseek-r1": "-",
    "llama3.1-8b": "--",
    "llama2-70b-99": "-.",
    "llama2-70b-99.9": ":",
}
FAMILY_HATCHES = {
    "DeepSeek-R1": "",
    "Llama 3.1 8B": "///",
    "Llama 2 70B": "\\\\\\",
}


def model_family(model: str) -> str:
    if model.startswith("deepseek-r1"):
        return "DeepSeek-R1"
    if model.startswith("llama3.1-8b"):
        return "Llama 3.1 8B"
    if model.startswith("llama2-70b"):
        return "Llama 2 70B"
    raise ValueError(f"Unknown model family for {model!r}")


def fmt_k(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    value = float(value)
    if value >= 1000:
        return f"{value / 1000:.0f}k"
    return f"{value:.0f}"


def fmt_axis_k(value: float, _pos: int) -> str:
    if value == 0:
        return "0"
    return f"{value / 1000:.0f}k"


def wrap_system_label(label: str) -> str:
    parts = label.split("-")
    if len(parts) >= 3:
        submitter = parts[0]
        model = parts[1]
        hardware = parts[-1]
        short = f"{submitter} {model} {hardware}"
    else:
        short = label
    return textwrap.shorten(short.replace("_", " "), width=34, placeholder="")


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    required = {
        "system",
        "submitter",
        "model",
        "scenario",
        "tokens_s",
        "accelerators",
        "availability",
        "id",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required CSV columns: {sorted(missing)}")
    if df["tokens_s"].isna().any() or df["accelerators"].isna().any():
        raise ValueError("tokens_s and accelerators must be complete in the audited CSV.")
    duplicated = df.duplicated(["system", "model", "scenario"])
    if duplicated.any():
        rows = df.loc[duplicated, ["system", "model", "scenario"]]
        raise ValueError(f"Duplicate system/model/scenario rows found:\n{rows}")

    df = df.copy()
    df["model_family"] = df["model"].map(model_family)
    df["tokens_per_accel"] = df["tokens_s"] / df["accelerators"]
    return df


def plot_heatmap(ax: plt.Axes, df: pd.DataFrame) -> None:
    pivot = (
        df.pivot_table(index=["system", "model", "model_family"], columns="scenario", values="tokens_s", aggfunc="first")
        .reindex(columns=SCENARIO_ORDER)
        .reset_index()
    )
    offline_sort = pivot["Offline"].fillna(-np.inf)
    server_sort = pivot["Server"].fillna(-np.inf)
    pivot = pivot.assign(_offline_sort=offline_sort, _server_sort=server_sort)
    pivot = pivot.sort_values(["_offline_sort", "_server_sort", "system"], ascending=[False, False, True])
    values = pivot[SCENARIO_ORDER].to_numpy(dtype=float)
    masked = np.ma.masked_invalid(values)

    cmap = LinearSegmentedColormap.from_list(
        "tokens_sequential",
        ["#F7F7F7", "#D8E7EF", "#9CC9DE", "#4D94B7", "#005A7D"],
    )
    cmap.set_bad("#F0F0F0")
    norm = Normalize(vmin=float(np.nanmin(values)), vmax=float(np.nanmax(values)))
    for y in range(masked.shape[0]):
        for x in range(masked.shape[1]):
            if masked.mask[y, x]:
                facecolor = "#F0F0F0"
            else:
                facecolor = cmap(norm(float(masked[y, x])))
            ax.add_patch(
                Rectangle(
                    (x - 0.5, y - 0.5),
                    1.0,
                    1.0,
                    facecolor=facecolor,
                    edgecolor="white",
                    linewidth=0.55,
                )
            )

    ax.set_xticks(np.arange(len(SCENARIO_ORDER)))
    ax.set_xticklabels(SCENARIO_ORDER, fontsize=7.2)
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", length=0, pad=7)
    ax.set_yticks(np.arange(len(pivot)))
    ax.set_yticklabels([wrap_system_label(s) for s in pivot["system"]], fontsize=6.1)
    ax.tick_params(axis="y", length=0, pad=2)

    for y, (_, row) in enumerate(pivot.iterrows()):
        family = row["model_family"]
        ax.add_patch(
            Rectangle(
                (-0.74, y - 0.42),
                0.13,
                0.84,
                facecolor=FAMILY_COLORS[family],
                edgecolor="none",
                clip_on=False,
                alpha=0.95,
            )
        )
        for x, scenario in enumerate(SCENARIO_ORDER):
            value = row[scenario]
            if pd.isna(value):
                ax.text(x, y, "n/a", ha="center", va="center", fontsize=6.2, color="#777777")
                continue
            text_color = "white" if norm(value) > 0.62 else "#111111"
            ax.text(x, y, fmt_k(value), ha="center", va="center", fontsize=6.2, color=text_color)

    ax.set_xlim(-0.78, len(SCENARIO_ORDER) - 0.5)
    ax.set_ylim(len(pivot) - 0.5, -0.5)
    ax.set_title("a  Throughput by system and inference scenario (tokens/s)", loc="left", fontsize=8.0, pad=24)

    ax.set_xticks(np.arange(-0.5, len(SCENARIO_ORDER), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(pivot), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=0.55)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    mappable = ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    cbar = plt.colorbar(mappable, ax=ax, fraction=0.035, pad=0.012)
    cbar.ax.tick_params(labelsize=6.8, length=2)
    cbar.ax.yaxis.set_major_formatter(FuncFormatter(fmt_axis_k))


def plot_pareto(ax: plt.Axes, df: pd.DataFrame) -> None:
    paired = df.pivot_table(
        index=["system", "model", "model_family", "accelerators"],
        columns="scenario",
        values="tokens_s",
        aggfunc="first",
    ).reset_index()
    paired = paired.dropna(subset=["Offline", "Server"])
    paired = paired.sort_values("Offline", ascending=False)

    for model in EXACT_MODEL_ORDER:
        sub = paired[paired["model"] == model]
        if sub.empty:
            continue
        family = model_family(model)
        ax.scatter(
            sub["Offline"],
            sub["Server"],
            s=20 + sub["accelerators"] * 4.6,
            marker=EXACT_MARKERS[model],
            facecolor=FAMILY_COLORS[family],
            edgecolor="#222222",
            linewidth=0.45,
            alpha=0.78,
            label=EXACT_MODEL_LABELS[model],
        )

    limit = max(float(paired["Offline"].max()), float(paired["Server"].max())) * 1.15
    ax.plot([0, limit], [0, limit], color="#8A8A8A", linestyle="--", linewidth=0.8, zorder=0)
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.xaxis.set_major_formatter(FuncFormatter(fmt_axis_k))
    ax.yaxis.set_major_formatter(FuncFormatter(fmt_axis_k))
    ax.xaxis.set_major_locator(MaxNLocator(4))
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.grid(True, color="#E6E6E6", linewidth=0.45)
    ax.set_xlabel("Offline tokens/s")
    ax.set_ylabel("Server tokens/s")
    ax.set_title("b  Offline-Server Pareto surface", loc="left", fontsize=8.2, pad=4)

    handles = [
        plt.scatter([], [], s=20 + n * 4.6, facecolor="#CFCFCF", edgecolor="#222222", linewidth=0.45)
        for n in [8, 32, 72]
    ]
    leg = ax.legend(handles, ["8", "32", "72"], title="accelerators", loc="upper left", fontsize=6.2, title_fontsize=6.4)
    leg._legend_box.align = "left"
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_ecdf(ax: plt.Axes, df: pd.DataFrame) -> None:
    offline = df[df["scenario"] == "Offline"].copy()
    for model in EXACT_MODEL_ORDER:
        sub = offline[offline["model"] == model].sort_values("tokens_per_accel")
        if sub.empty:
            continue
        x = sub["tokens_per_accel"].to_numpy(dtype=float)
        y = np.arange(1, len(x) + 1) / len(x)
        family = model_family(model)
        ax.step(
            x,
            y,
            where="post",
            color=FAMILY_COLORS[family],
            linestyle=EXACT_LINESTYLES[model],
            linewidth=1.35,
        )
        ax.scatter(
            x,
            y,
            marker=EXACT_MARKERS[model],
            s=15,
            facecolor=FAMILY_COLORS[family],
            edgecolor="white",
            linewidth=0.35,
            zorder=3,
            label=EXACT_MODEL_LABELS[model],
        )

    ax.set_xlim(0, offline["tokens_per_accel"].max() * 1.22)
    ax.set_ylim(0, 1.04)
    ax.xaxis.set_major_formatter(FuncFormatter(fmt_axis_k))
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.grid(True, color="#E6E6E6", linewidth=0.45)
    ax.set_xlabel("Offline tokens/s per accelerator")
    ax.set_title("c  Per-accelerator distribution", loc="left", fontsize=8.2, pad=4)
    ax.legend(loc="lower right", frameon=False, fontsize=6.1, handlelength=1.5, handletextpad=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_composition(ax: plt.Axes, df: pd.DataFrame) -> None:
    counts = (
        df.assign(scenario=pd.Categorical(df["scenario"], categories=SCENARIO_ORDER, ordered=True))
        .groupby(["scenario", "model_family"], observed=False)
        .size()
        .unstack(fill_value=0)
        .reindex(index=SCENARIO_ORDER, columns=FAMILY_ORDER, fill_value=0)
    )
    y = np.arange(len(counts))
    left = np.zeros(len(counts))
    for family in FAMILY_ORDER:
        values = counts[family].to_numpy()
        ax.barh(
            y,
            values,
            left=left,
            height=0.56,
            color=FAMILY_COLORS[family],
            edgecolor="#222222",
            linewidth=0.35,
            hatch=FAMILY_HATCHES[family],
            label=family,
        )
        for yi, x0, value in zip(y, left, values):
            if value > 0:
                ax.text(x0 + value / 2, yi, str(int(value)), ha="center", va="center", fontsize=6.4, color="#111111")
        left += values

    ax.set_yticks(y)
    ax.set_yticklabels(counts.index.tolist())
    ax.invert_yaxis()
    ax.set_xlabel("submission rows")
    ax.set_title("d  Scenario composition", loc="left", fontsize=8.2, pad=4)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, axis="x", color="#E6E6E6", linewidth=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def add_shared_legend(fig: plt.Figure) -> None:
    family_handles = [
        Patch(facecolor=FAMILY_COLORS[family], edgecolor="#222222", hatch=FAMILY_HATCHES[family], label=family)
        for family in FAMILY_ORDER
    ]
    fig.legend(
        handles=family_handles,
        loc="upper center",
        bbox_to_anchor=(0.59, 0.993),
        ncol=3,
        frameon=False,
        fontsize=6.4,
        handlelength=1.8,
        columnspacing=1.25,
        handletextpad=0.35,
    )


def make_figure() -> plt.Figure:
    if STYLE_PATH.exists():
        plt.style.use(STYLE_PATH)
    plt.rcParams.update(
        {
            "figure.figsize": (7.16, 8.25),
            "font.size": 7.8,
            "axes.labelsize": 7.6,
            "xtick.labelsize": 6.8,
            "ytick.labelsize": 6.8,
            "legend.fontsize": 6.6,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    df = load_data()

    fig = plt.figure(figsize=(7.16, 8.25), constrained_layout=False)
    grid = fig.add_gridspec(
        nrows=2,
        ncols=1,
        height_ratios=[5.28, 2.22],
        hspace=0.38,
        left=0.245,
        right=0.985,
        top=0.895,
        bottom=0.075,
    )
    ax_a = fig.add_subplot(grid[0, 0])
    bottom = grid[1, 0].subgridspec(1, 3, width_ratios=[1.2, 1.18, 0.96], wspace=0.46)
    ax_b = fig.add_subplot(bottom[0, 0])
    ax_c = fig.add_subplot(bottom[0, 1])
    ax_d = fig.add_subplot(bottom[0, 2])

    plot_heatmap(ax_a, df)
    plot_pareto(ax_b, df)
    plot_ecdf(ax_c, df)
    plot_composition(ax_d, df)
    add_shared_legend(fig)
    return fig


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    fig = make_figure()
    for suffix in ["pdf", "svg", "png"]:
        path = EXPORT_DIR / f"fig4_single_cell_systems_style.{suffix}"
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.025}
        if suffix == "png":
            kwargs["dpi"] = 600
        fig.savefig(path, **kwargs)
        print(f"wrote {path.relative_to(ROOT)}")
    plt.close(fig)


if __name__ == "__main__":
    main()
