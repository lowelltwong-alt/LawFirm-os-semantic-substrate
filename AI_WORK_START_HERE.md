# AI Work Start Here

This is the mandatory operational router for AI-assisted work in this repository.

## Required read order

Before any AI-assisted edit, read:

1. `AI_START_HERE.md`
2. `AGENTS.md`
3. `registry/source-of-truth.json`
4. `registry/design-authority.json`
5. `governance/AI_CONTROL_PLANE_BOUNDARY.md`
6. `governance/EXCEPTIONS_LAKE_BOUNDARY.md` when the task touches Exceptions Lake contracts
7. this file
8. the selected route template under `docs/governance/ai-workflow/templates/`

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

- Existing root-level Innovation OS schemas remain at `schemas/*.schema.json`.
- New autonomy schemas live under `schemas/autonomy/`.
- New harness schemas live under `schemas/harness/`.
- New local-only research lifecycle schemas live under `schemas/research/`.
- New Innovation OS objects that did not already exist at root live under `schemas/innovation/`.
- Registry discovery lives under `registry/`; do not create a parallel `registries/` root.

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
