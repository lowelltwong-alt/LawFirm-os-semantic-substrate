# Recent Work

## 2026-05-06 — Phase 2 Doc Hygiene: schema/ vs schemas/ Distinction And Pre-PR07 Draft Registry Disclosure

Codex task / PR: Documentation-only hygiene pass on `phase2/pr01-control-plane-schemas-policies`.

Files changed:
- Updated `AI_TABLE_OF_CONTENTS.md` to clarify `schemas/` (canonical JSON Schema authority) vs `schema/` (legacy Phase 1 draft doctrinal-comparison substrate, non-canonical) and to add a "Pre-PR07 Draft Scaffolds (non-canonical)" subsection.
- Updated `AI_WORK_START_HERE.md` Phase 2 schema and policy router with the same `schema/` vs `schemas/` distinction and a pre-PR07 draft registry note.
- Updated `README.md` Phase 2 schema layer paragraph to call out `schema/` as legacy and to disclose `registry/research-radar-source-registry.json` as pre-PR07 draft scaffolding.
- Updated `DATA_FLOW_MAP.md` with a "Pre-PR07 Draft Scaffolds (non-canonical)" subsection and a Research Radar canon-restoration boundary note.
- Updated `governance/PHASE_2_ROADMAP.md` PR07 section to acknowledge the existing draft source registry as pre-PR07 scaffolding.
- Updated `registry/research-radar-source-registry.json` with explicit non-authorizing metadata: `phase: "pre-pr07-draft"`, `non_authoritative: true`, and a `boundary_note` capturing the non-authorizing scope.

Schemas changed:
- None.

Commands/endpoints changed:
- None.

Data flow changed:
- None. Front-door clarification only.

Tests added/updated:
- None.

Risk color:
- Green for documentation-only hygiene clarifications.

Hardness/harness level:
- H0 documentation check only.

Leverage rationale:
- Removes ambiguity about whether the legacy `schema/` directory is a parallel authority surface and whether the pre-existing `research-radar-source-registry.json` constitutes pre-PR07 Research Radar authority. Prevents accidental reuse of `schema/` for new Phase 2 work and prevents misreading the draft source registry as live discovery authority.

Follow-up:
- Any future migration or renaming of `schema/` must be a separate compatibility-preserving cleanup PR.
- PR07 may later formalize, supersede, or reconcile the pre-PR07 draft Research Radar source registry.

## 2026-05-06 — PR01 Control-Plane Schemas And Policies

Codex task / PR: Phase 2 Innovation Autonomy + Harness Layer PR01.

Files changed:
- Added Phase 2 grouped schemas under `schemas/autonomy/`, `schemas/harness/`, `schemas/research/`, and `schemas/innovation/`.
- Added Phase 2 registries under `registry/`.
- Added Phase 2 governance docs under `governance/`.
- Updated README, AI front door, AGENTS guidance, endpoints/commands, and data-flow map.

Schemas changed:
- Existing root-level Innovation OS schemas preserved in place.
- New grouped schemas added only for genuinely new Phase 2 surfaces.

Commands/endpoints changed:
- No runtime endpoints added.
- Local validation command references updated in `ENDPOINTS_AND_COMMANDS.md`.

Data flow changed:
- Added Phase 2 flow from control-plane schema authority to Orchestrator and Exception Lake consumers.

Tests added/updated:
- Added Phase 2 schema placement and registry validation coverage.

Risk color:
- Yellow. This is a governance/schema authority change requiring human review before broader downstream adoption.

Hardness/harness level:
- H2. Planner plus schema/doc implementation plus tests.

Leverage rationale:
- Adds reusable authority surfaces for autonomy, harness depth, research loops, and Codex task packets without runtime canon mutation.

Follow-up:
- Implement PR02 in the Orchestrator repo after PR01 validation passes.

## 2026-05-06 — PR07 Roadmap Reservation

Codex task / PR: Roadmap-only addition before proceeding beyond PR06.

Files changed:
- Added `governance/PHASE_2_ROADMAP.md`.
- Updated README, AI front door, AI TOC, data-flow map, and Innovation Autonomy Layer docs.

Schemas changed:
- None. PR07 schemas are planned only.

Commands/endpoints changed:
- None.

Data flow changed:
- Reserved future decision intelligence inputs for stakes, reversibility, frequency, and Research Radar watchlists/briefs.

Tests added/updated:
- None.

Risk color:
- Green for roadmap-only local documentation.

Hardness/harness level:
- H0 documentation check only.

Leverage rationale:
- Prevents PR06 from absorbing decision intelligence and keeps Research Radar automation out of scope until explicitly approved.

Follow-up:
- Keep PR01-PR06 scopes unchanged. Implement PR07 later as local-only, schema-first foundations.

## 2026-05-06 — PR07 Research Radar Watchlist Seed

Codex task / PR: Roadmap-only addition for initial PR07 Research Radar seed.

Files changed:
- Updated `governance/PHASE_2_ROADMAP.md`.
- Updated README, AI front door, AI TOC, and data-flow map references.

Schemas changed:
- None. `research-radar-frontier-ai-001` is not yet a schema-validated object.

Commands/endpoints changed:
- None.

Data flow changed:
- Added a roadmap-only Research Radar seed for frontier AI capability signals that may affect harness intensity, autonomy assumptions, green-lane watch policy, and Codex task generation.

Tests added/updated:
- None.

Risk color:
- Green for roadmap-only documentation.

Hardness/harness level:
- H0 documentation check only.

Leverage rationale:
- Preserves an explicit local-only PR07 seed without expanding PR01-PR06 or adding live research automation.

Follow-up:
- Implement the watchlist as a local-only PR07 schema/object-builder artifact later. Do not add crawling, scheduled jobs, model calls, external APIs, external writes, or autonomous research execution.

## 2026-05-06 — PR07 Research Radar Topic Set Expansion

Codex task / PR: Roadmap-only expansion of PR07 Research Radar seed topics.

Files changed:
- Updated `governance/PHASE_2_ROADMAP.md`.
- Updated README, AI front door, AI TOC, and data-flow map references.

Schemas changed:
- None. The added topics are not schema-validated objects yet.

Commands/endpoints changed:
- None.

Data flow changed:
- Expanded the planned local-only Research Radar seed set to include frontier math breakthroughs, agent failure incidents, prompt injection/security, legal AI ethics, model provider policy changes, coding-agent harness design, RAG quality, workflow orchestration, decision science, creativity with AI, law-firm reputation risk, and billing/carrier changes.

Tests added/updated:
- None.

Risk color:
- Green for roadmap-only documentation.

Hardness/harness level:
- H0 documentation check only.

Leverage rationale:
- Gives PR07 a richer local-only watchlist seed set without adding live research automation or expanding PR01-PR06.

Follow-up:
- Implement these topics later as local-only PR07 watchlist objects after schemas and builders exist.
