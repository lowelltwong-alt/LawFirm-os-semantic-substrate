# Access Control and Compliance Model

## Purpose

Define the minimum access, confidentiality, and governance boundaries for the pilot.

## Core Principle

The pilot should only expose information to a user, workflow, or retrieval layer if that access is permitted by the governing source, the matter context, and the organization's confidentiality posture.

## Confidentiality Classes

- internal_general
- restricted
- matter_confidential
- client_restricted
- quarantine_only

## Access Model

### Identity
Access should be tied to authenticated organizational identity.

### Authorization
Access should be determined by:
- role
- matter relationship
- client restriction
- exception approval

### Retrieval Default
Default retrieval should prefer asserted and approved material.
Quarantine or restricted material should not be surfaced unless explicitly allowed.

## Compliance Rules

- do not expose client-restricted material through general retrieval
- do not treat AI-generated material as canonical by default
- maintain provenance for all promoted artifacts
- preserve explicit review and promotion paths

## Operational Guardrails

- document-level or object-level filtering should be enforced before answer generation
- sensitivity and source class should remain machine-readable
- exception paths must be explicit and reviewable

## Why This Matters

The pilot only becomes trustworthy if governance, confidentiality, and provenance remain intact when retrieval and AI layers are added.
