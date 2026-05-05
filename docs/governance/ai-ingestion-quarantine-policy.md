# AI Ingestion Quarantine Policy

AI-ingested or AI-extracted material must not be treated as canonical by default.

## Default Rule

New AI-ingested assertions belong in the `quarantine` graph partition unless a
separate governed process promotes them elsewhere.

## Why

This preserves:

- clear separation between generated and governed material
- safer provenance review
- non-destructive experimentation
- compatibility with the repository's trust and inference posture

## Promotion Requirements

Before quarantine material can move to `inferred`, `boundary`, or `asserted`,
it should have:

- stable identity
- explicit assertion kind
- provenance activity records
- evidence or source paths where material
- review status
- an explicit governance decision

## Retrieval Guidance

Quarantine material should be excluded from default retrieval neighborhoods
unless a workflow explicitly opts into experimental or review-oriented access.
