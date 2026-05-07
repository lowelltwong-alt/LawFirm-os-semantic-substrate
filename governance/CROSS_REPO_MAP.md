# Cross-Repo Map

This document is the authoritative naming and routing surface across the three sibling repositories that together implement the Law Firm OS Phase 2 Innovation Autonomy + Harness Layer.

It exists so that any human reader, AI assistant, or coding agent in any of the three repos can answer the same question the same way:

- which repo owns canonical authority for a given concern,
- what is the canonical machine name for that repo,
- what is the canonical human label,
- which file is the authoritative entry point in that repo,
- and where the boundary between control plane, execution plane, and evidence plane lies.

## Canonical names

| Repo | Canonical machine name | Canonical human label | Plane | Authority |
|---|---|---|---|---|
| Substrate | `LawFirm-os-semantic-substrate` | Law Firm OS Semantic Substrate | Control plane | Owns canonical schemas, registries, governance docs, route/event authority, manifest authority, autonomy/harness/research policy. |
| Orchestrator | `LawFirm-os-orchestrator` | Law Firm OS Orchestrator | Execution plane | Consumes substrate authority read-only. Builds evidence packets. Must not define canon. Must not invent route_id or event_class. |
| Evidence Lake | `exceptions-lake-runtime-main` | Law Firm OS Exceptions Lake Runtime | Evidence plane | Owns append-only runtime records and audit evidence. Must not promote or mutate canon. |

These canonical names supersede the following legacy or placeholder identities, which may still appear in older artifacts and must be reconciled when touched:

- `fmg-fractal-capability-ontology` (legacy substrate content id; preserved as `repo_id` in `registry/source-of-truth.json` for backward compatibility)
- `law-firm-ontology`, `law-firm-ontology-contracts`, `your-org/law-firm-ontology` (legacy or placeholder names previously used in evidence-lake artifacts)
- `Law Firm ontology contract repository` (legacy human label)

When a tool, doc, or lock file points to one of the legacy names, treat the substrate's canonical machine name `LawFirm-os-semantic-substrate` as the source of truth.

## Authoritative entry points

| Repo | Required-read first | Cross-repo discovery surface |
|---|---|---|
| Substrate | `registry/source-of-truth.json` then `governance/CROSS_REPO_MAP.md` (this file) then `AI_WORK_START_HERE.md` | `registry/orchestrator-contract-export.json`, `registry/exceptions-lake-contract-export.json`, `manifests/contract_manifest.v1.json` |
| Orchestrator | `README.md` then `AGENTS.md` then `AI_WORK_START_HERE.md` then substrate `governance/CROSS_REPO_MAP.md` | `contracts.lock.json` pinned against substrate; `docs/CANONICAL_ROUTE_MAPPING.md` |
| Evidence Lake | `README.md` then `docs/RUNTIME_BOUNDARY.md` then `AI_WORK_START_HERE.md` then substrate `governance/CROSS_REPO_MAP.md` | `contracts.lock.json` pinned against substrate; `docs/CANONICAL_ROUTE_MAPPING.md` |

## Plane responsibilities

### Control plane — `LawFirm-os-semantic-substrate`

Owns canonical authority for:

- ontology, taxonomy, controlled vocabularies
- schema authority (`schemas/`), including Phase 2 grouped schemas under `schemas/autonomy/`, `schemas/harness/`, `schemas/research/`, `schemas/innovation/`
- registry authority (`registry/`), single discovery surface for schema and governance references
- canonical `route_id` and `event_class` values (in `registry/exception-route-registry.json`)
- governance doctrine: red/yellow/green policy, harness intensity policy, green restoration policy, research signal ingestion policy, continuous autonomy assurance, internal idea lifecycle
- promotion authority: only humans approve promotion-decision; runtime evidence is never canonical
- contract manifests for runtime consumers: `manifests/contract_manifest.v1.json`, `registry/orchestrator-contract-export.json`, `registry/exceptions-lake-contract-export.json`

Must not:

- execute runtime behavior
- store real client, matter, employee, or policy facts
- run live model calls, scheduled jobs, external APIs, external writes, or live research crawling

### Execution plane — `LawFirm-os-orchestrator`

Owns:

- local CLI commands and bounded synthetic workflows
- model/tool routing decisions inside contract-allowed scopes
- autonomy gate, hardness scoring, leverage scoring, harness selection
- green-lane assumption watching
- Codex task packet generation
- evidence-packet preparation
- discovery-signal local imports (file-only; no network)

Must not:

- create or redefine `route_id` or `event_class`
- author canonical schemas, registries, or governance policy
- make live model calls in the MVP
- write into the substrate repo path
- treat its own outputs as canonical truth

Pins substrate via `contracts.lock.json`.

### Evidence plane — `exceptions-lake-runtime-main`

Owns:

- append-only runtime records (events, audit, validation results)
- contract loading from a pinned substrate checkout
- deny-by-default policy gating on synthetic envelopes only
- runtime route label mapping back to canonical `route_id`/`event_class` (`docs/CANONICAL_ROUTE_MAPPING.md`)

Must not:

- redefine schema meaning, lifecycle states, mutation rules, or promotion authority
- mutate canon
- create adaptation-proposal or promotion-decision records in the MVP
- write into the substrate repo path

Pins substrate via `contracts.lock.json`.

## Governed learning path (single source of truth)

All three repos share this exact path; if one repo states it differently, the substrate version is canonical:

```text
exception-event -> pressure-vector -> adaptation-proposal -> promotion-decision
```

The Phase 2 extended path that Innovation Autonomy + Harness work uses:

```text
exception-event
-> pressure-vector
-> opportunity-object
-> opportunity-scorecard
-> autonomy-decision-record
-> harness-plan
-> codex-task-packet
-> agent-review-record
-> validation-gate-record
-> scale-package-object
-> promotion-decision-object, only if canon changes
```

## Authority order across repos

When AI-facing files in any of the three repos disagree:

1. Substrate `registry/source-of-truth.json`
2. Substrate `registry/design-authority.json`
3. Substrate `governance/CROSS_REPO_MAP.md` (this file)
4. Substrate `governance/AI_CONTROL_PLANE_BOUNDARY.md`
5. Substrate `governance/EXCEPTIONS_LAKE_BOUNDARY.md` and `governance/ORCHESTRATOR_BOUNDARY.md`
6. Substrate `AGENTS.md`, `AI_START_HERE.md`, `AI_WORK_START_HERE.md`
7. Sibling-repo `README.md`, `AGENTS.md`, `AI_WORK_START_HERE.md`
8. Sibling-repo runtime route mapping documents
9. Vendor adapter files (`.claude/`, `.copilot/`, etc.)

Vendor adapters are consumers, never authorities.

## Pin-and-refresh discipline

Both runtime repos pin the substrate by SHA in `contracts.lock.json`. The lock fields are:

- `contract_repo`: the canonical machine name of the substrate (`LawFirm-os-semantic-substrate`)
- `contract_ref_type`: `git_sha`
- `contract_sha`: a substrate commit SHA that exists in substrate history
- `generated_at`: ISO8601 timestamp
- `generated_by`: the canonical machine name of the runtime repo

Refresh requires the substrate commit to exist in substrate history. Lock validation is fail-closed.

## Doctrine summary (from substrate authority)

- Risk color controls authority.
- Hardness controls harness depth.
- Leverage controls priority.
- Stakes size controls escalation sensitivity.
- Reversibility controls autonomy.
- Frequency controls compounding value.
- Green lanes are conditional and assumption-backed.
- Agents may downgrade green to yellow or red.
- Only humans may create or restore non-preapproved green authority.
- Runtime evidence and model outputs are proposals or evidence, never canonical truth.

## Hard prohibitions across all repos

- no real client data
- no real matter data
- no privileged content
- no external writes
- no live research automation
- no live model calls in the current MVP scope
- no scheduled jobs
- no runtime canon mutation
- no invented `route_id` or `event_class`
