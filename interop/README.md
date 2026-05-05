# Interop Package

This package defines governed mapping profiles from the repository's core entities and relations to selected external models.

## Goals

- expose explicit crosswalks to external vocabularies and governance frameworks
- communicate mapping confidence and lossiness to downstream consumers
- ensure mapping profiles stay in sync with core schema versions

## Directory Layout

- `profiles/`: mapping specifications per external profile
- `samples/`: sample transformed outputs

## Mapping Metadata Contract

Every mapping rule uses:

- `mapping_mode`: one of `exact`, `transformed`, or `unsupported`
- `confidence`: float between `0.0` and `1.0`
- `lossiness`: required note (`none` when no loss is expected)

Interpretation:

- **exact**: semantically equivalent transfer from source to target
- **transformed**: deterministic conversion or normalization is applied
- **unsupported**: no target expression in the selected profile; data must remain in sidecar/native payload

## Available Profiles

### 1) `w3c-semantic-core.v1.yaml`

Maps core ontology objects to W3C-aligned models:

- SKOS
- PROV-O
- DCTERMS

Includes sample output: `samples/w3c-semantic-core/intake-conflicts-ai.sample.jsonld`.

### 2) `nist-ai-rmf-profile.v1.yaml`

Maps governance-facing core objects into NIST AI RMF-oriented control and review semantics.

## Adoption Guide

1. **Select profile**
   - Choose the smallest profile that covers your exchange need.
   - Prefer `w3c-semantic-core` for graph interoperability.
   - Prefer `nist-ai-rmf-profile` for governance/risk reporting.

2. **Read unsupported fields first**
   - Inspect `mapping_mode: unsupported` rules.
   - Keep those fields in a native sidecar object to avoid semantic loss.

3. **Enforce minimum confidence threshold**
   - Suggested default threshold: `confidence >= 0.85` for automated publication.
   - Route lower-confidence transformed fields for human review.

4. **Track schema compatibility**
   - Run `python scripts/validation/validate_interop_mappings.py` in CI.
   - The validator fails if mapping profiles target stale core schema/type versions.

5. **Publish with provenance**
   - Include source object IDs and transform timestamp in outbound payload metadata.
   - Preserve native Law Firm IDs to support reverse-traceability.

## Validation

Run:

```bash
python scripts/validation/validate_interop_mappings.py
```

This checks:

- required profile structure
- mapping metadata contract compliance
- sample output file references
- alignment with `schema/manifest.yaml` version
- alignment with current `schema/types/*.yaml` versions for mapped entities/relations
