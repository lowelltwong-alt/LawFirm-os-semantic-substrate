# AI Table Of Contents

This repo is the LawFirm OS control-plane and semantic-substrate authority surface.

Canonical machine name: `LawFirm-os-semantic-substrate`. Human label: Law Firm OS Semantic Substrate. For sibling-repo names, plane responsibilities, and authority order across repos, see `governance/CROSS_REPO_MAP.md`.

## Start Here

- `registry/adversity-class-registry.candidate.json` - synthetic-only PR-LL4 candidate; no legal conflict or runtime authority
- `governance/ADVERSITY_CLASS_REGISTRY_BOUNDARY.md` - HD-4/HD-7 boundary and downstream ownership contract
- `governance/CROSS_REPO_MAP.md`
- `AI_WORK_START_HERE.md`
- `AI_START_HERE.md`
- `AGENTS.md`
- `README.md`
- `registry/ai-front-door-registry.json` — machine gate for AI TOC / workflow atlas integrity (see `governance/AI_FRONT_DOOR_BOUNDARY.md`)
- `registry/registry-full-manifest.json` — full index of `registry/*.json` surfaces
- `registry/governance-full-manifest.json` — full index of `governance/**/*.md` surfaces
- `registry/governance-dependency-map.json` — canonical governance-facing dependency map and child mirror update gate
- `governance/GOVERNANCE_DEPENDENCY_MAP.md` — human-readable rule and child mirror contract template

- `governance/GOVERNANCE_DECISION_DEPENDENCY_ATLAS.md` - map home for governance decisions, dependencies, downstream effects, and safe experiment planning

## Canonical Registries

- `registry/adversity-class-registry.candidate.json` - draft synthetic adversity vocabulary pinned to Intake PR #74
- `registry/source-of-truth.json`
- `registry/design-authority.json`
- `registry/schema-registry.json`
- `registry/ai-front-door-registry.json`
- `registry/registry-full-manifest.json`
- `registry/governance-full-manifest.json`
- `registry/governance-dependency-map.json`
- `registry/schema-surface-exclusions.json`
- `registry/exception-route-registry.json`
- `registry/orchestrator-contract-export.json`
- `registry/agent-control-contract-export.json`
- `registry/agent-hostile-control-registry.json`
- `registry/prompt-registry.json`
- `registry/tool-authority-registry.json`
- `registry/endpoint-authority-registry.json`
- `registry/exceptions-lake-contract-export.json`
- `registry/legal-knowledge-runtime-contract-export.json`
- `registry/decision-model-registry.schema.json` - canonical schema for decision-model registry entries
- `registry/decision-model-registry.seed.json` - initial decision-model seed registry
- `registry/architecture-flow-registry.json` — OS contract spine catalog (ContextBundle, EvidencePacket, SourceRef, PassageRef, ClaimRef, SkillTrustRecord, …)
- `registry/architecture-object-coverage-registry.json` — PR-09 sync-gate expectations

## Governance Decision Atlas

- `registry/governance-dependency-map.json` - canonical map for governance-facing files, dependencies, downstream mirrors, validators, and PR-description gates
- `governance/GOVERNANCE_DEPENDENCY_MAP.md` - companion human policy and child mirror template
- `governance/GOVERNANCE_DECISION_DEPENDENCY_ATLAS.md`
- `registry/governance-decision-dependency-atlas.seed.json` - seed machine map for governance decision nodes, dependency edges, downstream consumers, and layered agent expansion

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
- `governance/AGENT_HOSTILE_CONTROL_BOUNDARY.md`
- `governance/EXCEPTIONS_LAKE_BOUNDARY.md`
- `governance/PHASE_2_SCHEMA_PLACEMENT.md`
- `governance/PHASE_2_ROADMAP.md`
- `governance/INNOVATION_AUTONOMY_LAYER.md`
- `governance/AUTONOMY_RYG_POLICY.md`
- `governance/CONTINUOUS_AUTONOMY_ASSURANCE.md`
- `governance/HARNESS_INTENSITY_POLICY.md`
- `governance/LITIGATION_SIMULATION_ADAPTER_BOUNDARY.md`
- `governance/REAL_WORK_SHADOW_MODE_PILOT_GATES.md`
- `governance/RESEARCH_SIGNAL_INGESTION_POLICY.md`
- `governance/GREEN_RESTORATION_POLICY.md`
- `governance/INTERNAL_IDEA_LIFECYCLE.md`
- `docs/ORCHESTRATION_LAYER_DATA_FLOW.md`

## Planned PR07 Decision Intelligence

- Future control-plane schemas: `schemas/decision/`
- Decision model seed registry: `registry/decision-model-registry.seed.json`
- Decision model registry schema: `registry/decision-model-registry.schema.json`
- Future decision registries: `registry/decision-model-registry.json`, `registry/stakes-profile-registry.json`
- Future Research Radar registry: `registry/research-radar-registry.json`
- Proposed AI strategy doctrine, not canon until approved: `governance/AI_STRATEGY_DOCTRINE.md`
- Decision-bottleneck doctrine and local seed scaffolds: `governance/DECISION_BOTTLENECK_AND_DECISION_MODELS.md`
- Future governance docs: `governance/DECISION_INTELLIGENCE_MODEL.md`, `governance/STAKES_AND_REVERSIBILITY_POLICY.md`, `governance/RESEARCH_RADAR_OPERATING_MODEL.md`
- Initial local-only watchlist seed set: `research-radar-frontier-ai-001` plus reserved PR07 seed topics in `governance/PHASE_2_ROADMAP.md`

## AI Strategy Doctrine and Context Quality Governance

- [governance/AI_STRATEGY_DOCTRINE.md](governance/AI_STRATEGY_DOCTRINE.md) is the proposed controlling doctrine for vendor-agnostic AI strategy, proprietary context, decision models, Legal Context Bundles, Evidence Packets, model/provider adapters, skill trust records, and governed promotion paths.
- [governance/STRATEGIC_REFERENCE_PROPRIETARY_CONTEXT.md](governance/STRATEGIC_REFERENCE_PROPRIETARY_CONTEXT.md) is a strategy reference, not an implementation mandate.
- [governance/SHANNON_INFORMATION_THEORY_CROSSWALK.md](governance/SHANNON_INFORMATION_THEORY_CROSSWALK.md) is a technical crosswalk and must not be used as legal-truth math.
- [governance/CONTEXT_QUALITY_DOCTRINE.md](governance/CONTEXT_QUALITY_DOCTRINE.md) defines Legal Context Bundles and context-quality controls.
- [governance/INSTITUTIONAL_KNOWLEDGE_ENCODING_STANDARD.md](governance/INSTITUTIONAL_KNOWLEDGE_ENCODING_STANDARD.md) defines how institutional knowledge must be scoped, sourced, reviewed, and governed.
- None of these files are canon until approved through this repo's governance process.

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

## OS Contract Spine (PR-06–PR-08)

Governed runtime evidence objects (validated by `scripts/validate_architecture_object_coverage.py`):

| Object | Schema | Owning plane |
|--------|--------|----------------|
| ContextBundle | context-bundle-v1 | orchestrator |
| ExecutionRequest | execution-request-v1 | orchestrator |
| ExecutionDecision | execution-decision-v1 | orchestrator |
| ExecutionPassport | execution-passport-v1 | orchestrator |
| ExecutionResult | execution-result-v1 | orchestrator |
| AgentIdentity | agent-identity-v1 | semantic_substrate |
| PromptVersion | prompt-version-v1 | semantic_substrate |
| ToolAuthority / EndpointAuthority | tool-authority-v1 / endpoint-authority-v1 | semantic_substrate |
| RevocationPolicy | revocation-policy-v1 | semantic_substrate |
| AgentHostileControlBundle | agent-hostile-control-bundle-v1 | semantic_substrate |
| EvidencePacket | evidence-packet-v2 | orchestrator |
| ExceptionLakeAdmissionRecord | exception-lake-admission-record-v1 | exception_lake |
| DefectRecord / EvalCandidate | defect-record-v1 / eval-candidate-v1 | exception_lake |
| SourceRef / PassageRef / ClaimRef / CoverageRecord / VerificationRecord | source-ref-v1 … verification-record-v1 | legal_knowledge_runtime |
| UntrustedContentAnomalyRecord | untrusted-content-anomaly-record-v1 | legal_knowledge_runtime |
| SkillTrustRecord | skill-trust-record-v1 | skills_registry |

External legal data and PassageRef spans are **evidence**, not canon. Provider-specific runner metadata (Claude plugin IDs, etc.) belongs in `provider_metadata` at the skill package edge only.

## Front Doors

- `ENDPOINTS_AND_COMMANDS.md`
- `DATA_FLOW_MAP.md`
- `RECENT_WORK.md`

## Validation

- `scripts/run_full_pytest.py` (uses `config/validation-runtime-policy.yaml`; 3600 second pytest floor)
- `scripts/check_repo_drift.py`
- `scripts/validate_governance_dependency_map.py`
- `scripts/validate_intake_contract_promotion_review.py`
- `scripts/validate_real_work_and_simulation_boundaries.py`
- `scripts/validate_examples.py`
- `scripts/validation/tests/`

<!-- BEGIN DIGITAL_ASSET_DIRECTORY_TOC_ROWS -->
| Path | What It Is | Tags | Use When |
| --- | --- | --- | --- |
| `.digital-asset/dad-integration.json` | Versioned DAD enrollment contract and approved write boundary. | dad, enrollment, governance | Confirm DAD cadence, control planes, approval IDs, and managed paths. |
| `.digital-asset/context-map.json` | Repo context to DAD asset/control-plane route map. | dad, context, assets | Choose relevant DAD assets, skills, templates, or architecture references for a task. |
| `.digital-asset/governance-map.yaml` | Repo-local governance dependency mirror. | governance, authority, dependencies | Check local authority boundaries and DAD-managed surfaces. |
| `.digital-asset/data-map.yaml` | Repo-local sensitive-boundary and data-movement map. | data-map, privacy, release | Check what data can move through DAD mail or public-facing release paths. |
| `.digital-asset/mail/` | Candidate-only DAD inbox/outbox/archive. | mail, suggestions, daily | Read or send cross-repo suggestions without mutating source authority. |
| `.digital-asset/assets/index.jsonl` | Repo-local metadata-only digital asset cards using compact DAD address layers. | assets, address-model, learning | Record source-owned asset pointers, workflow refs, validation refs, and learning deltas without copying private content. |
<!-- END DIGITAL_ASSET_DIRECTORY_TOC_ROWS -->
