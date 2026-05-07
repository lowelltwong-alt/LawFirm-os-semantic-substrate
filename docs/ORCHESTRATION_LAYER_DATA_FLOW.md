# Orchestration Layer Data Flow

Status: `draft_metadata_only`.

## Canonical names

- Substrate (control plane): `LawFirm-os-semantic-substrate`
- Orchestrator (execution plane): `LawFirm-os-orchestrator`
- Evidence Lake (evidence plane): `exceptions-lake-runtime-main`

For sibling-repo names, plane responsibilities, and authority order across repos, see `governance/CROSS_REPO_MAP.md`.

## Authoritative orchestrator-facing surfaces

The orchestrator should consume the substrate read-only through these surfaces:

- `manifests/contract_manifest.v1.json` — canonical orchestrator-facing manifest with stable keys (`manifest_id`, `manifest_version`, `policy_bundle_id`, `canonical_schema_keys`, `registry_refs`, `governance_refs`).
- `registry/orchestrator-contract-export.json` — broader contract metadata.
- `registry/exception-route-registry.json` — canonical `route_id` and `event_class` authority.
- `registry/schema-registry.json` — schema discovery surface.
- `registry/autonomy-lane-registry.json`, `registry/harness-policy-registry.json`, `registry/red-flag-trigger-registry.json`, `registry/assumption-watch-registry.json` — Phase 2 autonomy/harness authority surfaces.
- `governance/ORCHESTRATOR_BOUNDARY.md` — orchestrator boundary doctrine.

## Current MVP flow

```mermaid
flowchart LR
    Caller[Operator or CLI caller] --> CLI[classify-exception CLI]

    subgraph SS[Semantic Substrate / control plane]
      Manifest[Contract manifest + hashes]
      Routes[Route registry]
      Events[Event-class registry]
      Policies[Runtime policy bundle]
      Boundaries[Governance boundaries]
    end

    subgraph OR[Orchestrator / execution plane]
      CLI --> Intake[Strict synthetic input gate]
      Intake --> Pin[Load pinned manifest]
      Pin --> Allowlist[Route + event-class allowlist]
      Allowlist --> Adapter[Mock or structured model adapter]
      Adapter --> Validate[Strict schema + policy validators]
      Validate --> Ledger[Append-only JSONL run ledger]
      Validate --> Packet[Contract-locked evidence packet]
    end

    subgraph EL[Exception Lake Runtime / evidence plane]
      Gateway[Disabled or dry-run gateway]
      Audit[Append-only audit records]
      Candidate[Learning candidates only]
    end

    Manifest --> Pin
    Routes --> Allowlist
    Events --> Allowlist
    Policies --> Intake
    Boundaries --> Validate
    Packet --> Gateway
    Gateway --> Audit
    Audit --> Candidate
    Candidate -. governed proposal only .-> SS
```

## Sequence flow

```mermaid
sequenceDiagram
    participant C as CLI caller
    participant O as Orchestrator
    participant S as Semantic Substrate files
    participant M as Model adapter or fake stub
    participant L as JSONL ledger
    participant P as Evidence packet
    participant E as Exception Lake gateway

    C->>O: classify-exception(input)
    O->>O: validate synthetic-only input
    O->>S: load pinned manifest and registries
    S-->>O: manifest_id, hashes, route_ids, event_classes
    O->>O: deterministic route/event allowlist check
    O->>L: append run_started
    O->>M: request structured classification
    M-->>O: proposed route_id and event_class
    O->>O: strict output and policy validation
    O->>L: append validation records
    O->>P: build contract-locked evidence packet
    P-->>O: evidence_id and packet_hash
    O->>L: append run_completed or run_failed
    O->>E: optional validate-only handoff
    E-->>O: not_attempted / accepted / rejected
```

## Evidence packet contents

```text
input artifact hash + synthetic flag
contract manifest id + hash
route/event registries and allowed IDs
model request and structured response
validation results: schema + policy + route
trace IDs: run_id, trace_id, correlation_id
source claim refs and artifact hashes
approval status and reason
optional Lake receipt or rejection
```

## Disallowed flow

```text
model output → canonical schema update
runtime pressure vector → direct substrate mutation
research paper → direct code deployment
Exception Lake candidate → automatic promotion
```

## Allowed learning loop

```text
runtime evidence
→ defect classification
→ pressure vector
→ upgrade hypothesis
→ shadow eval
→ human/proven promotion approval
→ versioned implementation
→ measured effect
```
