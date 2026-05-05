# Canonical Spine Policy

## Purpose

This document locks the repository's canonical spine so future expansion strengthens the validated kernel instead of creating parallel schema drift.

The canonical spine is the minimum authoritative path that governs how the repository reconciles, validates, and expands.

## Canonical Spine

The repository's canonical spine consists of:

- the v1 kernel priority
- the canonical claim and artifact schemas
- the canonical validation scripts
- the registry alignment layer
- the spine manifest used to verify that these remain coherent together

## Locked v1 Kernel

The v1 kernel priority remains:

- Person
- Client
- Matter
- Issue
- Document
- Clause
- Task
- Claim

No expansion should weaken this kernel or route around it through parallel object systems.

## Canonical Schema Authority

The canonical schema authority for validated examples is:

- `schemas/claim_v3.schema.json`
- `schemas/artifact.schema.json`

Registry stub schemas may continue to exist for routing and staged evolution, but they do not replace the canonical schema authority for the validated example spine.

## Canonical Validation Authority

The canonical validation authority is:

- `scripts/validate_examples_canonical.py`
- `scripts/validate_examples_registry.py`
- `scripts/validate_canonical_spine.py`

## Rules

### 1. Prefer canonical files over parallel drift
Future work should strengthen canonical files rather than create overlapping replacements without migration logic.

### 2. Expansion must pass through the spine
New schema types, retrieval layers, node types, and domain modules should be added only after they are aligned to the locked kernel and validation path.

### 3. Registry alignment is required
If schema registry routes, canonical schemas, and validators drift apart, the repository is considered structurally misaligned.

### 4. Validation is constitutional
Validation is not optional tooling. It is a constitutional part of the repository's operating system.

## Implementation Note

The machine-readable companion to this policy is:

- `governance/canonical_spine_manifest.json`

CI should treat that manifest as the source for spine alignment checks.
