# Governance Decision Dependency Atlas

**Status:** seed control-plane atlas
**Route:** `governance_bridge`
**Mode:** Plan/Edit
**Authority posture:** indexes governance decisions and dependencies; does not promote, downgrade, or mutate canon by itself.

## Source Basis

This atlas starts from the clean `main` clone set checked on 2026-06-16:

| Repo | Main SHA |
|---|---|
| `LawFirm-os-semantic-substrate` | `7651f8739f68c101c797ebb9f00a30ecdd8ae1e9` |
| `LawFirm-os-orchestrator` | `478b5d0d01799c0114ea1dc35fe5a95287daaebb` |
| `LawFirm-os-exceptions-lake-runtime` | `88bd8d2eaf6ded4fbbd92354bf310b775fb64a44` |
| `LawFirm-os-legal-knowledge-runtime` | `c99c3e187fbb83ff23eb825b2ca598d8e3a75194` |
| `LawFirm-os-skills-registry` | `fd3fa8f967235ce88be2856b350ffd4a51c22c2e` |

The complete source inventory for this atlas is the union of:

- `registry/governance-full-manifest.json`
- `registry/registry-full-manifest.json`
- `registry/ai-front-door-registry.json`
- `registry/lawfirm-os-repo-registry.json`
- the sibling repos named in `governance/CROSS_REPO_MAP.md`

## Purpose

LawFirm OS now has enough governance surfaces that a human should be able to ask:

- What governance decision exists?
- What setting or threshold does it control?
- What upstream authority does it depend on?
- What downstream repos, validators, routes, schemas, or runtime behaviors would likely move if it changed?
- What can be safely experimented with, and what requires an approved promotion path?

This atlas is the coordination home for answering those questions granularly.

## Canonical Boundary Analysis

This atlas may:

- inventory decisions, controls, thresholds, prohibitions, and approval gates;
- map dependency edges among governance docs, registries, schemas, validators, and runtime consumers;
- propose experiment packets or impact assessments;
- identify missing decision-model coverage.

This atlas may not:

- make runtime evidence canonical;
- restore green authority;
- create new route IDs, event classes, schemas, lifecycle states, or approval doctrine by implication;
- override `registry/source-of-truth.json`, `registry/design-authority.json`, or existing boundary docs;
- treat extracted candidate decisions as canon until the owning authority surface already supports that status.

Canonical mutation still follows:

```text
exception-event -> pressure-vector -> adaptation-proposal -> promotion-decision
```

## Decision Node Model

Every mapped governance decision should become a node with these fields in the machine map:

| Field | Meaning |
|---|---|
| `node_id` | Stable atlas identifier for the decision or setting. |
| `label` | Human-readable decision name. |
| `decision_class` | Boundary, prohibition, threshold, registry setting, approval gate, lifecycle rule, route rule, validation gate, or experiment control. |
| `authority_status` | Canonical, active contract, proposed, draft, non-authoritative, or candidate extraction. |
| `primary_sources` | Files that actually own or state the decision. |
| `key_settings` | The adjustable knobs, values, thresholds, allowed states, or forbidden states. |
| `depends_on` | Upstream decisions or source files. |
| `downstream_consumers` | Repos, schemas, validators, docs, examples, commands, or contract locks likely affected by changes. |
| `likely_change_effects` | Expected consequences if the setting changes. |
| `validation_surfaces` | Validators, tests, or review gates that should be run. |
| `experiment_notes` | How to explore without silently changing canon or production behavior. |

Decision-model and experiment nodes should also capture these dimensions when they apply:

- `decision_model_id`
- `owner_role`
- `alternatives`
- `evidence_minimums`
- `approval_rule`
- `risk_color`
- `hard_red_triggers`
- `harness_level`
- `stakes_size`
- `reversibility`
- `blast_radius`
- `frequency`
- `leverage`
- `data_class`
- `side_effect_class`
- `canonicality_class`
- `lifecycle_status`
- `contract_surface_status`
- `lock_refresh_impact`

## Dependency Edge Types

Use this vocabulary for the first pass. Additions need governance review so the graph does not fracture into synonyms.

| Edge | Meaning |
|---|---|
| `precedes` | Source has higher authority in conflict resolution. |
| `defines` | Source creates an allowed value, rule, or control. |
| `constrains` | Source limits what another surface may do. |
| `consumes` | Runtime/support repo reads the decision as an input. |
| `exports` | Contract export carries the decision to consumers. |
| `validates` | Validator enforces the decision. |
| `locks` | Contract lock pins a source SHA or surface. |
| `requires_approval` | Decision requires explicit human approval. |
| `blocks` | Decision forbids an action or state. |
| `permits` | Decision authorizes a bounded action or state. |
| `downgrades` | Decision may reduce authority or risk status. |
| `cannot_restore` | Decision may not restore authority without human approval. |
| `proposes_to` | Runtime or evidence output can propose a governed change. |

## Layer Map

| Layer | Decision focus | Primary sources | Typical downstream effects |
|---|---|---|---|
| 0. Authority spine | Precedence, owning plane, canonical mutation gateway | `registry/source-of-truth.json`, `registry/design-authority.json`, `governance/CROSS_REPO_MAP.md` | Every repo boundary, every validator, every conflict resolution. |
| 1. AI front door | Required read order, manifests, AI entry integrity | `registry/ai-front-door-registry.json`, `governance/AI_FRONT_DOOR_BOUNDARY.md` | AI TOC, workflow routing, sibling repo anchor checks. |
| 2. Schema and registry surface | Canonical schema discovery, exclusions, manifests | `registry/schema-registry.json`, `registry/schema-surface-exclusions.json`, manifest registries | Schema validators, contract exports, runtime schema loading. |
| 3. Route and event authority | Allowed `route_id`, `event_class`, learning path | `registry/exception-route-registry.json`, Exceptions Lake boundary docs | Evidence packet classification, lake admission, pressure/adaptation flow. |
| 4. Autonomy and approval | Red/yellow/green authority, human approvals, green restoration | `registry/autonomy-lane-registry.json`, `registry/human-approval-registry.json`, `governance/AUTONOMY_RYG_POLICY.md`, `governance/GREEN_RESTORATION_POLICY.md` | Orchestrator gating, approval packets, blocked automation. |
| 5. Harness and validation intensity | Harness levels, red flags, CI routing, release gates | `registry/harness-policy-registry.json`, `registry/red-flag-trigger-registry.json`, `registry/ci-test-route-registry.json` | Required tests, evaluator depth, rollback and review packets. |
| 6. Prompt/tool/endpoint/model control | Provider, prompt, tool, endpoint, identity, revocation authority | agent-hostile, prompt, tool, endpoint, model policy registries | Runtime adapter authorization, audit requirements, freeform parsing limits. |
| 7. Retrieval and legal knowledge | Access decisions, legal context bundles, ingestion boundaries | retrieval/access docs, legal knowledge registries, legal safety guardrails | Legal Knowledge Runtime preflight, bundle assembly, safety review. |
| 8. Skill-agent supply chain | Skill metadata, lifecycle, quality scoring, graph/workflow control | skill-agent registries and boundary docs | Skills Registry intake, quarantine, scoring, future graph discovery. |
| 9. Managed patch and contract locks | Protected-file changes, broad blast radius, surface hashing | managed patch policy, contract surface registry, lock boundary docs | Preservation validator, lock bumps, review records. |
| 10. Candidate/workflow/research surfaces | Candidate objects and non-authoritative watchlists | workflow atlas, research signal/radar docs and registries | Candidate evidence, roadmap proposals, no direct canon mutation. |

## Initial Downstream Flow

```text
authority spine
-> governance and registry decision nodes
-> schemas, manifests, route/event registries, and contract exports
-> runtime contract locks and local validators
-> orchestrator, exception lake, legal knowledge runtime, and skills registry behavior
-> evidence packets, exception events, eval records, skill records, and candidate proposals
-> adaptation proposals
-> promotion decisions only when canon changes
```

## Highest Blast-Radius Consumers

Start downstream-impact review with these consumers:

| Surface | Primary consumers | Likely effect of change |
|---|---|---|
| Contract surface hash and manifest | `contracts.lock.json` in all runtime/support repos | Lock drift, quarantine, or contract-loader failure. |
| `registry/runtime-reason-codes-registry.json` | Orchestrator and Exceptions Lake reason-code loaders and execution/admission guards | Import failures, changed denial reasons, or mutation-guard behavior changes. |
| `registry/exception-route-registry.json` | Orchestrator classification, Exceptions Lake admission, event examples | Rejected route/event pairs and evidence packet drift. |
| `registry/ai-front-door-registry.json` | Cross-repo front-door validator, legal runtime anchors, draft skill index | Broken AI entry gates, missing endpoint anchors, or stale example references. |
| Skill-agent control-plane registries | Skills Registry, workspace control-plane validator, future graph discovery | Lifecycle, scoring, metadata, and quarantine behavior changes. |
| Legal knowledge registries and schemas | Legal Knowledge Runtime CLI/helpers, Orchestrator legal adapter, smoke tests | Ingestion preflight, bundle assembly, grounding, or safety output drift. |

## Five-Repo Downstream Matrix

This is the first cross-repo consumer map. It should be expanded by future mapping agents until every governance/registry decision node has explicit consumer edges or an explicit no-consumer rationale.

| Repo | Consumer paths | Consumed governance surfaces | Likely downstream effect | Validation focus |
|---|---|---|---|---|
| `LawFirm-os-semantic-substrate` | `scripts/validate_ai_front_door.py`, `scripts/validate_skill_agent_control_plane.py`, `scripts/route_ci_tests.py`, `scripts/cross_repo_os_smoke_test.py` | AI front door, repo registry, governance/registry manifests, CI route registry, contract surface registry | Cross-repo gates, route selection, manifest closure, and smoke tests change first here. | Front-door gate, skill-agent gate, architecture coverage, CI route validation, full substrate pytest. |
| `LawFirm-os-orchestrator` | `contracts.lock.json`, `src/lawfirm_os_orchestrator/substrate/*`, `src/lawfirm_os_orchestrator/commands/classify_exception.py`, `src/lawfirm_os_orchestrator/policy/agent_hostile_controls.py`, `src/lawfirm_os_orchestrator/evidence/packet_v2.py`, `src/lawfirm_os_orchestrator/legal_knowledge/adapter.py` | Contract manifest, contract surface hash, schema registry, route/event registry, runtime reason codes, prompt/tool/endpoint/model policy, legal knowledge export | Lock drift can block contract loading; route/event or reason-code changes alter classification and execution decisions; agent-hostile changes can reject tool/model flows; legal schema changes alter evidence/context packets. | Contract lock tests, classify exception tests, reason-code loader tests, execution authority tests, evidence/context tests, legal adapter tests. |
| `LawFirm-os-exceptions-lake-runtime` | `contracts.lock.json`, `src/exceptions_lake_runtime/contract_loader.py`, `validation_gateway.py`, `evidence_packet_admission.py`, `validators/admission_validator.py`, `substrate/reason_codes.py`, `governance/substrate_mutation_guard.py`, `examples/*.json` | Exceptions Lake export, exception schemas, route/event registry, EvidencePacket v2, runtime reason codes, mutation boundary, front-door event examples | Schema or route drift rejects events or quarantines packets; reason-code changes affect admission/defect output; mutation guard changes affect canon-write prevention; example drift breaks front-door checks. | Contract loader tests, validation gateway tests, event ingestion tests, evidence packet admission tests, reason-code tests, no-canon-mutation tests, front-door example checks. |
| `LawFirm-os-legal-knowledge-runtime` | `contracts.lock.json`, `src/lawfirm_os_legal_knowledge/contracts.py`, `cli.py`, `ingestion.py`, `bundle.py`, `grounding.py`, `evals.py`, `safety.py`, `document_integrity.py`, `skill-agent-manifest.json` | Legal knowledge export, legal schemas, legal safety/eval registries, context-quality doctrine, front-door anchors, skill-agent control plane | Schema/export changes alter ingest preflight, bundle assembly, grounding, retrieval traces, safety checks, and anchored module discovery. | Ingestion preflight tests, source grounding tests, front-door validation, skill-agent validation, repo pytest. |
| `LawFirm-os-skills-registry` | `contracts.lock.json`, `src/lawfirm_os_skills_registry/contracts.py`, `domain/skill_trust_record.py`, `registry/store.py`, `registry/*.json`, `skill-agent-manifest.json`, `skills/draft/*/SKILL.md`, `factory/*.py` | Skill-agent control-plane registry, lifecycle policy, quality scoring, repo registry, AI front-door draft skill index, skill trust schema, contract surface hash | Lifecycle/scoring changes affect candidate status, quarantine, trust records, approvals, install/update audit behavior, and generated draft skills. | Skill trust tests, evaluation tests, security hardening tests, draft skill index tests, gap factory tests, first-party reactor tests, front-door and skill-agent validation. |

## Contract Lock Refresh Rule

Some governance decisions are also contract-surface decisions. When a mapped change touches a file included by `registry/contract-surface-registry.json`, downstream lock refresh must be coordinated.

Required sequence:

1. Commit the substrate contract-surface change.
2. Compute the contract surface hash from that committed substrate tree.
3. Refresh `contracts.lock.json` in each consumer repo.
4. Run contract-lock drift validation and each touched consumer repo's tests.

Do not refresh consumer locks from an uncommitted substrate working tree. The validator must fail closed when contract-surface paths are dirty.

## Experiment Rule

Experiments with governance settings must be treated as branch-local or proposal-local until approved.

| Experiment type | Allowed posture |
|---|---|
| Compare threshold values | Use a branch, draft decision node, or candidate impact packet. |
| Try different autonomy color | May propose downgrade; may not restore green without human approval. |
| Change validation intensity | Must identify validators and likely runtime test impact before merge. |
| Change route/event authority | Requires substrate governance review and runtime consumer checks. |
| Change external action approval | Requires human approval model review before any external side effect. |
| Change vendor/model/prompt/tool authority | Must preserve vendor-as-consumer, not authority. |

## Layered Agent Work Plan

Use separate agents or review passes so the map can scale without collapsing authority levels.

| Layer | Agent assignment | Output |
|---|---|---|
| Surface inventory | Confirm every path in governance and registry manifests is classified. | `covered`, `no-governance-decision`, or `decision-node-needed`. |
| Registry extraction | Extract allowed values, booleans, thresholds, states, and global controls from `registry/*.json`. | Machine decision nodes. |
| Prose extraction | Extract normative decisions from `governance/**/*.md`. | Candidate prose nodes with source line anchors. |
| Downstream mapping | Map sibling repo consumers, contract locks, validators, examples, and command surfaces. | Dependency edges and likely effects. |
| Human review | Resolve duplicates, authority status, and open conflicts. | Reviewed node set. |
| Experiment design | Define safe setting experiments and expected blast radius. | Candidate experiment packets. |

## Seed Machine Map

The seed machine map is:

- `registry/governance-decision-dependency-atlas.seed.json`

Coverage is complete only when every path in `registry/governance-full-manifest.json` and every top-level `registry/*.json` path in `registry/registry-full-manifest.json` has either:

- at least one decision node,
- an explicit edge to another decision node,
- or an explicit `no-governance-decision` classification with rationale.

## Related Surfaces

- `governance/DECISION_LOG.md`
- `governance/DECISION_BOTTLENECK_AND_DECISION_MODELS.md`
- `registry/decision-model-registry.seed.json`
- `governance/AI_FRONT_DOOR_BOUNDARY.md`
- `registry/ai-front-door-registry.json`
- `governance/CROSS_REPO_MAP.md`
