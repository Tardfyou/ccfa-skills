# Caption Draft

**Figure 4. MLCommons Inference v5.1 AI-system benchmark landscape.**  
(a) Dominant heatmap of audited public throughput results, with systems ordered by Offline throughput and cells reporting tokens/s rounded to thousands for in-figure readability. Missing scenario measurements in the supplied CSV are marked `n/a`. Row stripes encode model family. (b) Pareto view of systems that report both Offline and Server scenarios; bubble area encodes accelerator count, color encodes model family, and marker shape distinguishes the submitted model variant. The dashed line marks equal Offline and Server throughput. (c) Empirical CDF of Offline throughput per accelerator, computed as `tokens_s / accelerators` from the audited CSV and grouped by model. (d) Compact scenario composition showing the number of submitted rows by scenario and model family.

Data provenance: audited CSV supplied for this figure, derived from MLCommons Inference v5.1 `summary_results.json`; no numeric benchmark values were invented.

# ACM-Style Figure Description

Multi-panel benchmark summary. The upper panel is a heatmap with systems on rows and inference scenarios on columns, showing throughput in tokens per second. Lower panels show a Pareto scatterplot of Offline versus Server throughput, an ECDF of Offline throughput normalized by accelerator count, and stacked row counts by scenario and model family. Color and hatch encode model family; marker and line style distinguish model variants where applicable.
