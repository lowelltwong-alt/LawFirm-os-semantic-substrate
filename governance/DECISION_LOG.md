# Decision Log

## Purpose

This log records architectural and cleanup decisions made during repo alignment.

## 2026-04-13 / 2026-04-14 decisions

### 1. Repo role
Decision: Law Firm is treated as a semantic-governance substrate and Innovation OS contract repository.
Why: this keeps ontology, governance, document/evidence, retrieval contracts, and operating model in one governed layer.

### 2. Canonical vs derived boundary
Decision: embeddings, indexes, OCR model specifics, GraphRAG summaries, and runtime caches are derived artifacts, not canonical truth.
Why: this supports rebuildability and low lock-in.

### 3. Ontology split
Decision: maintain explicit separation between:
- stable core ontology
- Law Firm extension layer
- runtime learning objects
Why: prevents semantics, workflow state, and learning events from collapsing into one layer.

### 4. Runtime mutation boundary
Decision: raw exception and runtime objects may not directly mutate canonical meaning.
Why: canonical change must flow through governed promotion.

### 5. Remaining blocker
Decision: existing authoritative files still require in-place consolidation.
Why: the current connector path has been more reliable for new files than overwriting older authoritative files.

### 6. Retrieval result contracts
Decision: `retrieval-response` and `retrieval-trace` formally coexist.
Why: `retrieval-response` is the derived result artifact returned to downstream answer or review surfaces, while `retrieval-trace` preserves execution, ranking, filter, and telemetry lineage. Neither supersedes the other.

### 7. Retrieval and access schema promotion
Decision: `retrieval-request`, `retrieval-trace`, and `access-decision` are promoted from draft to active in the schema registry.
Why: the contracts now align with retrieval doctrine, preserve deny-by-default and canonical-boundary controls, and validate against updated example bundles alongside the already-active `retrieval-response` and `index-migration-plan` schemas.

### 8. SHACL scope for retrieval and access
Decision: do not expand core SHACL to cover `retrieval-response`, `access-decision`, or `index-migration-plan` in Phase 7.
Why: these are derived or policy contracts, not semantic-core classes. JSON Schema remains the authoritative validation surface for them unless a later phase introduces a dedicated derived-contract SHACL layer.

### 9. Fabric and SharePoint posture
Decision: keep Fabric and SharePoint adapter-only for now and do not create new canonical families in Phase 7.
Why: repo evidence does not yet justify a governed scorecard family for Fabric or a gold-standard asset family for SharePoint. Both remain blocked pending source payload evidence and explicit architecture review.

### 10. Phase 7B promotion boundary
Decision: do not promote any additional vendor adapters or mappings in Phase 7B.
Why: the repo evidence supports active Law Firm retrieval and access contracts, but vendor adapters still split into structurally sound drafts and evidence-blocked scaffolds. Promotion without live payload evidence would overstate certainty.

### 11. Closest promotion candidates
Decision: keep Azure Document Intelligence and Litify as structurally sound drafts rather than promoting them in Phase 7B.
Why: both surfaces now preserve Law Firm boundaries and use only repo-evidenced field families, but neither has a representative real export in the repo to confirm implementation-ready payload shapes.

### 12. Adapter evidence gate
Decision: keep Azure AI Search, Entra, Purview, and iManage blocked by missing payload evidence, and keep BillBlast, Fabric, and SharePoint blocked by both missing evidence and unresolved design decisions.
Why: placeholders in these files are intentional safeguards. The repo does not contain the real payloads or approved target slots needed to justify any further adapter promotion.

## Open decisions

- final normalized runtime schema field family
- exact source-of-truth precedence after registry rewrite
- whether to replace or extend some pre-existing governance docs
- whether a later phase should introduce a dedicated SHACL layer for derived retrieval/access contracts
- whether Fabric needs a governed scorecard canonical family after live export review
- whether SharePoint exemplar governance needs a dedicated gold-standard asset family after live export review
