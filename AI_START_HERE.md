# AI Start Here  -  LawFirm OS Semantic Substrate

This file is the primary entry point for AI systems and new contributors reading this repository.

It explains what this repo is, where authority lives, what to read first, and what not to assume.

---

## What this repository is

Law Firm is a **semantic-governance substrate** and **Innovation OS contract repository**.

It contains the governed artifacts that define:
- canonical meaning (ontology, taxonomy, controlled terms)
- validation and structural contracts (schemas, shapes, scripts)
- policy and change controls (registries, doctrine, authority boundaries)
- runtime learning and operating objects (exceptions, pressure, opportunity, promotion)
- retrieval and interoperability contracts
- tool-neutral AI contributor governance and adapter boundaries

It is **not** the canonical home for runtime embeddings, vector indexes, GraphRAG summaries, OCR model artifacts, or answer caches.

---

## Read in this order

Read these in sequence before editing, reasoning over the repo, or generating changes:

1. `AI_START_HERE.md`  -  this file
2. `AGENTS.md`  -  agent operating contract for narrow PRs, validation, and no-hallucination repo work
3. `registry/source-of-truth.json`  -  current repo role, authoritative files, precedence order, and layer model
4. `registry/design-authority.json`  -  design principles, authority posture, and non-negotiables
5. `governance/AI_CONTROL_PLANE_BOUNDARY.md`  -  neutral AI control-plane rule and adapter boundary
6. `governance/SYSTEM_MAP.md`  -  concise map of the major layers and folders
7. `governance/REPO_DOCTRINE.md`  -  canonical vs derived and mutation boundary
8. `governance/EXCEPTIONS_LAKE_BOUNDARY.md`  -  contract/runtime boundary for governed exception learning
9. `governance/canonical_spine_manifest.json`  -  current canonical schema set and validation scripts
10. `registry/schema-registry.json`  -  active schema key -> file mapping used by validators
11. `scripts/check_registry_refs.py`  -  verifies that referenced authoritative paths actually exist

## Handoff orientation

If the task is to understand or explain the repository, also read:

- `docs/HANDOFF_INDEX.md`
- `docs/REPO_ORIENTATION_GUIDE.md`
- `docs/ENTRYPOINT_AND_ENDPOINT_MAP.md`
- `docs/AI_FRONT_DOOR_QUESTIONS.md`

If the audience is executive or operational, read:

- `docs/CINO_EXECUTIVE_BRIEF.md`
- `docs/AUTOMATION_MANAGER_STARTER_PACK.md`

If the task involves future Exceptions Lake runtime planning, also read:

- `docs/EXCEPTIONS_LAKE_RUNTIME_BUILD_PACK.md`
- `docs/EXCEPTIONS_LAKE_CONTRACT_CONSUMPTION_MAP.md`
- `docs/EXCEPTIONS_LAKE_RUNTIME_REPO_SKELETON.md`

Use these documents to orient humans. Do not treat them as higher authority than `registry/source-of-truth.json`, `registry/design-authority.json`, or validated operational files.

---

## Important current-state note

The repo is in an active alignment phase.
Some older front-door documents and registries still refer to legacy or partially reconciled surfaces.

When two files seem to disagree, use this order:

1. `registry/source-of-truth.json`
2. `registry/design-authority.json`
3. `governance/AI_CONTROL_PLANE_BOUNDARY.md`
4. live validated operational files (`registry/schema-registry.json`, `governance/canonical_spine_manifest.json`, validation scripts)
5. narrative docs (`docs/`, older roadmap text, audit notes)

For **active schema resolution**, use `registry/schema-registry.json`.
Do **not** guess from filenames alone.

---

## Folder roles at a glance

- `governance/`  -  doctrine, manifests, operating rules, lifecycle guidance
- `registry/`  -  source-of-truth, design authority, registries, deprecations
- `.ai/`  -  neutral AI control-plane kernels, risk tiers, approval rules, and adapter guidance
- `ontology/`  -  semantic meaning layer
- `shapes/`  -  SHACL and validation shapes
- `schemas/`  -  concrete JSON schemas for governed object types
- `schema/`  -  schema-set manifest and interface/invariant structure
- `scripts/`  -  validation and enforcement tooling
- `interop/`, `mappings/`, `profiles/`, `standards/`  -  reference and interoperability layer
- `examples/`, `data/`, `graphs/`  -  examples and derived/non-authoritative artifacts
- `docs/`, `reports/`, `eval/`, `templates/`  -  supporting narrative and generated materials
- `legacy/`, `archive/`  -  historical only, not active authority

See `FOLDER_SEMANTICS.md` and `AUTHORITY_MAP.yaml` for the fuller version.

---

## What not to do

- Do not treat `examples/`, `data/`, `graphs/`, or `reports/` as canonical truth.
- Do not infer authority from filename similarity or recency.
- Do not confuse `schema/` with `schemas/`.
- Do not treat `docs/` as normative if it conflicts with `registry/` or `governance/`.
- Do not treat vendor adapter files as semantic authority.
- Do not mutate canonical meaning based on raw runtime artifacts.
- Do not use `legacy/` or `archive/` for active design decisions.
- Do not build runtime Exceptions Lake storage or ingestion behavior in this repo.

---

## Safe default

If you are unsure where truth lives, start at:
- `registry/source-of-truth.json`
- `registry/design-authority.json`
- `governance/AI_CONTROL_PLANE_BOUNDARY.md`
- `governance/SYSTEM_MAP.md`
- `registry/schema-registry.json`

If the task involves exception learning, agent review findings, failed validators, retrieval misses, or runtime-boundary questions, also read:
- `AGENTS.md`
- `governance/EXCEPTIONS_LAKE_BOUNDARY.md`
