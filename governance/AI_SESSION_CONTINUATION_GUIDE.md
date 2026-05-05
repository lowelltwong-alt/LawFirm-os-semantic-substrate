# AI Session Continuation Guide

Author: Lowell T. Wong

## Purpose

This document is a handoff and continuation guide for future AI chat sessions, agents, and collaborators working on this repository.

It explains:
- what this repository is trying to become
- what design decisions have already been made
- how the recursive / fractal / DNA-like architecture works
- where the self-reinforcing structure lives in the repository
- how to safely improve and extend the system
- what source materials must be uploaded if a future AI session is expected to reason from them directly

## Repository Position

This repository is a **governed example architecture**, not a production implementation.

It is a derivative adaptation of ontology and knowledge-architecture work originally developed by Lowell T. Wong in the Logos project and related personal architecture work, then adapted for an Law Firm work-resource context.

The repository is intended to demonstrate a bounded, governable ontology pattern that is:
- recursive
- fractal
- AI-ingestible
- retrieval-aware
- lineage-aware
- trust-aware
- governable across domains

## What Makes This Repository Different

This repository is not only trying to define entities and relationships.
It is trying to define an **ontology operating system** in which:
- artifacts are first-order governed objects
- claims are first-order governed reasoning objects
- trust applies to objects, artifacts, and edges
- structural address and lineage are treated as architectural concerns
- deterministic and probabilistic systems can interoperate without collapsing into each other
- future AI tools can map into the system rather than replace its semantics

## Core Design Decisions Already Made

### 1. First-order artifact thinking
Artifacts are treated as first-order governed objects, not passive files.

Core dimensions include:
- identity
- structural address
- graph relations
- lineage / attribution
- state / lifecycle
- optional semantic coordinates

### 2. Fractal address system
The system distinguishes between:
- stable identity (`id`)
- structural placement (`address`)

The address system is derived from Logos-project thinking and is intended to let each major object know where it sits in the larger system.

### 3. Trust-aware ontology
Trust and authority are not limited to source documents.
They apply to:
- objects
- artifacts
- claims
- edges / relationships
- retrieval objects

### 4. Claim layer as reasoning core
Nodes and predicates alone are not sufficient.
Claims are used as first-order governed statements with:
- subject / predicate / object
- trust level
- authority zone
- review state
- evidence refs
- lineage
- AI retrieval posture

### 5. Deterministic / probabilistic separation
The repository distinguishes between:
- structural truth (deterministic, governed)
- semantic enrichment (probabilistic, model-derived)

These can operate separately, sequentially, or in tandem.

### 6. Example, not production
The repository is intentionally labeled as:
- example architecture
- public-data-informed
- non-production

This distinction should be preserved unless and until a separate production layer is intentionally created.

## Where the Self-Reinforcing Structure Lives

Future AI sessions should look here first.

### Root framing
- `README.md`
- `EXAMPLE_USE_AND_LIMITATIONS.md`
- `SYSTEM_OVERVIEW.md`
- `LINEAGE_AND_ATTRIBUTION.md`
- `HOW_TO_READ_THIS_REPO.md`
- `ROADMAP.md`

### Governance core
- `governance/FIRST_ORDER_ARTIFACT_PRINCIPLES.md`
- `governance/FRACTAL_ADDRESS_SYSTEM.md`
- `governance/GRAPH_MODEL.md`
- `governance/RETRIEVAL_MODEL.md`
- `governance/SOURCE_LINEAGE_MODEL.md`
- `governance/DETERMINISTIC_AND_PROBABILISTIC_INTEROP.md`
- `governance/SEMANTIC_COORDINATES_AND_AI_LAYER.md`
- `governance/DOMAIN_EXTENSION_MODEL.md`
- `governance/CLAIM_LAYER_MODEL.md`
- `governance/ARTIFACT_ORDER_AND_LIFECYCLE.md`

### Canonical schemas and validation
- `schemas/claim_v3.schema.json`
- `schemas/artifact.schema.json`
- `registry/schema-registry.json`
- `scripts/validate_examples_canonical.py`
- `scripts/validate_examples_registry.py`
- `.github/workflows/validate-canonical.yml`
- `.github/workflows/validate-registry.yml`

### Example objects
- `examples/claims/`
- `examples/artifacts/`

## How the System Works Together

### Layer 1: Governance
Defines principles, rationale, and architectural constraints.

### Layer 2: Schemas
Defines machine-checkable object structures.

### Layer 3: Examples
Shows how the schemas are instantiated in example form.

### Layer 4: Validation
Uses scripts and GitHub Actions to enforce structural coherence.

### Layer 5: Future retrieval / reasoning / decision layers
This is where the system is intended to grow next.

## How to Reproduce This Architecture in Another Repo

1. Start with root framing documents.
2. Establish first-order artifact principles.
3. Separate identity from structural address.
4. Build claim layer, not just node layer.
5. Add trust, lineage, and lifecycle logic early.
6. Treat examples as example-only and non-production.
7. Add schema validation before large-scale content growth.
8. Move from folder-based validation toward self-declared schema routing.
9. Add domain modules only after the shared DNA is clear.
10. Expand one validated type at a time.

## How Future AI Sessions Should Improve This Repository

Future sessions should improve this repository in the following order:

### Priority 1: Keep the system coherent
- avoid duplicating workflows
- avoid overlapping schema generations without clear migration logic
- prefer canonical files over parallel drift

### Priority 2: Expand validation safely
- add node validation
- add retrieval validation
- add source / chunk validation
- add cross-reference validation

### Priority 3: Strengthen reasoning
- support / contradiction claim modeling
- resolution / promotion workflows
- confidence propagation

### Priority 4: Improve interoperability
- schema registry expansion
- migration from folder-based assumptions to self-declared schema routing
- external reference mappings for future systems

### Priority 5: Build execution layers
- decision-layer integration
- retrieval ranking rules
- graph-based cross-reference validation

## Source Documents and Upload Requirement

If a future AI session is expected to reason from source documents directly, those source materials must be uploaded to the chat or made accessible through the relevant connected source.

Do not assume a future AI session can infer or recover unuploaded source materials from prior conversation alone.

When source-driven work is needed, upload or provide:
- the relevant repo files
- source documents
- diagrams
- schema files
- current workflow files
- any comparison or error logs

## What to Preserve

Future AI sessions should preserve these high-level commitments unless intentionally changed:
- recursive / fractal design
- first-order artifact thinking
- separation of identity vs address
- claim-centered reasoning
- trust-aware ontology
- lineage and attribution chains
- deterministic / probabilistic interoperability
- example / non-production distinction

## Final Note to Future AI Sessions

Do not treat this repository as a random collection of files.
Treat it as a developing ontology operating system.

The correct pattern is:
- reconcile first
- validate second
- expand third
- automate fourth

If uncertainty exists, prefer:
- fewer canonical files
- stronger validation
- explicit lineage
- clearer design rationale

over premature expansion.
