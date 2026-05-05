# Named Graph Trust Boundaries

This repository uses named graph partitions as governance boundaries, not merely
as storage buckets.

## Graph Partitions

- `asserted`: reviewed, core governed assertions
- `inferred`: derived assertions that remain structurally separate from asserted material
- `boundary`: restricted or boundary-sensitive assertions that require heightened handling
- `quarantine`: imported or AI-ingested material not yet fit for canonical use

## Rules

- asserted material must not be silently mixed with inferred material
- boundary material must not be promoted into asserted or inferred graphs by default
- quarantine material must remain structurally separated until reviewed and governed
- retrieval defaults should prefer asserted, then inferred only when explicitly requested

## Purpose

The partition model preserves:

- trust clarity
- inference clarity
- review boundaries
- safer AI ingestion posture
- controlled promotion paths
