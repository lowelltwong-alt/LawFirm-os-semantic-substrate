# Claim Layer Model

Status: canonical
Owner: Law Firm ontology governance maintainers

## Purpose

This file defines the authoritative model for how claims operate as the semantic
layer between raw evidence and promoted ontology artifacts.

## Canonical claim-layer posture

- The claim layer is the repository's primary unit-of-meaning layer.
- Claims may accumulate, contradict, and be superseded without direct mutation
  of canonical ontology objects.
- Promotion from claim-layer state to canonical ontology state requires explicit
  governance review and provenance-complete evidence.

## Required governance invariants

- Every governed claim must conform to `governance/CLAIM_SCHEMA.md`.
- Every governed claim must be attributable to a trust zone and provenance path.
- Claim relationships (support, contradiction, supersession) are learning
  signals and must remain auditable.

## Ownership and authority context

- Design authority for this layer is anchored by `registry/source-of-truth.json`
  (`authoritative_files.claim_layer_model`).
- This document governs claim-layer semantics; implementation details in schema,
  templates, and scripts must align to this model.
