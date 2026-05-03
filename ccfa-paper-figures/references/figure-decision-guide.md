# Figure Decision Guide

Choose the figure type before choosing the tool. A CCF-A figure should be easy to regenerate,
easy to edit, and easy to inspect at the final paper size.

Use `source-basis.md` for the provenance of hard export/layout rules. This guide is a routing layer:
it converts a user's venue/domain/figure-type request into a reproducible data-plot choice.

## Intake Slots

Before choosing a tool, fill these slots from the user's request:

| Slot | Examples | Effect |
|---|---|---|
| `venue` | CCS, ICSE, CVPR, NeurIPS, USENIX Security, PLDI | Select exact publisher/profile from `venue-map.md`. |
| `domain` | AI, cybersecurity, software engineering, PL, systems, networking | Select data checks from `domain-patterns.md`. |
| `stage` | submission, camera-ready, revision, rebuttal | Submission emphasizes anonymity/template; camera-ready emphasizes production export. |
| `figure type` | ablation, benchmark comparison, CDF, heatmap, qualitative grid, schematic overview | Select plot family and checklist. |
| `output target` | one-column, double-column, appendix, slide reuse | Select size and final text scale. |
| `style intent` | compact, ordinary camera-ready, showpiece, Nature-like, "make it impressive" | Decide whether to use a single chart or a richer non-redundant multi-panel page. |

If `venue` and `domain` disagree, ask one concise clarification or choose the exact venue when the
paper target is clear.

## Ambiguous Data-First Requests

When the user supplies data but does not specify a chart type, choose the most expressive valid
figure type yourself. Do not ask the user to name a chart unless the data are structurally ambiguous
or too sparse.

Default workflow:

1. Save the supplied data as CSV when needed.
2. Run `scripts/suggest_showpiece.py <csv> --venue <venue> --domain <domain> --style showpiece`.
3. Treat the emitted "Self-Prompt" as the internal plan for the figure.
4. Implement the richest non-redundant plan the data support.
5. Run `figure_audit.py`; fix text-overlap warnings before calling the output ready.

Showpiece does not mean decorative. It means higher information density, stronger panel hierarchy,
and more complete evidence when the data support it.

Recommended showpiece mappings:

| Data shape | Preferred showpiece |
|---|---|
| `system,model,scenario,<performance>` | Benchmark landscape: heatmap + Pareto/bubble + ECDF + composition. |
| `row,column,value` with many cells | Matrix-led composite: dominant heatmap + marginal summaries + distribution. |
| `x,y[,series,size,label]` with many points | Pareto/trade-off landscape with sparse frontier labels and distributions. |
| `series,value` with many samples | Distribution-led composite with ECDF/CCDF, interval/rank, and sample counts. |
| `x,series,y` over a range | Scaling landscape with curves, endpoint ranking, and sensitivity/breakdown panel. |

## Quantitative Results

Use Matplotlib/Seaborn when the source is tabular or experimental data.

Best for:

- Ablation studies, baselines, sensitivity analysis, scaling curves.
- Error bars, confidence intervals, box/violin plots, ECDF/CCDF, Pareto frontiers.
- Multi-panel result summaries.

Default workflow:

1. Start from `assets/templates/matplotlib_result_plot.py`.
2. Apply `assets/ccfa_matplotlib.mplstyle`.
3. Use the Okabe-Ito palette or another colorblind-safe palette.
4. Encode series by color plus marker/dash/hatch.
5. Export PDF/SVG first, PNG/TIFF only when required.

When the target is:

- AI: include variance, seeds, benchmark versions, and train/test separation when relevant.
- Security: include attack success, detection, false-positive, or overhead definitions.
- Software engineering: include benchmark/project/sample count and statistical uncertainty.
- Systems/networking: include workload, hardware, topology, and tail-latency/throughput units.

Use SciencePlots when installed and helpful, especially `science` plus `ieee`, but do not make the
skill depend on it. The local style file is the fallback.

## LaTeX-Native Numeric Plots

Use PGFPlots when exact LaTeX typography or math-heavy labels matter.

Best for:

- Small mathematical plots.
- Compact benchmark plots embedded directly in LaTeX.
- Result plots whose labels must match paper notation.

Default workflow:

1. Start from `assets/templates/tikz_pgfplots.tex`.
2. Keep data in CSV where practical.
3. Compile to PDF and inspect line widths and font sizes at column width.

Do not use PGFPlots as a loophole for architecture or workflow schematics. Use the Matplotlib
schematic-composite path unless the user explicitly needs LaTeX-native source.

## Schematic-Led Architecture Composites

Use Matplotlib schematic composites when the source is a user-provided or audited model, system,
workflow, threat boundary, or data/control-flow description.

Best for:

- AI model/data-flow overviews with ablation or benchmark evidence below.
- Systems/networking architecture overviews with latency, throughput, scaling, or resource evidence.
- Security threat-boundary or attack/defense workflows with detection, success-rate, or overhead
  evidence.
- Software-engineering tool/benchmark pipelines with pass-rate, correctness, time, or coverage
  evidence.

Default workflow:

1. Read `references/schematic-patterns.md`.
2. Start from `assets/templates/matplotlib_schematic_composite.py`.
3. Build the JSON spec only from user-provided, audited public, or permission-cleared content.
4. Use semantic `kind` fields for component, flow, and boundary roles so data/control/attack/defense
   paths remain distinguishable in grayscale and do not rely on color alone.
5. Make one dominant schematic hero panel; add quiet subordinate data panels only when real data are
   available.
6. Export PDF/SVG first and audit the outputs.

Do not invent components, flows, threat actors, benchmark names, screenshots, or metrics. Do not copy
published paper architecture diagrams unless reuse rights are explicit.

## Raster Result Content

Use raster only when the data is inherently raster: screenshots, images, dense visual examples,
camera frames, or qualitative result grids.

Rules:

- Keep original resolution; do not upscale as a fix.
- Add labels/arrows in vector overlay when possible.
- Export final raster at the venue DPI.
- Avoid JPEG for plots.
- Crop consistently and document whether any image was resized, normalized, blurred, or masked.
- Use permission-cleared or user-provided examples. Do not invent qualitative examples.

## Non-Default Diagram-First Tools

Do not route active requests to Graphviz, Mermaid, or D2 by default. Public architecture/process/
security assets may be retained in `assets/reference-materials/` only after passing
`public-material-audit.md`; they are audited references, not permission to copy paper figures.

## Common Data-Figure Archetypes

- Experimental summary: 2-4 panel Matplotlib figure with consistent axes and visible uncertainty.
- Ablation: grouped bar, dot/interval, or line plot with full method and strongest baseline clear.
- Distribution: ECDF/CCDF, box/violin, histogram, or raincloud when skew matters.
- Latency/throughput: line, scatter, Pareto frontier, or CDF with units and workload context.
- Robustness/sensitivity: curve or heatmap with tested range and failure regions visible.
- Qualitative grid: comparable examples plus quantitative summary, not an oversized collage.
- Matrix/adjacency: heatmap or sparse matrix view when structure matters and labels remain readable.
- Schematic-led composite: dominant model/system/workflow overview plus smaller evidence panels.
