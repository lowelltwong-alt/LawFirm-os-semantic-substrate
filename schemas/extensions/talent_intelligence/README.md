# Talent Intelligence Extension Schemas

This directory contains the first machine-readable schema skeleton for the **Talent Intelligence / Attorney Market Intelligence** extension.

These schemas are intentionally narrow and should be treated as a **smallest useful extension kernel** rather than a complete domain model.

---

## Current Scope

The initial schema set includes:

- `attorney.schema.json`
- `law_firm.schema.json`
- `employment_episode.schema.json`
- `external_identifier.schema.json`
- `source_profile.schema.json`
- `talent_signal_claim.schema.json`

These are intended to establish a durable modeling pattern for:

- canonical attorney identity
- law firm identity
- time-bounded attorney employment
- external identifier attachment
- source-profile evidence inputs
- derived and evidence-backed talent signal claims

---

## Design Rules

### 1. Canonical identity remains primary

Canonical FMG entity identity should remain stable and opaque.

Examples:

- `ATY_...`
- `LF_...`

External identifiers such as bar numbers, profile URLs, CRM IDs, and vendor IDs should attach to canonical objects rather than replace them.

### 2. Source material is not ontology truth

Raw source records should enter as source profiles, intake artifacts, or evidence-linked inputs.

Promotion to stronger governed status should only occur after mapping, validation, and review.

### 3. Employment is time-bounded

Attorney affiliation with firms, offices, and titles should be modeled as episodes rather than overwritten single-state facts.

### 4. Analytics remain claims, not intrinsic identity

Signals such as:

- relationship warmth
- portability evidence
- firm instability
- outreach readiness

should remain modeled as claims or assessments with provenance, confidence, and review posture.

### 5. Authority and confidence must remain visible

Every important object or claim should preserve:

- authority zone
- status
- confidence posture
- source / evidence references where applicable

---

## Validation Direction

Future validation should enforce at least:

- required provenance on source-linked objects
- minimum structure for talent signal claims
- review gates for ambiguous identity merges
- no promotion of imported list labels into unquestioned truth
- explicit support for asserted / inferred / hypothesis separation

---

## Current Status

Initial schema scaffold only.

These files should be expanded carefully under repository governance rather than treated as final production models.