# Contributing

Thanks for contributing to this repository.

## Repository Model

This repo is the semantic control plane and Innovation OS contract surface.

When you edit it, keep four layers distinct:
- ontology and taxonomy
- evidence and provenance
- policy and governance
- action and runtime contracts

Do not flatten those layers into one mixed change set unless the boundary itself is the subject of the change.

## Authoritative Files

If you touch an authoritative file, rewrite it in place.

Do not create a parallel replacement for:
- top-level entrypoint docs
- authoritative registries
- core schemas
- core SHACL files
- contribution or governance entrypoints

Update `registry/source-of-truth.json` and the relevant registry file when a change alters an authoritative surface.

## Mutation Boundary

Raw exceptions, pressure vectors, retrieval traces, views, and other runtime or derived objects must not directly mutate canonical meaning.

Canonical change must flow through reviewed governance and promotion decisions.

When editing runtime or action-layer contracts, preserve that boundary explicitly.

## Draft Discipline

Draft files are allowed, but only when all of the following are true:
- the file says it is draft through status or registry entry
- it does not masquerade as the stable canonical contract
- it does not bypass the active mutation boundary or source-of-truth rules

## Pull Request Shape

Prefer one coherent concern per pull request.

Good change shapes:
- front-door and authority-surface reconciliation
- schema and registry alignment
- ontology and SHACL hardening
- document and evidence contract completion
- example or validation completion

Avoid bundling unrelated cleanup with contract changes.

## Local Validation

For the Phase 1 learning-loop validator repair, the smallest reproducible local setup is:
- `pip install -r requirements-dev.txt`
- `python -m unittest scripts.validation.tests.test_validate_learning_loop_transitions -v`

## Review Expectations

Changes in these paths require especially clear impact notes:
- `registry/`
- `schemas/`
- `shapes/`
- `ontology/`
- `standards/`
- `.github/workflows/`
- `scripts/`

Call out:
- what layer changed
- whether the mutation boundary changed
- whether any registry or validator must be updated with the change

## Minimal Reviewer Checklist

Reviewers should confirm:
- the changed file belongs to the intended layer
- no derived or runtime object is being promoted to truth source by accident
- registry entries match the changed authoritative files
- draft surfaces are still marked as draft
- no direct canonical mutation path was introduced
