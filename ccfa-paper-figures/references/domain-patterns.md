# Domain Patterns

Use this file after `venue-map.md` when the user specifies a domain or a venue whose figure culture is
domain-specific.

This file contains operational synthesis for data figures, not venue policy. For traceability, read
`source-basis.md`: official format/accessibility rules come from ACM, IEEE, USENIX, ICML, CVPR and
CCF pages; domain-specific patterns are retained only when they are consistent with those sources and
the curated public papers in `paper-exemplars.md`.

## AI And Machine Learning

Expected data-figure types:

- Experimental summary: accuracy/F1/AUROC, calibration, robustness, latency, memory, data efficiency.
- Ablation: components, data size, model size, prompt variants, retrieval modules, or augmentation.
- Scaling: parameter count, dataset size, compute, tokens, latency, throughput, or memory.
- Qualitative results: image/text/code samples only when user-provided or permission-cleared.

Checks:

- Separate train/validation/test and inference-time measurements.
- Do not imply causal importance from attention/saliency alone.
- Show uncertainty or repeats when benchmark variance matters.
- Avoid qualitative cherry-picking; label examples as representative, typical, or failure cases.
- Use consistent colors for method families across all panels.

Recommended encodings:

- Scaling curves: log x-axis when appropriate, direct labels, confidence bands or error bars.
- Ablations: grouped bars or dot/interval plots; include full method and strongest baseline.
- Trade-offs: Pareto scatter with latency/compute on one axis and quality on the other.
- Confusion/error: normalized heatmaps with readable labels, not dense unreadable matrices.

## Cybersecurity

Expected data-figure types:

- Attack/defense evaluation: attack success rate, detection rate, FPR/FNR, overhead, robustness.
- Timing/reliability: exploit timing, detection latency, retry count, failure rate, time-to-compromise.
- Sensitivity: attacker budget, noise, patch level, configuration, dataset, or threshold.
- Measurement summary: vulnerability counts, campaign frequency, affected versions, or severity mix.

Checks:

- Define attack success, detection, FPR/FNR, and overhead precisely.
- State assumptions in labels or captions when they shape the result.
- Distinguish capability, action, observation, and inference in metric names.
- Use red for attacker/failure only if redundant labels and shapes also identify the role.
- Use CDF/CCDF for timing and reliability instead of mean-only bars when distributions are skewed.

Recommended encodings:

- CDF/CCDF for exploit timing, overhead, detection latency, and reliability.
- Small multiples for defense performance across attacks, datasets, or configurations.
- Dot/interval plots for per-benchmark or per-CVE effects.
- Stacked bars only when categories sum to a meaningful total.

## Software Engineering

Expected data-figure types:

- Empirical result: benchmark-level distributions, per-project results, effect sizes, time/cost.
- Repair/testing/evaluation: pass rate, patch correctness, flaky tests, mutation score, coverage.
- Dataset/benchmark composition: project count, issue class, language, test count, or time span.
- Case study: source snippet or bug trace plus the quantitative context.

Checks:

- Include benchmark/project/sample count where relevant.
- Use paired plots when comparing tools on the same projects.
- Avoid mean-only bars for skewed distributions; prefer box, violin, ECDF, or dot/interval.
- Distinguish training, tuning, and held-out evaluation.
- Keep project IDs readable or aggregate only when aggregation is statistically defensible.

Recommended encodings:

- Raincloud/box/violin for distributions.
- Forest/dot interval for per-project effect sizes.
- ECDF for time-to-fix, test runtime, patch count, or issue-resolution distributions.
- Heatmap for tool-by-project or category-by-benchmark matrices when labels remain legible.

## Programming Languages

Expected data-figure types:

- Empirical PL result: runtime, memory, compile time, verification time, bug finding, soundness
  coverage, benchmark-suite comparisons.
- Sensitivity: program size, optimization level, solver timeout, threads, or analysis precision.
- Small notation-heavy numeric plots embedded in LaTeX.

Checks:

- Keep notation consistent with the paper.
- Prefer PGFPlots for mathematical typography when plots live near formal notation.
- Use tables instead of figures for tiny formal comparisons when visual comparison adds no value.
- Separate compile-time, runtime, and verification-time metrics.

Recommended encodings:

- PGFPlots or Matplotlib line/scatter plots for benchmark scaling.
- Dot/interval plots for per-benchmark speedup or memory change.
- Log scale for runtime ratios when multiplicative effects matter.

## Systems, Architecture, And Networking

Expected data-figure types:

- Evaluation: latency, tail latency, throughput, scalability, CPU/memory/IO breakdown, cost, energy.
- Distribution: request latency, queueing delay, flow completion time, packet loss, failure recovery.
- Sensitivity: cluster size, node/GPU count, workload, cache size, batch size, topology, trace.

Checks:

- Put units on every measurement axis.
- Show workload, cluster size, dataset, trace, or hardware context when it affects interpretation.
- Avoid starting y-axes at non-zero for latency/throughput unless the caption makes it explicit.
- Use log scales only when multiplicative differences matter and tick labels stay clear.
- Tail latency and CDF plots must define percentile or distribution clearly.

Recommended encodings:

- CDF/CCDF for latency distributions.
- Stacked bars for resource breakdown only when components sum to a meaningful total.
- Line plots for scalability with markers and error bars.
- Pareto/frontier scatter for latency-throughput or cost-quality trade-offs.
