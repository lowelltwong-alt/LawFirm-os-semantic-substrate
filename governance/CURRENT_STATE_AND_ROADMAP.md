# Current State and Roadmap

## Purpose

This roadmap describes where the repository currently sits and what should happen next. It is written for executives, maintainers, automation leaders, and coding agents.

## Current state

The repository is a governed semantic-control-plane and contract repository for the Innovation OS.

It currently includes:

- authority surfaces and precedence rules
- schema registry and validation stack
- source-ingestion manifest gate
- fail-closed unsupported-claim behavior
- sensitivity and allowed-use evidence gates
- grounded-answer evaluation readiness
- Exceptions Lake boundary doctrine and synthetic learning-loop harnesses
- agent operating rules
- truthful SHACL fail-closed boundary

## Current validation posture

Focused validators pass.

The full audit is expected to pass earlier stages and then stop at the known truthful SHACL fail-closed gate. Core SHACL conformance for the current core pair is not claimed.

## Roadmap

### Phase 1  -  Handoff readiness

Goal: make the repo legible to CINO, automation manager, maintainers, reviewers, and AI agents.

Outputs:

- handoff index
- CINO executive brief
- automation manager starter pack
- orientation guide
- endpoint/entrypoint map
- suggested AI front-door questions

Success condition:

A new reviewer can understand what the repo is, what it guarantees, what it does not claim, and how to orient without reading every file.

### Phase 2  -  Runtime planning, not runtime implementation

Goal: plan future runtime systems without building them inside the contract repo.

Potential outputs:

- runtime Exceptions Lake implementation plan
- Exceptions Lake runtime build-pack guide
- contract consumption map for a separate runtime repo
- separate runtime repo skeleton
- metadata-only contract export manifest
- ingestion architecture plan
- source-system connector inventory
- access-control integration plan
- telemetry and audit plan

Success condition:

Runtime systems consume versioned contracts from this repo and do not redefine canonical meaning.

### Phase 3  -  First governed automation pilots

Goal: run small, measurable automation pilots using the Innovation OS loop.

Candidate pilot types:

- billing guideline exception queue
- carrier portal exception routing
- AR aging exception triage
- matter metadata completeness checks
- source-ingestion manifest readiness checks

Success condition:

Each pilot has an owner, evidence source, allowed-use basis, KPI, exception queue, validation gate, and rollback path.

### Phase 4  -  Internal corpus ingestion readiness

Goal: admit real internal sources only after provenance, access, retention, and allowed-use gates are operational.

Prerequisites:

- source inventory
- access policy mapping
- sensitivity classification
- ingestion manifest population
- content hash/digest pipeline
- retention and lifecycle review
- evaluation plan

Success condition:

No real internal source becomes governed without complete provenance and access metadata.

### Phase 5  -  Evaluation and production claims

Goal: support real performance claims only after approved corpus and gold cases exist.

Potential claims after evidence exists:

- retrieval accuracy
- citation coverage
- answer faithfulness
- refusal precision
- support-unavailable handling
- automation cycle-time impact

Success condition:

Production claims are backed by approved evaluation cases, not synthetic fixtures.

## Non-negotiables

- No runtime lake implementation inside this repo.
- No real internal corpus content inside this repo.
- No raw exception directly mutates canon.
- No production retrieval/answer-quality claims without real evaluated corpus evidence.
- No SHACL green claim until the core pair has trustworthy same-namespace focus-node data.
