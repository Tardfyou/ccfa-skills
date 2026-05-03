# Readiness Note

Figure ID: `fig4-single-cell-systems-style`

Venue profile used: OSDI / SOSP systems-paper profile. The figure is prepared at double-column width (`7.16 in`) with PDF/SVG vector-first exports, 600 dpi PNG fallback, restrained colors, redundant encodings, and final-size text kept at or above roughly 6 pt for dense labels.

Artifacts:

- Source CSV: `data/mlcommons_inference_v5_1_public_summary_audited.csv`
- Plotting source: `source/plot_fig4_single_cell_systems_style.py`
- Matplotlib style: `source/ccfa_matplotlib.mplstyle`
- Exports: `exports/fig4_single_cell_systems_style.pdf`, `exports/fig4_single_cell_systems_style.svg`, `exports/fig4_single_cell_systems_style.png`
- Audit log: `exports/figure_audit.txt`
- Caption draft and figure description: `caption_draft.md`

Data provenance and integrity:

- Input data are the user-supplied audited public benchmark CSV derived from MLCommons Inference v5.1 `summary_results.json`.
- The CSV contains 41 rows: 20 Offline, 20 Server, and 1 Interactive measurement across 20 system labels and 4 model labels.
- The plotting script validates required columns and rejects duplicate `system` / `model` / `scenario` rows.
- Figure values are derived only by pivoting, counting rows, pairing Offline/Server rows, and computing `tokens_s / accelerators` for panel c.
- Panel-a annotations are rounded to nearest thousand for readability; exact values remain in the CSV.
- Missing scenario measurements are explicitly marked `n/a`.

Audit result:

- `figure_audit.py` passes for PDF, SVG, and PNG.
- PDF and SVG are vector-capable. The audit notes raster image elements because Matplotlib encodes the continuous colorbar gradient as an image; plot text, axes, markers, and heatmap cells remain editable vector elements.
- PNG export is 4390 x 4766 px at 600 dpi.

Visual/readiness checks:

- Panel a is intentionally dominant; panels b-d use quieter support scales.
- Model family is consistently encoded by color and hatch; model variants use marker shape and line style in the scatter/ECDF panels.
- Units are included on throughput axes and colorbar.
- Final manuscript integration should still verify caption spacing, exact column placement, and grayscale reproduction in the target OSDI/SOSP template.
