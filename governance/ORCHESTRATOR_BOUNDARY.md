# LawFirm OS Orchestrator Boundary

## Status

`draft_metadata_only` until schema examples, validators, and cross-repo tests are promoted.

## Canonical names

- Substrate (control plane): `LawFirm-os-semantic-substrate`
- Orchestrator (execution plane): `LawFirm-os-orchestrator`
- Evidence Lake (evidence plane): `exceptions-lake-runtime-main`

For the full naming and authority order across repos, see `governance/CROSS_REPO_MAP.md`.

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

## Manifest-first loading

The Orchestrator loads substrate contracts in this order:

1. `manifests/contract_manifest.v1.json` — canonical orchestrator-facing manifest. Required when present. A manifest-aware orchestrator version must fail closed if the manifest is absent.
2. `registry/orchestrator-contract-export.json` — broader contract metadata that complements the manifest.
3. `registry/exception-route-registry.json` — canonical `route_id` and `event_class` authority.

Required manifest fields (must not be silently defaulted):

- `manifest_id`
- `manifest_version`
- `policy_bundle_id`
- `canonical_schema_keys`
- `registry_refs`
- `governance_refs`

`policy_bundle_id` in particular must be read from the manifest and must not be defaulted by the consumer.

## Pin-and-refresh discipline

The Orchestrator pins the substrate by SHA in `contracts.lock.json`. Required fields:

- `contract_repo` — must equal the canonical machine name `LawFirm-os-semantic-substrate`
- `contract_ref_type` — `git_sha`
- `contract_sha` — a substrate commit SHA that exists in substrate history
- `generated_at` — ISO8601 timestamp
- `generated_by` — `LawFirm-os-orchestrator`

Lock validation is fail-closed on missing fields, invalid fields, or SHA drift.

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
