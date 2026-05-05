# Exceptions Lake Boundary

## Purpose

This repository defines the contract boundary for the Exceptions Lake. It does not implement or store the production Exceptions Lake runtime.

The Exceptions Lake is a governed learning surface for runtime observations, review findings, failed validations, retrieval misses, access-denial discoveries, workflow exceptions, and other operational signals.

These signals are evidence and learning inputs. They are not canonical truth.

## What this repository owns

This repository owns the canonical contract spine:

- schemas
- registries
- validators
- lifecycle rules
- mutation-boundary doctrine
- synthetic contract tests
- promotion rules for canonical change

## What this repository does not own

This repository does not own or store:

- production event storage
- runtime telemetry lakes
- dashboards
- real exception events
- internal incident records
- real client, matter, employee, or policy facts
- ingestion jobs
- production runtime pipelines

A future runtime implementation may live in a separate repository or deployment environment.

## Required runtime boundary

Any future runtime Exceptions Lake must consume versioned contracts from this repository.

Runtime systems must not redefine:

- schema meaning
- mutation rules
- lifecycle states
- promotion authority
- canonical ontology meaning
- canonical governance policy

Generated exports, adapters, telemetry, indexes, dashboards, and runtime records are derived implementation artifacts. They are not canonical authority.

## Governed learning path

Runtime observations may influence canon only through the governed path:

```text
exception-event -> pressure-vector -> adaptation-proposal -> promotion-decision
```

Raw observations, review findings, runtime exceptions, failed validators, retrieval misses, and access denials may become exception candidates.

They may not directly mutate ontology, taxonomy, schemas, registries, or governance policy.

## Agent-learning posture

Coding-agent review findings, failed validators, stale docs, unsupported claims, retrieval misses, and access-denial discoveries are exception candidates.

They must be routed through governed learning and review. They are not direct authorization to rewrite canonical meaning.

## Current main state

The Exceptions Lake contract spine has already landed on `main` in this repository.

Current repository coverage includes:

- boundary doctrine for contract vs runtime ownership
- governed exception-learning schemas and registries
- synthetic examples for the governed learning path
- validators for exception governance and learning-loop transitions
- synthetic test coverage for valid and invalid governed-learning chains

These surfaces make the Exceptions Lake boundary explicit and testable inside the
contract repository.

## Future runtime work

Future runtime work may implement storage, telemetry, ingestion, and operational
handling outside this repository.

That future runtime work must continue to use this repository's versioned
contracts, validators, and promotion boundary as the canonical source of truth.

This repository must still not build a production runtime lake.

For runtime build-pack planning, see:

- `docs/EXCEPTIONS_LAKE_RUNTIME_BUILD_PACK.md`
- `docs/EXCEPTIONS_LAKE_CONTRACT_CONSUMPTION_MAP.md`
- `docs/EXCEPTIONS_LAKE_RUNTIME_REPO_SKELETON.md`
- `registry/exceptions-lake-contract-export.json`
