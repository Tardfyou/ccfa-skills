# Plot API

Use this file when implementing a CCF-A data figure in Matplotlib. It mirrors the operational level
of `nature-skills/nature-figure/references/api.md`, but is scoped to audited data figures and contains
no invented experiment values.

## Bundled Helper

Copy or import:

```python
from ccfa_plot_helpers import (
    apply_ccfa_style,
    add_panel_label,
    add_direct_label,
    move_legend_outside,
    make_legend_axis,
    tighten_axis,
    finalize_figure,
    plot_series,
    plot_grouped_bar,
    plot_dot_interval,
    plot_ecdf,
    plot_heatmap,
    plot_image_grid,
    plot_scatter,
    plot_stacked_area,
    plot_radar,
)
```

The scaffold script copies `assets/templates/ccfa_plot_helpers.py` beside
`matplotlib_result_plot.py`, so scaffolded figures can import it directly.

## Style

Always call:

```python
apply_ccfa_style("ccfa_matplotlib.mplstyle", width="single")
```

Width options:

| Option | Use |
|---|---|
| `single` | 3.5 in single-column plot. |
| `double` | 7.16 in double-column plot. |
| `square` | Single-column square-ish heatmap or matrix. |

The helper enforces:

- sans-serif font stack: Arial, Helvetica, DejaVu Sans
- editable/searchable SVG text: `svg.fonttype = none`
- editable PDF/PS text: font type 42
- local CCF-A style defaults from `ccfa_matplotlib.mplstyle`

## CSV Contracts

`assets/templates/matplotlib_result_plot.py` accepts these chart families:

| Chart | Required CSV columns | Best for |
|---|---|---|
| `line` | `x,series,y[,yerr]` | Scaling, latency/throughput, robustness, sensitivity, learning curves. |
| `bar` | `category,series,y[,yerr]` | Benchmark group comparisons and compact ablations. |
| `dot-interval` | `label,estimate,low,high[,series]` | Per-project effects, confidence intervals, forest-style summaries. |
| `cdf` | `series,value` | Latency, overhead, exploit timing, runtime, time-to-fix distributions. |
| `heatmap` | `row,column,value` | Method-by-benchmark, class-by-metric, confusion/error matrices. |
| `scatter` | `x,y[,series,size,label]` | Pareto frontiers, trade-offs, correlations, bubble summaries. |
| `area` | `x,series,y` | Stacked contribution, composition over time, workload mix. |
| `radar` | `axis,series,value[,min,max]` | Compact multi-metric profiles when axes are few and normalized honestly. |
| `image-grid` | `image,row,column[,label]` | Qualitative result grids from user-provided or permission-cleared images. |

Use only user-provided, audited public, or permission-cleared paper data.

## Helper Behavior

- `plot_series`: sorts numeric x values within each series and draws error bars when `yerr` exists.
- `plot_grouped_bar`: groups categories, adds black edges and hatch cycling for grayscale readability.
- `plot_dot_interval`: draws horizontal intervals with one dot per estimate.
- `plot_ecdf`: computes empirical CDF curves from raw values.
- `plot_heatmap`: builds a row/column matrix, masks missing cells white, and can add a colorbar.
- `plot_scatter`: draws grouped scatter/bubble plots and optional point labels.
- `plot_stacked_area`: draws stacked area data from repeated `x,series,y` rows.
- `plot_radar`: draws normalized radar charts; optional `min,max` columns define per-axis ranges.
- `plot_image_grid`: assembles a black-backed qualitative grid from local image files.
- `tighten_axis`: tighten x/y limits to observed data with a margin.
- `move_legend_outside` and `make_legend_axis`: keep large legends out of the data region.
- `add_direct_label`: use direct labels when a legend would create avoidable eye travel.
- `finalize_figure`: saves PDF, SVG, and PNG, then closes the figure.

Template refinements:

- `--annotate`: add compact value labels for `bar` and `heatmap`.
- `--legend-outside`: move legends outside the plotting area for supported chart families.
- `--xscale log` / `--yscale log`: use log axes when multiplicative differences matter.

## Guardrails

- Do not add demo numbers to the helper or template.
- Do not keep generated benchmark charts as reusable assets.
- Do not use `image-grid` with copied paper figures unless redistribution rights are explicit.
- Prefer direct labels or compact legends; do not let legends hide data.
- Use color plus marker, dash, hatch, or position. Hue alone is insufficient.
- Run `scripts/figure_audit.py` on exported files and inspect at final paper size.
