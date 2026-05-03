---
name: ccfa-paper-figures
description: >-
  Create, redesign, review, or export publication-ready data/statistical figures and
  schematic-led architecture composites for CCF-A and top CS venues, especially AI,
  cybersecurity, software engineering, PL, systems, architecture, and networking. Use for
  ACM/IEEE/USENIX/NeurIPS/ICML/CVPR/ICCV/ACL/AAAI/IJCAI/ICSE/FSE/ASE/ISSTA/PLDI/POPL/OOPSLA/SOSP/OSDI/CCS/NDSS/S&P/SIGCOMM/NSDI-ready
  result plots, ablations, benchmark summaries, CDF/CCDF, latency-throughput, scalability,
  distributions, heatmaps, confusion matrices, scatter/Pareto, stacked-area, radar,
  qualitative grids, model/data-flow overviews, system architecture composites, security
  threat-boundary workflows, SE pipelines, Matplotlib/Seaborn/PGFPlots workflows, and
  camera-ready audits for vector export, embedded fonts, grayscale/colorblind safety, and
  final-size legibility.
---

# CCF-A Paper Figures

Produce figures as paper artifacts, not slide art. Prefer reproducible source plus
vector-first exports. Treat every figure as a claim-supporting object: it should answer one
research question, survive one-column scaling, and remain interpretable in grayscale.

Current scope covers data/statistical figures plus Nature-style schematic-led composites: one
dominant model/system/workflow/architecture panel, often with subordinate quantitative evidence
panels. Use Matplotlib primitives and audited/user-provided content for these schematics. Do not make
Graphviz, Mermaid, D2, or diagram-first workflow languages the default path.

## Source Discipline

- Use official venue, publisher, or author-kit instructions first.
- Use `references/source-audit.md` when a rule needs justification or when adding new web-derived
  material.
- Use `references/public-material-audit.md` before using any public figure, screenshot, dataset,
  benchmark table, icon, or architecture material as a reusable material source.
- Use `references/extension-gates.md` before extending venues, templates, scripts, examples, or
  bundled assets.
- Do not copy published paper figures into the active skill. Derive rules from observed data-figure
  patterns and cite source pages instead.
- Do not add self-drawn example figures to the reusable library. Generated figures are task outputs,
  not reusable examples, unless the user explicitly supplied and approved them.
- Do not invent numeric results, benchmark labels, architecture components, system names, workflow
  stages, screenshots, or paper examples. Require user-provided content, audited public material, or
  permission-cleared paper data/material.
- For architecture/schematic figures, draw only the user's described design or audited source
  material. Public paper figures remain link-only unless redistribution rights are explicit.
- Reuse the local Nature-style figure rules only where they generalize to CS data figures: editable
  SVG/PDF, restrained palettes, non-redundant panels, hero-panel hierarchy, and final-size
  readability.

## Resource Map

- `references/venue-map.md`: CCF-A venue families, publisher profiles, and data-figure defaults for
  AI, cybersecurity, software engineering, PL, systems, architecture, and networking.
- `references/figure-decision-guide.md`: choose Matplotlib/Seaborn or PGFPlots for data figures.
- `references/domain-patterns.md`: domain-specific result-plot patterns and integrity checks.
- `references/matplotlib-patterns.md`: publication Matplotlib conventions adapted from mature
  Nature-style resources.
- `references/plot-api.md`: reusable helper functions, CSV contracts, and export helpers.
- `references/chart-cookbook.md`: chart-family recipes for line, bar, dot-interval, CDF, heatmap,
  scatter, area, radar, image-grid, and multi-panel data figures.
- `references/schematic-patterns.md`: Nature-style schematic-led composites for CS
  model/data-flow, system architecture, security overview, and SE workflow figures.
- `references/quality-checklist.md`: final readiness checklist for data figures.
- `references/source-basis.md`: rule-to-source traceability, separating official policy from
  operational synthesis.
- `references/source-audit.md`: audited official sources and material-retention decisions.
- `references/public-material-audit.md`: strict audit ledger for public materials and reuse status,
  including audited architecture materials.
- `references/extension-gates.md`: mandatory gates for extending venues, materials, templates,
  scripts, gallery assets, reference material, and Stable status.
- `references/paper-exemplars.md`: curated link-only paper references for data-figure inspiration.
- `scripts/figure_audit.py`: lightweight export audit for PDF/SVG/PNG/JPEG/TIFF.
- `scripts/suggest_showpiece.py`: profile a supplied CSV and emit a high-information figure plan
  plus a self-prompt for vague data-first requests.
- `scripts/scaffold_figure.py`: create a venue/domain-aware data-figure workspace from existing
  plotting templates.
- `assets/ccfa_matplotlib.mplstyle`, `assets/templates/ccfa_plot_helpers.py`,
  `assets/templates/matplotlib_result_plot.py`,
  `assets/templates/matplotlib_schematic_composite.py`, `assets/templates/tikz_pgfplots.tex`,
  `assets/gallery/`, and `assets/chart-atlas/`: data-plot and schematic-composite source templates
  plus migrated Nature baseline previews.
- `assets/reference-materials/`: audited public architecture/process/security materials. Treat these
  as reference material, not preapproved reusable templates; check `public-material-audit.md` before
  use.

## Workflow

1. Parse the user's targeting information before designing:
   - `venue`: exact conference or journal if named, such as `CCS`, `ICSE`, `CVPR`, `NeurIPS`,
     `USENIX Security`, `S&P`, `PLDI`, or `OSDI`.
   - `domain`: AI, cybersecurity, software engineering, programming languages, systems,
     architecture, or networking.
   - `stage`: submission, rebuttal, camera-ready, journal revision, slide reuse, or unknown.
   - `figure type`: result comparison, ablation, CDF/CCDF, scalability, latency-throughput,
     distribution, heatmap, confusion matrix, robustness, calibration, qualitative result grid, or
     case-study data summary, schematic-led composite, model overview, system architecture,
     security/threat-boundary overview, or SE workflow/pipeline.
   - `style intent`: strict/compact, ordinary camera-ready, or showpiece/high-impact/most visually
     expressive. If the user gives only data and a vague style request, infer `showpiece` only when
     the data are rich enough to support a non-redundant multi-panel figure.
2. Choose the strictest profile from exact venue first, then domain, then publisher family. Load
   `references/venue-map.md` for venue mapping and `references/domain-patterns.md` for domain
   patterns. If unknown, use the strict profile: PDF/SVG source, 3.5 in single-column or 7.16 in
   double-column, common embedded fonts, colorblind-safe palette, and grayscale readability.
3. For vague data-first requests, profile the CSV before choosing the chart:
   - Run `scripts/suggest_showpiece.py <csv> --venue <venue> --domain <domain> --style showpiece`
     when the user says things like "make it high-quality", "more impressive", "Nature-like",
     "show the data well", or gives only a CSV plus this skill.
   - Use the emitted plan as an internal self-prompt. Do not ask the user to choose a chart unless
     the data are too small, ambiguous, or missing the claim-critical variables.
   - Prefer the richest non-redundant data page that the CSV supports: matrix-led landscape,
     benchmark landscape, Pareto/trade-off composite, distribution-led composite, or scaling
     composite.
   - Reject forced complexity. If the CSV has too few rows or only one meaningful variable, choose a
     clean single-family chart and explain why a showpiece layout would be misleading.
4. Classify the figure:
   - Tabular experimental data: use Matplotlib/Seaborn with `assets/ccfa_matplotlib.mplstyle`.
     The bundled Matplotlib template supports `line`, `bar`, `dot-interval`, `cdf`, `heatmap`,
     `scatter`, `area`, `radar`, and `image-grid` CSV contracts.
   - Schematic-led architecture/model/workflow composite: read `references/schematic-patterns.md`
     and use `assets/templates/matplotlib_schematic_composite.py`. Put the schematic in a dominant
     hero panel and place optional quantitative evidence below it. The JSON spec must come from
     user-provided, audited public, or permission-cleared content. Use semantic `kind` slots for
     components, arrows, and boundaries when the architecture has data, control, attack, defense,
     runtime, storage, human, external, deployment, or trust roles.
   - LaTeX-native numeric plots: use PGFPlots when paper font consistency matters most.
   - Dense heatmaps, qualitative result grids, UI/image examples, or screenshots: keep raster
     content at submission DPI, add labels in vector overlay where possible, and avoid invented or
     cherry-picked examples.
5. Create a figure folder when generating assets:
   `figures/<figure-id>/source`, `figures/<figure-id>/exports`, and `figures/<figure-id>/data` when
   data are available.
6. Export at least one editable source and one publication file:
   - Preferred: `.pdf` plus `.svg` for vector figures.
   - IEEE-compatible: `.pdf`, `.eps`, `.png`, or `.tiff`; avoid JPEG for plots.
   - ACM TAPS-compatible: `.svg`, `.pdf`, `.eps`, `.png`, `.jpg`, `.tiff`, or `.emf`.
7. Audit final exports with `scripts/figure_audit.py` where possible, then inspect visually at final
   paper size. Do not call a figure ready until small text, legends, color encodings, uncertainty
   notation, panel labels, and all text placement are readable with no overlaps.

## Data-Figure Rules

- Use vector graphics for line art, charts, plots, axes, labels, and legends.
- Use color plus redundant encoding: marker shape, dash style, hatch, annotation, or direct label.
- Avoid `jet`, rainbow heatmaps, 3D chart effects, decorative shadows, low-contrast text, and
  screenshot-only evidence.
- Do not accept overlapping text. Axis labels, tick labels, legends, annotations, panel letters,
  callouts, direct labels, colorbar labels, and in-cell heatmap text must not collide with each other
  or with dense marks at final paper size.
- Keep final-size axis/tick/legend text around 7-10 pt unless the venue template requires otherwise.
- Put units in axis labels, define acronyms in the caption, and keep captions out of the image.
- Make every multi-panel figure non-redundant: main result, mechanism, boundary, robustness, or case
  panels should each answer a different question.
- For ACM submissions, prepare figure descriptions separately from captions when applicable.
- For cybersecurity data figures, define attack success, detection rate, FPR/FNR, overhead, and
  assumptions in labels or captions.
- For software engineering data figures, show sample size, benchmark identity, project splits, and
  statistical uncertainty when relevant.
- For AI data figures, show train/validation/test separation, benchmark versions, seeds or variance,
  and avoid qualitative cherry-picking.

## Schematic And Architecture Rules

- Use a dominant schematic/overview panel when the central claim is mechanism, architecture,
  workflow, or data/control flow; allocate about half the figure height to it when supporting plots
  are present.
- Draw semantic elements only: components, stages, data stores, trust boundaries, tensor/data/control
  flows, attack/defense roles, or evidence callouts. Avoid decorative icons and generic clip art.
- Reuse the schematic palette in subordinate plots so the page reads as one claim, not as a
  dashboard.
- Keep source editable: prefer Matplotlib patches, text, arrows, and raster image plates only when
  the underlying image is user-provided or permission-cleared.
- Do not copy architecture diagrams from papers into generated outputs unless the user has reuse
  rights. If using public architecture material as inspiration, cite it and keep it link-only unless
  `public-material-audit.md` says bundling is allowed.

## Tool Preference

- Matplotlib/Seaborn: empirical plots, ablations, distributions, error bars, Pareto/frontier charts,
  CDF/CCDF, latency-throughput, robustness, calibration, and attack-success curves.
- PGFPlots/TikZ: LaTeX-native numeric plots and compact math-heavy result plots. Keep CSV data
  external and do not invent values.
- Raster plus vector overlay: qualitative result grids, UI screenshots, dense image evidence, and
  camera/image panels when the underlying material is permission-cleared.
- Matplotlib schematic composite: model/data-flow overview, system architecture, security workflow,
  threat-boundary overview, and software-engineering pipeline figures when the content is supplied
  or audited.

Do not select Graphviz, Mermaid, D2, or diagram-first workflows as the default. Use them only when
the user explicitly requests that source language and accepts that it is outside the Nature-style
Matplotlib composite path.

## Deliverables

When creating a figure, provide:

- Source file(s): `.py`, `.tex`, `.csv`, `.svg`, or other reproducible data/source files.
- Export file(s): at least `.pdf` or `.svg`; add `.png`/`.tiff` when raster submission is needed.
- A short caption draft, and an ACM-style figure description when useful.
- A readiness note: venue profile used, export formats, audit result, data provenance, and any checks
  that still require the manuscript template.
