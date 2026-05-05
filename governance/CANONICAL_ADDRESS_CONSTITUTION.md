# Canonical Address Constitution

Author: Lowell T. Wong

## Purpose

This document establishes the single canonical address model for the repository.

All schemas, code, registries, and governed objects must conform to this structure.

## Canonical Address Pattern

`/environment/authority_zone/layer/domain/module/object_type/object_id/version`

Example:

`/example/public/governance/legal/intake_conflicts/claim/CLM-000101/v1`

## Canonical Enforcement

The 8-part address model defined in this document is the only valid address
system for this repository.

All prior address models, including any 4-part or conceptual address
structures, are deprecated.

No new objects, schemas, or scripts may use legacy address formats.

All validation, parsing, and routing must assume the 8-part structure.

## Segment Definitions

- environment -> example | production
- authority_zone -> public | internal_general | restricted | experimental
- layer -> governance | ontology | schema | data | retrieval
- domain -> business area, for example legal or finance
- module -> capability area, for example intake_conflicts
- object_type -> claim, artifact, node, source, chunk, decision_record,
  learning_event
- object_id -> stable identity with a controlled prefix
- version -> version tag in the form v{integer}

## Rules

- address must be deterministic
- address must be parseable
- address must be registry-validatable
- all address segments except object_id must be lowercase snake_case
- object_id must remain stable across migrations
- object_id must be prefixed
- address may change only with migration tracking

## Required Representations

Every governed object must include:
- address (string)
- address_struct (object form)

## Relationship to ID

- ID answers: what is this?
- Address answers: where is this?

These must remain distinct.

## Enforcement

- schemas must validate this format
- code must parse and build this format
- registry must validate segments
- CI must enforce compliance

## Object ID Prefixes

- CLM -> claim
- ART -> artifact
- NODE -> ontology node
- SRC -> source
- CHK -> chunk
- DEC -> decision_record
- LRN -> learning_event

## Deprecation Notice

Legacy address systems may exist temporarily for migration purposes.

However:
- they must not be used as primary identifiers
- they must be mapped to canonical addresses
- they will be removed in future enforcement phases

## Supersession

This file supersedes earlier partial address specifications.
