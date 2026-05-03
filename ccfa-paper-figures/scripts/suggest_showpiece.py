#!/usr/bin/env python3
"""Suggest a high-information CCF-A figure plan from a CSV.

The script does not invent data or draw a figure. It profiles the supplied CSV and emits a
showpiece-oriented plan plus a self-prompt that another agent can follow.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Suggest a showpiece CCF-A figure plan from CSV data.")
    parser.add_argument("csv_path", help="Input CSV file.")
    parser.add_argument("--venue", default="unknown", help="Target venue, e.g. OSDI, CCS, ICSE, CVPR.")
    parser.add_argument("--domain", default="unknown", help="Domain, e.g. AI systems, security, SE.")
    parser.add_argument("--style", default="showpiece", choices=["showpiece", "strict", "compact"])
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not reader.fieldnames:
        raise SystemExit("CSV has no header row.")
    if not rows:
        raise SystemExit("CSV has no data rows.")
    return list(reader.fieldnames), rows


def as_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def profile_columns(headers: list[str], rows: list[dict[str, str]]) -> dict[str, Any]:
    profile: dict[str, Any] = {
        "rows": len(rows),
        "columns": headers,
        "numeric_columns": [],
        "categorical_columns": [],
        "mostly_unique_columns": [],
        "cardinality": {},
    }
    for column in headers:
        values = [(row.get(column) or "").strip() for row in rows]
        nonempty = [value for value in values if value]
        numeric = [as_float(value) for value in nonempty]
        numeric_count = sum(value is not None for value in numeric)
        unique_count = len(set(nonempty))
        profile["cardinality"][column] = unique_count
        if nonempty and numeric_count / len(nonempty) >= 0.85:
            profile["numeric_columns"].append(column)
        else:
            profile["categorical_columns"].append(column)
        if unique_count >= max(8, len(rows) * 0.45):
            profile["mostly_unique_columns"].append(column)
    return profile


def has_columns(headers: list[str], *names: str) -> bool:
    lowered = {header.lower() for header in headers}
    return all(name.lower() in lowered for name in names)


def choose_plan(profile: dict[str, Any], venue: str, domain: str, style: str) -> dict[str, Any]:
    headers = profile["columns"]
    lowered = {header.lower(): header for header in headers}
    categorical = profile["categorical_columns"]
    numeric = profile["numeric_columns"]
    rows = int(profile["rows"])

    plan: dict[str, Any] = {
        "style_mode": style,
        "venue": venue,
        "domain": domain,
        "confidence": "medium",
        "archetype": "multi-panel experimental summary",
        "why": [],
        "panels": [],
        "guardrails": [
            "Use only supplied, audited public, or permission-cleared values.",
            "Do not keep generated charts as reusable gallery assets.",
            "Run figure_audit.py and resolve text-overlap warnings before calling the figure ready.",
        ],
    }

    if has_columns(headers, "system", "model", "scenario") and any(name in lowered for name in ["tokens_s", "throughput", "latency"]):
        value = lowered.get("tokens_s") or lowered.get("throughput") or lowered.get("latency")
        plan["confidence"] = "high"
        plan["archetype"] = "fig4-style benchmark landscape"
        plan["why"] = [
            "System/model/scenario structure supports a dense benchmark landscape.",
            "A numeric performance column supports heatmap, Pareto, ECDF, and composition panels.",
            "This is the closest CS analogue of the gallery's fig4 multi-modal systems page.",
        ]
        plan["panels"] = [
            f"Panel a: dominant heatmap, system x scenario, value = {value}.",
            f"Panel b: Pareto/bubble scatter using two scenario values for {value}; bubble size from accelerators/nodes if present.",
            f"Panel c: ECDF or distribution of normalized {value}, grouped by model or submitter.",
            "Panel d: compact stacked composition/count panel by scenario and model family.",
        ]
    elif has_columns(headers, "row", "column", "value") and rows >= 20:
        plan["confidence"] = "high"
        plan["archetype"] = "matrix-led heatmap composite"
        plan["why"] = ["Row/column/value data naturally forms a dense heatmap.", "Enough rows exist for a dominant matrix panel."]
        plan["panels"] = [
            "Panel a: dominant ordered heatmap.",
            "Panel b: marginal bar/dot summary by row group.",
            "Panel c: marginal bar/dot summary by column group.",
            "Panel d: distribution or ranked interval of cell values.",
        ]
    elif has_columns(headers, "x", "y") and rows >= 20:
        plan["confidence"] = "high"
        plan["archetype"] = "Pareto/trade-off landscape"
        plan["why"] = ["Two numeric axes support a trade-off view.", "Many rows support labels for only frontier points."]
        plan["panels"] = [
            "Panel a: dominant scatter or bubble Pareto plot.",
            "Panel b: ECDF of the x metric.",
            "Panel c: ECDF of the y metric.",
            "Panel d: grouped count or small heatmap by series/category.",
        ]
    elif has_columns(headers, "series", "value") and rows >= 30:
        plan["archetype"] = "distribution-led landscape"
        plan["why"] = ["Series/value data is distributional; a mean-only bar would waste information."]
        plan["panels"] = [
            "Panel a: dominant ECDF/CCDF curves.",
            "Panel b: compact box/violin/rug distribution.",
            "Panel c: ranked summary dot plot.",
            "Panel d: sample-count or category composition panel.",
        ]
    elif has_columns(headers, "x", "series", "y") and rows >= 24:
        plan["archetype"] = "scaling and composition landscape"
        plan["why"] = ["Repeated x/series/y data supports scaling curves and stacked composition."]
        plan["panels"] = [
            "Panel a: dominant multi-series scaling curve.",
            "Panel b: relative gain or normalized heatmap.",
            "Panel c: endpoint dot/interval summary.",
            "Panel d: stacked area or contribution panel if series share a meaningful total.",
        ]
    elif len(numeric) >= 3 and len(categorical) >= 1 and rows >= 12:
        plan["archetype"] = "multi-metric profile composite"
        plan["why"] = ["Multiple numeric metrics support a radar or parallel small-multiple summary."]
        plan["panels"] = [
            "Panel a: dominant normalized multi-metric profile or grouped dot plot.",
            "Panel b: metric-by-method heatmap.",
            "Panel c: Pareto scatter for the two most important metrics.",
            "Panel d: compact rank/interval summary.",
        ]
    else:
        plan["confidence"] = "low"
        plan["archetype"] = "compact single-family figure"
        plan["why"] = ["The CSV is small or has limited structure; avoid forced complexity."]
        plan["panels"] = ["Use the strongest single chart family from chart-cookbook.md and keep it clean."]

    if style == "compact":
        plan["panels"] = plan["panels"][:2]
        plan["why"].append("Compact mode limits the design to the two strongest panels.")
    elif style == "strict" and plan["confidence"] == "low":
        plan["guardrails"].append("Ask for more data or a target claim before creating a showpiece layout.")

    return plan


def self_prompt(csv_path: Path, plan: dict[str, Any]) -> str:
    panel_lines = "\n".join(f"- {panel}" for panel in plan["panels"])
    guardrail_lines = "\n".join(f"- {item}" for item in plan["guardrails"])
    return f"""Use $ccfa-paper-figures to create a {plan['archetype']} from `{csv_path}`.

Target:
- venue: {plan['venue']}
- domain: {plan['domain']}
- style mode: {plan['style_mode']}
- output: PDF, SVG, PNG

Use this self-selected plan:
{panel_lines}

Requirements:
{guardrail_lines}
- Keep one dominant panel and quieter support panels when using a multi-panel layout.
- Use consistent semantic color mapping across panels.
- Keep all labels readable at final paper size; no text overlap is allowed.
- Include source, exports, caption draft, and readiness note.
"""


def emit_markdown(csv_path: Path, profile: dict[str, Any], plan: dict[str, Any]) -> None:
    print("# Showpiece Figure Suggestion")
    print()
    print(f"- Rows: {profile['rows']}")
    print(f"- Numeric columns: {', '.join(profile['numeric_columns']) or 'none'}")
    print(f"- Categorical columns: {', '.join(profile['categorical_columns']) or 'none'}")
    print(f"- Recommended archetype: {plan['archetype']}")
    print(f"- Confidence: {plan['confidence']}")
    print()
    print("## Why")
    for item in plan["why"]:
        print(f"- {item}")
    print()
    print("## Panel Plan")
    for item in plan["panels"]:
        print(f"- {item}")
    print()
    print("## Self-Prompt")
    print("```text")
    print(self_prompt(csv_path, plan).strip())
    print("```")


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv_path)
    headers, rows = read_rows(csv_path)
    profile = profile_columns(headers, rows)
    plan = choose_plan(profile, args.venue, args.domain, args.style)
    if args.json:
        print(json.dumps({"profile": profile, "plan": plan, "self_prompt": self_prompt(csv_path, plan)}, indent=2))
    else:
        emit_markdown(csv_path, profile, plan)


if __name__ == "__main__":
    main()
