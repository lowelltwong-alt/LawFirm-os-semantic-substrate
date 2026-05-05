# SHACL Seed Shapes

This directory contains SHACL seed shapes for the doctrinal comparison
substrate.

These shapes are intentionally lightweight. They are meant to prepare the
repository for later graph-facing hardening without asserting that the Phase 1
substrate is already a fully operational RDF runtime layer.

## Shape Files

- `core.ttl`: shared governed object expectations
- `doctrine.ttl`: doctrinal comparison and position expectations
- `comparison.ttl`: comparison and relationship object expectations
- `trust-zones.ttl`: governance zone and trust posture expectations
- `provenance.ttl`: source and evidence-bearing expectations
- `lifecycle.ttl`: lifecycle and review posture expectations
- `semantic-stack.ttl`: JSON-LD context and named-graph manifest seed constraints
- `projection.ttl`: property-graph projection seed constraints

## Current Role

- document future validation intent
- provide parsable TTL scaffolding for SHACL tooling
- keep shape language aligned to the current repo shell
- prepare semantic stack hardening without changing canonical validation gates
