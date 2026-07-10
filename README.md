# LawFirm OS Semantic Substrate

Canonical machine name: `LawFirm-os-semantic-substrate`. Human label: Law Firm OS Semantic Substrate. Sibling repos and authority order across repos are defined in `governance/CROSS_REPO_MAP.md`.

Law Firm is the semantic-governance substrate and Innovation OS contract repository for this project.

It is the canonical home for machine-readable meaning, evidence structure, change policy, and governed operating contracts. It is not a production runtime, a system-of-record deployment, or the canonical store for embeddings, indexes, OCR model specifics, GraphRAG summaries, or answer caches.

## What Lives Here

The repository keeps four layers explicit:

1. Ontology and taxonomy
   Stable meaning, identifiers, classes, relations, and controlled vocabularies.

2. Evidence and provenance
   Canonical document, span, citation, trace, and derivation contracts that preserve source structure.

3. Policy and governance
   Design authority, lifecycle, mutation boundary, access rules, promotion logic, and authoritative registries.

4. Action and runtime contracts
   Governed exception intake, pressure aggregation, operating objects, validation gates, scale packages, and promotion decisions.

## Phase 2 Innovation Autonomy + Harness Layer

This repo now carries the control-plane authority artifacts for the Phase 2 Innovation Autonomy + Harness Layer.

Core law:

```text
Risk color controls authority.
Hardness controls harness depth.
Leverage controls priority.
Stakes size controls escalation sensitivity.
Reversibility controls autonomy.
Frequency controls compounding value.
```

`schemas/` (plural) is the canonical machine-readable JSON Schema authority layer. New Phase 2 machine-readable schemas go under `schemas/` unless a future compatibility-preserving governance change says otherwise. `registry/` is the canonical discovery surface for schema and governance references.

A separate `schema/` (singular) directory exists as a legacy / Phase 1 / draft doctrinal-comparison substrate. It does **not** replace `schemas/` and is non-canonical for Phase 2 work. Any future migration or renaming of `schema/` must be a separate compatibility-preserving cleanup PR.

Existing root-level Innovation OS schemas remain in place for backward compatibility and remain discoverable through `registry/schema-registry.json` and `registry/innovation-object-registry.json`. New Phase 2 schema families are grouped by concern:

- `schemas/autonomy/` for red/yellow/green lane, assumption watch, reclassification, and restoration records.
- `schemas/harness/` for harness plans, agent reviews, frontier reviews, and Codex task packets.
- `schemas/research/` for local-only research requests, briefs, and incident analogy records.
- `schemas/innovation/` only for genuinely new Innovation OS objects that did not already exist at root.

See:

- `registry/adversity-class-registry.candidate.json` and `governance/ADVERSITY_CLASS_REGISTRY_BOUNDARY.md` for the synthetic-only PR-LL4 adversity vocabulary review contract; it does not define legal conflict classes or authorize runtime use.
- `governance/PHASE_2_SCHEMA_PLACEMENT.md`
- `governance/PHASE_2_ROADMAP.md`
- `governance/INNOVATION_AUTONOMY_LAYER.md`
- `governance/AUTONOMY_RYG_POLICY.md`
- `governance/HARNESS_INTENSITY_POLICY.md`
- `DATA_FLOW_MAP.md`
- `AI_WORK_START_HERE.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ENDPOINTS_AND_COMMANDS.md`
- `RECENT_WORK.md`

Roadmap note: PR07 is reserved for Decision Intelligence, Stakes Model, and Research Radar Seeding. It is local-only and schema-first. It must not add live web crawling, scheduled jobs, model calls, external APIs, external writes, autonomous research execution, or production research automation.

## AI Strategy Doctrine and Context Quality Governance

The following Semantic Substrate governance documents are proposed doctrine or reference materials and are not canon until approved through this repo's governance process:

- [governance/AI_STRATEGY_DOCTRINE.md](governance/AI_STRATEGY_DOCTRINE.md) is the proposed controlling doctrine for vendor-agnostic AI strategy, proprietary context, decision models, Legal Context Bundles, Evidence Packets, model/provider adapters, skill trust records, and governed promotion paths.
- [governance/STRATEGIC_REFERENCE_PROPRIETARY_CONTEXT.md](governance/STRATEGIC_REFERENCE_PROPRIETARY_CONTEXT.md) is a strategy reference, not an implementation mandate.
- [governance/SHANNON_INFORMATION_THEORY_CROSSWALK.md](governance/SHANNON_INFORMATION_THEORY_CROSSWALK.md) is a technical crosswalk and must not be used as legal-truth math.
- [governance/CONTEXT_QUALITY_DOCTRINE.md](governance/CONTEXT_QUALITY_DOCTRINE.md) defines Legal Context Bundles and context-quality controls.
- [governance/INSTITUTIONAL_KNOWLEDGE_ENCODING_STANDARD.md](governance/INSTITUTIONAL_KNOWLEDGE_ENCODING_STANDARD.md) defines how institutional knowledge must be scoped, sourced, reviewed, and governed.

Related decision-bottleneck scaffolds remain separate from the draft doctrine above:

- `governance/DECISION_BOTTLENECK_AND_DECISION_MODELS.md`
- `registry/decision-model-registry.schema.json`
- `registry/decision-model-registry.seed.json`

The first planned PR07 Research Radar watchlist seed is `research-radar-frontier-ai-001` for `frontier_ai_capability`. The roadmap also reserves additional local-only seed topics for math breakthroughs, agent failures, prompt injection, legal AI ethics, model provider policy changes, harness design, RAG quality, workflow orchestration, decision science, creativity with AI, law-firm reputation risk, and billing/carrier changes. These are roadmap evidence only until PR07 adds schemas and local object builders.

`registry/research-radar-source-registry.json` already exists as pre-PR07 draft scaffolding. It is metadata-only and non-authorizing, and does not authorize live crawling, scheduled jobs, model calls, external APIs, external writes, or production research automation. PR07 may later formalize, supersede, or reconcile it.

## Mutation Boundary

Raw runtime objects must never rewrite canonical meaning directly.

The lawful paths are:
- `exception-event -> pressure-vector -> adaptation-proposal -> promotion-decision`
- `exception-event -> pressure-vector -> opportunity-object -> sprint-object or pilot-object -> validation-gate-record -> scale-package-object -> promotion-decision`

Nothing before `promotion-decision` may directly mutate ontology, taxonomy, core schema, or canonical policy files.

## Contract Surfaces

This repository distinguishes three tiers of contract surface and one derived layer. These tiers match `AUTHORITY_MAP.yaml` and `MACHINE_NAVIGATION_MANIFEST.json`.

**Canonical tier**  -  authoritative meaning, precedence, and mutation rules. Changes here require an explicit promotion decision.
- `registry/`
- `governance/`

**Operational tier**  -  implements and enforces the canonical layer. Governed, but not the final seat of authority.
- `ontology/`
- `shapes/`
- `schemas/`

**Reference tier**  -  external alignment and interoperability surfaces.
- `profiles/`
- `standards/`

**Derived or regenerable surfaces**  -  must not redefine canonical meaning.
- chunks
- embeddings
- indexes
- GraphRAG summaries
- answer caches
- release snapshots
- merge packs
- environment-specific execution artifacts

## Active Entry Points

Start here:
1. `AI_START_HERE.md`
2. `registry/source-of-truth.json`
3. `registry/design-authority.json`
4. `governance/SYSTEM_MAP.md`
5. `governance/REPO_DOCTRINE.md`
6. `governance/ALIGNMENT_FIRST_ROADMAP.md`
7. `governance/PHASED_INTEGRATION_BACKLOG.md`
8. `governance/INNOVATION_OS_OPERATING_SYSTEM.md`

## Handoff and Orientation

For role-based orientation and handoff:

- `docs/HANDOFF_INDEX.md`  -  role-based table of contents
- `docs/CINO_EXECUTIVE_BRIEF.md`  -  executive framing and current decision posture
- `docs/AUTOMATION_MANAGER_STARTER_PACK.md`  -  intake, scoring, and first-30/90-day guidance
- `docs/EXCEPTIONS_LAKE_RUNTIME_BUILD_PACK.md`  -  future runtime build-pack guidance, contract consumption map, and separate runtime repo skeleton
- `docs/ENTRYPOINT_AND_ENDPOINT_MAP.md`  -  human and machine entrypoints, validation map, and boundary map
- `docs/REPO_ORIENTATION_GUIDE.md`  -  plain-English explanation of what this repo is
- `docs/AI_FRONT_DOOR_QUESTIONS.md`  -  suggested orientation questions for humans and AI assistants
- `governance/CURRENT_STATE_AND_ROADMAP.md`  -  current state, next phases, and explicit non-negotiables

These handoff docs help people orient quickly. They do not outrank `registry/source-of-truth.json`, `registry/design-authority.json`, or validated operational files.

## Repository Layout

- `ontology/` canonical semantic modules
- `shapes/` SHACL validation for ontology modules
- `schemas/` JSON contracts for canonical, runtime, retrieval, and view objects
- `examples/` validating example objects and thin slices
- `profiles/` vendor and system adapter profiles
- `mappings/` explicit source-to-canonical mappings
- `governance/` doctrine, operating rules, and release guidance
- `registry/` authoritative registries and precedence surfaces
- `standards/` stable cross-cutting policies
- `scripts/` validation and build tooling
- `docs/` role-based orientation, executive handoff, and operator guidance

## Current Scope

The current contract surface already includes:
- stable core ontology and taxonomy scaffolds
- canonical document and evidence modeling
- governed exception and pressure schemas
- Innovation OS action-layer schemas
- retrieval, access, and view contracts
- draft vendor profiles and thin-slice examples

What is still being hardened:
- registry coverage across all active schema files
- in-place consolidation of older authoritative docs
- missing examples for some document, retrieval, and view contracts
- deeper SHACL coverage beyond the core path
- CI hardening for the newer contract surface
- intake-to-budget candidate contract review, including the Orchestrator/Lake
  packet-boundary lane, before any canonical promotion

## Current Guarantees

What this repo can accurately claim today:

- contract readiness for canonical, retrieval, governance, and governed-learning surfaces
- validation readiness through unit tests, drift checks, schema/example checks, and the repo-wide audit wrapper
- fail-closed unsupported-claim behavior when governed support is absent
- metadata-only source-ingestion gating before an internal document is treated as a governed source
- deny-by-default sensitivity and allowed-use gating for governed evidence
- an Exceptions Lake contract boundary seed and synthetic governed-learning harnesses
- synthetic grounded-answer evaluation readiness for grounding, refusal, and unavailable-support behavior

Release-grade summary for reviewers and contributors:
- `reports/RELEASE_READINESS_AUDIT.md`

## What This Repo Does Not Claim

This repo does **not** currently claim:

- internal corpus completeness or ingested firm knowledge coverage
- production retrieval accuracy, precision, recall, or coverage
- production answer quality or business correctness
- a production runtime Exceptions Lake
- production-safe autonomous runtime behavior
- validation against live firm operations or internal incident history
- core SHACL conformance for `shapes/core.ttl` against `shapes/core.shacl.ttl`

## Local Checks

Reviewer command block:

Install the local validation dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the focused unit test suite:

```bash
python -m unittest discover -s scripts/validation/tests -p 'test_*.py'
```

Run pytest through the validation runtime wrapper:

```bash
python scripts/run_full_pytest.py
```

`config/validation-runtime-policy.yaml` sets a 3600 second minimum ceiling for full and focused pytest. Direct `python -m pytest` is blocked so local validation cannot fail just because an agent inherited a short/default timeout.

Run the repo drift gate:

```bash
python scripts/check_repo_drift.py
```

Run the full audit:

```bash
bash scripts/run_full_audit.sh
```

Expected full-audit note:

- the audit currently stops at the known truthful SHACL fail-closed gate
- that stop is expected because `shapes/core.ttl` is not yet a trustworthy same-namespace focus-node data graph for `shapes/core.shacl.ttl`
- core SHACL conformance is not currently claimed until that data-vs-shape pair exists
- no earlier validation stage should fail when the repo is healthy

## Next Major Steps

- approved internal corpus ingestion through the source-ingestion manifest and provenance gate
- approved gold cases for real evaluation scoring beyond synthetic readiness
- resolution of the known SHACL fail-closed condition with a trustworthy same-namespace test pair
- future runtime implementations that consume this repo's versioned contracts without redefining them
- runtime build-pack planning through `docs/EXCEPTIONS_LAKE_RUNTIME_BUILD_PACK.md`, `docs/EXCEPTIONS_LAKE_CONTRACT_CONSUMPTION_MAP.md`, and `docs/EXCEPTIONS_LAKE_RUNTIME_REPO_SKELETON.md`

## Working Rules

- Prefer in-place rewrites of authoritative files over parallel replacements.
- Keep ontology, evidence, policy, and action layers distinct.
- Register draft files as draft; do not let draft contracts masquerade as stable canon.
- Preserve the no-direct-mutation boundary from raw runtime evidence to canonical truth.

## Status

Draft canonical contract repository with validating examples and active reconciliation work.

---

## Related Runtime Repositories

This repo is designed to govern related runtime/application repos.

Primary related repo:

- `exceptions-lake-runtime-main`  -  runtime/prototype layer for exception capture, classification, scoring, routing, and learning loops.

The ontology repo defines the language and governance model. Runtime repos should align to it rather than creating conflicting definitions.

## License

This project is **source-available**, not open source: the materials are publicly visible for review, discussion, and portfolio or reference purposes only, and all rights are reserved. See [LICENSE.md](LICENSE.md) for copyright notice, restrictions, and how to request written permission or discuss commercial use.
