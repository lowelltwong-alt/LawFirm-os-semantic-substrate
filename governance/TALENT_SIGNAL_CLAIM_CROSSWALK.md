# TALENT_SIGNAL_CLAIM_CROSSWALK

## Purpose

This document explains how the `talent_signal_claim` object in the Talent Intelligence / Attorney Market Intelligence extension should map back to the repository's broader **core claim model**.

The goal is to prevent the extension from becoming a parallel claim system.

---

## Core Rule

`talent_signal_claim` is **not** a separate philosophy of claims.

It is a **domain-specialized claim profile** that should remain compatible with the repository's general claim discipline:

- subject
- statement / assertion
- provenance
- evidence
- authority / trust posture
- epistemic status
- lifecycle / review posture
- structural placement

In other words:

- the repo's core claim model remains sovereign
- `talent_signal_claim` is a constrained talent-domain expression of that model

---

## Why a Separate Talent Claim Profile Exists

The talent domain has recurring assessment patterns that deserve a more constrained reusable profile, such as:

- relationship warmth
- introducer strength
- market visibility
- portable book evidence
- firm instability
- outreach readiness

Without a profile, these tend to degrade into:

- loose CRM notes
- undocumented scores
- ungoverned recruiter opinions
- downstream workflow fields that masquerade as ontology truth

The purpose of `talent_signal_claim` is therefore to preserve claim discipline while still being practical for the talent-intelligence domain.

---

## Crosswalk

### Core claim concept -> Talent signal claim field mapping

| Core claim concern | Talent signal claim expression |
|---|---|
| claim identity | `claim_id` |
| subject | `subject_ref` |
| related objects | `related_object_refs` |
| claim statement | `statement` |
| claim type / profile | `signal_type` |
| evidence linkage | `evidence_refs` |
| source linkage | `source_profile_refs` |
| epistemic posture | `confidence_posture` |
| authority / access posture | `authority_zone` |
| lifecycle status | `status` |
| review posture | `review_status` |
| validity window | `valid_from`, `valid_to` |
| optional quantitative assessment | `score`, `score_band` |
| human explanation / annotation | `notes` |

---

## What This Means Semantically

A `talent_signal_claim` should be understood as:

- a first-class governed claim object
- scoped to talent-intelligence use cases
- capable of carrying evidence and review posture
- explicitly separable from intrinsic person or firm identity

Examples:

- "This law firm shows elevated instability signals."
- "This attorney appears to be a warm outreach target."
- "This attorney shows medium portable-book evidence."

These are **claims about a subject**, not intrinsic truths about what the subject is.

---

## What Must Not Happen

### 1. Scores must not float without statement logic
A raw score alone is insufficient.

### 2. CRM tags must not silently replace claims
A workflow tag may mirror a claim, but it should not become the canonical semantic object.

### 3. Talent claims must not flatten epistemic status
Asserted, inferred, hypothesis, and reviewed postures must remain visible.

### 4. Domain specialization must not sever core compatibility
The talent extension should remain mappable back to the repo's broader claim layer.

---

## Promotion Pattern

The intended pattern is:

1. evidence or source observations appear  
2. a talent-domain claim is formed  
3. review posture is applied  
4. downstream workflow systems may consume the result  
5. ontology truth remains in the governed claim object, not in the workflow field

---

## Resting Place In The Layer Model

This crosswalk primarily anchors `talent_signal_claim` in:

- Layer 3. Claim layer
- Layer 5. Validation layer
- Layer 8. Artifact / evidence layer

and only secondarily in optional layer 9 for downstream consumption.

---

## Status

Initial semantic crosswalk. Intended to preserve one claim philosophy across the repository while allowing domain-specific talent claim profiles.