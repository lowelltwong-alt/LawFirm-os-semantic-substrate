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
