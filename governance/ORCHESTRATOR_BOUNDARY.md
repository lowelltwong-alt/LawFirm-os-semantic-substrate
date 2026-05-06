# LawFirm OS Orchestrator Boundary

## Status

`draft_metadata_only` until schema examples, validators, and cross-repo tests are promoted.

## Purpose

The Orchestrator is the LawFirm OS execution plane. It coordinates bounded model/tool workflows under pinned Semantic Substrate contracts and emits contract-locked evidence packets to the Exception Lake boundary.

The Orchestrator is not a semantic authority.

## Authority split

| Plane | Owns | Must not own |
|---|---|---|
| Semantic Substrate | Canonical schemas, route IDs, event classes, policy bundles, validation contracts, approval doctrine, promotion decisions | Runtime run state, model session state, ad hoc runtime rewrites |
| Orchestrator | Run execution, model/tool routing, policy gates, approvals, budgets, ledgers, evidence packet assembly, evals, proposal generation | Canonical schemas, route/event-class invention, substrate mutation, promotion authority |
| Exception Lake Runtime | Validation outcomes, append-only event/audit records, learning candidates, pressure vectors | Canonical semantics, ontology mutation, automatic promotion |

## Allowed Orchestrator actions

- read pinned manifests, registries, boundary docs, schemas, and policy bundles;
- validate synthetic-only inputs;
- route among allowed canonical route IDs and event classes;
- call one bounded structured model adapter or deterministic mock adapter for the MVP;
- write append-only local JSONL ledger records;
- assemble local evidence packet directories;
- hand off only through approved Exception Lake client modes;
- emit improvement proposals and semantic-change requests for human review.

## Forbidden Orchestrator actions

- write to Semantic Substrate;
- invent route IDs, event classes, schemas, lifecycle states, or governance doctrine;
- treat model output as canonical truth;
- ingest real client or matter data in the public MVP;
- bypass Exception Lake validation;
- persist unrestricted prompt transcripts, hidden reasoning, raw privileged content, credentials, or secrets;
- perform production connector writes or side effects;
- auto-promote research findings, pressure vectors, or runtime evidence into canon.

## Required MVP flow

```text
synthetic input
→ pinned Semantic Substrate manifest
→ deterministic route/event allowlist validation
→ bounded mock or structured model adapter
→ strict output validation
→ append-only JSONL run ledger
→ contract-locked evidence packet
→ Exception Lake disabled or dry-run by default
```

## Learning boundary

Runtime evidence may become:

```text
defect tags → pressure vectors → upgrade hypotheses → shadow evals → proposals → approval → versioned implementation
```

It must not become:

```text
runtime evidence → direct canonical mutation
```

## Research radar boundary

External research is method evidence only. It may propose changes to prompts, evals, validators, routing thresholds, evidence templates, and observability fields after credibility scoring and shadow evaluation. It must not modify canonical route IDs, event classes, approval doctrine, production connectors, real-data handling, or protected workflow transitions without governance approval.
