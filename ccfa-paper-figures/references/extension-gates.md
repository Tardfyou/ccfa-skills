# Extension Gates

Use this file before extending `ccfa-paper-figures`. These gates are mandatory. If a proposed
addition cannot pass the relevant gate, do not add it to the skill.

## Non-Negotiable Rules

- Current main scope is data/statistical paper figures plus Nature-style schematic-led composites.
- Do not add diagram-first Graphviz, Mermaid, or D2 workflows to the active skill unless the user
  explicitly requests that source language and the docs explain the tradeoff.
- Architecture/process/security material may be retained only under `assets/reference-materials/` after
  `public-material-audit.md` records source authority, license, quality, local path, and hash.
- Do not add self-drawn reusable examples. Generated figures are task outputs, not library assets.
- Do not copy figures from papers, proceedings, blogs, slides, or social media unless redistribution
  rights are explicit and recorded.
- Do not add public material without a completed entry in `public-material-audit.md`.
- Do not encode a venue rule as official unless it is backed by the current venue, publisher,
  society, or author-kit source.
- Do not add invented numeric data, invented paper titles, invented benchmark labels, or invented
  screenshots.

## Source Tiers

| Tier | Source type | Allowed use |
|---|---|---|
| S | Official venue/publisher/society/author-kit documentation | Hard rules and venue profiles. |
| A | Official benchmark, government feed, project repository, dataset with clear license | Data source or audited reference material. |
| B | Open-access paper page or PDF | Link-only exemplar unless figure/data license is separately verified. |
| C | Blog, social media, personal checklist, mirror | Discovery only; not retained as authority. |
| Reject | Unknown license, unclear origin, copied paper figure, AI/self-drawn example | Do not add. |

## Adding Public Material

Before adding any public figure, screenshot, dataset, benchmark table, icon, diagram,
architecture material, or example:

1. Record it in `public-material-audit.md`.
2. Fill source URL, material type, authority, license/reuse status, redistribution decision, quality
   decision, audit date, and local path/hash if bundled.
3. Use `bundle-ok` only when redistribution is explicit.
4. Use `bundle-ok reference-only` for non-data materials retained under `assets/reference-materials/`.
5. Use `data-only` only for raw data that can be legally reused; generated charts must remain
   task-specific outputs unless separately approved.
6. Use `link-only` for paper figures and public pages whose content is useful but not redistributable.
7. Reject anything with unclear origin, unclear license, or weak visual/technical quality.

## Adding A Venue

Required:

- Current official CFP, author instructions, publisher page, or template URL.
- CCF routing source if the venue is claimed as CCF-A.
- Publisher profile: ACM, IEEE, USENIX, CVF, PMLR, ACL, IACR, or venue-specific.
- Data-figure guidance: allowed formats, width/DPI/font constraints, accessibility, anonymity or
  camera-ready caveats.

Files to update:

- `venue-map.md`
- `source-audit.md`
- `source-basis.md`

Validation:

- Search the venue name in `venue-map.md`.
- Verify annual rules are marked "verify current author kit" when they can change.

## Adding A Domain Pattern

Required:

- At least one official/publisher constraint or audited exemplar basis.
- Clear statement whether the rule is official or synthesized.
- No unsupported "must" language for a heuristic.
- Pattern must be a data-figure or Nature-style schematic-composite pattern.

Files to update:

- `domain-patterns.md`
- `source-basis.md`
- `paper-exemplars.md` or `public-material-audit.md` when the pattern comes from public material.

## Adding A Template

Required:

- Template must support data/statistical figures or Nature-style schematic-led composites.
- No invented results, labels, screenshots, or paper-specific content.
- Use neutral slots or require user/audited input data.
- Preserve editable source.
- Export path and audit path must be clear.

Validation:

- Run the template on a minimal user/audited input fixture outside the skill assets.
- Run `scripts/figure_audit.py` on produced exports.
- Remove temporary output.

## Adding A Script

Required:

- Deterministic behavior for a repeated data-figure or schematic-composite task.
- No hidden network dependency unless the script is explicitly an audit/fetch helper.
- Clear errors for missing inputs.
- No generated reusable example figures.

Validation:

- Execute the script.
- Confirm it does not write outside the requested output directory.
- Keep only source code, not generated task outputs, unless assets are separately audited.

## Adding Gallery Assets

Allowed only when:

- migrated from an already approved local source such as `nature-skills`; or
- the asset is `bundle-ok` in `public-material-audit.md`; or
- the user explicitly supplies and approves the asset for this skill.

Not allowed:

- Codex-drawn examples;
- regenerated benchmark charts kept as reusable examples;
- copied paper figures without redistribution rights;
- screenshots whose license or provenance is unclear.

## Schematic Expansion Gate

Do not add or broaden architecture/threat/workflow schematic support unless all conditions pass:

- User explicitly requests the expansion or it clearly follows from active schematic-composite scope.
- All candidate materials are audited in `public-material-audit.md`.
- Any schematic templates are source-only, reproducible, and not misleading self-drawn examples.
- `SKILL.md`, `README.md`, `figure-decision-guide.md`, and `scaffold_figure.py` are revised together.
- At least one validation checks that schematic requests do not degrade data-figure behavior.

## Stable Promotion Gate

Do not mark the skill Stable until all conditions pass:

- `quick_validate.py` passes.
- All bundled public materials have audit entries.
- No self-drawn reusable examples remain.
- No invented numeric data remains in templates or assets.
- Active templates are data-figure templates or audited/user-content schematic-composite templates.
- At least one forward test has used the skill on a realistic AI, security, and software-engineering
  data-figure request without relying on hidden context.
- `README.md`, `SKILL.md`, `source-audit.md`, `source-basis.md`, and `public-material-audit.md` agree
  on what is active, reference-only, linked, rejected, and why.
- `rg` checks find no stale placeholder, toy, fake, or generated-gallery references.

Suggested checks:

```bash
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py ccfa-paper-figures
rg -n "TODO|FIXME|placeholder|toy|fake|invented|generated native|native-gallery|native-data" ccfa-paper-figures README.md
python ccfa-paper-figures/scripts/figure_audit.py ccfa-paper-figures/assets/gallery/*.png ccfa-paper-figures/assets/chart-atlas/*.png
```
