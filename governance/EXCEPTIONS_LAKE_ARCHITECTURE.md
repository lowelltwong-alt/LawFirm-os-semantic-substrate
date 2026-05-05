# Exceptions Lake Architecture

## Purpose

The Exceptions Lake is the append-only memory for governed pressure signals.
It captures retrieval misses, workflow escalations, and authority conflicts in a machine-legible format so learning can be reviewed, routed, and promoted without destabilizing canonical ontology truth.

## Architectural principles

1. **Append-only intake**: raw exception events are written as immutable records.
2. **Governed routing**: every event must carry explicit route metadata to a learning loop.
3. **Trust-aware handling**: every event must carry authority and trust metadata.
4. **Promotion boundary**: raw exceptions cannot directly mutate canonical ontology artifacts.
5. **Auditable learning path**: all downstream tuning and promotion decisions remain traceable to event IDs.

## Core objects

- `exception-event` (`schemas/exception-event.schema.json`): canonical envelope for governed exception capture.
- `pressure-vector` (`schemas/pressure-vector.schema.json`): normalized pressure signal emitted by one or more exceptions.

## Flow

1. Capture exception event into append-only examples/events corpus.
2. Validate against schema and governance checks.
3. Route to retrieval/workflow/governance learning loop via registry.
4. Aggregate into pressure vectors.
5. Review recurring pressure for promotion packet eligibility.
6. Apply approved changes through promotion layer only.

## Control boundaries

- **Allowed from raw events**: tagging, triage, routing, and pressure aggregation.
- **Disallowed from raw events**: direct canonical ontology edits, taxonomy rewrites, schema mutation, or address-system mutation.
- **Required for canonical changes**: promoted and approved packet in governance path.

## Current repository scope

This repository currently defines the Exceptions Lake contract boundary and a
synthetic learning-loop harness only.

It does not contain:

- a production Exceptions Lake
- real exception events
- production runtime storage

Runtime learning remains subordinate to adaptation-proposal review and
promotion-decision authority. Incomplete chains are not promotion-eligible.
Any future runtime implementation must consume this repository's versioned
contracts rather than redefining them locally.

## Minimal success criteria

- Exception events validate.
- Route + trust metadata are always present.
- Direct canonical mutation attempts fail validation.
- Retrieval/workflow/governance loops can query pressure vectors by class, route, and authority.
