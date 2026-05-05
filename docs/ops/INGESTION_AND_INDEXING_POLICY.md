# Ingestion and Indexing Policy

## Purpose

Define how source material enters the pilot and becomes eligible for governed retrieval.

## Source Classes

- governed_internal
- external_restriction
- matter_condition
- quarantine_only

## Ingestion Rules

### Governed Internal Material
May be ingested for pilot use if provenance, ownership, and source class are recorded.

### External Restriction Material
May be ingested if the restriction source is explicitly linked to the governing workflow.

### Matter Condition Material
May be ingested only when scoped to the relevant matter or workflow boundary.

### Quarantine Material
May be ingested for analysis, but must not be treated as canonical or surfaced by default retrieval.

## Required Metadata

Every indexed item should carry:
- source system id
- source class
- authority zone
- lifecycle or review posture
- matter or restriction scope where relevant
- provenance reference where available

## Chunking Guidance

- preserve semantic boundaries where possible
- do not split away governing qualifiers from their restrictions
- keep traceable references from chunks back to governed source objects

## Retrieval Eligibility

A record should only be eligible for default retrieval when:
- it is not quarantine-only
- it is appropriately scoped
- access filters allow it
- provenance and governance posture are present

## Why This Matters

Retrieval quality and governance quality depend on disciplined ingestion. If indexing ignores source class, access boundaries, or provenance, answer quality and trust will degrade quickly.
