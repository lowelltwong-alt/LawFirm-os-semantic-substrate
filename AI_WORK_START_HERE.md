# AI_WORK_START_HERE.md

<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->
Managed bootstrap for AI-assisted work in the LawFirm OS multi-repo workspace. Route through the canonical AI front door and Skill-Agent Control Plane, but preserve local repo operating doctrine.

Required bootstrap read order:

1. AGENTS.md
2. skill-agent-manifest.json
3. Semantic Substrate registry/ai-front-door-registry.json
4. Semantic Substrate registry/skill-agent-control-plane-registry.json
5. Semantic Substrate governance/SKILL_AGENT_CONTROL_PLANE_BOUNDARY.md

Repo: LawFirm-os-semantic-substrate
Plane: semantic substrate / control plane
Repo purpose: Canonical schemas, registries, governance, AI front door, lifecycle policy, schema registry, repo registry, skill-agent graph, and workspace validators.
This repo must not own: Runtime observations, model execution, raw legal payload storage.

Run workspace preservation and control-plane validation before reporting success on managed patch work.
<!-- END LAWFIRM_OS_BOOTSTRAP -->

<!-- BEGIN REPO_SPECIFIC_INSTRUCTIONS -->
# AI Work Start Here

This is the mandatory operational router for AI-assisted work in this repository.

## Required read order

Before any AI-assisted edit, read:

1. `AI_START_HERE.md`
2. `AGENTS.md`
3. `registry/source-of-truth.json`
4. `registry/design-authority.json`
5. `governance/CROSS_REPO_MAP.md` for sibling-repo names and authority order across repos
6. `governance/AI_CONTROL_PLANE_BOUNDARY.md`
7. `governance/EXCEPTIONS_LAKE_BOUNDARY.md` when the task touches Exceptions Lake contracts
8. `governance/ORCHESTRATOR_BOUNDARY.md` when the task touches Orchestrator contracts
9. this file
10. `governance/AI_FRONT_DOOR_BOUNDARY.md` when touching registries, schemas, governance trees, or cross-repo AI entry points
11. the selected route template under `docs/governance/ai-workflow/templates/`

Architecture sync gate (PR-09 — run when changing spine schemas, exports, or cross-repo commands):

- `registry/architecture-flow-registry.json`
- `registry/architecture-object-coverage-registry.json`
- `python scripts/validate_architecture_object_coverage.py --workspace ..`

Machine integrity manifests (AI TOC / front door gate — run `python scripts/validate_ai_front_door.py` when changing surfaces):

- `registry/ai-front-door-registry.json`
- `registry/governance-full-manifest.json`
- `registry/registry-full-manifest.json`

## Universal work cycle

1. Orient
2. Sync safely
3. Classify task
4. Choose mode: Explore / Plan / Edit / Execute
5. Choose tool settings
6. Choose route template
7. Execute inside scope
8. Validate
9. Open PR
10. Report outcome
11. Check whether the router itself needs updating

## Core rule

Route before work. Do not edit until the task has a route, mode, allowed paths, forbidden paths, validation plan, and stop conditions.

## Repository boundary

This repo is Law Firm's semantic-governance substrate and Innovation OS contract repository. It defines canonical meaning, evidence structure, governance, schemas, validation expectations, and runtime contracts. It is not the production runtime, production transcript store, production audit lake, connector worker, dashboard system, or system of record.

Runtime implementations may consume these contracts, but they must not redefine canonical meaning, lifecycle states, mutation authority, or promotion authority.

## Phase 2 schema and policy router

For Phase 2 Innovation Autonomy + Harness work:

- `schemas/` (plural) is the canonical machine-readable JSON Schema authority layer. All new Phase 2 machine-readable schemas go under `schemas/` unless a future compatibility-preserving governance change says otherwise.
- `schema/` (singular) is a legacy / Phase 1 / draft doctrinal-comparison substrate. It does **not** replace `schemas/` and is non-canonical for Phase 2 work. Do not author new Phase 2 schemas there. Any future migration or renaming of `schema/` must be a separate compatibility-preserving cleanup PR.
- Existing root-level Innovation OS schemas remain at `schemas/*.schema.json`.
- New autonomy schemas live under `schemas/autonomy/`.
- New harness schemas live under `schemas/harness/`.
- New local-only research lifecycle schemas live under `schemas/research/`.
- New Innovation OS objects that did not already exist at root live under `schemas/innovation/`.
- `registry/` is the canonical discovery surface for schema and governance references; do not create a parallel `registries/` root.
- `manifests/contract_manifest.v1.json` is the canonical orchestrator-facing manifest. Required keys for runtime consumers: `manifest_id`, `manifest_version`, `policy_bundle_id`, `canonical_schema_keys`, `registry_refs`, `governance_refs`. Consumers must not silently default `policy_bundle_id`.

Start Phase 2 control-plane work from:

1. `governance/PHASE_2_SCHEMA_PLACEMENT.md`
2. `governance/PHASE_2_ROADMAP.md`
3. `governance/INNOVATION_AUTONOMY_LAYER.md`
4. `governance/AUTONOMY_RYG_POLICY.md`
5. `governance/CONTINUOUS_AUTONOMY_ASSURANCE.md`
6. `governance/HARNESS_INTENSITY_POLICY.md`
7. `governance/RESEARCH_SIGNAL_INGESTION_POLICY.md`
8. `registry/innovation-object-registry.json`
9. `registry/autonomy-lane-registry.json`
10. `registry/harness-policy-registry.json`
11. `registry/red-flag-trigger-registry.json`

Do not duplicate an existing root schema into a grouped folder unless a compatibility need is documented and the grouped file is clearly marked as a non-authoritative alias.

PR07 is reserved for Decision Intelligence, Stakes Model, and Research Radar Seeding. Do not pull PR07 work into PR01-PR06 unless a small compatibility hook is required. PR07 is still local-only: no live crawling, scheduled jobs, model calls, external APIs, external writes, autonomous research execution, or production research automation.

The roadmap names `research-radar-frontier-ai-001` as the initial detailed local-only Research Radar watchlist seed and reserves an expanded PR07 topic set. Treat all PR07 watchlist seeds as roadmap evidence only until PR07 creates schemas and local object builders.

`registry/research-radar-source-registry.json` already exists as **pre-PR07 draft scaffolding**. It is metadata-only and non-authorizing. It does not authorize live crawling, scheduled jobs, model calls, external APIs, external writes, or production research automation. PR07 may later formalize, supersede, or reconcile it. Research Radar outputs are candidate evidence only; they may recommend green-to-yellow or green-to-red downgrades, but may not restore green or promote canon.

## AI interaction audit principle

Law Firm defines the audit contracts and governance. Runtime systems capture and persist audit events. Raw production AI prompts, outputs, and transcripts must not be stored in this repository. Raw transcripts belong only in a secure, encrypted, access-controlled, retention-governed audit store.

## Routing files

- `docs/governance/ai-workflow/README.md`
- `docs/governance/ai-workflow/ai-work-cycle.md`
- `docs/governance/ai-workflow/ai-routing-algorithm.md`
- `docs/governance/ai-workflow/ai-routing-update-policy.md`
- `docs/governance/ai-workflow/ai-task-route-table.yaml`
- `docs/governance/ai-workflow/ai-tool-settings-matrix.md`
- `docs/governance/ai-workflow/stop-conditions.md`
- `docs/governance/ai-workflow/validation-and-pr-requirements.md`
- `docs/governance/ai-workflow/ai-interaction-audit-roadmap.md`
- `docs/governance/ai-workflow/ai-interaction-audit-framework.md`
- `docs/governance/ai-workflow/ai-audit-retention-and-privacy.md`

## Clean-room rule

Do not copy leaked code, private prompts, or leak-derived repositories. Allowed lessons are architectural only: mode separation, permissions, hooks, approval gates, auditability, source boundaries, and trust zones.

<!-- END REPO_SPECIFIC_INSTRUCTIONS -->

## Skill-Agent Control Plane References

- skill-agent-manifest.json
- Semantic Substrate registry/skill-agent-control-plane-registry.json
- Semantic Substrate registry/skill-agent-lifecycle-policy-registry.json
- Semantic Substrate registry/skill-agent-quality-scoring-registry.json
- Semantic Substrate scripts/validate_skill_agent_control_plane.py

## Validation Commands

    python scripts/validate_ai_front_door.py
    python scripts/validate_skill_agent_control_plane.py --workspace ..
    python scripts/validate_managed_patch_preservation.py --workspace ..
    python -m pytest -q