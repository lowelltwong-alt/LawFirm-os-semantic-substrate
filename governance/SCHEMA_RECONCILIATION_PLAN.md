# Schema Reconciliation Plan

Historical note: this document records an earlier reconciliation plan for aligning the active registry and validation surface with the claim-v3 and governed-learning objects. The plan's target steady state has already been absorbed into the active registry on `main`.

Current active schema resolution uses `registry/schema-registry.json`. See `registry/source-of-truth.json` for precedence and `AI_START_HERE.md` for current read order.

## Original purpose

This note explained how to align the active registry and validation surface with the repo's newer claim and governed-learning objects.

## Earlier gap (now resolved)

The repo previously had:

- older registry references centered on claim v2
- newer claim modeling centered on claim v3
- governed-learning schemas for exception events, pressure vectors, adaptation proposals, and promotion decisions
- multiple validation scripts that did not yet converge on one default path

## Earlier vNext snapshot

The following artifacts were introduced as part of the vNext plan:

- `registry/schema-registry.vnext.json`  -  historical snapshot only; not authoritative, not used by validators, and now flagged as superseded in its own contents
- `scripts/validate_repository_vnext.py`  -  still live; it reads the current `registry/schema-registry.json` for schema IDs
- `.github/workflows/validate-repository-vnext.yml`  -  still live; it exercises the same validator against current `main`

## Current steady state on main

The active default registry `registry/schema-registry.json` already covers:

- `schemas/artifact.schema.json`
- `schemas/claim_v3.schema.json`
- `schemas/exception-event.schema.json`
- `schemas/pressure-vector.schema.json`
- `schemas/adaptation-proposal.schema.json`
- `schemas/promotion-decision.schema.json`
- the canonical-document family, retrieval/access family, and the Innovation OS operating-object drafts

`claim-schema-v2` is marked deprecated in the active registry and its example is preserved only under `examples/claims/legacy/`.

## What this means for contributors

- Do not edit `registry/schema-registry.vnext.json` to drive active schema resolution.
- Add or change schema entries only in `registry/schema-registry.json`.
- Follow `registry/source-of-truth.json` for precedence and `AI_START_HERE.md` for read order.
- Preserve the no-direct-mutation boundary: canonical changes still require a reviewed promotion decision, not a registry edit.
