# Source Audit

Use this file when adding or revising rules from web material. Keep only sources that pass the audit.
For rule-to-source traceability, use `source-basis.md`; this file records source-retention decisions.
For development and extension thresholds, use `extension-gates.md`.

## Acceptance Criteria

Keep a source when it is:

- Official venue, publisher, society, proceedings, or author-kit documentation.
- Current enough for the target task, or clearly marked as a stable production rule.
- Directly relevant to data figures, templates, accessibility, production formats, or CCF venue mapping.
- Paraphrased into actionable rules without copying long source text.
- Recorded in `public-material-audit.md` when the source contributes a figure, screenshot, dataset,
  benchmark table, icon, reference material, or reusable example material.

Reject or downgrade a source when it is:

- A blog post, social-media thread, private checklist, or unverified mirror, unless used only as a
  discovery aid.
- A published paper figure used as a visual style source without permission to redistribute.
- Any public material whose license or redistribution status cannot be established.
- Any Codex-generated figure proposed as a reusable example asset.
- Outdated annual author instructions for a year-specific venue, unless no current public page exists
  and the rule is clearly stable.
- In conflict with the current CFP or publisher production page.

## Audited Sources Kept

### CCF venue routing

- CCF academic evaluation directory landing page:
  https://www.ccf.org.cn/Academic_Evaluation/By_category/
- CCF AI category page:
  https://www.ccf.org.cn/Academic_Evaluation/AI/
- CCF network and information security category page:
  https://www.ccf.org.cn/Academic_Evaluation/NIS/
- CCF software engineering / system software / programming languages page:
  https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/
- CCF computer networks page:
  https://www.ccf.org.cn/Academic_Evaluation/CN/
- CCF computer architecture / parallel and distributed computing / storage systems page:
  https://www.ccf.org.cn/Academic_Evaluation/ARCH_DCP_SS/
- Third-party CCF mirror used only for cross-checking category rows, not as the final authority:
  https://ccf.atom.im/

Decision: keep official CCF links as primary routing sources. Use the mirror only to quickly inspect
tables when CCF dynamic pages are hard to parse.

Verified on 2026-05-03:

- AI A-conference routing: AAAI, NeurIPS, ACL, CVPR, ICCV, ICML, IJCAI.
- Network and information security A-conference routing: CCS, EUROCRYPT, S&P, CRYPTO, USENIX
  Security, NDSS.
- Software engineering / system software / programming languages A-conference routing: PLDI, POPL,
  FSE, SOSP, OOPSLA, ASE, ICSE, ISSTA, OSDI, FM.
- Computer networks A-conference routing: SIGCOMM, MobiCom, INFOCOM, NSDI.
- Computer architecture / parallel and distributed computing / storage systems A-conference routing:
  PPoPP, FAST, DAC, HPCA, MICRO, SC, ASPLOS, ISCA, USENIX ATC, EuroSys.

### ACM

- ACM TAPS image specifications:
  https://authors.acm.org/proceedings/production-information/taps-image-specifications
- ACM figure descriptions:
  https://authors.acm.org/proceedings/production-information/describing-figures

Decision: keep. These are official ACM production/accessibility pages and directly specify formats
and figure-description practice.

### IEEE

- IEEE resolution and size:
  https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/
- IEEE file formatting:
  https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/
- IEEE conference graphics guidance:
  https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/improve-your-graphics/

Decision: keep. These are official IEEE author-center pages and support size, DPI, format, font, and
grayscale guidance.

### USENIX

- USENIX conference paper templates:
  https://www.usenix.org/templates-conference-papers
- USENIX Security submission policies example:
  https://www.usenix.org/conference/usenixsecurity22/submission-policies-and-instructions

Decision: keep with caveat. The template page is stable and official. The USENIX Security 2022 page is
used only for general workflow cues; exact annual policy must be checked for the target year.

### AI / CVF examples

- ICML 2026 author instructions:
  https://icml.cc/Conferences/2026/AuthorInstructions
- CVPR 2026 author guidelines:
  https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines

Decision: keep as examples of current annual author instructions. Exact target year still wins.

### Paper exemplars

- Segment Anything:
  https://arxiv.org/abs/2304.02643
- Large Language Models are Zero-Shot Reasoners:
  https://proceedings.neurips.cc/paper_files/paper/2022/hash/8bb0d291acd4acf06ef112099c16f326-Abstract-Conference.html
- Efficient Memory Management for Large Language Model Serving with PagedAttention:
  https://arxiv.org/abs/2309.06180
- SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
  https://arxiv.org/abs/2310.06770
- Misbinding Attacks on Secure Device Pairing and Bootstrapping:
  https://arxiv.org/abs/1902.07550

Decision: keep as linked references only. Do not bundle their paper figures unless redistribution
rights are explicitly checked and recorded. Use the public abstract/proceedings/arXiv pages for
attribution, then paraphrase reusable data-figure patterns.

### Audited architecture reference materials

Official repository raw assets and licenses were checked on 2026-05-03 for SAM, SAM 2, vLLM,
SWE-bench, and OWASP Threat Dragon. Detailed local path, source URL, license, quality decision, and
hash are recorded in `public-material-audit.md`.

Decision: keep only under `assets/reference-materials/`. These materials support active schematic-led
composites through audited reference material, but they do not authorize copied paper figures or
invented architecture content.

## Material Intentionally Not Kept

- Published paper figures from CCF-A venues: not bundled or copied because the skill should not
  redistribute copyrighted content. Only general, paraphrased data-figure layout patterns are retained.
- Local synthetic CCF-A gallery assets: removed after review. Example images in this repository must
  come from `nature-skills` migration or audited external sources.
- Local invented numeric example data: not retained. Quantitative templates must read external CSV
  data supplied by the user, extracted from an audited public source, or cleared for reuse from a
  paper/project.
- Codex-generated native gallery assets and derivative data snapshots: removed. Public data sources
  may be linked and audited, but generated charts must remain task-specific outputs rather than
  reusable library examples.
- Active D2/Graphviz/Mermaid diagram templates: removed from active templates because the current
  skill uses the Matplotlib schematic-composite path instead.
- Unofficial "best paper figure" galleries and social-media advice: useful for inspiration but not
  authoritative enough for this skill.
- Venue-specific rules not checked from official pages: left as "verify current author kit" instead
  of being encoded as hard rules.

## Update Procedure

When adding a new venue or rule:

1. Search for the official CFP, author instructions, publisher production page, or template.
2. Save only the rule summary and URL in this file.
3. Add the actionable rule to `venue-map.md`, `domain-patterns.md`, or `quality-checklist.md`.
4. Mark year-specific rules with the year.
5. If a rule may change annually, write "verify current author kit" in the operational file.
