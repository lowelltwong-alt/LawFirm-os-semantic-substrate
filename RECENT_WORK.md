# Recent Work

## 2026-05-06 — Cross-Repo Coherence Patch 2: Orchestrator Manifest Surface

Codex task / PR: Cross-repo coherence fix train Patch 2.

Files changed:
- Added `manifests/contract_manifest.v1.json` as the canonical orchestrator-facing manifest. Stable keys: `manifest_id`, `manifest_version`, `policy_bundle_id`, `canonical_schema_keys`, `registry_refs`, `governance_refs`. Marks `non_claims`, `consumer_lock_requirements`, and `manifest_first_loading_policy`.
- Updated `registry/orchestrator-contract-export.json` to reference the new canonical manifest as `primary_orchestrator_manifest`, added `canonical_repo_name`, expanded `depends_on` and `required_docs` to include the cross-repo map, ORCHESTRATOR_BOUNDARY, and ORCHESTRATION_LAYER_DATA_FLOW.
- Augmented `governance/ORCHESTRATOR_BOUNDARY.md` with canonical-name section, manifest-first loading doctrine, and pin-and-refresh discipline. The pre-existing authority-split table and forbidden-actions list remain unchanged.
- Augmented `docs/ORCHESTRATION_LAYER_DATA_FLOW.md` with canonical-names section and a manifest-first authoritative-surface index. Existing Mermaid flow and sequence remain unchanged.
- Updated `registry/source-of-truth.json` to enumerate `orchestrator_contract_manifest`, `orchestrator_boundary`, `orchestration_layer_data_flow` and to add `manifests/contract_manifest.v1.json` to the `phase_2_innovation_autonomy_layer` block.
- Updated `AI_TABLE_OF_CONTENTS.md` with a new "Canonical Manifests" section and added `governance/CROSS_REPO_MAP.md`, `governance/ORCHESTRATOR_BOUNDARY.md`, `governance/EXCEPTIONS_LAKE_BOUNDARY.md`, and `docs/ORCHESTRATION_LAYER_DATA_FLOW.md` to the Phase 2 Governance section.
- Updated `AI_WORK_START_HERE.md` Phase 2 schema and policy router with canonical-manifest doctrine and the explicit "must not silently default `policy_bundle_id`" rule.
- Updated `DATA_FLOW_MAP.md` with an "Orchestrator-Facing Surfaces" section.

Schemas changed:
- None. The manifest references existing canonical schema keys without introducing new schemas.

Commands/endpoints changed:
- None.

Data flow changed:
- Made the orchestrator-facing manifest path (`manifests/contract_manifest.v1.json`) explicit. The runtime consumer should now prefer this path over a silent fallback to `registry/orchestrator-contract-export.json`.

Tests added/updated:
- None.

Risk color:
- Yellow. New canonical surface in the substrate that runtime repos will consume.

Hardness/harness level:
- H2. Planner plus implementation plus existing validation.

Leverage rationale:
- Eliminates silent shape coercion in the orchestrator's substrate reader. Once orchestrator Patch 3 lands, `policy_bundle_id` is required from the manifest and the runtime fail-closes if absent.

Follow-up:
- Patch 3 will refresh orchestrator `contracts.lock.json` against this commit and require the new manifest in the orchestrator's substrate reader.

## 2026-05-06 — Cross-Repo Coherence Patch 1: source-of-truth Phase 2 Enumeration And Cross-Repo Map

Codex task / PR: Cross-repo coherence fix train Patch 1.

Files changed:
- Updated `registry/source-of-truth.json` to enumerate Phase 2 registries, governance docs, and grouped schema surfaces. Added `canonical_repo_name`, `human_label`, and `sibling_repos` keys. Added a `phase_2_innovation_autonomy_layer` and `pre_pr07_draft_scaffolds` section to `layer_model`. Inserted Phase 2 entries into `precedence_order`.
- Added `governance/CROSS_REPO_MAP.md` defining canonical machine names and human labels for the substrate, orchestrator, and evidence-lake repos; plane responsibilities; authority order across repos; pin-and-refresh discipline; and hard prohibitions.
- Cross-linked the cross-repo map from `README.md`, `AI_WORK_START_HERE.md`, `AI_TABLE_OF_CONTENTS.md`, `DATA_FLOW_MAP.md`, and this file.

Schemas changed:
- None.

Commands/endpoints changed:
- None.

Data flow changed:
- None. Cross-repo identity disambiguation only.

Tests added/updated:
- None. Existing validation suite re-run.

Risk color:
- Yellow. Front-door authority surface change requiring human review before broader downstream adoption.

Hardness/harness level:
- H1 documentation/registry update plus existing validation.

Leverage rationale:
- Resolves the five-name identity sprawl across repos by naming `LawFirm-os-semantic-substrate` as canonical machine name and `Law Firm OS Semantic Substrate` as canonical human label. Lets PR02–PR06 reference Phase 2 surfaces from a single discoverable index.

Follow-up:
- Patch 2 will publish `manifests/contract_manifest.v1.json`, `governance/ORCHESTRATOR_BOUNDARY.md`, and `docs/ORCHESTRATION_LAYER_DATA_FLOW.md`.

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
