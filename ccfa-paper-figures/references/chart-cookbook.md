# Chart Cookbook

Use this file when choosing a concrete CCF-A data-figure form. It fills the gap between the high-level
decision guide and the executable Matplotlib template.

No section contains invented example results. Each recipe states the input contract and the audit
questions to answer before plotting.

## Baseline Or Ablation Comparison

Use `--chart bar` when categories are few enough to remain readable.

CSV contract:

```text
category,series,y[,yerr]
```

Use for:

- AI component ablations.
- Security defenses across attack families.
- SE tools across benchmark groups.
- Systems configurations across workload classes.

Checks:

- `series` names are real method/configuration names from the manuscript or source data.
- `category` values are benchmark groups, metrics, or ablation stages, not invented labels.
- `yerr` is defined in the caption as SD, SEM, CI, or another statistic.
- If categories are many, switch to `dot-interval` or small multiples.
- Use `--annotate` only when labels remain readable at final paper size.
- Use `--legend-outside` when the legend would hide bars or force tiny axes.

## Scaling, Sensitivity, Or Robustness Curve

Use `--chart line`.

CSV contract:

```text
x,series,y[,yerr]
```

Use for:

- Dataset/model/workload scaling.
- Robustness across perturbation strength.
- Throughput across clients, batch size, or nodes.
- Security success/detection across threshold or attacker budget.

Checks:

- `x` is numeric and has units or a clear dimension.
- Log scale is used only when multiplicative differences matter.
- Saturation, timeout, or failure points are shown rather than silently removed.

## Distribution Or Tail Behavior

Use `--chart cdf`.

CSV contract:

```text
series,value
```

Use for:

- Latency, overhead, runtime, detection latency, exploit timing.
- SE time-to-fix, test runtime, patch count, or issue-resolution time.
- Any skewed metric where mean-only bars would mislead.

Checks:

- The plotted direction is clear: ECDF, CDF, or CCDF if manually adapted.
- Units are in the x-axis label.
- Heavy tails are not clipped without a visual marker or caption note.

## Per-Project Or Per-Benchmark Effect

Use `--chart dot-interval`.

CSV contract:

```text
label,estimate,low,high[,series]
```

Use for:

- Per-project SE effects.
- Per-benchmark speedups.
- Security defense impact by attack class.
- Systems improvement with confidence intervals.

Checks:

- `low` and `high` are real interval endpoints, not visual padding.
- Labels fit at final paper size.
- A reference line may be added manually when the metric has a meaningful null point.

## Matrix, Heatmap, Or Confusion-Style Figure

Use `--chart heatmap`.

CSV contract:

```text
row,column,value
```

Use for:

- Method-by-benchmark scores.
- Error/confusion matrices.
- Class-by-metric summaries.
- Dataset or project composition matrices.

Checks:

- Row and column order is meaningful; alphabetical order is only a fallback.
- Missing values are deliberately blank or masked.
- A diverging colormap is used only when the center has a real meaning.
- Cell annotations are added only when readable at final size.
- Use `--annotate` for compact matrices where exact cell values matter.

## Trade-Off, Pareto, Or Correlation

Use `--chart scatter`.

CSV contract:

```text
x,y[,series,size,label]
```

Use for:

- Latency vs accuracy.
- Cost vs quality.
- Throughput vs tail latency.
- Security overhead vs detection improvement.

Checks:

- Both axes have units or metric definitions.
- Bubble `size`, when used, has a real measurement meaning.
- Point labels are sparse enough to remain readable.
- Do not imply causality from correlation without manuscript support.

## Stacked Contribution Or Composition Over Time

Use `--chart area`.

CSV contract:

```text
x,series,y
```

Use for:

- Workload mix over time.
- Benchmark or vulnerability category composition.
- Resource contribution where components sum to a meaningful total.

Checks:

- Stacked values share the same unit and sum to a meaningful total.
- Category order is stable across panels.
- Hatching or direct labels may be needed for grayscale readability.
- Use direct labels or an outside legend when categories are stable across panels.

## Radar Or Multi-Metric Profile

Use `--chart radar` sparingly.

CSV contract:

```text
axis,series,value[,min,max]
```

Use for:

- Compact multi-metric method profiles with three to eight axes.
- Benchmarks where per-axis normalization is explicitly disclosed.

Checks:

- Axis ranges are honest; include `min,max` when metrics have different natural scales.
- The caption states that values are normalized when ranges differ.
- Do not use radar for precise value comparison when a table or dot plot is clearer.

## Qualitative Result Grid

Use `--chart image-grid` for user-provided or permission-cleared result images.

CSV contract:

```text
image,row,column[,label]
```

Use for:

- CVPR/ICCV qualitative comparisons.
- UI or screenshot result panels.
- Visual examples paired with a quantitative result panel.

Checks:

- Every image path points to material the user owns, supplied, or has permission to reuse.
- Rows and columns compare like with like; do not mix unrelated examples in one grid.
- Crops and normalization are documented when they affect interpretation.
- Labels are short and do not cover important evidence.

## Multi-Panel Layout

For multi-panel figures, combine generated plots manually with Matplotlib `GridSpec` after each
single-panel contract is validated.

When the user supplies only data plus a broad style request, run
`scripts/suggest_showpiece.py <csv> --style showpiece` and use its output as the first draft of the
panel plan. The goal is to select the most expressive truthful layout automatically, not to force a
busy page.

Recommended CS data progression:

| Panel role | Question | Common chart |
|---|---|---|
| Main result | Does the method improve the target metric? | `line`, `bar`, or `dot-interval` |
| Mechanism | Which component or condition matters? | `bar`, `line`, or `heatmap` |
| Boundary | Where does it fail or cost more? | `cdf`, `line`, or `dot-interval` |
| Context | What benchmark/workload explains the comparison? | compact `heatmap` or table-like inset |
| Trade-off | Which point is efficient or Pareto-optimal? | `scatter` |
| Qualitative evidence | What does the method output look like? | `image-grid` plus a quantitative panel |

Anti-redundancy checks:

- Do not show the same values as both bar and heatmap.
- Do not split panels only because the plotting code was convenient.
- Each panel should have a distinct axis-label vocabulary or a distinct claim.
- Put large legends in a dedicated axis with `make_legend_axis` or outside the data region with
  `move_legend_outside`.
- In cramped showpiece layouts, combine panel letters with left-aligned titles and avoid separate
  floating panel-letter text.
- If direct labels collide in ECDF/scatter panels, replace them with a compact legend placed in true
  empty space or outside the axes.
- Treat colorbars as part of the text layout: pad their labels, or move units into the panel title
  when the colorbar is narrow.
