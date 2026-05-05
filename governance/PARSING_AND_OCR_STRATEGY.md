# Parsing and OCR Strategy

## Goal

Produce structured, page-grounded document representations that preserve text,
hierarchy, tables, spans, and provenance strongly enough for grounded retrieval,
review, and citation.

## Canonical Output Requirement

Parser and OCR outputs must be normalized into the canonical document model
before they are used by chunking, indexing, retrieval, or generation.

The canonical output chain is:

- `document`
- `source-artifact`
- `document-version`
- `canonical-text`
- `component`
- `span-selector`

## Preferred Outputs

- canonical text
- section and paragraph structure
- table structure
- span offsets
- page anchors and regions
- parse provenance

## Platform Posture

- managed-first option: Azure Document Intelligence
- source-system lineage anchors: iManage and SharePoint metadata
- local or open fallback option: Docling
- adapter fallback option: Unstructured

## Non-Negotiable Rules

- preserve exact source traceability
- preserve page and region anchors when available
- preserve parser provenance and model metadata
- do not let parser-local structure redefine canonical document boundaries
- keep OCR artifacts derived and rebuildable

## Vendor Boundary

Azure Document Intelligence may enrich structure, but it does not become the
semantic authority for Law Firm document meaning. The profile must map its outputs
into Law Firm canonical objects and keep any unsupported vendor features explicitly
non-canonical.
