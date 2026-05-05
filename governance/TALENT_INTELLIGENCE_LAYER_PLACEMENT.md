# TALENT_INTELLIGENCE_LAYER_PLACEMENT

## Purpose

This document defines where the Talent Intelligence / Attorney Market Intelligence extension should **terminate** inside the LawFirm OS Semantic Substrate so that it fits neatly into the repository's existing layer architecture.

---

## Core Placement Rule

The extension should **end semantically inside the repository's governed ontology layers** and should **not end in downstream workflow systems**.

In practice, that means:

- ontology truth ends in layers 1 through 8
- workflow, sync, campaign, and CRM execution concerns should end in an optional later orchestration layer if formalized

---

## Layer-by-Layer Resting Place

### Layer 1. Identity layer
The extension should terminate stable person and firm identity here.

Examples:
- canonical attorney ID
- canonical law firm ID
- governed external identifier attachment

### Layer 2. Node layer
The extension should terminate durable domain entities here.

Examples:
- Attorney
- LawFirm
- EmploymentEpisode
- SourceProfile

### Layer 3. Claim layer
The extension should terminate derived talent assessments here, not as intrinsic identity truth.

Examples:
- firm instability claim
- relationship warmth claim
- portable book evidence claim
- outreach readiness claim

### Layer 4. Predicate / graph layer
The extension should use governed relationship grammar here, but should not create a shadow graph outside repository discipline.

### Layer 5. Validation layer
The extension should terminate promotion, merge, and review discipline here.

Examples:
- collision controls
- provenance requirements
- source review posture
- signal review posture

### Layer 6. Retrieval layer
The extension should eventually terminate governed recruiter / market retrieval neighborhoods here.

### Layer 7. Fractal address layer
The extension should terminate structural placement here so that objects, claims, and artifacts remain addressable inside the larger architecture.

### Layer 8. Artifact layer
The extension should terminate imported lists, snapshots, source captures, and other intake materials here.

Examples:
- Leopard List artifacts
- recruiter spreadsheets
- source snapshots
- vendor exports

### Optional Layer 9. Orchestration / workflow layer
If a ninth layer is later formalized, this is where the extension should place:

- CRM / ATS sync
- campaign packaging
- workflow state transitions
- import jobs
- validation jobs
- promotion pipelines

This layer should remain downstream from ontology truth.

---

## Neat-Fit Rule

A simple test for future additions:

- if it defines **what a thing is**, it likely belongs in layers 1 through 3
- if it governs **whether a thing can be trusted or promoted**, it likely belongs in layer 5
- if it preserves **where a thing came from**, it likely belongs in layer 8
- if it performs **automation or movement across systems**, it likely belongs in optional layer 9

---

## Practical Ending For This Extension

The cleanest current resting place is:

- semantic center of gravity: layers 1, 2, 3, 5, and 8
- future expansion path: layers 6 and 7
- downstream operational end: optional layer 9

That means this extension is best understood as:

- identity-aware
- claim-aware
- evidence-aware
- validation-aware
- artifact-aware

rather than as a CRM-first or workflow-first module.

---

## Status

Initial placement guidance only. Intended to keep the extension architecturally neat as buildout continues.