# TALENT_INTELLIGENCE_VALIDATION_RULES

## Purpose

This document establishes initial validation and review rules for the **Talent Intelligence / Attorney Market Intelligence** extension.

These rules are intentionally governance-first and should be read as a starting validation posture rather than as a complete enforcement implementation.

---

## Core Principle

The talent-intelligence extension must preserve the repository's non-negotiables:

- claim container discipline
- authority / trust zones
- asserted / inferred / hypothesis separation
- provenance preservation
- fractal address placement
- clear example / production distinction

---

## Initial Validation Rules

### Rule 1. Canonical attorney identity must be opaque and stable

A canonical attorney record must:

- use a stable internal Law Firm-style attorney ID
- not encode firm, office, jurisdiction, or source system in the ID
- remain distinct from external identifiers

### Rule 2. External identifiers may not replace canonical identity

Bar numbers, registration numbers, profile URLs, CRM IDs, and vendor IDs must be modeled as external identifiers or source-linked evidence.

They must not be treated as the sole canonical identity key.

### Rule 3. Source-linked objects require provenance

Any source profile or source-derived object should preserve, where applicable:

- source type
- source artifact reference
- source record reference
- timestamps for observation or import

### Rule 4. Imported list labels are not ontology truth

Labels such as:

- top target
- portable book
- warm lead
- priority lateral

should remain source-linked claims, assessments, or intake metadata unless independently validated.

### Rule 5. Employment should be modeled as episodes

Changes in firm, office, or title should not overwrite canonical attorney identity.

Where possible, employment should be represented as time-bounded employment episodes.

### Rule 6. Common-name collisions require elevated review

Potentially ambiguous names should not auto-merge on name alone.

Elevated review should be required when:

- names are common
- corroborating identifiers are missing
- practice / office / jurisdiction data conflicts
- active employment episodes conflict

### Rule 7. Talent signals must remain claim-like

Signals such as:

- firm instability
- portability evidence
- relationship warmth
- outreach readiness

must remain modeled as claims or assessments with:

- subject reference
- statement
- confidence posture
- evidence or source references where possible
- review status

### Rule 8. Confidence posture must remain explicit

Important objects and claims should preserve one of the repository's epistemic postures, such as:

- asserted
- inferred
- hypothesis
- reviewed

### Rule 9. Authority zone must remain explicit

Objects and claims should carry an authority / access posture appropriate to the source and usage context.

### Rule 10. Promotion should be review-aware and reversible

If an intake mapping, identity merge, or talent signal was wrong, the system should support:

- review
- correction
- deprecation
- rollback or replacement posture where practical

---

## Initial Review Gates

### Review Gate A. Identity merge gate

Before promoting separate source-linked records into one canonical attorney identity, require at least one of:

- strong external identifier match
- strong multi-factor corroboration
- explicit human review

### Review Gate B. Provisional-to-active attorney promotion gate

A provisional attorney should not be promoted to stronger status without:

- minimum structural completeness
- at least one source profile or equivalent evidence reference
- no unresolved severe collision flags

### Review Gate C. Derived signal promotion gate

A derived signal claim should not be treated as durable governed output without:

- an intelligible statement
- a subject reference
- confidence posture
- evidence or source references where available
- review status

---

## Future Enforcement Targets

This governance document should later be translated into executable validation through:

- schema constraints
- registry-based routing
- CI checks
- example validation
- promotion workflow checks

---

## Status

Initial validation posture only. Intended for later operationalization in schemas, CI, and example checks.