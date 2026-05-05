# Address System Evolution

Author: Lowell T. Wong

## Purpose

This document upgrades the fractal address system from a useful conceptual locator into a more enterprise-grade architectural layer.

It defines:
- why the address system must evolve
- what enterprise-grade addressability requires
- how future migrations should preserve stability
- how the address system should remain fractal across scales

## Core Position

A mature ontology operating system needs more than stable IDs.
It also needs a structured, governed, upgradeable answer to where an object sits in the larger system.

The address system is therefore a first-order architectural concern.

## Why the Current Address Model Is Not Yet Enough

The earlier address model established the distinction between:
- stable identity
- structural placement

That is correct and should be preserved.

However, an enterprise-grade system needs stronger address capabilities, including:
- environment awareness
- authority-zone awareness
- module awareness
- version awareness
- migration safety
- registry-backed validation

## Enterprise-Grade Address Pattern

The target address structure is:

`/environment/authority_zone/layer/domain/module/object_type/object_id/version`

Example:

`/example/public/governance/legal/intake_conflicts/claim/CLM-000101/v1`

## Why This Matters

This allows future systems to know, from the address alone:
- whether the object is example vs production-like
- which authority boundary it belongs to
- which architectural layer it lives in
- which domain and module govern it
- what type of object it is
- which version is being referenced

## Required Architectural Distinction

Every important governed object should be able to carry:
- stable ID
- canonical string address
- structured address object

The ID answers what the object is.
The address answers where it sits.

## Address Registry Requirement

Address segments should be validated against a registry of allowed values.
At minimum, these controlled segments should be governed:
- environment
- authority_zone
- layer
- domain
- module
- object_type

## Migration Rule

If an object's placement changes over time:
- the object ID should remain stable where possible
- address changes should be represented through migration records or aliases
- systems should be able to resolve both current and prior structural placement

## Fractal Requirement

The same address logic should work across scales, including:
- repository-level artifacts
- governance docs
- schemas
- claims
- artifacts
- chunks
- retrieval objects
- decision records
- learning events

## Interaction With Other Layers

The address system should work together with:
- claim containers
- trust / authority zones
- validation
- retrieval templates
- lineage / attribution chains

It should not replace those layers.
It should make them more navigable and governable.

## Future Direction

The next implementation steps for the address layer are:
- formal address schema
- formal structured-address schema
- registry-driven validation
- migration records
- CI enforcement
