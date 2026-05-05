# TALENT_INTELLIGENCE_EXTENSION

## Purpose

This document reserves and frames a future **Talent Intelligence / Attorney Market Intelligence** extension within the LawFirm OS Semantic Substrate.

It is intentionally positioned as a **governed extension** that must fit under the repository's existing architecture rather than compete with or supersede it.

---

## Design Position

The current repository architecture remains sovereign.

The talent-intelligence domain should therefore be modeled as:

- a reuse-heavy extension
- evidence-backed and provenance-aware
- authority-aware
- claim-aware
- identity-disciplined
- compatible with fractal address placement

This extension should not introduce a parallel top-level ontology.

---

## Domain Scope

This future extension is expected to support concepts such as:

- Attorney
- LawFirm
- Office
- PracticeArea
- EmploymentEpisode
- BarCredential
- ExternalProfile
- RelationshipEdge
- IntroducerEdge
- Recognition
- ThoughtLeadershipArtifact
- LeadershipRole
- CourtFilingActivity
- CandidateOpportunity
- FirmInstabilitySignal
- PortableBookEvidence

These concepts must be connected back to the repository's existing identity, node, claim, validation, artifact, retrieval, and address layers.

---

## Layer Fit

This extension is expected to fit the repository's current multi-layer system as follows:

### Layer 1. Identity layer
- stable Law Firm attorney IDs
- stable law-firm IDs
- external identifiers attached but not treated as canonical identity

### Layer 2. Node layer
- Attorney
- LawFirm
- Office
- PracticeArea
- CandidateOpportunity

### Layer 3. Claim layer
- relationship claims
- portability evidence claims
- instability signal claims
- recognition claims
- employment claims

### Layer 4. Predicate / graph layer
- works_at
- worked_at
- admitted_in
- recognized_by
- connected_to
- introduced_by
- affiliated_with

### Layer 5. Validation layer
- merge review posture
- source validation
- required provenance
- common-name collision checks

### Layer 6. Retrieval layer
- recruiter / talent neighborhoods
- firm-centered and attorney-centered retrieval packages
- relationship and signal-aware context expansion

### Layer 7. Fractal address layer
- structural placement of talent objects, claims, and artifacts inside the larger ontology grammar

### Layer 8. Artifact layer
- firm bios
- imported lists
- recruiter notes
- vendor exports
- market reports
- source snapshots

### Optional Layer 9. Derived / orchestration layer
If the repository later formalizes a ninth layer for orchestration, packaging, or execution logic, talent intelligence should also fit there through:

- CRM sync mappings
- workflow packaging
- campaign objects
- recruiter task bundles
- promotion rules from provisional to governed objects

This document does not create that ninth layer, but it leaves room for it.

---

## Architectural Fit Rules

### 1. Reuse core primitives first

Wherever possible, this extension should reuse existing repository primitives for:

- identity
- governed nodes
- claim containers
- evidence linkage
- authority zones
- trust posture
- retrieval neighborhoods
- lifecycle state
- fractal address placement

### 2. Keep analytics separate from ontology truth

Items such as the following should not be treated as intrinsic ontology truth:

- portability score
- instability score
- outreach priority
- relationship warmth score
- visibility score

These should remain modeled as assessments, claims, or derived artifacts with:

- provenance
- evidence
- confidence
- review posture
- lineage

### 3. Preserve time-bounded reality

Attorney careers change over time.

The ontology should therefore preserve:

- employment episodes
- title changes
- practice changes
- office movement
- recognition periods
- relationship history

### 4. Preserve source separation

Raw source material should remain distinguishable from normalized ontology objects.

Examples:

- law firm bio page
- LinkedIn profile snapshot
- bar directory result
- Leopard List import
- recruiter spreadsheet
- CRM system record

### 5. Preserve example / production distinction

This extension remains planning and governance work unless and until a production-bound implementation layer is intentionally created.

---

## Future Buildout Targets

Likely future expansion areas include:

- schemas for talent-intelligence entities and claims
- examples for identity resolution
- governed intake artifacts for market lists
- relationship and introducer modeling
- recruiter retrieval neighborhoods
- synchronization rules for CRM / ATS tools

---

## Status

Reserved for future governed buildout.