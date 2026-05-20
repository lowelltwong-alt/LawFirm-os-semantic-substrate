# Agent-Hostile Control Boundary

## Status

`active` as the canonical control-plane boundary for agent-hostile runtime contracts.

## Authority

The Semantic Substrate owns the canonical agent-hostile control schemas and registries. These include agent identity, prompt version authority, tool authority, endpoint authority, revocation policy, and the agent-hostile control bundle.

The Orchestrator consumes these contracts read-only through `contracts.lock.json`, `manifests/contract_manifest.v1.json`, and pinned registry/schema references. The Orchestrator may carry local fixtures for tests or bootstrapping, but those fixtures are non-canonical.

The Orchestrator owns enforcement code, run state, model/tool routing, policy gates, ledgers, and evidence packet assembly. It does not own policy meaning.

The Exception Lake owns append-only evidence, validation records, audit records, and learning candidates. It does not own policy meaning.

Model outputs, runtime observations, tool results, and evidence packets are proposals or evidence. They are never canon.

## Governed Contract Families

Prompt registries, tool authority, endpoint authority, and revocation contract schemas are governance contracts. Runtime systems may implement enforcement, but the shape and meaning of those records are governed here.

Runtime revocation state can live in the Orchestrator or operational stores. The shape and meaning of revocation records are governed by `schemas/revocation-policy.schema.json` and the canonical registries in `registry/`.

## Required Runtime Posture

- Unknown agent, prompt, tool, endpoint, route, or revocation subject handling must fail closed.
- Agent-callable surfaces must require authentication, agent identity, audit events, explicit risk class, and an approval policy.
- Side-effecting surfaces must require human approval policy.
- Runtime evidence may downgrade, block, or propose. It may not promote semantic authority.

## Hard Prohibitions

- No autonomous writes.
- No live connectors.
- No scheduled jobs.
- No external APIs.
- No external writes.
- No production data.
- No real client data.
- No real matter data.
- No semantic promotion without human approval.

