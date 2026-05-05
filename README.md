# LawFirm OS Semantic Substrate

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
