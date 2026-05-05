# Fractal Address System Specification

Author: Lowell T. Wong

## Purpose

This document defines the **machine-readable and human-readable structure** of the address system.

The goal is to ensure that any future system can:
- parse an address
- understand its hierarchy
- infer placement
- navigate the ontology structurally

## Core Concept

Each object has:

- `id` -> stable identity
- `address` -> structural location

These must remain distinct.

## Address Structure (Conceptual)

An address is a structured path composed of segments:

```
/<layer>/<domain>/<object_type>/<object_id>
```

Example:

```
/governance/ontology/claim/CLM-000101
```

## Address Requirements

Each address must:
- be deterministic
- be parseable
- map to a known layer
- map to a known object type
- be stable enough for referencing

## Required Fields (Machine-Readable)

Future systems should treat address as both:
- a string
- a structured object

Example JSON representation:

```
{
  "layer": "governance",
  "domain": "ontology",
  "object_type": "claim",
  "object_id": "CLM-000101"
}
```

## Why This Matters

Without structured addresses:
- traversal becomes ambiguous
- validation becomes weaker
- cross-domain expansion becomes inconsistent

With structured addresses:
- systems can route logic
- validation can be layered
- traversal becomes deterministic

## Future Extension

Future versions may include:
- version segments
- authority zones
- environment layers (example vs production)

## Implementation Note

Future systems should implement:
- address parser
- address validator
- address builder

These should exist as code, not just documentation.
