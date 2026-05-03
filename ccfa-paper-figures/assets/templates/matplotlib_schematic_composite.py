"""CCF-A paper figure template: schematic-led architecture composite.

Use this template only with user-provided, audited public, or permission-cleared content.
The template contains no reusable example architecture. It renders a Nature-style hero
schematic and, optionally, a quiet row of quantitative evidence panels.

Usage:
    python assets/templates/matplotlib_schematic_composite.py --spec path/to/spec.json --figure-id overview

Spec shape:
    {
      "title": "optional",
      "schematic": {
        "components": [{"id": "...", "label": "...", "kind": "proposed", "xy": [0.1, 0.5], "width": 0.2, "height": 0.1}],
        "arrows": [{"from": "...", "to": "...", "kind": "data", "label": "optional"}],
        "boundaries": [{"label": "optional", "kind": "runtime", "xy": [0.05, 0.45], "width": 0.5, "height": 0.25}],
        "callouts": [{"xy": [0.3, 0.6], "text_xy": [0.4, 0.8], "text": "..."}],
        "images": [{"path": "permission-cleared.png", "xy": [0.7, 0.2], "width": 0.2, "height": 0.2}]
      },
      "data_panels": [
        {"chart": "line", "csv": "results.csv", "xlabel": "...", "ylabel": "...", "title": "..."}
      ]
    }
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from ccfa_plot_helpers import (
    PALETTE,
    add_panel_label,
    apply_ccfa_style,
    draw_arrow,
    draw_boundary,
    draw_callout,
    draw_component_box,
    finalize_figure,
    schematic_arrow_style,
    schematic_boundary_style,
    schematic_component_style,
    plot_dot_interval,
    plot_ecdf,
    plot_grouped_bar,
    plot_heatmap,
    plot_scatter,
    plot_series,
    plot_stacked_area,
    style_schematic_axis,
)
from matplotlib_result_plot import (
    read_area_rows,
    read_bar_rows,
    read_cdf_rows,
    read_dot_interval_rows,
    read_heatmap_rows,
    read_line_rows,
    read_scatter_rows,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a CCF-A schematic-led composite figure.")
    parser.add_argument("--spec", required=True, help="JSON spec with user/audited schematic content.")
    parser.add_argument("--figure-id", default="schematic-composite", help="Figure folder id.")
    parser.add_argument("--width", choices=["single", "double"], default="double")
    parser.add_argument("--formats", default="pdf,svg,png", help="Comma-separated export formats.")
    return parser.parse_args()


def style_path() -> Path:
    here = Path(__file__).resolve()
    candidates = [
        here.with_name("ccfa_matplotlib.mplstyle"),
        here.parents[1] / "ccfa_matplotlib.mplstyle",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise SystemExit("Could not find ccfa_matplotlib.mplstyle; use the scaffolded template folder.")


def color_value(value: str | None, default: str) -> str:
    if not value:
        return default
    return PALETTE.get(value, value)


def load_spec(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        spec = json.load(handle)
    if not isinstance(spec, dict):
        raise SystemExit("Spec root must be a JSON object.")
    schematic = spec.get("schematic")
    if not isinstance(schematic, dict):
        raise SystemExit("Spec must contain a 'schematic' object.")
    components = schematic.get("components", [])
    if not isinstance(components, list) or not components:
        raise SystemExit("Spec schematic.components must contain at least one user/audited component.")
    return spec


def resolve_path(path: str, base_dir: Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = base_dir / candidate
    if not candidate.exists():
        raise SystemExit(f"Referenced file does not exist: {candidate}")
    return candidate


def component_center(component: dict[str, Any]) -> tuple[float, float]:
    x, y = component["xy"]
    return float(x) + float(component["width"]) / 2, float(y) + float(component["height"]) / 2


def component_anchor(component: dict[str, Any], anchor: str) -> tuple[float, float]:
    x, y = [float(v) for v in component["xy"]]
    width = float(component["width"])
    height = float(component["height"])
    anchors = {
        "center": (x + width / 2, y + height / 2),
        "left": (x, y + height / 2),
        "right": (x + width, y + height / 2),
        "top": (x + width / 2, y + height),
        "bottom": (x + width / 2, y),
    }
    return anchors.get(anchor, anchors["center"])


def as_xy(value: Any, field: str) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) != 2:
        raise SystemExit(f"{field} must be a two-number array.")
    return float(value[0]), float(value[1])


def draw_schematic(ax: plt.Axes, schematic: dict[str, Any], base_dir: Path) -> None:
    xlim = tuple(schematic.get("xlim", [0.0, 1.0]))
    ylim = tuple(schematic.get("ylim", [0.0, 1.0]))
    style_schematic_axis(ax, (float(xlim[0]), float(xlim[1])), (float(ylim[0]), float(ylim[1])))

    for boundary in schematic.get("boundaries", []):
        style = schematic_boundary_style(str(boundary.get("kind")) if boundary.get("kind") else None)
        draw_boundary(
            ax,
            as_xy(boundary["xy"], "boundary.xy"),
            float(boundary["width"]),
            float(boundary["height"]),
            label=boundary.get("label"),
            edgecolor=color_value(boundary.get("edgecolor"), str(style["edgecolor"])),
            facecolor=color_value(boundary.get("facecolor"), str(style["facecolor"])),
            linestyle=boundary.get("linestyle", str(style["linestyle"])),
            linewidth=float(boundary.get("linewidth", style["linewidth"])),
        )

    for image in schematic.get("images", []):
        image_path = resolve_path(str(image["path"]), base_dir)
        xy = as_xy(image["xy"], "image.xy")
        width = float(image["width"])
        height = float(image["height"])
        ax.imshow(mpimg.imread(image_path), extent=[xy[0], xy[0] + width, xy[1], xy[1] + height])
        if image.get("label"):
            ax.text(xy[0], xy[1] + height + 0.012, image["label"], ha="left", va="bottom")

    components: dict[str, dict[str, Any]] = {}
    for component in schematic["components"]:
        component_id = component.get("id")
        if not component_id:
            raise SystemExit("Every schematic component must have an id.")
        components[str(component_id)] = component
        style = schematic_component_style(str(component.get("kind")) if component.get("kind") else None)
        draw_component_box(
            ax,
            as_xy(component["xy"], "component.xy"),
            float(component["width"]),
            float(component["height"]),
            str(component["label"]),
            facecolor=color_value(component.get("facecolor"), str(style["facecolor"])),
            edgecolor=color_value(component.get("edgecolor"), str(style["edgecolor"])),
            textcolor=color_value(component.get("textcolor"), str(style["textcolor"])),
        )

    for arrow in schematic.get("arrows", []):
        style = schematic_arrow_style(str(arrow.get("kind")) if arrow.get("kind") else None)
        if "from" in arrow and "to" in arrow:
            source = components.get(str(arrow["from"]))
            target = components.get(str(arrow["to"]))
            if source is None or target is None:
                raise SystemExit(f"Arrow references unknown component: {arrow}")
            start = component_anchor(source, arrow.get("from_anchor", "right"))
            end = component_anchor(target, arrow.get("to_anchor", "left"))
        else:
            start = as_xy(arrow["start"], "arrow.start")
            end = as_xy(arrow["end"], "arrow.end")
        draw_arrow(
            ax,
            start,
            end,
            label=arrow.get("label"),
            color=color_value(arrow.get("color"), str(style["color"])),
            connectionstyle=arrow.get("connectionstyle", "arc3,rad=0.0"),
            linestyle=arrow.get("linestyle", str(style["linestyle"])),
            linewidth=float(arrow.get("linewidth", style["linewidth"])),
            arrowstyle=str(arrow.get("arrowstyle", "-|>")),
            mutation_scale=float(arrow.get("mutation_scale", 11)),
            alpha=float(arrow.get("alpha", 1.0)),
        )

    for callout in schematic.get("callouts", []):
        draw_callout(
            ax,
            as_xy(callout["xy"], "callout.xy"),
            as_xy(callout["text_xy"], "callout.text_xy"),
            str(callout["text"]),
            color=color_value(callout.get("color"), PALETTE["red"]),
        )


def draw_data_panel(ax: plt.Axes, panel: dict[str, Any], base_dir: Path) -> None:
    csv_path = resolve_path(str(panel["csv"]), base_dir)
    chart = panel.get("chart", "line")
    xlabel = panel.get("xlabel", "")
    ylabel = panel.get("ylabel", "")
    if chart == "line":
        plot_series(ax, read_line_rows(csv_path), xlabel, ylabel)
    elif chart == "bar":
        plot_grouped_bar(ax, read_bar_rows(csv_path), xlabel, ylabel, annotate=bool(panel.get("annotate", False)))
    elif chart == "dot-interval":
        plot_dot_interval(ax, read_dot_interval_rows(csv_path), xlabel, ylabel)
    elif chart == "cdf":
        plot_ecdf(ax, read_cdf_rows(csv_path), xlabel or "value", ylabel or "ECDF")
    elif chart == "heatmap":
        plot_heatmap(
            ax,
            read_heatmap_rows(csv_path),
            xlabel,
            ylabel,
            colorbar_label=panel.get("colorbar_label"),
            annotate=bool(panel.get("annotate", False)),
        )
    elif chart == "scatter":
        plot_scatter(ax, read_scatter_rows(csv_path), xlabel, ylabel)
    elif chart == "area":
        plot_stacked_area(ax, read_area_rows(csv_path), xlabel, ylabel)
    else:
        raise SystemExit(f"Unsupported data panel chart: {chart}")
    if panel.get("title"):
        ax.set_title(str(panel["title"]), fontsize=plt.rcParams["font.size"] * 0.92)
    if panel.get("xscale") in {"linear", "log"}:
        ax.set_xscale(panel["xscale"])
    if panel.get("yscale") in {"linear", "log"}:
        ax.set_yscale(panel["yscale"])


def make_figure(spec: dict[str, Any], spec_path: Path, width: str) -> plt.Figure:
    apply_ccfa_style(style_path(), width)
    base_dir = spec_path.parent
    data_panels = spec.get("data_panels", [])
    if not isinstance(data_panels, list):
        raise SystemExit("data_panels must be a list when present.")

    if data_panels:
        n_panels = min(max(len(data_panels), 1), 4)
        fig = plt.figure(figsize=(7.16, 5.6) if width == "double" else (3.5, 5.0))
        gs = fig.add_gridspec(2, n_panels, height_ratios=[2.25, 1.0], hspace=0.28, wspace=0.38)
        ax_schematic = fig.add_subplot(gs[0, :])
        data_axes = [fig.add_subplot(gs[1, idx]) for idx in range(n_panels)]
    else:
        fig = plt.figure(figsize=(7.16, 3.9) if width == "double" else (3.5, 3.5))
        ax_schematic = fig.add_subplot(111)
        data_axes = []

    draw_schematic(ax_schematic, spec["schematic"], base_dir)
    add_panel_label(ax_schematic, "a", x=0.0, y=1.02)
    if spec.get("title"):
        ax_schematic.set_title(str(spec["title"]), fontsize=plt.rcParams["font.size"] * 1.05)

    for index, (ax, panel) in enumerate(zip(data_axes, data_panels), start=1):
        draw_data_panel(ax, panel, base_dir)
        add_panel_label(ax, chr(ord("a") + index), x=-0.18, y=1.04)
    return fig


def main() -> None:
    args = parse_args()
    spec_path = Path(args.spec)
    spec = load_spec(spec_path)
    fig = make_figure(spec, spec_path, args.width)
    formats = [fmt.strip().lower() for fmt in args.formats.split(",") if fmt.strip()]
    out = Path("figures") / args.figure_id / "exports" / args.figure_id
    saved = finalize_figure(fig, out, formats=formats, dpi=450)
    print("Wrote exports:")
    for path in saved:
        print(f"  {path.resolve()}")


if __name__ == "__main__":
    main()
