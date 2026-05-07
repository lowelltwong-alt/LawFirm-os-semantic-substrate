# AI Table Of Contents

This repo is the LawFirm OS control-plane and semantic-substrate authority surface.

Canonical machine name: `LawFirm-os-semantic-substrate`. Human label: Law Firm OS Semantic Substrate. For sibling-repo names, plane responsibilities, and authority order across repos, see `governance/CROSS_REPO_MAP.md`.

## Start Here

- `governance/CROSS_REPO_MAP.md`
- `AI_WORK_START_HERE.md`
- `AI_START_HERE.md`
- `AGENTS.md`
- `README.md`

## Canonical Registries

- `registry/source-of-truth.json`
- `registry/design-authority.json`
- `registry/schema-registry.json`
- `registry/exception-route-registry.json`
- `registry/orchestrator-contract-export.json`
- `registry/exceptions-lake-contract-export.json`

## Canonical Manifests

- `manifests/contract_manifest.v1.json` — canonical orchestrator-facing manifest. Stable keys for runtime consumers: `manifest_id`, `manifest_version`, `policy_bundle_id`, `canonical_schema_keys`, `registry_refs`, `governance_refs`.

## Phase 2 Registries

- `registry/innovation-object-registry.json`
- `registry/autonomy-lane-registry.json`
- `registry/assumption-watch-registry.json`
- `registry/harness-policy-registry.json`
- `registry/red-flag-trigger-registry.json`
- `registry/research-signal-registry.json`

## Phase 2 Governance

- `governance/CROSS_REPO_MAP.md`
- `governance/ORCHESTRATOR_BOUNDARY.md`
- `governance/EXCEPTIONS_LAKE_BOUNDARY.md`
- `governance/PHASE_2_SCHEMA_PLACEMENT.md`
- `governance/PHASE_2_ROADMAP.md`
- `governance/INNOVATION_AUTONOMY_LAYER.md`
- `governance/AUTONOMY_RYG_POLICY.md`
- `governance/CONTINUOUS_AUTONOMY_ASSURANCE.md`
- `governance/HARNESS_INTENSITY_POLICY.md`
- `governance/RESEARCH_SIGNAL_INGESTION_POLICY.md`
- `governance/GREEN_RESTORATION_POLICY.md`
- `governance/INTERNAL_IDEA_LIFECYCLE.md`
- `docs/ORCHESTRATION_LAYER_DATA_FLOW.md`

## Planned PR07 Decision Intelligence

- Future control-plane schemas: `schemas/decision/`
- Future decision registries: `registry/decision-model-registry.json`, `registry/stakes-profile-registry.json`
- Future Research Radar registry: `registry/research-radar-registry.json`
- Future governance docs: `governance/DECISION_INTELLIGENCE_MODEL.md`, `governance/STAKES_AND_REVERSIBILITY_POLICY.md`, `governance/RESEARCH_RADAR_OPERATING_MODEL.md`
- Initial local-only watchlist seed set: `research-radar-frontier-ai-001` plus reserved PR07 seed topics in `governance/PHASE_2_ROADMAP.md`

## Schema Locations

- `schemas/` is the canonical machine-readable JSON Schema authority layer.
- `schema/` (singular) is a legacy / Phase 1 / draft doctrinal-comparison substrate. It does **not** replace `schemas/` and is non-canonical for Phase 2 work. Any future migration or renaming of `schema/` must be a separate compatibility-preserving cleanup PR.
- New Phase 2 machine-readable schemas go under `schemas/` unless a future compatibility-preserving governance change says otherwise.
- `registry/` is the canonical discovery surface for schema and governance references.
- Existing Innovation OS schemas: `schemas/*.schema.json`
- New Phase 2 autonomy schemas: `schemas/autonomy/`
- New Phase 2 harness schemas: `schemas/harness/`
- New Phase 2 research lifecycle schemas: `schemas/research/`
- New Phase 2-only innovation schemas: `schemas/innovation/`
- Legacy Phase 1 doctrinal-comparison substrate (draft, non-canonical): `schema/` (`schema/manifest.yaml`, `schema/interfaces/`, `schema/types/`, `schema/enums/`, `schema/contracts/`, `schema/invariants/`).

## Pre-PR07 Draft Scaffolds (non-canonical)

These artifacts already exist in the repository as pre-PR07 draft scaffolding. They are metadata-only and non-authorizing. They do not authorize live crawling, scheduled jobs, model calls, external APIs, external writes, or production research automation. PR07 may later formalize, supersede, or reconcile them.

- `registry/research-radar-source-registry.json` — pre-PR07 draft source-class scaffold for Research Radar discovery. Marked `non_authoritative: true` and `phase: "pre-pr07-draft"`.
- `schema/` (singular) — Phase 1 doctrinal-comparison draft substrate (see Schema Locations).

## Front Doors

- `ENDPOINTS_AND_COMMANDS.md`
- `DATA_FLOW_MAP.md`
- `RECENT_WORK.md`

## Validation

- `scripts/check_repo_drift.py`
- `scripts/validate_examples.py`
- `scripts/validation/tests/`
