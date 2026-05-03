#!/usr/bin/env python3
"""Scaffold a CCF-A paper-figure workspace.

Example:
    python ccfa-paper-figures/scripts/scaffold_figure.py result-ablation --venue ICSE --domain se --type quantitative
    python ccfa-paper-figures/scripts/scaffold_figure.py model-overview --venue SOSP --domain systems --type schematic
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
STYLE_FILE = ROOT / "assets" / "ccfa_matplotlib.mplstyle"
HELPER_FILE = TEMPLATES / "ccfa_plot_helpers.py"


TYPE_TO_TEMPLATE = {
    "quantitative": "matplotlib_result_plot.py",
    "result": "matplotlib_result_plot.py",
    "ablation": "matplotlib_result_plot.py",
    "benchmark": "matplotlib_result_plot.py",
    "cdf": "matplotlib_result_plot.py",
    "scaling": "matplotlib_result_plot.py",
    "latency": "matplotlib_result_plot.py",
    "throughput": "matplotlib_result_plot.py",
    "pgfplots": "tikz_pgfplots.tex",
    "schematic": "matplotlib_schematic_composite.py",
    "architecture": "matplotlib_schematic_composite.py",
    "overview": "matplotlib_schematic_composite.py",
    "workflow": "matplotlib_schematic_composite.py",
    "composite": "matplotlib_schematic_composite.py",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a reproducible CCF-A paper-figure folder.")
    parser.add_argument("figure_id", help="Figure id, e.g. result-ablation or latency-cdf.")
    parser.add_argument("--venue", default="unknown", help="Target venue, e.g. CCS, ICSE, CVPR.")
    parser.add_argument("--domain", default="unknown", help="Domain: ai, security, se, pl, systems.")
    parser.add_argument(
        "--type",
        default="quantitative",
        choices=sorted(TYPE_TO_TEMPLATE),
        help="Figure template family.",
    )
    parser.add_argument("--root", default="figures", help="Output root directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = Path(args.root) / args.figure_id
    source = base / "source"
    exports = base / "exports"
    data = base / "data"
    for path in [source, exports, data]:
        path.mkdir(parents=True, exist_ok=True)

    template_name = TYPE_TO_TEMPLATE[args.type]
    template = TEMPLATES / template_name
    target = source / template_name
    if not template.exists():
        raise SystemExit(f"Template not found: {template}")
    if not target.exists():
        shutil.copy2(template, target)
    if template_name in {"matplotlib_result_plot.py", "matplotlib_schematic_composite.py"}:
        style_target = source / STYLE_FILE.name
        if not style_target.exists():
            shutil.copy2(STYLE_FILE, style_target)
        helper_target = source / HELPER_FILE.name
        if not helper_target.exists():
            shutil.copy2(HELPER_FILE, helper_target)
    if template_name == "matplotlib_schematic_composite.py":
        result_template = TEMPLATES / "matplotlib_result_plot.py"
        result_target = source / "matplotlib_result_plot.py"
        if not result_target.exists():
            shutil.copy2(result_template, result_target)

    metadata = source / "figure_profile.txt"
    metadata.write_text(
        "\n".join(
            [
                f"figure_id: {args.figure_id}",
                f"venue: {args.venue}",
                f"domain: {args.domain}",
                f"type: {args.type}",
                "scope: data/statistical figure or Nature-style schematic-led composite",
                "stage: unknown",
                "data_provenance: user-provided, audited public, or permission-cleared data/material required",
                "profile_note: verify current CFP/author kit before final submission.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Created {base.resolve()}")
    print(f"Template: {target}")
    print("Next: fill data/material from user-provided or audited sources, export PDF/SVG, then run scripts/figure_audit.py.")


if __name__ == "__main__":
    main()
