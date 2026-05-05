# Phase 2 Validation Layer

## Execution Control

Roadmap execution order is controlled by `docs/roadmap/READINESS_GATES.md`.
A phase advances only when the applicable readiness gate passes.

## Goal

Add the first validation shell around the doctrinal comparison substrate while
keeping the current repository architecture stable.

## Added In This Phase

- YAML validation scaffolding for the new `schema/` substrate
- SHACL seed shapes for core, doctrine, comparison, trust, provenance, and lifecycle concerns
- deterministic ID and filename checks
- export scaffolding for downstream projections
- GitHub Actions workflow stubs for repeatable validation

## What Phase 2 Still Does Not Do

- enforce the doctrinal substrate as a runtime schema surface
- replace the current `schemas/` validation layer
- register new doctrinal object families in the canonical registries
- define final ID prefix rules for doctrinal object types

## Phase 3 Should Implement Next

- JSON Schema projections for the doctrinal substrate
- LinkML generation or equivalent typed model output
- canonical doctrinal examples using the 8-part address shell
- registry integration and source-of-truth registration
- stricter SHACL constraints over governed graph-facing objects
- compatibility tests for trust zones, lifecycle status, and inference posture
