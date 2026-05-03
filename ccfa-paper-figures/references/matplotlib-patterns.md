# Matplotlib Patterns

This file adapts mature Nature-style figure practices to CCF-A computer-science papers. Use it for
quantitative plots and multi-panel experimental figures.

Traceability: export, font, size and accessibility defaults are grounded in `source-basis.md`.
Palette and panel-architecture rules are operational synthesis adapted from `nature-skills` and the
paper exemplars. Treat them as strict local defaults, not as verbatim venue policy.

## Required rcParams

Use the local style file by default:

```python
plt.style.use("assets/ccfa_matplotlib.mplstyle")
```

The bundled Matplotlib template intentionally does not contain demo numbers. It reads a CSV with
one of the contracts in `plot-api.md`; fill that CSV from user-provided experimental data, audited
public benchmark data, or permission-cleared paper values.

Use `assets/templates/ccfa_plot_helpers.py` for reusable style, export, panel-label, line, bar,
dot-interval, CDF, and heatmap helpers. The scaffold script copies it beside the Matplotlib template.

If writing a standalone script, include these export-critical settings:

```python
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["svg.fonttype"] = "none"
```

Rationale:

- PDF/PS font type 42 keeps text closer to editable/searchable TrueType workflows.
- SVG `fonttype = none` keeps text as text nodes rather than paths.
- Arial/Helvetica/DejaVu Sans are safer cross-platform choices for CS papers than exotic fonts.

## Palette

Prefer Okabe-Ito-like, colorblind-safe defaults:

```python
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
```

Rules:

- Use one method color consistently across all panels.
- Add marker, dash, hatch, or direct label; never rely on hue alone.
- Reserve red for attacker/failure/regression only when labels also encode that role.
- Avoid `jet` and rainbow colormaps. Use `viridis`, `cividis`, `magma`, or a diverging map with a
  meaningful zero point.

## Figure Size

Use venue width first:

| Purpose | Size |
|---|---|
| Single-column plot | `(3.5, 2.35)` |
| Single-column square-ish diagram | `(3.5, 3.0)` |
| Double-column multi-panel | `(7.16, 3.2)` to `(7.16, 4.8)` |
| Compact appendix plot | `(3.2, 2.1)` |

Final-size text should usually be 7-10 pt. Do not create a huge slide-sized figure and shrink it
blindly into a paper column.

## Multi-Panel Data Figure Structure

Each panel must answer a distinct question. A common CS pattern is:

| Panel role | Question | Common encoding |
|---|---|---|
| Main result | Does the method improve the target metric? | Line/dot/bar with uncertainty |
| Mechanism | Why or where does it help? | Ablation, breakdown, or sensitivity |
| Boundary | When does it fail or cost more? | Stress test, robustness, overhead |
| Context | What data split, benchmark, or workload explains the comparison? | Compact table-like inset, grouped labels, or small multiple |

Avoid duplicate encodings:

- Do not show a table, bar plot, and heatmap of the same values.
- Do not repeat the same ranking as both a bar chart and a line chart.
- Do not split panels merely because metrics are visually convenient; split by scientific question.

## Recommended Plot Patterns

### Baseline Comparison

Prefer dot/interval or grouped bar with uncertainty. For many benchmarks, use per-benchmark dots plus
an aggregate marker instead of a crowded grouped bar.

Template support: `--chart bar` or `--chart dot-interval`; add `--annotate` only when value labels
stay readable.

### Scalability

Use line plots with markers. If x spans orders of magnitude, use log scale with explicit tick labels.
Show saturation or failure points instead of clipping them away.

Template support: `--chart line`.

### CDF / CCDF

Use for latency, overhead, exploit timing, and distributional performance. Label percentile direction
clearly. Avoid too many overlapping curves.

Template support: `--chart cdf` for ECDF; adapt manually for CCDF when the paper needs tail survival.

### Ablation

Use a single method-family color with alpha or ordered shade changes. Keep the full method visually
strongest and the most ablated variant weakest.

### Heatmap

Use heatmaps for matrix structure, not as a substitute for unreadable tables. Annotate only if labels
remain legible at final size. Use a diverging colormap only when the center has a real meaning.

Template support: `--chart heatmap`; add `--annotate` for compact matrices.

### Legend Economy

Use direct labels when category identity is spatially stable. Move large legends outside the axes or
into a legend-only axis so they never cover data.

Template support: `--legend-outside`.

### Text Collision Control

Final figures must have no overlapping text. This is a readiness gate, not a polish preference.

Before exporting:

- Prefer outside legends or a dedicated legend axis for crowded multi-panel figures.
- Rotate or shorten tick labels only when they remain readable; otherwise group labels or move detail
  into the caption.
- Use fewer direct point labels in scatter/bubble plots; label only the Pareto/frontier or claim
  critical points.
- Disable heatmap cell annotations when the matrix is too dense, or enlarge the panel and reduce the
  number of displayed rows/columns.
- Increase `hspace`, `wspace`, and label padding when panel titles, colorbars, or tick labels touch.
- Inspect the SVG/PDF at final paper width after running `figure_audit.py`; resolve any text-overlap
  warning before calling the figure ready.

## Export

Always save vector first:

```python
fig.savefig("figures/<id>/exports/<id>.pdf")
fig.savefig("figures/<id>/exports/<id>.svg")
fig.savefig("figures/<id>/exports/<id>.png", dpi=300)
plt.close(fig)
```

Run:

```bash
python ccfa-paper-figures/scripts/figure_audit.py figures/<id>/exports/<id>.pdf figures/<id>/exports/<id>.svg
```
