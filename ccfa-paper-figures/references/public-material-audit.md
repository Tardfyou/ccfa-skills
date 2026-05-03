# Public Material Audit

Use this file before adding any public figure, screenshot, dataset, benchmark result, icon, diagram,
architecture material, or example to the skill.

## Hard Rule

The active skill supports data/statistical paper figures and Nature-style schematic-led composites.
Public diagram and architecture material may be retained only under `assets/reference-materials/`
after audit. It is reference material unless explicitly promoted by `extension-gates.md`; copied
paper figures remain disallowed without redistribution rights.

Do not add self-drawn example figures to the reusable library. If a reusable example is needed, use
one of these routes:

- migrate an approved asset from `nature-skills`;
- link to an audited public source without copying it;
- use user-provided material;
- use source data only when the license permits reuse, and keep the generated result as a task output,
  not as a bundled reusable example.

## Audit Fields

Every public material candidate must record:

| Field | Required content |
|---|---|
| Source URL | Official project, publisher, repository, dataset, or government URL. |
| Material type | Figure, screenshot, dataset, benchmark table, icon, template, paper exemplar, or architecture material. |
| Authority | Why this source is authoritative for CCF-A / CS paper figures or architecture/schematic work. |
| License / reuse status | SPDX license, publisher license, government/public-domain status, or `link-only`. |
| Redistribution decision | `bundle-ok`, `data-only`, `link-only`, or `reject`; add `reference-only` when the material is not an active template. |
| Quality decision | Why the material is visually or technically strong enough to keep. |
| Audit date | Exact date of review. |
| Local path / hash | Required when a copied asset is bundled. |

## Redistribution Decisions

- `bundle-ok`: may be copied into `assets/` only when the license explicitly allows redistribution.
- `bundle-ok reference-only`: may be copied under `assets/reference-materials/`; usable as audited
  inspiration or user-approved source material, not as a default copied template or output template.
- `data-only`: raw data may be used; generated charts are task outputs and must not become library
  examples unless separately reviewed.
- `link-only`: cite or inspect the source but do not copy assets into the repo.
- `reject`: do not use except as a negative example in private reasoning.

## Audited Data Sources

| Source | Material type | License / reuse status | Decision | Audit date | Notes |
|---|---|---|---|---|---|
| https://github.com/mlcommons/inference_results_v5.1 | Benchmark results | Apache-2.0 repository | data-only | 2026-05-03 | Useful for AI/systems benchmark data. Do not bundle Codex-generated charts as reusable examples. |
| https://raw.githubusercontent.com/mlcommons/inference_results_v5.1/main/summary_results.json | Benchmark data file | Apache-2.0 repository | data-only | 2026-05-03 | Use as raw data only after citing MLCommons version. |
| https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | Security catalog feed | Official CISA public feed | data-only | 2026-05-03 | Useful for security trend data. Verify current catalog version before use. |
| https://github.com/rjust/defects4j | Software-engineering benchmark metadata | MIT repository | data-only | 2026-05-03 | Useful for benchmark composition data; generated charts are task outputs only. |

## Audited Link-Only Paper Exemplars

| Source | Material type | License / reuse status | Decision | Audit date | Notes |
|---|---|---|---|---|---|
| https://arxiv.org/abs/2304.02643 | Paper exemplar | Link-only unless license is checked per asset | link-only | 2026-05-03 | Use for visual/data-figure analysis only; do not copy figures. |
| https://proceedings.neurips.cc/paper_files/paper/2022/hash/8bb0d291acd4acf06ef112099c16f326-Abstract-Conference.html | Paper exemplar | Link-only | link-only | 2026-05-03 | Use for benchmark/result-panel analysis only; do not copy figures. |
| https://arxiv.org/abs/2309.06180 | Paper exemplar | Link-only unless license is checked per asset | link-only | 2026-05-03 | Use for systems evaluation plot analysis; do not copy figures. |
| https://arxiv.org/abs/2310.06770 | Paper exemplar | Link-only unless license is checked per asset | link-only | 2026-05-03 | Use for SE benchmark/result framing; do not copy figures. |
| https://arxiv.org/abs/1902.07550 | Paper exemplar | Link-only unless license is checked per asset | link-only | 2026-05-03 | Use for security metric/evaluation context; do not copy figures. |

## Audited Architecture Reference Materials

These assets are retained as a quality-controlled architecture/process material library. They may
inform schematic design after checking license and context, but they are not copied paper figures or
default templates.

| Local path | Source URL | Material type | Authority | License / reuse status | Decision | Quality decision | SHA-256 | Audit date |
|---|---|---|---|---|---|---|---|---|
| `assets/reference-materials/architecture-library/sam/model_diagram.png` | https://raw.githubusercontent.com/facebookresearch/segment-anything/main/assets/model_diagram.png | Model architecture figure | Official Segment Anything repository from Meta AI | Apache-2.0 repository license verified from https://raw.githubusercontent.com/facebookresearch/segment-anything/main/LICENSE | bundle-ok reference-only | High-quality canonical model/promptable-segmentation architecture asset; AI schematic reference only. | `80F88CCC64FDEFC08B28682661B41832E25E4C1612E7E430DC30ED551EE51D86` | 2026-05-03 |
| `assets/reference-materials/architecture-library/sam2/model_diagram.png` | https://raw.githubusercontent.com/facebookresearch/sam2/main/assets/model_diagram.png | Model architecture figure | Official SAM 2 repository from Meta AI | Apache-2.0 repository license verified from https://raw.githubusercontent.com/facebookresearch/sam2/main/LICENSE | bundle-ok reference-only | Canonical model/data-flow figure with clean modular structure; AI schematic reference only. | `08A6E3D958194BB79BEE120EDC3DD80CD4C1B0741418CCBA0B028533173AA5DE` | 2026-05-03 |
| `assets/reference-materials/architecture-library/vllm/llm_engine.excalidraw.png` | https://raw.githubusercontent.com/vllm-project/vllm/main/docs/assets/design/arch_overview/llm_engine.excalidraw.png | System architecture figure | Official vLLM documentation repository | Apache-2.0 repository license verified from https://raw.githubusercontent.com/vllm-project/vllm/main/LICENSE | bundle-ok reference-only | Useful serving-engine architecture reference with explicit component boundaries; systems schematic reference only. | `BF641DDD64C294E72FDD50243603CA15E8D19827104ADD4A71C77CB93DC2D73B` | 2026-05-03 |
| `assets/reference-materials/architecture-library/vllm/v1_process_architecture_tp4.png` | https://raw.githubusercontent.com/vllm-project/vllm/main/docs/assets/design/arch_overview/v1_process_architecture_tp4.png | Process architecture figure | Official vLLM documentation repository | Apache-2.0 repository license verified from https://raw.githubusercontent.com/vllm-project/vllm/main/LICENSE | bundle-ok reference-only | Detailed process/parallelism architecture reference; high information density, so active use requires simplification and user/source context. | `8602FECBABF3B5FB4CEEB831F608DC178D14EC4A686E2F2CFF58B1AF78F8951D` | 2026-05-03 |
| `assets/reference-materials/architecture-library/swe-bench/collection.png` | https://raw.githubusercontent.com/SWE-bench/SWE-bench/main/docs/assets/figures/collection.png | Benchmark construction workflow figure | Official SWE-bench repository | MIT repository license verified from https://raw.githubusercontent.com/SWE-bench/SWE-bench/main/LICENSE | bundle-ok reference-only | Clean benchmark-collection process reference; SE workflow reference only. | `11B003915A7274419B22732ABB68E7441126C69FCAE5075F88E331D5E779EA69` | 2026-05-03 |
| `assets/reference-materials/architecture-library/swe-bench/evaluation.png` | https://raw.githubusercontent.com/SWE-bench/SWE-bench/main/docs/assets/figures/evaluation.png | Benchmark evaluation workflow figure | Official SWE-bench repository | MIT repository license verified from https://raw.githubusercontent.com/SWE-bench/SWE-bench/main/LICENSE | bundle-ok reference-only | Clear task/evaluation framing reference; SE workflow reference only. | `DDB87FF78303EF97C6DA85EF45E45F944FE23F0BF816EF02EB9128F91E7D811B` | 2026-05-03 |
| `assets/reference-materials/architecture-library/owasp-threat-dragon/demo-threat-model.json` | https://raw.githubusercontent.com/OWASP/threat-dragon/main/ThreatDragonModels/demo-threat-model.json | Threat-model JSON example | Official OWASP Threat Dragon repository | Apache-2.0 repository license verified from https://raw.githubusercontent.com/OWASP/threat-dragon/main/license.txt | bundle-ok reference-only | Authoritative structured threat-model example; security schematic reference only; use through schematic-composite path. | `E92CD19F99AB0FFD3671D06B79238DC7161FC312BADF8A0A4C0844B869B74267` | 2026-05-03 |

## Rejected / Removed

| Material | Decision | Reason |
|---|---|---|
| Codex-generated native gallery PNG/SVG files | removed | Self-drawn examples are not acceptable as reusable library assets. |
| Codex-generated derivative CSV snapshots | removed | Keep source URLs and regenerate only for a concrete user task. |
| Active D2/Graphviz/Mermaid diagram templates | removed from active templates | Diagram-first generation is outside the current Nature-style schematic-composite path. |
