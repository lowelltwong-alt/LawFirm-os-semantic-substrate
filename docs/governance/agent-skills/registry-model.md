# Registry Model

This document defines the canonical registry model for the Agent/Skill Capability Graph surface.

## Registry operating model

The canonical layer in this surface is a stewarded set of registry cards, controlled tags, typed canonical edges, ownership assignments, review cadence records, and audit posture declarations.

The registry is meant to support future discovery, indexing, and similarity analysis at large scale while preserving a clear distinction between canonical governance and derived discovery outputs.

## Canonical node classes

Document these neutral classes:
- `agent`
- `subagent`
- `skill`
- `monitor`
- `orchestrator`
- `workflow`
- `tag_cluster`
- `owner_role`
- `review_surface`

These are documented governance classes in the first PR, not schemas.

## Registry posture

- canonical cards are steward-guided
- canonical tags are controlled
- canonical edges are typed and reviewed
- derived discovery outputs are consumers of canonical cards
- generated surfaces must never become semantic authority

## Large-scale design intent

This surface should remain navigable even with thousands or tens of thousands of entries by relying on:
- stable card identifiers
- controlled tag axes
- typed edge vocabulary
- clear ownership and cadence
- explicit canonical-versus-derived boundaries
- future generated summaries that remain non-canonical
