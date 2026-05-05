# Phase 6 Semantic Graph Stack

## Execution Control

Roadmap execution order is controlled by `docs/roadmap/READINESS_GATES.md`.
A phase advances only when the applicable readiness gate passes.

## Goal

Add a governed semantic graph execution plan that prepares JSON-LD, named-graph,
SHACL, property-graph projection, retrieval feedback, and bounded pilot
artifacts without disturbing the current canonical validation shell.

## Added In This Phase

- phased stack execution plan for semantic graph hardening
- JSON-LD context contract for pilot-facing graph material
- named-graph manifest contract aligned to existing graph partition governance
- SHACL and validation scaffold for later semantic enforcement
- property-graph projection contract for downstream traversal and visualization
- retrieval feedback and proposal-promotion sidecars for governed iteration
- additive intake-conflicts-ai pilot examples proving the stack can compose

## What This Phase Preserves

- the current `schemas/` JSON validation surface
- canonical example validators and integrity checks
- assertion, provenance, trust-zone, and graph-partition separation
- additive shell-first evolution rather than runtime replacement

## Execution Order

1. Add stack contracts as preparatory machine-readable types and templates.
2. Add SHACL seed shapes and validation scaffold without making them canonical gates.
3. Add projection and retrieval sidecars as governed derivative layers.
4. Add bounded pilot examples under `data/` and `graphs/` rather than `examples/`.
5. Keep canonical validators green before any broader registry or runtime promotion.

## Phase 7 Should Implement Next

- registry integration for semantic stack object families
- cross-file semantic validation between contexts, manifests, projections, and sidecars
- governed export packaging for RDF and property-graph publication
- promotion workflows from pilot artifacts into broader retrieval neighborhoods
