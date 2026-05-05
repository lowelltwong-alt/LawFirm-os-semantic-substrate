# Codex Desktop Runbook

Historical note: this document records the earlier repo-alignment cleanup sequence.
It is not the current branch-policy authority for the repository.
Use `AI_START_HERE.md`, `AGENTS.md`, `registry/source-of-truth.json`, and `README.md` for current operating guidance.

## Purpose

This file is a historical handoff for the earlier repo cleanup, alignment, and coherence push in Codex Desktop.

The current repository already contains major new layers:
- doctrine and implementation order
- ontology, taxonomy, provenance, and alignment scaffolds
- Innovation OS runtime schemas and examples
- canonical document/evidence doctrine and core schemas
- retrieval, privilege, parsing, security, view, and evaluation scaffolds
- thin-slice READMEs

The main remaining work is **consolidation of older authoritative files** and **completion of missing contracts/examples**.

## Branch policy

Historical branch context:
- `main`
- `feature/repo-alignment-finalize` during the completed alignment pass

Current contributors should follow the active workflow guidance in `README.md` and the current repo state on `main`, not the branch assumptions below.

## Execution order

### Phase 1  -  Audit
Produce:
- file inventory
- placeholder audit
- registry coverage report
- schema/example coverage report
- stale-authority file list

Primary output location:
- `reports/repo-audit/2026-04-14/`

### Phase 2  -  Rewrite stale authoritative files in place
Rewrite first:
- `README.md`
- `governance/ALIGNMENT_FIRST_ROADMAP.md`
- `governance/PHASED_INTEGRATION_BACKLOG.md`
- `registry/source-of-truth.json`
- `registry/schema-registry.json`
- `registry/exceptions-schema-registry.json`
- `registry/exception-route-registry.json`
- `schemas/exception-event.schema.json`
- `schemas/pressure-vector.schema.json`
- `schemas/promotion-decision.schema.json`
- `shapes/core.shacl.ttl`
- `CONTRIBUTING.md`

### Phase 3  -  Complete missing document/evidence and integration contracts
Complete:
- document-version, source-artifact, canonical-text, component, citation, chunk-set, embedding-set, index-build
- retrieval-response and index-migration-plan
- remaining Azure, BillBlast, iManage, SharePoint profiles
- mappings from source systems to Law Firm canonical objects

### Phase 4  -  Finish views, examples, and evaluation assets
Complete:
- example payloads for the view schemas
- evaluation examples
- thin-slice example JSON artifacts

### Phase 5  -  Replace placeholder CI and helper scripts with working implementations
Harden:
- `.github/workflows/validate.yml`
- `.github/workflows/shacl.yml`
- `scripts/check_registry_refs.py`
- `scripts/validate_examples.py`
- `scripts/build_release_snapshots.py`

## Placeholder policy

### Must replace now
- active README / roadmap / registry entrypoints
- placeholder SHACL in core paths
- older runtime schemas that conflict with the newer family
- placeholder CI and scripts in active execution paths

### Allowed as draft
- alignment scaffolds
- some vendor profiles and mappings
- draft ontology modules

Draft files must say they are draft and must be registered as such.

## Commit policy

One commit per phase or tightly related pass. Avoid micro-commits.

Suggested commit sequence:
1. `repo audit: current-state inventory and placeholder classification`
2. `docs: reconcile repo front door and roadmap`
3. `registry: reconcile authoritative surfaces`
4. `ontology: replace placeholder shapes and align semantic core`
5. `schemas: normalize runtime object family`
6. `documents: complete canonical document and evidence model`
7. `profiles: complete vendor adapters and mappings`
8. `views: complete renderers and evaluation examples`
9. `ci: replace placeholder checks with real validation`
10. `examples: complete thin slices`

## Stop conditions

Stop and request review if:
- identifier strategy changes materially
- lifecycle states change materially
- a canonical class or relation is removed
- the mutation boundary is weakened
- cross-matter retrieval or access rules are broadened

## Goal state

A coherent repo where:
- entrypoint docs match the actual structure
- all active files are registered
- stale authority files are removed or rewritten
- core shapes are real, not placeholders
- runtime schemas are normalized
- thin slices are complete and validating
- CI checks are meaningful
