# Clean-Room and Source Boundaries

This repository must preserve clean-room architecture discipline.

## Clean-room rule

Do not copy leaked code, private prompts, proprietary prompt libraries, or leak-derived repositories.

Allowed lessons are architectural only:

- mode separation
- permissions
- hooks
- approval gates
- auditability
- source boundaries
- trust zones
- role isolation
- deterministic validation gates

## Source boundary rules

- Public official documentation may be summarized and cited when needed.
- Uploaded or connected user-provided files may be used only within the task scope.
- Real internal law firm records must not be invented, ingested, or stored in this repo.
- Copyrighted full text must not be copied into the repo unless an explicit license and ingestion route allows it.
- Runtime logs, production transcripts, answer caches, embeddings, indexes, and telemetry are derived/runtime surfaces and do not belong in this repository.

## Trust-zone promotion

No source may silently move from lower trust to higher trust.

Research does not become governance without a governance route.
Governance does not become schema without a schema route.
Runtime observations do not become canonical truth without the governed promotion path.
