# Quality Checklist

Run this checklist before saying a data figure is submission-ready.

Items about file formats, DPI, size, accessibility and descriptions are source-backed in
`source-basis.md`. Domain-specific gates are operational checks; use them to catch data-figure
failures, but verify the final target venue instructions when they affect submission.

## Targeting

- Exact venue, domain, stage, and output width are known or a strict default was used.
- Annual CFP/author kit is checked when the user asks for a specific current conference.
- Publisher production rules are checked for camera-ready outputs.
- The readiness note names the profile used, for example `ACM/CCS security data plot`,
  `IEEE/CVF vision result grid`, or `USENIX systems latency plot`.

## Claim And Structure

- The figure supports one clear claim or comparison.
- Every panel is referenced from the caption or nearby text.
- Panel labels are consistent and ordered by reading flow.
- Captions define symbols, abbreviations, line styles, colors, and error bars.
- The figure does not duplicate a table unless visual comparison adds value.
- For architecture/schematic composites, the hero panel explains the claim and the support panels
  validate the claim rather than restating the same flow.

## Data Integrity

- Data provenance is known: user-provided, audited public source, or permission-cleared paper data.
- Axes start, scales, transformations, and omitted ranges are defensible and described.
- Error bars specify SD, SEM, CI, bootstrap interval, or another statistic.
- Sample size, benchmark version, seeds, workload, or project count is shown or stated when relevant.
- Qualitative examples are user-provided or permission-cleared and are not cherry-picked without explanation.
- AI-generated or edited imagery is disclosed if the venue requires it.
- Copyrighted third-party figures are not reused without permission.
- For architecture figures, every component, flow, and boundary must trace to user text, audited
  public material, or permission-cleared source material.

## Size And Readability

- Final width is chosen intentionally: single column, double column, or venue-specific.
- Text remains readable at final paper size, usually around 7-10 pt.
- No text overlaps at final paper size. Check axis labels, tick labels, legends, panel labels,
  callouts, direct labels, value annotations, colorbar labels, and heatmap cell labels.
- Labels do not collide with plotted marks in a way that changes the reading of the data.
- Line widths and markers remain visible after scaling.
- Legends do not hide data and are replaced by direct labels when cleaner.
- White space is cropped without clipping labels.

## Accessibility

- The figure is interpretable in grayscale.
- Color is not the only encoding for categories.
- Palette is colorblind-safe.
- Contrast is sufficient for print and projector viewing.
- ACM-style figure descriptions are prepared when applicable.
- For schematic-led figures, data/control/attack/defense flows remain distinguishable when printed
  without color.

## Technical Export

- Vector figures are exported as PDF/SVG/EPS where accepted.
- Raster figures meet the venue DPI and are not artificially upscaled.
- Fonts are embedded, converted to outlines, or chosen from safe publisher fonts.
- No external image links remain inside SVG files.
- The source file can regenerate the final export.
- The manuscript compiles with the figure included.
- `figure_audit.py` SVG text-overlap warnings are resolved or explicitly checked by rendered visual
  inspection before the figure is called ready.

## Domain-Specific Data Gates

- AI: train/eval data are not mixed; benchmark versions and variance are shown when relevant.
- Cybersecurity: attack-success, detection, FPR/FNR, overhead, and assumptions are defined.
- Software engineering: artifacts, datasets, benchmark/sample counts, and uncertainty are visible when relevant.
- PL: notation and metric definitions match the paper; runtime/compile/verification metrics are separated.
- Systems/networking: workload, hardware/topology context, units, and tail behavior are clear.

## Fast Audit Commands

Use the bundled audit script for file-level checks:

```bash
python scripts/figure_audit.py figures/main_result/exports/main_result.pdf
python scripts/figure_audit.py figures/results/exports/result.svg figures/results/exports/result.png
```

The script catches simple file/export issues. It does not replace visual inspection in the final paper template.
