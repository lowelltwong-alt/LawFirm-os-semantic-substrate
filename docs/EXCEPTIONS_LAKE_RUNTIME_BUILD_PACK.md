# Exceptions Lake Runtime Build Pack

## Purpose

This guide prepares a future Exceptions Lake runtime implementation without
building that runtime inside this contract repository.

The future runtime must consume versioned Law Firm contracts from this repository.
It must not redefine schema meaning, mutation authority, lifecycle states, or
promotion authority locally.

## What A Future Runtime Is

A future runtime Exceptions Lake is a separate operational system that:

- receives runtime observations
- normalizes them into governed exception candidates
- stores production events outside this repo
- routes reviewed pressure into opportunity, sprint, pilot, and scale flows
- exports derived operational views without changing canonical meaning

This repo does not contain that runtime today.

## Boundary

This repo owns:

- schemas
- registries
- validators
- lifecycle rules
- mutation-boundary doctrine
- synthetic examples
- release/export guidance
- AI contributor and adapter policies

Future runtime owns:

- production event storage
- real exception events
- ingestion jobs
- connector workers
- runtime telemetry
- runtime queues
- dashboards
- operational SLAs
- live access enforcement
- deployment secrets/configuration

## What This Repo Provides To The Runtime

The runtime should treat this repo as the versioned contract pack for:

- governed exception intake and aggregation:
  - `schemas/exception-event.schema.json`
  - `schemas/pressure-vector.schema.json`
  - `registry/exceptions-schema-registry.json`
  - `registry/exception-route-registry.json`
- governed learning and promotion:
  - `schemas/adaptation-proposal.schema.json`
  - `schemas/promotion-decision.schema.json`
  - `registry/governed-learning-schema-registry.json`
- Innovation OS operating objects:
  - `schemas/opportunity-object.schema.json`
  - `schemas/sprint-object.schema.json`
  - `schemas/pilot-object.schema.json`
  - `schemas/validation-gate-record.schema.json`
  - `schemas/scale-package-object.schema.json`
  - `schemas/view-executive-brief.schema.json`
- provenance, access, and grounded-answer boundaries:
  - `schemas/source-ingestion-manifest.schema.json`
  - `schemas/access-decision.schema.json`
  - `schemas/evaluation-run.schema.json`
  - `governance/RETRIEVAL_ARCHITECTURE.md`
- AI contributor and adapter boundaries:
  - `governance/AI_CONTROL_PLANE_BOUNDARY.md`
  - `.ai/instruction-kernel.yaml`
  - `.ai/action-risk-tiers.yaml`
  - `.ai/approval-matrix.yaml`
- export and packaging guidance:
  - `registry/exceptions-lake-contract-export.json`
  - `scripts/build_release_snapshots.py`
  - `fmg release-snapshot --version <version>`

## What The Runtime Must Build Outside This Repo

The future runtime must build, operate, and secure its own:

- connector adapters into source systems
- event ingestion workers
- event store and retention controls
- approval queue and operational review UX
- live access enforcement path
- runtime telemetry, dashboards, and alerting
- deployment configuration, secrets, and environment isolation
- operational SLAs, runbooks, and on-call procedures

Those concerns are real runtime implementation, not contract-repo work.

## What Must Never Be Implemented Inside This Repo

Do not build these inside this repository:

- production event storage
- live exception ingestion
- connector workers
- operational approval runtime
- live dashboards
- runtime queues
- deployment secrets or runtime configuration
- production telemetry lakes
- direct runtime writeback into canon

## Governed Flow From Runtime Observation To Canon

Runtime observations may become governed exception candidates.

The canonical path remains:

```text
runtime observation
  -> exception-event
  -> pressure-vector
  -> adaptation-proposal or opportunity-object
  -> promotion-decision
  -> canonical change only if approved
```

Innovation OS operating flow may proceed in parallel:

```text
exception-event
  -> pressure-vector
  -> opportunity-object
  -> sprint-object or pilot-object
  -> validation-gate-record
  -> scale-package-object
  -> promotion-decision
```

Runtime observations do not directly mutate canon.

## Minimum Contract Gates Before Runtime Signals Influence Canon

Before any runtime event can influence canonical change, the future runtime
should prove all of the following:

1. Raw intake validates as governed exception structure.
   - `python scripts/validation/validate_exception_events.py`
2. Route, trust, and no-direct-mutation controls pass governance checks.
   - `python scripts/validation/validate_exception_governance.py`
3. If source-linked evidence is involved, provenance is complete and
   metadata-only source-ingestion requirements are met.
   - `python scripts/validation/validate_source_ingestion_manifests.py`
   - `python scripts/validate_integrity.py`
4. If support is restricted, stale, or otherwise gated, access and
   allowed-use boundaries are preserved.
   - `python scripts/validation/validate_canonical_grounding_chain.py`
   - `python scripts/validation/validate_grounded_answer_evaluation_harness.py`
5. Innovation OS chain objects resolve to the governed exception and pressure
   inputs they claim.
   - `python scripts/validation/validate_learning_loop_transitions.py`
6. Canonical mutation remains blocked until promotion review is complete.
   - `schemas/promotion-decision.schema.json`
   - `governance/EXCEPTIONS_LAKE_BOUNDARY.md`

## Release And Export Guidance

This repo can publish metadata-only contract exports and placeholder release
snapshots for handoff and packaging.

- `registry/exceptions-lake-contract-export.json` is metadata only.
- `fmg release-snapshot --version <version>` builds a placeholder export pack
  under `release-snapshots/<version>/`.

These exports are build-pack guidance only. They are not runtime deployment
artifacts, not live telemetry, and not proof of production readiness.

## Non-Claims

This guide does not claim:

- any production runtime exists here
- any real internal events are stored here
- any production dashboards exist here
- any live connector workers exist here
- any internal corpus ingestion is claimed here
- any runtime Exceptions Lake deployment is claimed here

The future runtime must consume versioned contracts from this repo.
It must not redefine them.
Runtime observations do not directly mutate canon.
