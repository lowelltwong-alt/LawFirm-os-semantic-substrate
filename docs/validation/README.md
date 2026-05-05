# Phase 2 Validation Layer

This directory documents the Phase 2 validation layer scaffolding for the
enterprise doctrinal comparison substrate.

## Purpose

Phase 1 established a machine-readable substrate. Phase 2 establishes the first
validation shell around that substrate without replacing the repository's
current authoritative `schemas/` layer.

## Scope

This layer currently provides:

- substrate YAML structure checks
- deterministic ID and filename checks
- SHACL seed shapes for later graph-facing hardening
- export scaffolding for downstream schema projections
- GitHub Actions workflow scaffolding for repeatable validation

## Non-Goals

This layer does not yet provide:

- full runtime JSON Schema enforcement for doctrinal objects
- full SHACL validation over canonical data graphs
- registry integration for new doctrinal runtime object families
- canonical example objects using the Phase 1 substrate

## Alignment Rules

- preserve the existing repo shell
- reuse current governance language such as `authority_zone` and `trust_level`
- preserve asserted, derived, and hypothesis separation
- keep the canonical address system as the active routing shell
- prepare for later hardening without introducing a parallel ontology grammar
