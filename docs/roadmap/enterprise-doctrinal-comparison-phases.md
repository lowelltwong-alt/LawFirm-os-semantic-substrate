# Enterprise Doctrinal Comparison Phases

## Execution Control

Roadmap execution order is controlled by `docs/roadmap/READINESS_GATES.md`.
A phase advances only when the applicable readiness gate passes.

## Phase 1: Substrate Definition

Establish the machine-readable substrate for doctrinal comparison without
changing the current canonical shell.

Includes:

- substrate manifest
- reusable interfaces
- type seeds
- controlled vocab seeds
- compatibility framing against current repo governance

Does not include:

- full JSON Schema hardening
- SHACL constraints
- registry registration for new runtime objects
- canonical doctrinal examples

## Phase 2: Constraint Hardening

Implement the first real validation and interoperability layer.

Should include:

- JSON Schema projections for the substrate types
- LinkML or equivalent typed model generation
- SHACL seed constraints for graph-facing objects
- explicit inference mode constraints
- ID and prefix policy proposal aligned to the current registry model
- compatibility checks against current trust-zone and lifecycle vocabularies

## Phase 3: Canonical Example Surface

Add governed example objects that prove the substrate works inside the current shell.

Should include:

- canonical examples for thinkers, doctrines, positions, witnesses, and bundles
- anchor and citation examples aligned to the current address model
- comparison examples that remain claim-mediated where interpretation matters
- provenance completeness checks

## Phase 4: Integration and Retrieval

Integrate the substrate into the broader repo architecture.

Should include:

- registry integration
- retrieval neighborhood patterns
- graph export and comparison views
- CI validation hooks
- migration guidance for future doctrinal expansion

## Phase 5: Operational Governance and Pilot Slice

Make the doctrinal substrate operational in a bounded way.

Should include:

- governed action types and action logs
- object-set governance and reviewer-role structure
- bounded pilot slice definition and seed data
- operational lifecycle and promotion policy framing
- workflow scaffolding that proves the slice can be governed end to end

## Phase 6: Semantic Graph Stack

Add the semantic graph-facing execution layer above the current substrate.

Should include:

- JSON-LD context contracts for pilot graph material
- named-graph manifest contracts aligned to graph partition governance
- SHACL seed shapes and semantic validation scaffolding
- property-graph projection contracts for downstream graph tooling
- retrieval feedback and proposal-promotion sidecars
- bounded pilot artifacts that prove semantic stack composition without disturbing canonical validators
