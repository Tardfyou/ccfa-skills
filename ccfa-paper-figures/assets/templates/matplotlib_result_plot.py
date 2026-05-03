"""CCF-A paper figure template: audited data plot.

Usage:
    python assets/templates/matplotlib_result_plot.py --csv data/results.csv --chart line --venue ICSE --domain se --figure-id results

Input CSV contracts:
    line:         x,series,y[,yerr]
    bar:          category,series,y[,yerr]
    dot-interval: label,estimate,low,high[,series]
    cdf:          series,value
    heatmap:      row,column,value
    scatter:      x,y[,series,size,label]
    area:         x,series,y
    radar:        axis,series,value[,min,max]
    image-grid:   image,row,column[,label]

Do not use invented numbers. Populate the CSV from user-provided experiment data, audited public
benchmark data, or values extracted from a paper the user has permission to reuse.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt

from ccfa_plot_helpers import (
    apply_ccfa_style,
    finalize_figure,
    plot_dot_interval,
    plot_ecdf,
    plot_grouped_bar,
    plot_heatmap,
    plot_image_grid,
    plot_radar,
    plot_scatter,
    plot_series,
    plot_stacked_area,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a CCF-A style data figure.")
    parser.add_argument("--csv", required=True, help="Source CSV matching the selected --chart contract.")
    parser.add_argument(
        "--chart",
        choices=["line", "bar", "dot-interval", "cdf", "heatmap", "scatter", "area", "radar", "image-grid"],
        default="line",
        help="Data-figure family.",
    )
    parser.add_argument("--venue", default="unknown", help="Target venue, e.g. CCS, ICSE, CVPR.")
    parser.add_argument("--domain", default="unknown", help="Domain: ai, security, se, pl, systems.")
    parser.add_argument("--figure-id", default="results", help="Figure folder id.")
    parser.add_argument("--width", choices=["single", "double", "square"], default="single")
    parser.add_argument("--xlabel", default="", help="X-axis label.")
    parser.add_argument("--ylabel", default="", help="Y-axis label.")
    parser.add_argument("--colorbar-label", default="", help="Heatmap colorbar label.")
    parser.add_argument("--xscale", choices=["linear", "log"], default="linear", help="X-axis scale for axis-based charts.")
    parser.add_argument("--yscale", choices=["linear", "log"], default="linear", help="Y-axis scale for axis-based charts.")
    parser.add_argument("--annotate", action="store_true", help="Add compact value labels for bar and heatmap charts.")
    parser.add_argument("--legend-outside", action="store_true", help="Move the legend outside the plotting area when applicable.")
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
    raise SystemExit("Could not find ccfa_matplotlib.mplstyle; pass a scaffolded copy or run from the skill template tree.")


def require_columns(reader: csv.DictReader, required: set[str]) -> None:
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        missing = ", ".join(sorted(required - set(reader.fieldnames or [])))
        raise SystemExit(f"CSV is missing required column(s): {missing}")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if not reader.fieldnames:
            raise SystemExit("CSV has no header row.")
    if not rows:
        raise SystemExit("CSV contains no data rows.")
    return rows


def read_line_rows(path: Path) -> dict[str, list[tuple[float, float, float | None]]]:
    rows: dict[str, list[tuple[float, float, float | None]]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"x", "series", "y"})
        for raw in reader:
            series = (raw.get("series") or "").strip()
            if not series:
                raise SystemExit("CSV contains an empty series label.")
            yerr_raw = (raw.get("yerr") or "").strip()
            yerr = float(yerr_raw) if yerr_raw else None
            rows.setdefault(series, []).append((float(raw["x"]), float(raw["y"]), yerr))
    if not rows:
        raise SystemExit("CSV contains no data rows.")
    return rows


def read_bar_rows(path: Path) -> dict[str, list[tuple[str, float, float | None]]]:
    rows: dict[str, list[tuple[str, float, float | None]]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"category", "series", "y"})
        for raw in reader:
            category = (raw.get("category") or "").strip()
            series = (raw.get("series") or "").strip()
            if not category or not series:
                raise SystemExit("CSV contains an empty category or series label.")
            yerr_raw = (raw.get("yerr") or "").strip()
            yerr = float(yerr_raw) if yerr_raw else None
            rows.setdefault(series, []).append((category, float(raw["y"]), yerr))
    if not rows:
        raise SystemExit("CSV contains no data rows.")
    return rows


def read_dot_interval_rows(path: Path) -> list[tuple[str, float, float, float, str]]:
    parsed: list[tuple[str, float, float, float, str]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"label", "estimate", "low", "high"})
        for raw in reader:
            label = (raw.get("label") or "").strip()
            if not label:
                raise SystemExit("CSV contains an empty interval label.")
            series = (raw.get("series") or "estimate").strip()
            parsed.append((label, float(raw["estimate"]), float(raw["low"]), float(raw["high"]), series))
    if not parsed:
        raise SystemExit("CSV contains no data rows.")
    return parsed


def read_cdf_rows(path: Path) -> dict[str, list[float]]:
    rows: dict[str, list[float]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"series", "value"})
        for raw in reader:
            series = (raw.get("series") or "").strip()
            if not series:
                raise SystemExit("CSV contains an empty series label.")
            rows.setdefault(series, []).append(float(raw["value"]))
    if not rows:
        raise SystemExit("CSV contains no data rows.")
    return rows


def read_heatmap_rows(path: Path) -> list[tuple[str, str, float]]:
    parsed: list[tuple[str, str, float]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"row", "column", "value"})
        for raw in reader:
            row = (raw.get("row") or "").strip()
            column = (raw.get("column") or "").strip()
            if not row or not column:
                raise SystemExit("CSV contains an empty row or column label.")
            parsed.append((row, column, float(raw["value"])))
    if not parsed:
        raise SystemExit("CSV contains no data rows.")
    return parsed


def read_scatter_rows(path: Path) -> dict[str, list[tuple[float, float, float | None, str | None]]]:
    parsed: dict[str, list[tuple[float, float, float | None, str | None]]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"x", "y"})
        for raw in reader:
            series = (raw.get("series") or "data").strip()
            size_raw = (raw.get("size") or "").strip()
            label = (raw.get("label") or "").strip() or None
            size = float(size_raw) if size_raw else None
            parsed.setdefault(series, []).append((float(raw["x"]), float(raw["y"]), size, label))
    if not parsed:
        raise SystemExit("CSV contains no data rows.")
    return parsed


def read_area_rows(path: Path) -> dict[str, list[tuple[float, float]]]:
    parsed: dict[str, list[tuple[float, float]]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"x", "series", "y"})
        for raw in reader:
            series = (raw.get("series") or "").strip()
            if not series:
                raise SystemExit("CSV contains an empty series label.")
            parsed.setdefault(series, []).append((float(raw["x"]), float(raw["y"])))
    if not parsed:
        raise SystemExit("CSV contains no data rows.")
    return parsed


def read_radar_rows(path: Path) -> dict[str, list[tuple[str, float, float | None, float | None]]]:
    parsed: dict[str, list[tuple[str, float, float | None, float | None]]] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"axis", "series", "value"})
        for raw in reader:
            axis = (raw.get("axis") or "").strip()
            series = (raw.get("series") or "").strip()
            if not axis or not series:
                raise SystemExit("CSV contains an empty radar axis or series label.")
            low_raw = (raw.get("min") or "").strip()
            high_raw = (raw.get("max") or "").strip()
            low = float(low_raw) if low_raw else None
            high = float(high_raw) if high_raw else None
            parsed.setdefault(series, []).append((axis, float(raw["value"]), low, high))
    if not parsed:
        raise SystemExit("CSV contains no data rows.")
    return parsed


def read_image_grid_rows(path: Path) -> list[tuple[Path, int, int, str | None]]:
    parsed: list[tuple[Path, int, int, str | None]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader, {"image", "row", "column"})
        for raw in reader:
            image_raw = (raw.get("image") or "").strip()
            if not image_raw:
                raise SystemExit("CSV contains an empty image path.")
            image_path = Path(image_raw)
            if not image_path.is_absolute():
                image_path = path.parent / image_path
            if not image_path.exists():
                raise SystemExit(f"Image file does not exist: {image_path}")
            label = (raw.get("label") or "").strip() or None
            parsed.append((image_path, int(raw["row"]), int(raw["column"]), label))
    if not parsed:
        raise SystemExit("CSV contains no data rows.")
    return parsed


def make_figure(args: argparse.Namespace) -> tuple[plt.Figure, plt.Axes]:
    apply_ccfa_style(style_path(), args.width)
    fig, ax = plt.subplots()
    csv_path = Path(args.csv)
    xlabel = args.xlabel or ("value" if args.chart == "cdf" else "")
    ylabel = args.ylabel or ("ECDF" if args.chart == "cdf" else "")

    if args.chart == "line":
        plot_series(ax, read_line_rows(csv_path), xlabel, ylabel)
    elif args.chart == "bar":
        plot_grouped_bar(ax, read_bar_rows(csv_path), xlabel, ylabel, annotate=args.annotate)
    elif args.chart == "dot-interval":
        plot_dot_interval(ax, read_dot_interval_rows(csv_path), xlabel, ylabel)
    elif args.chart == "cdf":
        plot_ecdf(ax, read_cdf_rows(csv_path), xlabel, ylabel)
    elif args.chart == "heatmap":
        plot_heatmap(ax, read_heatmap_rows(csv_path), xlabel, ylabel, args.colorbar_label or None, annotate=args.annotate)
    elif args.chart == "scatter":
        plot_scatter(ax, read_scatter_rows(csv_path), xlabel, ylabel)
    elif args.chart == "area":
        plot_stacked_area(ax, read_area_rows(csv_path), xlabel, ylabel)
    elif args.chart == "radar":
        fig.clear()
        ax = plot_radar(fig, read_radar_rows(csv_path), ylabel)
    elif args.chart == "image-grid":
        fig.clear()
        ax = plot_image_grid(fig, read_image_grid_rows(csv_path))
    else:
        raise SystemExit(f"Unsupported chart type: {args.chart}")
    if args.chart not in {"radar", "image-grid"}:
        ax.set_xscale(args.xscale)
        ax.set_yscale(args.yscale)
        if args.legend_outside:
            from ccfa_plot_helpers import move_legend_outside

            move_legend_outside(ax)
    return fig, ax


def main() -> None:
    args = parse_args()
    out = Path("figures") / args.figure_id / "exports" / args.figure_id
    fig, _ = make_figure(args)
    saved = finalize_figure(fig, out, formats=["pdf", "svg", "png"], dpi=450)
    print("Wrote exports:")
    for path in saved:
        print(f"  {path.resolve()}")


if __name__ == "__main__":
    main()
