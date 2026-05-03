# Venue Map

Use this file when the user names a conference, journal, publisher, or domain. Prefer the exact
current-year CFP, author kit, and proceedings instructions for the final target. This file gives a
strict data-figure default when the exact venue instructions are not available.

Research notes:

- CCF official pages and a third-party mirror were checked on 2026-05-03.
- Public official pages expose CCF recommended international conference and journal category tables.
  A CCF landing page for academic evaluation also exists and should be checked before final
  submission advice.
- Treat CCF membership as a routing aid for data-figure style, not as a claim about paper quality.

## Targeting Decision Tree

1. Exact venue named: use the venue row below.
2. Exact venue absent but publisher known: use publisher profile.
3. Only domain named: use the domain profile.
4. Nothing named: use `unknown-strict`.

When stage is `camera-ready`, prioritize publisher production rules. When stage is `submission`,
prioritize the annual author kit and anonymity policy.

## Exact Venue Profiles

| Venue | Domain | Publisher/profile | Data-figure defaults |
|---|---|---|---|
| AAAI | AI | AAAI author kit | PDF vector result plots; accessible colors; verify current AAAI template. |
| NeurIPS | AI/ML | NeurIPS annual style | PDF vector result plots; avoid unreadable tiny ablation grids; current-year style wins. |
| ICML | AI/ML | PMLR/ICML annual style | LaTeX-first; PDF vector figures; accessibility encouraged; current-year style wins. |
| ACL | NLP/AI | ACL Rolling Review / ACL anthology style | Figure text must survive two-column PDF; define task/data abbreviations in caption. |
| CVPR, ICCV | Vision/AI | CVF / IEEE profile | Qualitative grids need consistent crops; vector labels around raster examples; avoid tiny image mosaics. |
| IJCAI | AI | IJCAI author kit | PDF vector result plots; verify current page/file rules. |
| CCS | Cybersecurity | ACM profile | Data plots should define attack success, detection, FPR/FNR, overhead, and assumptions. |
| S&P, IEEE S&P | Cybersecurity | IEEE profile | Use IEEE-compatible figure sizes/formats; grayscale and redundant encoding are mandatory. |
| USENIX Security | Cybersecurity | USENIX profile | Two-column USENIX style; security result plots must be readable when printed grayscale. |
| NDSS | Cybersecurity | Internet Society/NDSS author instructions | Verify current templates; use security data-figure checks. |
| CRYPTO, EUROCRYPT | Cryptography | IACR/LNCS-like profile | Prefer LaTeX-native numeric plots and clear notation for result comparisons. |
| ICSE | Software engineering | ACM/IEEE profile by year | Empirical plots need benchmark/sample context and uncertainty. |
| FSE/ESEC | Software engineering | ACM profile | ACM figure formats and descriptions; empirical plots with statistical clarity. |
| ASE, ISSTA, FM | Software engineering / formal methods | ACM/IEEE/profile by year | Show baselines, data splits, statistical tests, and benchmark details. |
| PLDI, POPL, OOPSLA | PL | ACM profile | Runtime, compile-time, memory, and verification plots should use paper notation consistently. |
| SOSP | Systems | ACM profile | Measurement figures must show workload, hardware context, and bottleneck metric. |
| OSDI, FAST, USENIX ATC | Systems/storage | USENIX profile | Two-column USENIX; latency/throughput/CDF figures must be clear at column width. |
| EuroSys | Systems | ACM profile | Workload-aware evaluation; verify current EuroSys author instructions. |
| SIGCOMM | Networking | ACM profile | Performance figures need clear traffic direction, units, uncertainty, and topology/workload context. |
| MobiCom | Networking/mobile systems | ACM profile | Measurement figures need scenario, trace, device, and link assumptions. |
| INFOCOM | Networking | IEEE profile | Use IEEE-compatible sizes and redundant encodings for line-heavy performance plots. |
| NSDI | Networking/systems | USENIX profile | Use USENIX defaults; evaluate grayscale readability for line-heavy plots. |
| ASPLOS, ISCA, MICRO, HPCA | Architecture | ACM/IEEE profile by year | Hardware/system evaluation plots must expose workload, units, and resource context. |
| DAC | Design automation | ACM/IEEE profile by year | Prefer compact benchmark plots with clear circuit/EDA metrics and units. |
| SC | High-performance computing | ACM/IEEE profile by year | Scaling figures need hardware, node/GPU count, workload, and communication/computation breakdowns. |
| PPoPP | Parallel programming | ACM profile | Runtime/scalability plots need execution model, synchronization metric, workload, and uncertainty. |

## Domain Profiles

### AI

Typical CCF-A examples: AAAI, NeurIPS, ACL, CVPR, ICCV, ICML, IJCAI.

Default data-figure mix:

- Results: ablation, scaling, robustness, calibration, data-efficiency, and latency/accuracy trade-off.
- Qualitative grids: consistent crop, comparable examples, vector method labels, and no oversized collage.
- Benchmark summaries: include dataset version, metric definition, seeds or uncertainty when relevant.

### Cybersecurity

Typical CCF-A examples: CCS, EUROCRYPT, IEEE S&P, CRYPTO, USENIX Security, NDSS.

Default data-figure mix:

- Evaluation: attack success rate, detection rate, false positives/negatives, overhead, exploitability, and sensitivity curves.
- Distribution: exploit timing, detection latency, retry reliability, and overhead CDF/CCDF.
- Dataset/case summaries: vulnerability counts, severity mix, affected products, and benchmark composition.

### Software Engineering

Typical CCF-A examples: FSE/ESEC, ASE, ICSE, ISSTA; related PL/system venues include PLDI, POPL,
OOPSLA, SOSP, OSDI, FM.

Default data-figure mix:

- Empirical results: distributions, paired comparisons, effect sizes, confidence intervals, and sample sizes.
- Benchmark composition: projects, languages, issue classes, test counts, and time/cost.
- Case study: representative example plus quantitative summary, not only a screenshot.

### Programming Languages

Typical CCF-A examples: PLDI, POPL, OOPSLA.

Default data-figure mix:

- Empirical PL results: compile time, runtime, memory, verification time, bug finding, and benchmark suites.
- Sensitivity plots: optimization level, program size, solver timeout, or analysis precision.
- Prefer PGFPlots when math notation must match LaTeX.

### Computer Networks

Typical CCF-A examples: SIGCOMM, MobiCom, INFOCOM, NSDI.

Default data-figure mix:

- Performance: latency CDF/CCDF, throughput, packet loss, scalability, and failure behavior.
- Measurement: trace/device/link assumptions, traffic direction, and units.
- Trade-offs: cost/latency, throughput/fairness, utilization/tail latency.

### Architecture, Storage, Parallel, And Distributed Systems

Typical CCF-A examples: PPoPP, FAST, DAC, HPCA, MICRO, SC, ASPLOS, ISCA, USENIX ATC, EuroSys.

Default data-figure mix:

- Performance: latency CDF, throughput, tail latency, scalability, resource breakdown, cost, and ablation.
- Sensitivity: cluster size, cache size, batch size, workload, dataset, and hardware configuration.
- Efficiency: energy, memory, IO, communication/computation breakdowns, and utilization.

## CCF A-Conference Routing Snapshot

Checked against official CCF category pages on 2026-05-03. Use it for routing; still verify the
current venue author kit before giving submission-specific instructions.

| CCF source category | A venues encoded in this file |
|---|---|
| Artificial intelligence | AAAI, NeurIPS, ACL, CVPR, ICCV, ICML, IJCAI |
| Network and information security | CCS, EUROCRYPT, IEEE S&P, CRYPTO, USENIX Security, NDSS |
| Software engineering / system software / programming languages | PLDI, POPL, FSE/ESEC, SOSP, OOPSLA, ASE, ICSE, ISSTA, OSDI, FM |
| Computer networks | SIGCOMM, MobiCom, INFOCOM, NSDI |
| Architecture / parallel and distributed computing / storage | PPoPP, FAST, DAC, HPCA, MICRO, SC, ASPLOS, ISCA, USENIX ATC, EuroSys |

## Publisher Profiles

### ACM / ACM TAPS

Use for many CCF-A venues such as SIGCOMM, CCS, FSE, OOPSLA, PLDI, POPL, SOSP, SIGMOD/PODS, CHI,
and many ACM Transactions.

Rules to respect:

- TAPS accepts SVG, PS, EPS, PDF, PNG, JPG, EMF, and TIFF.
- Convert Word drawing objects into image files before submission.
- Embed fonts or convert text to outlines for vector PDF/EPS/PS.
- Remove extra whitespace around image edges.
- Prepare figure descriptions when using ACM publishing workflows; descriptions are not captions.

Sources:

- https://authors.acm.org/proceedings/production-information/taps-image-specifications
- https://authors.acm.org/proceedings/production-information/describing-figures

### IEEE / IEEE Computer Society

Use for S&P, INFOCOM, ICDE, ICDM, TPAMI/TSE/TKDE, and IEEE-partnered proceedings such as CVPR/ICCV.

Rules to respect:

- Prefer vector formats: PS, EPS, or PDF.
- Accepted graphics include PS, EPS, PDF, PNG, and TIFF.
- Non-vector color/grayscale graphics should be at least 300 dpi; black-and-white line art should be
  at least 600 dpi.
- Common final widths: one column 3.5 in / 88.9 mm; two columns 7.16 in / 182 mm.
- Recommended fonts include Helvetica, Times New Roman, Arial, Cambria, and Symbol.
- Text should appear about 9-10 pt at full size.
- Do not use the Lena image.
- Check line graphs in grayscale and encode data with color plus shape/dash/labels.

Sources:

- https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/
- https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/
- https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/improve-your-graphics/

### USENIX

Use for USENIX Security, OSDI, FAST, NSDI-like workflows, ATC, and related systems/security venues.

Rules to respect:

- Start from the conference template and anonymity/blinding policy.
- Common proceedings format is two-column, U.S. letter, with a 7 in by 9 in text block and 10 pt
  Times-like body text.
- Ensure the submission PDF and embedded figures are intelligible when printed in grayscale.

Sources:

- https://www.usenix.org/templates-conference-papers
- https://www.usenix.org/conference/usenixsecurity22/submission-policies-and-instructions

## unknown-strict

Use when the user gives no venue and no domain:

- Single-column width: 3.5 in; double-column width: 7.16 in.
- Export PDF and SVG for vector figures; add PNG/TIFF only for raster submission.
- Use 7-10 pt final text, 0.7-1.2 pt lines, colorblind-safe palette, and redundant encodings.
- Keep source files reproducible and store exports separately.
