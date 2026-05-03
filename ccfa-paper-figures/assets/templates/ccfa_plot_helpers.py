"""Reusable helpers for CCF-A data figures.

The helpers contain no example data. Use them with user-provided, audited public, or
permission-cleared paper data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


PALETTE = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "red": "#D55E00",
    "purple": "#CC79A7",
    "sky": "#56B4E9",
    "yellow": "#F0E442",
    "black": "#000000",
    "grey": "#777777",
}

DEFAULT_COLORS = [
    PALETTE["blue"],
    PALETTE["orange"],
    PALETTE["green"],
    PALETTE["red"],
    PALETTE["purple"],
    PALETTE["sky"],
    PALETTE["grey"],
]

MARKERS = ["o", "s", "^", "D", "v", "P", "X"]
LINESTYLES = ["-", "--", "-.", ":"]
HATCHES = ["", "//", "\\\\", "xx", "..", "++", "oo"]

SCHEMATIC_COMPONENT_STYLES = {
    "default": {"facecolor": "#EAF2FA", "edgecolor": "#2F4A60", "textcolor": "#111111"},
    "input": {"facecolor": "#F1F4F6", "edgecolor": "#6E7F89", "textcolor": "#111111"},
    "output": {"facecolor": "#F1F4F6", "edgecolor": "#6E7F89", "textcolor": "#111111"},
    "external": {"facecolor": "#FFFFFF", "edgecolor": "#777777", "textcolor": "#111111"},
    "runtime": {"facecolor": "#EAF2FA", "edgecolor": "#0072B2", "textcolor": "#111111"},
    "control": {"facecolor": "#FFF3D7", "edgecolor": "#B87900", "textcolor": "#111111"},
    "storage": {"facecolor": "#FFF8CC", "edgecolor": "#8A7A00", "textcolor": "#111111"},
    "model": {"facecolor": "#EDE7F3", "edgecolor": "#7E5A9B", "textcolor": "#111111"},
    "proposed": {"facecolor": "#DDEEF8", "edgecolor": "#0072B2", "textcolor": "#111111"},
    "baseline": {"facecolor": "#EFEFEF", "edgecolor": "#777777", "textcolor": "#111111"},
    "human": {"facecolor": "#F6E7F1", "edgecolor": "#A35683", "textcolor": "#111111"},
    "attacker": {"facecolor": "#FCE6DC", "edgecolor": "#D55E00", "textcolor": "#111111"},
    "defense": {"facecolor": "#E5F4EE", "edgecolor": "#009E73", "textcolor": "#111111"},
    "evidence": {"facecolor": "#F8F8F8", "edgecolor": "#777777", "textcolor": "#111111"},
}

SCHEMATIC_ARROW_STYLES = {
    "data": {"color": "#333333", "linestyle": "-", "linewidth": 1.0},
    "control": {"color": PALETTE["blue"], "linestyle": "--", "linewidth": 1.0},
    "attack": {"color": PALETTE["red"], "linestyle": "--", "linewidth": 1.1},
    "defense": {"color": PALETTE["green"], "linestyle": "-", "linewidth": 1.1},
    "feedback": {"color": PALETTE["purple"], "linestyle": ":", "linewidth": 1.1},
    "dependency": {"color": PALETTE["grey"], "linestyle": ":", "linewidth": 0.9},
}

SCHEMATIC_BOUNDARY_STYLES = {
    "process": {"edgecolor": PALETTE["grey"], "facecolor": "none", "linestyle": "--", "linewidth": 0.9},
    "runtime": {"edgecolor": PALETTE["blue"], "facecolor": "none", "linestyle": "--", "linewidth": 0.9},
    "deployment": {"edgecolor": PALETTE["grey"], "facecolor": "none", "linestyle": "-", "linewidth": 0.9},
    "trust": {"edgecolor": PALETTE["red"], "facecolor": "none", "linestyle": "--", "linewidth": 1.0},
    "data": {"edgecolor": PALETTE["green"], "facecolor": "none", "linestyle": "--", "linewidth": 0.9},
}


def apply_ccfa_style(style_file: str | Path | None = None, width: str = "single") -> None:
    """Apply the local CCF-A Matplotlib defaults."""
    if style_file:
        plt.style.use(style_file)
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    plt.rcParams["svg.fonttype"] = "none"
    if width == "double":
        plt.rcParams["figure.figsize"] = (7.16, 3.0)
    elif width == "square":
        plt.rcParams["figure.figsize"] = (3.5, 3.0)


def is_dark(hex_color: str, threshold: float = 0.5) -> bool:
    """Return True when white text is likely more readable on the color."""
    color = hex_color.lstrip("#")
    red = int(color[0:2], 16) / 255
    green = int(color[2:4], 16) / 255
    blue = int(color[4:6], 16) / 255
    return (0.299 * red + 0.587 * green + 0.114 * blue) < threshold


def add_panel_label(ax: plt.Axes, label: str, x: float = -0.12, y: float = 1.04) -> None:
    """Place a compact paper-style panel label."""
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontweight="bold",
    )


def add_direct_label(
    ax: plt.Axes,
    x: float,
    y: float,
    text: str,
    color: str = "black",
    **kwargs,
) -> None:
    """Add a direct label at data coordinates."""
    ax.text(x, y, text, color=color, ha=kwargs.pop("ha", "center"), va=kwargs.pop("va", "center"), **kwargs)


def _semantic_style(styles: dict[str, dict[str, object]], kind: str | None, **overrides) -> dict[str, object]:
    base = dict(styles.get("default", {}))
    if kind:
        base.update(styles.get(kind, {}))
    for key, value in overrides.items():
        if value is not None:
            base[key] = value
    return base


def schematic_component_style(kind: str | None = None, **overrides) -> dict[str, object]:
    """Return component colors for a semantic architecture role."""
    return _semantic_style(SCHEMATIC_COMPONENT_STYLES, kind, **overrides)


def schematic_arrow_style(kind: str | None = None, **overrides) -> dict[str, object]:
    """Return arrow styling for a semantic flow role."""
    return _semantic_style(SCHEMATIC_ARROW_STYLES, kind or "data", **overrides)


def schematic_boundary_style(kind: str | None = None, **overrides) -> dict[str, object]:
    """Return boundary styling for process, runtime, deployment, trust, or data regions."""
    return _semantic_style(SCHEMATIC_BOUNDARY_STYLES, kind or "process", **overrides)


def move_legend_outside(ax: plt.Axes, loc: str = "center left", anchor: tuple[float, float] = (1.02, 0.5)) -> None:
    """Move the legend outside the plotting area."""
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, loc=loc, bbox_to_anchor=anchor, borderaxespad=0.0)


def make_legend_axis(ax: plt.Axes, handles, labels) -> None:
    """Turn an axes into a legend-only panel."""
    ax.legend(handles, labels, loc="center", frameon=False)
    ax.set_axis_off()


def tighten_axis(ax: plt.Axes, values, axis: str = "y", margin_fraction: float = 0.10, include_zero: bool = False) -> None:
    """Tighten an axis to data range with a small margin."""
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return
    lo = float(np.min(arr))
    hi = float(np.max(arr))
    if include_zero:
        lo = min(lo, 0.0)
        hi = max(hi, 0.0)
    span = hi - lo
    margin = (span if span > 0 else max(abs(hi), 1.0)) * margin_fraction
    limits = (lo - margin, hi + margin)
    if axis == "x":
        ax.set_xlim(limits)
    else:
        ax.set_ylim(limits)


def polish_axes(ax: plt.Axes, xlabel: str | None = None, ylabel: str | None = None) -> None:
    """Apply final axis labels and remove nonessential spines."""
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def style_schematic_axis(
    ax: plt.Axes,
    xlim: tuple[float, float] = (0.0, 1.0),
    ylim: tuple[float, float] = (0.0, 1.0),
) -> None:
    """Prepare an axes for a white-background schematic or architecture panel."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)


def draw_component_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    label: str,
    facecolor: str = "#EAF2FA",
    edgecolor: str = "#2F4A60",
    textcolor: str = "#111111",
    radius: float = 0.012,
    linewidth: float = 0.9,
    fontsize: float | None = None,
) -> FancyBboxPatch:
    """Draw a semantic component box for schematic-led CS paper figures."""
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        label,
        ha="center",
        va="center",
        color=textcolor,
        fontsize=fontsize or plt.rcParams["font.size"],
        wrap=True,
    )
    return patch


def draw_boundary(
    ax: plt.Axes,
    xy: tuple[float, float],
    width: float,
    height: float,
    label: str | None = None,
    edgecolor: str = "#777777",
    facecolor: str = "none",
    linestyle: str = "--",
    linewidth: float = 0.9,
) -> Rectangle:
    """Draw a process, trust, runtime, or subsystem boundary."""
    patch = Rectangle(
        xy,
        width,
        height,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linestyle=linestyle,
        linewidth=linewidth,
    )
    ax.add_patch(patch)
    if label:
        ax.text(
            xy[0],
            xy[1] + height + 0.018,
            label,
            ha="left",
            va="bottom",
            color=edgecolor,
            fontsize=plt.rcParams["font.size"] * 0.85,
        )
    return patch


def draw_arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    label: str | None = None,
    color: str = "#333333",
    linewidth: float = 1.0,
    connectionstyle: str = "arc3,rad=0.0",
    linestyle: str = "-",
    arrowstyle: str = "-|>",
    mutation_scale: float = 11,
    alpha: float = 1.0,
) -> FancyArrowPatch:
    """Draw a semantic data, control, attack, or dependency flow arrow."""
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle=arrowstyle,
        mutation_scale=mutation_scale,
        linewidth=linewidth,
        color=color,
        linestyle=linestyle,
        connectionstyle=connectionstyle,
        shrinkA=2,
        shrinkB=2,
        alpha=alpha,
    )
    ax.add_patch(arrow)
    if label:
        ax.text(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2,
            label,
            ha="center",
            va="center",
            color=color,
            fontsize=plt.rcParams["font.size"] * 0.78,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.8, "alpha": 0.85},
        )
    return arrow


def draw_callout(
    ax: plt.Axes,
    xy: tuple[float, float],
    text_xy: tuple[float, float],
    text: str,
    color: str = "#D55E00",
    linewidth: float = 0.9,
) -> None:
    """Add a compact callout for one mechanism, failure mode, or evidence hook."""
    ax.annotate(
        text,
        xy=xy,
        xytext=text_xy,
        ha="center",
        va="center",
        color=color,
        fontsize=plt.rcParams["font.size"] * 0.82,
        arrowprops={
            "arrowstyle": "-|>",
            "lw": linewidth,
            "color": color,
            "shrinkA": 2,
            "shrinkB": 2,
        },
    )


def annotate_bar_containers(ax: plt.Axes, containers, fmt: str = "{:.2f}") -> None:
    """Annotate bars with luminance-aware text color."""
    for container in containers:
        for bar in container:
            height = bar.get_height()
            if not np.isfinite(height):
                continue
            face = bar.get_facecolor()
            luminance = 0.299 * face[0] + 0.587 * face[1] + 0.114 * face[2]
            color = "white" if luminance < 0.5 else "black"
            y_offset = 0.02 * (ax.get_ylim()[1] - ax.get_ylim()[0] or 1.0)
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + y_offset,
                fmt.format(height),
                ha="center",
                va="bottom",
                color=color,
                fontsize=plt.rcParams["font.size"] * 0.85,
            )


def plot_series(
    ax: plt.Axes,
    rows: dict[str, list[tuple[float, float, float | None]]],
    xlabel: str,
    ylabel: str,
) -> None:
    """Plot line/errorbar series from grouped numeric rows."""
    for index, (series, points) in enumerate(rows.items()):
        ordered = sorted(points)
        x_values = [item[0] for item in ordered]
        y_values = [item[1] for item in ordered]
        yerr_values = [item[2] for item in ordered]
        yerr = None if all(item is None for item in yerr_values) else [item or 0.0 for item in yerr_values]
        ax.errorbar(
            x_values,
            y_values,
            yerr=yerr,
            marker=MARKERS[index % len(MARKERS)],
            linestyle=LINESTYLES[index % len(LINESTYLES)],
            capsize=2,
            label=series,
        )
    polish_axes(ax, xlabel, ylabel)
    ax.legend(loc="best")


def plot_grouped_bar(
    ax: plt.Axes,
    rows: dict[str, list[tuple[str, float, float | None]]],
    xlabel: str,
    ylabel: str,
    annotate: bool = False,
) -> None:
    """Plot grouped categorical bars from series -> category/value rows."""
    categories = sorted({category for points in rows.values() for category, _, _ in points})
    x_positions = np.arange(len(categories), dtype=float)
    n_series = max(len(rows), 1)
    width = min(0.78 / n_series, 0.32)
    offsets = (np.arange(n_series) - (n_series - 1) / 2) * width
    category_index = {category: idx for idx, category in enumerate(categories)}
    containers = []
    for index, (series, points) in enumerate(rows.items()):
        values_by_category = {category: (value, err) for category, value, err in points}
        values = [values_by_category.get(category, (np.nan, None))[0] for category in categories]
        errors_raw = [values_by_category.get(category, (np.nan, None))[1] for category in categories]
        errors = None if all(err is None for err in errors_raw) else [err or 0.0 for err in errors_raw]
        bars = ax.bar(
            x_positions + offsets[index],
            values,
            width=width,
            yerr=errors,
            capsize=2,
            label=series,
            color=DEFAULT_COLORS[index % len(DEFAULT_COLORS)],
            edgecolor="black",
            linewidth=0.6,
        )
        containers.append(bars)
        hatch = HATCHES[index % len(HATCHES)]
        for bar in bars:
            bar.set_hatch(hatch)
        _ = category_index
    if annotate:
        tighten_axis(ax, [bar.get_height() for container in containers for bar in container], axis="y", include_zero=True)
        annotate_bar_containers(ax, containers)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(categories, rotation=25, ha="right")
    polish_axes(ax, xlabel, ylabel)
    ax.legend(loc="best")


def plot_dot_interval(
    ax: plt.Axes,
    rows: list[tuple[str, float, float, float, str]],
    xlabel: str,
    ylabel: str,
) -> None:
    """Plot dot/interval estimates such as per-project effects or confidence intervals."""
    labels = [row[0] for row in rows]
    y_positions = np.arange(len(rows))[::-1]
    groups = {
        group: DEFAULT_COLORS[idx % len(DEFAULT_COLORS)]
        for idx, group in enumerate(sorted({row[4] for row in rows}))
    }
    for y_pos, (label, estimate, low, high, group) in zip(y_positions, rows):
        color = groups[group]
        ax.plot([low, high], [y_pos, y_pos], color=color, linewidth=1.3)
        ax.plot(estimate, y_pos, marker="o", color=color, markersize=4.0, label=group)
    handles, labels_seen = ax.get_legend_handles_labels()
    unique = dict(zip(labels_seen, handles))
    if len(unique) > 1:
        ax.legend(unique.values(), unique.keys(), loc="best")
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)
    polish_axes(ax, xlabel, ylabel)


def plot_ecdf(ax: plt.Axes, rows: dict[str, list[float]], xlabel: str, ylabel: str) -> None:
    """Plot empirical CDF curves from value lists."""
    for index, (series, values) in enumerate(rows.items()):
        ordered = np.sort(np.asarray(values, dtype=float))
        if ordered.size == 0:
            continue
        y_values = np.arange(1, ordered.size + 1) / ordered.size
        ax.step(
            ordered,
            y_values,
            where="post",
            label=series,
            color=DEFAULT_COLORS[index % len(DEFAULT_COLORS)],
            linestyle=LINESTYLES[index % len(LINESTYLES)],
        )
    polish_axes(ax, xlabel, ylabel)
    ax.legend(loc="best")


def plot_heatmap(
    ax: plt.Axes,
    rows: list[tuple[str, str, float]],
    xlabel: str,
    ylabel: str,
    colorbar_label: str | None = None,
    annotate: bool = False,
    fmt: str = "{:.2f}",
) -> None:
    """Plot a row/column/value heatmap."""
    row_labels = sorted({row for row, _, _ in rows})
    col_labels = sorted({col for _, col, _ in rows})
    matrix = np.full((len(row_labels), len(col_labels)), np.nan)
    row_index = {label: idx for idx, label in enumerate(row_labels)}
    col_index = {label: idx for idx, label in enumerate(col_labels)}
    for row, col, value in rows:
        matrix[row_index[row], col_index[col]] = value
    masked = np.ma.masked_invalid(matrix)
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad(color="white")
    image = ax.imshow(masked, aspect="auto", cmap=cmap)
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_xticklabels(col_labels, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_yticklabels(row_labels)
    if colorbar_label:
        cbar = ax.figure.colorbar(image, ax=ax)
        cbar.set_label(colorbar_label)
    if annotate:
        finite_values = matrix[np.isfinite(matrix)]
        if finite_values.size:
            lo = float(np.nanmin(finite_values))
            hi = float(np.nanmax(finite_values))
            span = hi - lo if hi > lo else 1.0
            cmap_obj = plt.get_cmap("viridis")
            for row_idx in range(matrix.shape[0]):
                for col_idx in range(matrix.shape[1]):
                    value = matrix[row_idx, col_idx]
                    if not np.isfinite(value):
                        continue
                    rgba = cmap_obj((value - lo) / span)
                    luminance = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
                    color = "white" if luminance < 0.5 else "black"
                    ax.text(
                        col_idx,
                        row_idx,
                        fmt.format(value),
                        ha="center",
                        va="center",
                        color=color,
                        fontsize=plt.rcParams["font.size"] * 0.85,
                    )
    ax.set_frame_on(False)
    polish_axes(ax, xlabel, ylabel)


def plot_scatter(
    ax: plt.Axes,
    rows: dict[str, list[tuple[float, float, float | None, str | None]]],
    xlabel: str,
    ylabel: str,
) -> None:
    """Plot scatter or bubble rows grouped by series."""
    for index, (series, points) in enumerate(rows.items()):
        x_values = [item[0] for item in points]
        y_values = [item[1] for item in points]
        sizes = [item[2] for item in points]
        marker_size = 28 if all(item is None for item in sizes) else [max(8.0, item or 8.0) for item in sizes]
        ax.scatter(
            x_values,
            y_values,
            s=marker_size,
            label=series,
            color=DEFAULT_COLORS[index % len(DEFAULT_COLORS)],
            marker=MARKERS[index % len(MARKERS)],
            alpha=0.82,
            edgecolors="white",
            linewidths=0.5,
        )
        for x_val, y_val, _, label in points:
            if label:
                ax.text(x_val, y_val, label, fontsize=plt.rcParams["font.size"] * 0.85)
    polish_axes(ax, xlabel, ylabel)
    ax.legend(loc="best")


def plot_stacked_area(
    ax: plt.Axes,
    rows: dict[str, list[tuple[float, float]]],
    xlabel: str,
    ylabel: str,
) -> None:
    """Plot stacked area data from x/series/y rows."""
    x_values = sorted({x for points in rows.values() for x, _ in points})
    series_names = list(rows)
    value_matrix = []
    for series in series_names:
        value_by_x = {x: value for x, value in rows[series]}
        value_matrix.append([value_by_x.get(x, 0.0) for x in x_values])
    ax.stackplot(
        x_values,
        value_matrix,
        labels=series_names,
        colors=[DEFAULT_COLORS[idx % len(DEFAULT_COLORS)] for idx in range(len(series_names))],
        alpha=0.82,
    )
    polish_axes(ax, xlabel, ylabel)
    ax.legend(loc="best")


def plot_radar(
    fig: plt.Figure,
    rows: dict[str, list[tuple[str, float, float | None, float | None]]],
    ylabel: str,
) -> plt.Axes:
    """Plot a radar chart from axis/series/value rows.

    Optional min/max values normalize metrics with different scales. If omitted, each axis uses the
    observed min/max across series.
    """
    axis_labels = sorted({axis for points in rows.values() for axis, _, _, _ in points})
    if len(axis_labels) < 3:
        raise ValueError("Radar charts require at least three axes.")

    bounds: dict[str, tuple[float, float]] = {}
    for axis in axis_labels:
        observed = [(value, low, high) for points in rows.values() for a, value, low, high in points if a == axis]
        lows = [low for _, low, _ in observed if low is not None]
        highs = [high for _, _, high in observed if high is not None]
        values = [value for value, _, _ in observed]
        lo = lows[0] if lows else min(values)
        hi = highs[0] if highs else max(values)
        if hi <= lo:
            hi = lo + 1.0
        bounds[axis] = (lo, hi)

    angles = np.linspace(0, 2 * np.pi, len(axis_labels), endpoint=False)
    closed_angles = np.append(angles, angles[0])
    ax = fig.add_subplot(111, projection="polar")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    for index, (series, points) in enumerate(rows.items()):
        value_by_axis = {axis: value for axis, value, _, _ in points}
        normalized = []
        for axis in axis_labels:
            lo, hi = bounds[axis]
            value = value_by_axis.get(axis, lo)
            normalized.append((value - lo) / (hi - lo))
        closed_values = np.append(normalized, normalized[0])
        color = DEFAULT_COLORS[index % len(DEFAULT_COLORS)]
        ax.plot(closed_angles, closed_values, color=color, linewidth=1.3, label=series)
        ax.fill(closed_angles, closed_values, color=color, alpha=0.08)
        ax.scatter(angles, normalized, color=color, s=16)
    ax.set_xticks(angles)
    ax.set_xticklabels(axis_labels)
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    ax.grid(linewidth=0.4, alpha=0.55)
    if ylabel:
        ax.set_title(ylabel, pad=12)
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.10))
    return ax


def plot_image_grid(
    fig: plt.Figure,
    rows: list[tuple[Path, int, int, str | None]],
    label_color: str = "white",
) -> plt.Axes:
    """Plot a qualitative result grid from user-provided or permission-cleared images."""
    max_row = max(row for _, row, _, _ in rows)
    max_col = max(col for _, _, col, _ in rows)
    axes = fig.subplots(max_row + 1, max_col + 1, squeeze=False)
    for ax in axes.ravel():
        ax.set_axis_off()
        ax.set_facecolor("black")
    for image_path, row, col, label in rows:
        ax = axes[row][col]
        image = mpimg.imread(image_path)
        ax.imshow(image)
        ax.set_axis_off()
        if label:
            ax.text(
                0.02,
                0.98,
                label,
                transform=ax.transAxes,
                ha="left",
                va="top",
                color=label_color,
                fontsize=plt.rcParams["font.size"],
                bbox={"facecolor": "black", "alpha": 0.35, "edgecolor": "none", "pad": 1.5},
            )
    return axes[0][0]


def finalize_figure(fig: plt.Figure, out_base: str | Path, formats: Iterable[str], dpi: int = 450) -> list[Path]:
    """Save a figure in multiple formats and close it."""
    base = Path(out_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=0.6)
    saved: list[Path] = []
    for fmt in formats:
        path = base.with_suffix(f".{fmt}")
        kwargs = {"dpi": dpi} if fmt.lower() in {"png", "jpg", "jpeg", "tif", "tiff"} else {}
        fig.savefig(path, **kwargs)
        saved.append(path)
    plt.close(fig)
    return saved
