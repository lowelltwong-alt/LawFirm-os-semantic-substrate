# Canonical Document Model

## Purpose

The canonical document model defines the stable source structure for document identity, normalized text, structural components, citations, and exact spans.

It exists so retrieval, provenance, and grounded answers can be rebuilt from a governed source layer instead of treating chunks, embeddings, indexes, or answer payloads as the source of truth.

## Source-of-truth rule

Canonical document structure is the source of truth.

That means:
- `document`
- `source-artifact`
- `document-version`
- `canonical-text`
- `component`
- `span-selector`
- `citation-mention`
- `citation-target`

These objects define what the document is, where structure boundaries exist, and exactly which spans support later retrieval and answer artifacts.

## Ingestion readiness gate

Before an internal document source is treated as a governed source, it must have a metadata-only `source-ingestion-manifest`.

The ingestion manifest records stable source and document identifiers, source type, originating system metadata, capture time, checksum, stewardship, confidentiality class, access policy, and lifecycle readiness.

For governed-answer readiness, the minimum source metadata gate also includes:
- `confidentiality_class`
- `access_policy_ref`
- `lifecycle_status`
- `retention_rule`

The manifest may not embed source content. This repo includes only synthetic metadata examples for that gate and does not ingest internal corpus content in this contract surface.

## Derived rule

The following are derived and rebuildable:
- `chunk-set`
- `chunk`
- `embedding-set`
- `index-build`
- `retrieval-response`
- `answer-event`
- `answer-evidence`
- `index-migration-plan`

Derived artifacts may optimize retrieval and answer generation, but they may not redefine canonical document boundaries.

## Required traceability chain

Every grounded answer must be traceable through this chain:

1. `document`
2. `document-version`
3. `canonical-text`
4. `component`
5. `span-selector`
6. optional `citation-mention` and `citation-target`
7. derived `chunk`
8. derived `retrieval-response`
9. derived `answer-evidence`
10. derived `answer-event`

If an answer cannot be traced back to exact canonical spans, it is not fully grounded.

## Canonical structure requirements

- Document identity must remain stable across versions.
- Every document version must point to its source artifact and canonical text.
- Canonical text must preserve a hierarchical structure model.
- Components must define canonical boundaries for sections, clauses, paragraphs, tables, footnotes, exhibits, and other meaningful legal units.
- Span selectors must preserve exact character-level traceability, with page anchors when available.
- Citation mentions must resolve to normalized citation targets without inventing new document structure.

## Derived artifact requirements

- Chunk sets must derive from canonical components and span selectors.
- Structure-aware chunking is the canonical default.
- Embedding sets and index builds must be rebuildable from chunk sets.
- Retrieval responses must reference exact canonical spans, not just scores or opaque chunk IDs.
- Answer evidence must reference document versions, components, span selectors, and supporting chunks.
- Index migration plans must reuse canonical source structure and must not require reparsing the document to accommodate an index upgrade.

## Operating rule

A change to chunking, embeddings, indexing, or answer generation is a regeneration step, not a redefinition of canonical structure.

Canonical structure changes require document-version and component/span updates. Retrieval improvements alone do not.
