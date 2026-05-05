# Gold Standard Backbone

## Purpose

Define the thinnest Law Firm-controlled semantic layer for stewarded Gold Standard
assets used by KM and search without expanding the repository into a broad
knowledge-management ontology program.

## What This Backbone Is

The Gold Standard backbone is a governed canonical KM layer that designates
which source-aligned assets are stewarded, reviewable, and safe to use as
high-trust anchors for KM, search, and answer preparation.

It is anchored to existing canonical Law Firm objects:

- `document`
- `source-artifact`
- `document-version`
- `component`
- `span-selector`
- `access_policy_ref`

It does not replace canonical document structure, retrieval contracts, or
vendor profiles.

## First Canonical KM Family

The first family is `gold-standard-asset`.

A Gold Standard asset is a stewarded designation over existing canonical
documents and exact spans. It exists to:

- mark approved high-trust assets for KM and search use
- keep lifecycle and stewardship explicit
- preserve exact traceability to source-aligned material
- support narrow optional external alignment references without making them
  canonical truth

## Minimum Contract

Every `gold-standard-asset` must carry:

- stable Law Firm asset identity
- a schema type and version
- a title or display label
- lifecycle status
- document and document-version anchors
- one or more canonical `component` references
- one or more exact `span-selector` references
- an access policy reference
- a steward reference or steward role
- a bounded asset kind
- scope references
- one or more source-artifact references

Optional:

- `alignment_refs[]` for narrow external alignment seeds such as LMSS or SALI

## Canonical Boundary

Gold Standard assets are canonical KM designations, but they are not a new
source of document truth.

That means:

- canonical document structure still lives in `document`, `document-version`,
  `canonical-text`, `component`, and `span-selector`
- Gold Standard assets may point to canonical boundaries, but may not redefine
  them
- retrieval, ranking, answer generation, and telemetry remain derived

## What Stays Adapter-Only

The following remain adapter, delivery, or projection surfaces in this phase:

- SharePoint
- iManage
- Azure AI Search
- Azure Document Intelligence
- Litify
- Entra
- Purview
- Fabric

These systems may supply provenance, scope, or retrieval inputs, but they do
not define canonical Gold Standard semantics.

## Glossary And Projection Posture

Business glossary labels, Purview-style terminology, and business-facing
projection artifacts belong in the governance or projection layer rather than
the deepest canonical semantic layer.

They may reference Gold Standard assets, but they must not replace Law Firm
canonical meaning.

## Retrieval And Rendering Boundary

Gold Standard assets may guide retrieval scope and rendering selection, but:

- `retrieval-request` remains derived
- `retrieval-trace` remains derived
- `retrieval-response` remains derived
- `answer-event` remains derived
- `answer-evidence` remains derived

No retrieval or rendering artifact may redefine a Gold Standard asset or the
underlying canonical document boundaries.

## External Alignment Posture

Optional `alignment_refs[]` may record narrow external seeds such as LMSS or
SALI references.

Those alignments are:

- optional
- non-authoritative
- subordinate to Law Firm canonical meaning

This phase does not import or expand external taxonomies into Law Firm canon.

## Activation Posture

The Gold Standard backbone lands as a draft family first.

Promotion requires:

- a validating example
- schema registration
- source-of-truth registration
- stewarded review

This phase intentionally stops before any SharePoint, iManage, or retrieval
adapter promotion.
