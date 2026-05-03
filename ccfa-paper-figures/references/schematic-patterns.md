# Schematic Patterns

Use this file for architecture, model-overview, workflow, threat-boundary, and mixed schematic +
quantitative figures. The target is Nature-style paper composition adapted to CCF-A CS venues, not
diagram-first tooling.

## Operating Rule

Create a claim-supporting figure, not a generic architecture poster. The schematic should explain the
mechanism or system boundary that the paper evaluates, and the subordinate panels should provide the
evidence that the schematic needs.

The Nature-style transfer is page architecture, not biological subject matter: one dominant
mechanism/architecture panel, quiet evidence panels, consistent semantic color mapping, direct labels
instead of oversized legends, and final-size readability.

Acceptable content sources:

- User-provided architecture, model, pipeline, threat model, or workflow description.
- Audited public project/repository material recorded in `public-material-audit.md`.
- Permission-cleared paper material supplied by the user.
- Link-only paper exemplars used as visual inspiration, not copied assets.

Reject:

- Invented architecture components, labels, workflows, screenshots, or benchmark claims.
- Copied paper diagrams without explicit redistribution rights.
- Decorative icons, vendor logos, or clip art that do not carry semantic meaning.

## Nature-Style Layout Archetypes

### Schematic Hero With Evidence Row

Use when one mechanism, model path, system architecture, or workflow must lead.

- Allocate roughly 45-60% of figure height to the schematic.
- Put 1-4 small quantitative panels below: ablation, latency, accuracy, error, overhead, CDF, or
  resource breakdown.
- Reuse schematic colors in data panels where the same component/method appears.
- Keep supporting plots quieter than the schematic: thinner lines, smaller titles, compact legends.
- Treat the top panel as the reading anchor. If the paper claim is about a scheduler, detector,
  verifier, cache, retriever, or repair loop, that element should be visually central rather than one
  equal box among many.

### Asymmetric Mixed-Modality Composite

Use when one overview panel is central but smaller data, image, or table-like evidence surrounds it.

- Do not force equal panel sizes when the argument is unequal.
- Put the most explanatory panel where reading starts: usually top or left for CS papers.
- Use whitespace and alignment to group panels; avoid decorative frames.
- Use this layout when an architecture overview needs one side panel for a trace, screenshot, code
  excerpt, confusion matrix, or qualitative example. The raster or excerpt must be user-provided or
  permission-cleared.

### Image Or Screenshot Plate With Vector Overlay

Use when the architecture evidence includes UI screenshots, qualitative examples, generated outputs,
or system traces.

- Underlying raster content must be user-provided or permission-cleared.
- Keep raster at native resolution and place labels/arrows as vector overlays.
- Use consistent crop geometry and scale/caption notation.

## CS-Specific Schematic Types

### AI / ML Model Or Data Flow

Show:

- Data source, preprocessing, model/module sequence, training/evaluation split, inference path, and
  optional feedback or retrieval path.
- Tensor, token, embedding, image, graph, or code-flow labels when they clarify the claim.
- Component-level ablations in the evidence row when the figure argues for architecture choices.

Avoid:

- Treating attention maps or saliency as proof of causality without quantitative support.
- Mixing train and test flows visually unless the separation is explicit.

### Systems / Architecture / Networking Overview

Show:

- Client/workload, control plane, data plane, cache/storage/network boundary, scheduler, runtime,
  kernel/device boundary, or deployment topology.
- Data flow and control flow with distinct line styles or labels.
- Workload, hardware, topology, and queue/resource context in labels or caption.

Avoid:

- Overfilling the schematic with implementation details not used by the evaluation.
- Hiding assumptions behind generic labels such as "service" or "module".

### Cybersecurity / Threat-Boundary Overview

Show:

- Attacker capability, trusted/untrusted boundary, observation channel, defense action, detection
  point, and measured outcome.
- Attack or failure paths with redundant encoding: line style, label, and color.
- Assumptions that shape the evaluation, either in the schematic or caption.

Avoid:

- Red-only attacker encodings without labels or line-style redundancy.
- Implying broader attacker capabilities than the evaluation actually covers.

### Software-Engineering Workflow Or Tool Pipeline

Show:

- Input artifact, analysis/build/test/repair/generation stage, feedback loop, benchmark split, and
  output artifact.
- Human/tool boundary when developer action is part of the method.
- Evidence panels for pass rate, correctness, time, cost, per-project effect, or benchmark coverage.

Avoid:

- Turning every pipeline stage into an equal box when one stage is the actual contribution.
- Omitting benchmark identity, project count, or train/test split when relevant.

## Matplotlib Composite Template

Use `assets/templates/matplotlib_schematic_composite.py` for the active schematic path. It consumes a
JSON spec with these slots:

- `schematic.components`: semantic boxes with `id`, `label`, `xy`, `width`, and `height`.
- `schematic.components[].kind`: optional role styling. Supported roles include `input`, `output`,
  `external`, `runtime`, `control`, `storage`, `model`, `proposed`, `baseline`, `human`,
  `attacker`, `defense`, and `evidence`.
- `schematic.arrows`: flows using `from`/`to` component ids or explicit `start`/`end` coordinates.
- `schematic.arrows[].kind`: optional flow styling. Supported roles include `data`, `control`,
  `attack`, `defense`, `feedback`, and `dependency`.
- `schematic.boundaries`: dashed or solid boxes for trust, process, deployment, data, or runtime
  regions.
- `schematic.boundaries[].kind`: optional boundary styling. Supported roles include `process`,
  `runtime`, `deployment`, `trust`, and `data`.
- `schematic.callouts`: short evidence hooks pointing to one component or flow.
- `schematic.images`: optional user-provided or permission-cleared raster material.
- `data_panels`: optional CSV-backed charts using the same contracts as
  `matplotlib_result_plot.py` for `line`, `bar`, `dot-interval`, `cdf`, `heatmap`, `scatter`, and
  `area`.

The JSON spec is a source artifact. Store it beside the script and keep referenced CSV/image files
under the figure folder. Do not keep generated outputs or temporary specs as reusable skill assets.

Before writing the JSON spec, extract a source table from the user's material:

| Slot | Required content |
|---|---|
| Components | Exact names from the user, paper section, audited repository diagram, or permission-cleared source. |
| Flows | Direction, role (`data`, `control`, `attack`, etc.), and any label actually supported by the source. |
| Boundaries | Trust/runtime/deployment/data boundaries and assumptions that affect evaluation. |
| Evidence hooks | Which evaluation panel validates which component, path, or assumption. |
| Omitted detail | Implementation details intentionally left out because they are not part of the evaluated claim. |

## Visual Rules

- Use small bold lowercase panel labels.
- Keep labels inside or near the component they describe; avoid detached legends for fixed flows.
- Use one neutral family, one signal family, and one accent family. Saturated red should usually mean
  attack, failure, warning, or explicit callout.
- Differentiate data flow, control flow, and attack/failure flow with labels and line style, not hue
  alone.
- Keep text final-size readable. Prefer fewer components with accurate labels over dense unreadable
  architecture.
- Reuse `kind` styling rather than manually inventing a new palette for each component.
- Use callouts sparingly: one repeated accent style is better than several unrelated annotation
  treatments.
- Export PDF/SVG first; add PNG/TIFF only when needed.

## Audited Reference Materials

Audited architecture/process/security materials live under
`assets/reference-materials/architecture-library/` and are recorded in
`references/public-material-audit.md`. They are quality references and permission-cleared local
materials, not preapproved default templates. Use them in one of three ways:

- Study them for component grouping, flow economy, and information hierarchy.
- Use them as source material only when the target task explicitly concerns that project or the user
  authorizes reuse under the recorded license.
- Keep copied paper figures link-only unless `public-material-audit.md` records explicit
  redistribution rights.

## Default Refusal / Clarification Behavior

If the user asks for an architecture figure but provides no architecture content, ask for the system
description, component list, or paper section to convert. Do not invent a plausible architecture.

If the user wants a public paper's architecture diagram reproduced, require permission-cleared
source material or produce a new figure only from textual facts the user provides. Keep the original
paper diagram as a citation/link, not a copied asset.
