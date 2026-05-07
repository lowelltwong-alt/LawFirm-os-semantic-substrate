# Recent Work

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
