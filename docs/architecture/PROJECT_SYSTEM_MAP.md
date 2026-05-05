# Project System Map

## Purpose

Explain how the repository works as one integrated system instead of a loose set
of ontology, schema, document, retrieval, and sponsor artifacts.

## Core Idea

Law Firm is a semantic-governance substrate and Innovation OS contract repository.

It combines:
- stable canonical meaning
- machine-checkable validation layers
- governed runtime learning objects
- canonical document structure
- derived document and evidence artifacts
- retrieval and access control contracts
- sponsor and operator handoff surfaces

## System Layers

### 1. Canonical Meaning Layer

The ontology and taxonomy modules define stable meaning. This is the design
authority for concepts, relationships, provenance expectations, and controlled
semantic boundaries.

### 2. Contract and Validation Layer

SHACL, JSON Schema, and the active registries define what the repository will
accept as structurally valid. This layer keeps doctrine, examples, runtime
objects, and derived outputs from drifting apart.

### 3. Runtime Learning Layer

The exceptions and Innovation OS objects capture friction, pressure, ranked
opportunities, bounded execution, gate review, scale packaging, and promotion
decisions.

This layer is operational and governed, but it is not canonical meaning.

### 4. Canonical Document Structure Layer

The document model preserves stable source structure, exact spans, citations,
and canonical boundaries. This is the source-of-truth layer for document
identity, versions, normalized text, components, citations, and span selectors.

### 5. Derived Document and Evidence Layer

Chunks, embeddings, index builds, retrieval-support objects, and answer-support
objects are rebuildable derivatives of canonical document structure. They may
accelerate retrieval and grounding, but they may not redefine source
boundaries.

### 6. Retrieval and Access Control Layer

Retrieval, answer, and access-control contracts consume canonical document
structure and its derived evidence artifacts. This is where privilege-aware
filtering, eligibility rules, observability, and grounded answer assembly
happen.

### 7. View and Adoption Layer

Executive packets, one-page views, supported questions, prompt kits, and role
handoff materials make the governed stack usable by sponsors, KM owners, and
platform architects.

### 8. Governance and Operating Cadence Layer

Lifecycle, stewardship, review roles, mutation controls, and release guidance
define how the system changes safely over time.

## How The Pieces Work Together

1. ontology and taxonomy define stable meaning
2. registries, shapes, and schemas declare the allowed control surface
3. canonical document structure preserves source truth and exact traceability
4. derived document and evidence artifacts are rebuilt from that canonical structure
5. retrieval and access contracts consume canonical structure and derived evidence safely
6. runtime learning objects capture friction and propose change candidates
7. promotion decisions remain the only lawful path for canonical change
8. sponsor and operator materials translate the governed system into action

## Design Rules

- Keep canonical meaning, runtime learning, evidence, and action surfaces distinct.
- Treat document structure as the source of truth and retrieval artifacts as derived.
- Preserve the mutation boundary: runtime objects may inform change but may not
  directly rewrite canonical ontology, taxonomy, schema, or policy surfaces.
- Prefer one active control surface over duplicate doctrine or parallel schema families.

## Boundary Contracts

Use these as the active control documents:

- `governance/SYSTEM_MAP.md`
- `governance/DECISION_LOG.md`
- `governance/ONTOLOGY_BOUNDARY_CONTRACT.md`
- `governance/CANONICAL_DOCUMENT_MODEL.md`

## Practical Reading Order

1. `README.md`
2. `governance/SYSTEM_MAP.md`
3. `governance/DECISION_LOG.md`
4. `docs/poc/CINO_EXECUTIVE_BRIEF.md`
5. `docs/poc/ONE_PAGE_ARCHITECTURE_VIEW.md`
6. `docs/governance/CONTENT_STEWARDSHIP_MODEL.md`
7. `docs/prompts/README.md`
