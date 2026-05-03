# Source Basis

Use this file when you need traceability for a rule in `ccfa-paper-figures`. Keep the line between
official policy and operational synthesis explicit.

## Rule Classes

- `[official]` direct vendor / society / venue / author-kit guidance.
- `[synthesized]` operational pattern inferred from official guidance plus curated papers.
- `[reference-only]` material retained as an audited reference for active schematic work; not a
  default copied template.

## Official Sources

| Rule cluster | Basis | Use |
|---|---|---|
| ACM figure formats | ACM TAPS image specifications; ACM figure descriptions | SVG/PS/EPS/PDF/PNG/JPG/EMF/TIFF acceptance, font embedding/outlining, whitespace removal, figure descriptions. |
| IEEE figure sizing | IEEE resolution and size; IEEE file formatting; IEEE graphics guidance | 3.5 in / 7.16 in widths, >300 dpi color/grayscale, >600 dpi line art, vector preference. |
| USENIX paper layout | USENIX conference paper templates | U.S. letter, two-column, 7 x 9 text block, 10-point Times-like body text, template/blinding reminder. |
| ICML accessibility | ICML 2026 author instructions | Accessible submissions are encouraged. |
| CVPR review policy | CVPR 2026 author guidelines | Double-blind review and anonymity constraints for submission materials. |
| CCF routing | CCF academic evaluation directory and official category pages | Venue-family routing and A-conference lists for AI, security, SE/PL/systems, networks, and architecture/storage. |
| Public material reuse | `public-material-audit.md` plus source license pages | Decides whether a public material is bundle-ok, data-only, link-only, reject, or reference-only. |
| Extension gates | `extension-gates.md` | Defines the minimum bar for adding venues, materials, templates, scripts, gallery assets, reference material, and Stable status. |

## Operational Synthesis

| Pattern | Basis | Why it belongs |
|---|---|---|
| Keep one dominant result question and subordinate evidence panels | Synthesis from Nature-style and CCF-A exemplar figures | Prevents redundant multi-panel pages. |
| Use direct labels when the legend would be larger than the figure logic | ACM figure-description guidance + CCF-A exemplars | Improves readability at paper size. |
| Keep train/eval, source/target, attacker/defender, and workload contexts visually distinct in data plots | Official review/layout guidance + exemplar figures | Prevents leakage of meaning between panels. |
| Prefer one method family color across a figure | IEEE/ACM accessibility expectations + exemplar figures | Reduces visual noise and helps grayscale fallback. |
| Define security metrics such as attack success, FPR/FNR, detection, and overhead in the figure/caption | Security-paper evaluation pattern | Makes data plots interpretable outside the full method text. |
| Show benchmark IDs, sample counts, seeds, workload, or hardware context in empirical figures when relevant | Empirical CS exemplar pattern | Helps the plot survive outside the paper text. |

## Reference Material Basis

Architecture/process/security-diagram assets under `assets/reference-materials/` are backed by
official project repositories and license files recorded in `public-material-audit.md`. They support
active schematic-led figure work as audited references, but they do not justify copying paper figures
or inventing source content.

## Linked Sources And Ledgers

- ACM TAPS image specifications:
  https://authors.acm.org/proceedings/production-information/taps-image-specifications
- ACM figure descriptions:
  https://authors.acm.org/proceedings/production-information/describing-figures
- IEEE resolution and size:
  https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/
- IEEE file formatting:
  https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/
- IEEE conference graphics guidance:
  https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/improve-your-graphics/
- USENIX conference paper templates:
  https://www.usenix.org/templates-conference-papers
- ICML 2026 author instructions:
  https://icml.cc/Conferences/2026/AuthorInstructions
- CVPR 2026 author guidelines:
  https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines
- CCF academic evaluation directory:
  https://www.ccf.org.cn/Academic_Evaluation/By_category/
- CCF AI:
  https://www.ccf.org.cn/Academic_Evaluation/AI/
- CCF network and information security:
  https://www.ccf.org.cn/Academic_Evaluation/NIS/
- CCF software engineering / system software / programming languages:
  https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/
- CCF computer networks:
  https://www.ccf.org.cn/Academic_Evaluation/CN/
- CCF architecture / parallel and distributed computing / storage systems:
  https://www.ccf.org.cn/Academic_Evaluation/ARCH_DCP_SS/
- Public material audit ledger:
  public-material-audit.md
- Extension gate ledger:
  extension-gates.md

## Notes

- Do not treat every synthesized pattern as a policy rule. Some are layout heuristics that help the
  figure read well but are not stated verbatim by a venue.
- When a pattern can be traced to an official page, prefer that page over memory or local convention.
- When a rule is only a heuristic, label it as such in the operational file that uses it.
