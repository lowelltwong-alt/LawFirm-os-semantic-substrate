# Retrieval Architecture

## Purpose

Define how retrieval is built on top of canonical documents, evidence objects,
access decisions, and vendor adapter profiles without allowing any adapter or
index to become semantic authority.

## Canonical Input Chain

Retrieval may consume only the governed canonical and derived chain:

1. `document`
2. `document-version`
3. `canonical-text`
4. `component`
5. `span-selector`
6. `chunk-set`
7. `embedding-set`
8. `index-build`

Retrieval requests, traces, responses, and answer artifacts remain derived.

## Default Posture

Use a mixed retrieval approach:

- lexical retrieval
- dense retrieval
- optional graph-guided retrieval for cross-document synthesis

Rank-based fusion is the default. Weighted score fusion is allowed only when
validated against grounded-answer quality and policy-safe access outcomes.

## Canonical Boundary

Retrieval consumes canonical document structure, stable identifiers, selectors,
provenance, and access decisions. It does not redefine canonical meaning, source
boundaries, or lifecycle authority.

## Access And Security Boundary

- deny by default
- require an access decision before retrieval response rendering
- filter by matter scope, confidentiality class, client restriction, and review posture
- exclude quarantine material from default retrieval
- preserve evidence and access boundaries in all answer-facing outputs

## Vendor Adapter Posture

Vendor services are adapters, not semantic authorities.

- Azure AI Search maps index and query behavior into Law Firm retrieval contracts.
- Azure Fabric maps derived analytics into runtime-learning and monitoring inputs.
- Azure Purview DLP maps classification and restriction signals into access decisions.
- Azure Entra maps authenticated identity and claims into requester and subject context.
- Azure Document Intelligence maps parsing outputs into the canonical document model.
- Litify, BillBlast, iManage, and SharePoint provide source-system identifiers,
  scope, document lineage, and exception signals that are normalized into Law Firm objects.

## Required Retrieval Outputs

A valid retrieval flow should be able to produce:

- `retrieval-request`
- `access-decision`
- `retrieval-trace`
- `retrieval-response`
- optional `answer-event` and `answer-evidence`

Each output must preserve exact source traceability back to document versions,
components, and span selectors.

## Empty Corpus Rule

When no governed sources are ingested, or when a claim or answer cannot resolve
to governed source and evidence references, the system must fail closed.

- It may describe repository structure, validation posture, or missing-ingest state.
- It may not assert internal factual conclusions, client facts, employee facts,
  policy conclusions, or grounded answer text as if governed support exists.
- Restricted source support without an explicit allowed-use or access basis must not be cited.
- Stale, withdrawn, retired, deprecated, or otherwise non-active governed source support must not be cited as active evidence.
- Answers may report that support exists but is unavailable because of sensitivity,
  allowed-use, lifecycle, or ingest readiness constraints.

## Contract Status

The active internal retrieval and access control surface is:

- `retrieval-request`
- `access-decision`
- `retrieval-trace`
- `retrieval-response`
- `index-migration-plan`

`retrieval-response` does not supersede `retrieval-trace`.

- `retrieval-response` is the ranked result artifact used by answer and review surfaces.
- `retrieval-trace` is the derived execution and observability record for adapter runs, filter enforcement, and score lineage.

## Adapter Readiness

Structurally sound drafts:

- Azure Document Intelligence
- Litify matter scope

Blocked pending source payload evidence:

- Azure AI Search
- Azure Entra
- Azure Purview DLP
- BillBlast
- iManage

Blocked pending source payload evidence and architecture review:

- Azure Fabric
- SharePoint gold-standard profile

## Design Rules

- Retrieval eligibility is policy-aware, not relevance-only.
- Vendor profile logic may transform fields, but not invent canonical semantics.
- Cross-matter retrieval is prohibited unless an explicit access decision permits it.
- Observability is derived and auditable; telemetry cannot become semantic truth.
