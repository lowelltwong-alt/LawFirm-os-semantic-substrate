# INTAKE_LAYER_PATTERN

## Purpose

This document reserves a future governance and modeling pattern for **structured intake of external lists, exports, and source artifacts** into the LawFirm OS Semantic Substrate.

It is especially intended for future sources such as:

- Leopard List
- recruiter spreadsheets
- law-firm target lists
- conference attendee lists
- internal relationship lists
- vendor exports
- future purchased market datasets

---

## Design Position

Imported lists should not be treated as ontology truth.

They should enter the system as governed artifacts and mapped source rows that can later contribute to:

- provisional entities
- provisional claims
- review queues
- promoted governed objects

This preserves provenance, reviewability, and authority boundaries.

---

## Layer Fit

### Layer 1. Identity layer
Intake may propose or attach identifiers but should not unilaterally define canonical identity.

### Layer 2. Node layer
Intake may propose provisional entities such as:

- Attorney
n- LawFirm
- Office
- PracticeArea
- CandidateOpportunity
- ExternalProfile

### Layer 3. Claim layer
Imported rows may generate provisional claims, including:

- person appears on target list
- person works at firm
- person linked to practice
- person marked as relationship lead
- person flagged as target opportunity

### Layer 5. Validation layer
This is a major concern for intake.

Validation should eventually govern:

- required source metadata
- field mapping completeness
- controlled-value normalization
- duplicate detection posture
- review status
- promotion eligibility

### Layer 6. Retrieval layer
Intake should support later retrieval packaging such as:

- source-specific neighborhoods
- review queues
- list-to-entity traceability
- recruiter context bundles

### Layer 7. Fractal address layer
Imported artifacts, mapped rows, and promoted objects should all remain structurally addressable.

### Layer 8. Artifact layer
Primary concern.

Examples:

- raw spreadsheet upload
- vendor CSV export
- PDF list
- copied roster
- report snapshot
- annotated recruiter source file

### Optional Layer 9. Orchestration / workflow layer
If formalized later, intake should support:

- import pipelines
- staged review workflows
- promotion workflows
- sync jobs
- rejection / rollback handling

---

## Recommended Intake Stages

### Stage 1. Raw intake artifact
The unmodified incoming object.

Examples:

- CSV
- XLSX
- PDF
- scraped page snapshot
- copied table

### Stage 2. Parsed / mapped source rows
Rows or records are extracted into structured form while preserving source lineage.

### Stage 3. Provisional entities and claims
Mapped records generate provisional ontology candidates.

These are not yet promoted to governed truth.

### Stage 4. Validation and review
The system checks:

- required fields
- schema compatibility
- identifier conflicts
- duplicate risk
- authority posture
- sensitivity posture

### Stage 5. Promotion
Only after validation and review should objects or claims be promoted into stronger governed status.

---

## Core Governance Rules

### 1. Preserve provenance
Every imported row or record should preserve:

- source type
- source artifact
- import time
- row or record reference
- importer / workflow if available

### 2. Preserve source text where useful
Do not discard original source values prematurely.

Normalized values and raw source values should remain distinguishable.

### 3. Do not flatten list labels into ontology truth
List labels such as:

- top targets
- portable book
- warm lead
- priority lateral

may reflect useful sourcing judgment, but they should remain source-linked claims or assessments unless separately validated.

### 4. Authority and trust must remain explicit
Different list sources may warrant different:

- trust posture
- access controls
- review requirements
- downstream usage constraints

### 5. Promotion must be reversible where appropriate
If an intake mapping or merge was wrong, the system should support review, correction, and rollback.

---

## Leopard List And Similar Sources

Leopard List and similar recruiting or market datasets should be modeled as:

- intake artifacts
- mapped source rows
- evidence inputs
- candidate signal inputs

They should not directly define:

- canonical identity
- final employment truth
- final relationship truth
- unquestioned opportunity ranking

---

## Future Documentation / Schema Targets

Likely future follow-on work:

- source artifact schema
- import manifest schema
- mapped row schema
- promotion decision schema
- examples for list import and normalization
- intake-to-identity-resolution examples

---

## Status

Reserved for future governed buildout.