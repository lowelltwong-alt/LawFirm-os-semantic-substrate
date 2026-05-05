# Metadata Standard (v1)

All governed artifacts must include machine-readable metadata.

## Canonical Core Fields

- `id`: stable unique identifier
- `title`: human-readable title
- `artifact_type`: type classification
- `status`: lifecycle status
- `version`: artifact version
- `schema_id`: schema reference
- `template_id`: template reference
- `authority_zone`: trust and permission zone
- `trust_level`: confidence posture for use and retrieval
- `owner`: accountable steward
- `created_at`: ISO timestamp
- `updated_at`: ISO timestamp
- `address`: canonical string address
- `address_struct`: structured canonical address
- `attribution_chain`: provenance and derivation record

## Artifact-Specific Required Fields

- `artifact_order`: first-order, second-order, or third-order role encoded as an integer

## Optional Extensions

- `artifact_subtype`
- `aliases`
- `steward`
- `reviewer`
- `review_by`
- `depends_on`
- `enables`
- `supersedes`
- `superseded_by`
- `intended_use`
- `audience`
- `ai_ingestible`
- `ai_priority`
- `validation_status`
- `confidentiality`
- `access_scope`

## Naming Rules

- `id` is the canonical identifier field for governed artifacts
- `doc_id` is deprecated and must not be used in new artifact metadata
- `authority_zone` is the canonical governance field
- `authority_level` is deprecated and must not be used in new artifact metadata
- `version` refers to the artifact itself, not the schema version
- provenance source references should use canonical `SRC-...` identifiers
- internal derivation links should resolve to governed object IDs in the repository whenever they are not external references

## Example

```yaml
id: ART-000001
title: Example Artifact
artifact_type: framework
artifact_order: 2
status: draft
version: 1.0.0
schema_id: artifact-schema-v1
template_id: artifact-template-v1
authority_zone: public
trust_level: medium
owner: Lowell T. Wong
created_at: 2026-03-31T12:00:00Z
updated_at: 2026-03-31T12:00:00Z
address: /example/public/governance/legal/intake_conflicts/artifact/ART-000001/v1
address_struct: {...}
attribution_chain: {...}
```
